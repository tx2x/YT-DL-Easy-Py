#!/usr/bin/env python3
"""YT-DL Easy Py: cross-platform interactive frontend for yt-dlp."""
from __future__ import annotations
import argparse, os, shlex, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

APP, VERSION = "YT-DL Easy Py", "1.0.0"

class UI:
    def __init__(self, color=True):
        self.color = color and sys.stdout.isatty() and "NO_COLOR" not in os.environ
        if self.color and os.name == "nt":
            try:
                import ctypes
                k = ctypes.windll.kernel32; h = k.GetStdHandle(-11); mode = ctypes.c_uint()
                if k.GetConsoleMode(h, ctypes.byref(mode)): k.SetConsoleMode(h, mode.value | 4)
            except Exception: self.color = False
    def p(self, s, c): return f"\033[{c}m{s}\033[0m" if self.color else s
    def banner(self):
        print(self.p("=" * 68, "36")); print(self.p(f"  {APP}  |  v{VERSION}", "1;36")); print(self.p("=" * 68, "36"))
    def info(self,s): print(self.p("[i] ","36")+s)
    def ok(self,s): print(self.p("[+] ","32")+s)
    def warn(self,s): print(self.p("[!] ","33")+s)
    def error(self,s): print(self.p("[x] ","31")+s)

def yes_no(prompt, default=True):
    while True:
        a=input(f"{prompt} {'[Y/n]' if default else '[y/N]'} ").strip().lower()
        if not a: return default
        if a in ("y","yes"): return True
        if a in ("n","no"): return False
        print("Please enter Y or N.")

def choice(prompt, allowed, default=None):
    while True:
        a=input(prompt).strip().lower()
        if not a and default is not None: return default
        if a in allowed: return a
        print("Invalid choice. Available options: "+", ".join(sorted(allowed)))

def playlist_from_url(url):
    p=urlparse(url); q=parse_qs(p.query)
    if q.get("list") and (p.hostname or "").endswith(("youtube.com","youtu.be")):
        return "https://www.youtube.com/playlist?list="+q["list"][0]
    return None

def is_url(s):
    p=urlparse(s); return p.scheme in ("http","https") and bool(p.netloc)

def resolve_exe(name):
    found=shutil.which(name)
    if found: return found
    p=Path(name).expanduser()
    if p.is_file(): return str(p.resolve())
    local=Path(__file__).resolve().parent/name
    return str(local.resolve()) if local.is_file() else None

def run(cmd, capture=False):
    try:
        return subprocess.run(cmd, text=True, encoding="utf-8", errors="replace",
                              stdout=subprocess.PIPE if capture else None,
                              stderr=subprocess.STDOUT if capture else None, check=False)
    except KeyboardInterrupt:
        print("\nInterrupted."); return subprocess.CompletedProcess(cmd,130)
    except OSError as e:
        print(f"Could not start yt-dlp: {e}"); return subprocess.CompletedProcess(cmd,1)

def read_urls(path):
    with path.open(encoding="utf-8-sig") as f:
        return [x.strip() for x in f if x.strip() and not x.lstrip().startswith("#")]

def select_format(exe, url, ui):
    print("\nFormat options")
    print("  1) Best quality (recommended; merge separate streams when needed)")
    print("  2) Best single-file format (no merge)")
    print("  3) Best quality, prefer MP4 container")
    print("  4) Enter a format code manually")
    print("  5) Audio only")
    print("  6) Extract audio to MP3")
    print("  7) Video only")
    c=choice("Select format [1]: ",set("1234567"),"1")
    mapping={"1":(["-f","bv*+ba/b"],"Best quality"),"2":(["-f","b"],"Best single-file format"),
             "3":(["-f","bv*+ba/b","--merge-output-format","mp4"],"Best quality (MP4)"),
             "5":(["-f","bestaudio/best"],"Audio only"),"6":(["-f","bestaudio/best","-x","--audio-format","mp3"],"Audio to MP3"),
             "7":(["-f","bestvideo"],"Video only")}
    if c!="4": return mapping[c]
    print("\nAvailable format codes (combine streams as VIDEO+AUDIO, e.g. 137+140):")
    run([exe,"--no-warnings","-F",url])
    while True:
        code=input("Format code: ").strip()
        if code and not code.startswith("-"): return ["-f",code],f"Custom format: {code}"
        print("Enter a format code.")

