import sys, os, time, subprocess

sys.stdout.reconfigure(encoding='utf-8')

VIDEO_FILE = "LEVEL-FIVE-TUMI-Official.mp4"
VIDEO_PATH = os.path.abspath(VIDEO_FILE)

LINES = [
    "Sopne amar tomar chobi chupti kore ase...",
    "Sokal theke rater seshe thako amar pase...",
    "Ta ta ta tarara, tarara rara rara rara rara",
    "Ta ta ta tarara, tarara rara rara rara rara",
    "~~ Music ~~",
    "Proti rate amader kotha bola...",
    "Tomar sathe hazaro golpo lekha...",
    "Amader angule jot bandha...",
    "Amader bhalo laga...",
    "~~ Guitar Solo ~~",
    "Alo jwole, alo jwole...",
    "Amar mone, amar mone...",
    "Tomar chobi chokher samne eshe bhashe...",
    "Brishti pore, brishti pore...",
    "Thoter majhe golpo jome...",
    "Tomay ami khuji sarakkhon...",
    "Ei amar mon...",
    "Ei amar mon...",
    "Ei amar mon... Tumi.",
    "~~ Level Five - Tumi Shesh ~~"
]

COLORS = [
    "CYAN", "PINK", "MAGENTA", "BLUE", "YELLOW",
    "GREEN", "CYAN", "PINK", "MAGENTA", "YELLOW",
    "GREEN", "BLUE", "CYAN", "PINK", "MAGENTA",
    "BLUE", "RED", "RED", "MAGENTA", "YELLOW"
]

def play_audio():
    ps_code = f"""
    Add-Type -AssemblyName PresentationCore
    $player = New-Object System.Windows.Media.MediaPlayer
    $player.Open([System.Uri]"{VIDEO_PATH}")
    Start-Sleep -Milliseconds 500
    $player.Position = [System.TimeSpan]::FromSeconds(60)
    $player.Play()
    while ($player.Position.TotalSeconds -lt 238) {{
        Start-Sleep -Milliseconds 200
    }}
    """
    ps_file = os.path.join(os.path.dirname(VIDEO_PATH), "calib_bg.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_code)
    proc = subprocess.Popen(
        ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-File", ps_file],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return proc, ps_file

def save_to_play_tumi(timestamps):
    lyrics_code = "LYRICS = [\n"
    for i, t in enumerate(timestamps):
        c = COLORS[i]
        l = LINES[i]
        comma = "," if i < len(timestamps) - 1 else ""
        lyrics_code += f'    ({round(t, 2):<6}, {c:<8}, "{l}"){comma}\n'
    lyrics_code += "]\n"

    script_content = f'''import sys, os, time, subprocess

sys.stdout.reconfigure(encoding='utf-8')

VIDEO_FILE = "LEVEL-FIVE-TUMI-Official.mp4"
VIDEO_PATH = os.path.abspath(VIDEO_FILE)

MAGENTA = "\\033[1;35m"
CYAN    = "\\033[1;36m"
GREEN   = "\\033[1;32m"
YELLOW  = "\\033[1;33m"
RED     = "\\033[1;31m"
PINK    = "\\033[1;95m"
BLUE    = "\\033[1;34m"
WHITE   = "\\033[1;37m"
RESET   = "\\033[0m"

{lyrics_code}
def play_audio():
    ps_code = f"""
    Add-Type -AssemblyName PresentationCore
    $player = New-Object System.Windows.Media.MediaPlayer
    $player.Open([System.Uri]{{VIDEO_PATH}})
    Start-Sleep -Milliseconds 500
    $player.Position = [System.TimeSpan]::FromSeconds(60)
    $player.Play()
    while ($player.Position.TotalSeconds -lt 238) {{{{
        Start-Sleep -Milliseconds 200
    }}}}
    """
    ps_file = os.path.join(os.path.dirname(VIDEO_PATH), "play_bg.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_code)

    proc = subprocess.Popen(
        ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-File", ps_file],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return proc, ps_file

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\\n  {{MAGENTA}}LEVEL FIVE - TUMI{{RESET}}\\n  ------------------\\n")

    audio_proc, ps_file = play_audio()
    time.sleep(1.5)
    start = time.time()

    try:
        for offset, color, line in LYRICS:
            wait = (start + offset) - time.time()
            if wait > 0:
                time.sleep(wait)
            if "~~" in line:
                print(f"    {{color}}  {{line}}{{RESET}}", flush=True)
            else:
                print(f"    {{color}}> {{line}}{{RESET}}", flush=True)

    except KeyboardInterrupt:
        pass
    finally:
        try: audio_proc.terminate()
        except: pass
        try: os.remove(ps_file)
        except: pass
        print(f"\\n  ------------------\\n  {{MAGENTA}}Gaan shesh! Dhonnobad!{{RESET}}\\n")

if __name__ == "__main__":
    main()
'''
    with open("play_tumi.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    print("\n  [SUCCESS] play_tumi.py file has been automatically updated with your exact recorded timestamps!\n")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n  === TUMI LYRICS AUTOMATIC CALIBRATION TOOL ===\n")
    print("  Gaan cholbe. Jei muhurte singer line ta BOLBE,")
    print("  sei muhurte ENTER chapben.\n")
    print("  Seshe apnar exact timestamps swoyongkrio bhabe 'play_tumi.py'-te save hoye jabe!\n")
    print("  Press ENTER to start...")
    input()

    audio_proc, ps_file = play_audio()
    time.sleep(1.5)
    start = time.time()

    print("\n  Gaan shuru hocche... Shunun ar ENTER chapun!\n")

    timestamps = []
    for i, line in enumerate(LINES):
        print(f"  [{i+1}/{len(LINES)}] Waiting for: \033[1;33m{line}\033[0m")
        input()
        t = time.time() - start
        timestamps.append(t)
        print(f"         -> Recorded: {t:.2f}s\n")

    try: audio_proc.terminate()
    except: pass
    try: os.remove(ps_file)
    except: pass

    save_to_play_tumi(timestamps)

if __name__ == "__main__":
    main()