def main():
    ap=argparse.ArgumentParser(description="Interactive cross-platform yt-dlp frontend.",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--exe",default="yt-dlp",help="yt-dlp executable name or path")
    ap.add_argument("--output",default="Outputs",help="Output directory")
    ap.add_argument("--desktop",action="store_true",help="Use Desktop/Outputs")
    ap.add_argument("--ffmpeg-location",help="FFmpeg executable or directory")
    ap.add_argument("--options",default="",help="Additional yt-dlp arguments, quoted as one string")
    ap.add_argument("--no-color",action="store_true",help="Disable terminal colors")
    ap.add_argument("--debug",action="store_true",help="Show diagnostic details")
    ap.add_argument("--version",action="version",version=f"%(prog)s {VERSION}")
    a=ap.parse_args(); ui=UI(not a.no_color); ui.banner()
    exe=resolve_exe(a.exe)
    if not exe:
        ui.error(f"yt-dlp not found: {a.exe}"); print("Install: python -m pip install -U yt-dlp"); return 2
    if a.desktop:
        desktop=Path.home()/"Desktop"
        if not desktop.exists() and os.name=="nt": desktop=Path(os.environ.get("USERPROFILE",str(Path.home())))/"Desktop"
        out=desktop/"Outputs"
    else:
        out=Path(a.output).expanduser(); out=out if out.is_absolute() else Path.cwd()/out
    out.mkdir(parents=True,exist_ok=True)
    ffmpeg=a.ffmpeg_location or shutil.which("ffmpeg")
    if not ffmpeg: ui.warn("FFmpeg not detected. Install it to merge separate streams or convert audio.")
    if a.debug:
        print(f"Python: {sys.version.split()[0]} | Platform: {sys.platform}\nyt-dlp: {exe}\nOutput: {out}\nFFmpeg: {ffmpeg or 'not detected'}")
    raw=input("\nEnter a video/playlist URL or a text file containing URLs: ").strip().strip('"')
    if not raw: ui.error("No input provided."); return 1
    source=Path(raw).expanduser(); file_mode=source.is_file()
    if file_mode:
        try: urls=read_urls(source)
        except (OSError,UnicodeError) as e: ui.error(f"Cannot read URL file: {e}"); return 1
        if not urls: ui.error("The URL file is empty."); return 1
        if any(not is_url(u) for u in urls): ui.error("The URL file contains a non-HTTP(S) entry."); return 1
        ui.info(f"Loaded {len(urls)} URL(s).")
    else:
        if not is_url(raw): ui.error("Enter a valid HTTP(S) URL or an existing text file."); return 1
        urls=[raw]
    playlist_mode=file_mode
    if not file_mode:
        pl=playlist_from_url(urls[0]); q=parse_qs(urlparse(urls[0]).query)
        if pl and q.get("v"):
            print("\nThis link contains both a video and a playlist.")
            if choice("Download [V]ideo only or [P]laylist? [V]: ",{"v","p"},"v")=="p": urls=[pl]; playlist_mode=True
        elif pl: playlist_mode=True
    if file_mode: playlist_mode=True
    if len(urls)>1: playlist_mode=True
    # A single video URL with a playlist parameter is explicitly kept in video-only mode.
    single_video=len(urls)==1 and not playlist_mode
    if single_video:
        print("\nAvailable formats:"); run([exe,"--no-warnings","-F",urls[0]])
        fmt,label=select_format(exe,urls[0],ui)
    else:
        print("\nPlaylist / URL-list mode: the chosen format rule applies to every item.")
        if yes_no("Customize the format?",default=True): fmt,label=select_format(exe,urls[0],ui)
        else: fmt,label=["-f","bv*+ba/b"],"Best quality"
    count=f"{len(urls)} URL(s)" if file_mode or len(urls)>1 else "the selected video/playlist"
    if not yes_no(f"Start downloading {count} using '{label}'?",True): ui.info("Cancelled."); return 0
    cmd=[exe,"--no-mtime","--embed-metadata"]
    if ffmpeg: cmd += ["--ffmpeg-location",ffmpeg]
    if playlist_mode: cmd += ["--yes-playlist"]
    elif playlist_from_url(urls[0]): cmd += ["--no-playlist"]
    template=str(out/"%(playlist_title)s"/"%(playlist_index)03d - %(title)s.%(ext)s") if (not file_mode and playlist_mode) else str(out/"%(title)s.%(ext)s")
    cmd += ["-o",template]+fmt
    if a.options:
        try: cmd += shlex.split(a.options,posix=(os.name!="nt"))
        except ValueError as e: ui.error(f"Cannot parse --options: {e}"); return 1
    if a.debug: print("\nCommand arguments:\n"+"\n".join(f"  [{i}] {x}" for i,x in enumerate(cmd)))
    print(); ui.info("Downloading. Press Ctrl+C to stop.")
    failed=0
    for i,url in enumerate(urls,1):
        if len(urls)>1: print(f"\n--- URL {i}/{len(urls)} ---")
        result=run(cmd+[url])
        if result.returncode==0: ui.ok("Completed successfully.")
        else: failed+=1; ui.error(f"yt-dlp exited with code {result.returncode}.")
    if failed: ui.warn(f"{failed} of {len(urls)} input(s) failed."); return 1
    ui.ok("All downloads completed."); return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except KeyboardInterrupt: print("\nCancelled."); raise SystemExit(130)
