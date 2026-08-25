import sys, os, time, subprocess

sys.stdout.reconfigure(encoding='utf-8')

VIDEO_FILE = "LEVEL-FIVE-TUMI-Official.mp4"
VIDEO_PATH = os.path.abspath(VIDEO_FILE)

# ANSI Color Codes for vibrant styling
MAGENTA = "\033[1;35m"
CYAN    = "\033[1;36m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
RED     = "\033[1;31m"
PINK    = "\033[1;95m"
BLUE    = "\033[1;34m"
WHITE   = "\033[1;37m"
RESET   = "\033[0m"
DIM     = "\033[2m"

# Playback starts from the very beginning of the song
START_SECS = 0

# Shift all lyrics forward/backward if audio sync needs micro-adjustment (in seconds)
# Increase if lyrics appear too early; decrease if they appear too late.
TIME_OFFSET = -0.5

# Absolute timestamps (in seconds) parsed from official LRC file (converted to Banglish)
LYRICS = [
    (0.00,   YELLOW,  "~~ Level Five - Tumi ~~"),
    (31.08,  CYAN,    "Tumi shamne nei, tao tumi bhasho..."),
    (46.76,  PINK,    "Moner majhe lukiye ektukhani hasho..."),
    (61.99,  GREEN,   "Sopne amar tomar chobi..."),
    (65.87,  GREEN,   "Chupti kore ase..."),
    (69.66,  CYAN,    "Sokal theke rater seshe..."),
    (73.28,  CYAN,    "Thako amar pase..."),
    (77.98,  MAGENTA, "Ta ta ta tarara..."),
    (81.00,  MAGENTA, "Tarara rara rara rara rara..."),
    (84.00,  BLUE,    "Ta ta ta tarara..."),
    (87.00,  BLUE,    "Tarara rara rara rara rara..."),
    (90.00,  YELLOW,  "~~ Music Interlude ~~"),
    (140.44, GREEN,   "Proti rate amader kotha bola..."),
    (147.84, PINK,    "Tomar sathe hazaro golpo lekha..."),
    (155.46, MAGENTA, "Amader angule jot bandha..."),
    (162.96, BLUE,    "Amader bhalo laga..."),
    (168.00, YELLOW,  "~~ Guitar Solo ~~"),
    (182.67, GREEN,   "Alo jwole, alo jwole..."),
    (186.33, GREEN,   "Amar mone, amar mone..."),
    (190.22, CYAN,    "Tomar chobi chokher samne eshe bhashe..."),
    (197.61, PINK,    "Brishti pore, brishti pore..."),
    (201.39, PINK,    "Thoter majhe golpo jome..."),
    (204.94, BLUE,    "Tomay ami khuji sarakkhon..."),
    (210.37, RED,     "Ei amar mon..."),
    (214.48, RED,     "Ei amar mon..."),
    (218.40, RED,     "Ei amar mon..."),
    (227.03, MAGENTA, "Tumi..."),
    (236.00, YELLOW,  "~~ Level Five - Tumi Shesh ~~")
]

def play_audio():
    ps_code = f"""
    Add-Type -AssemblyName PresentationCore
    $player = New-Object System.Windows.Media.MediaPlayer
    $player.Open([System.Uri]"{VIDEO_PATH.replace('\\', '/')}")
    Start-Sleep -Milliseconds 500
    $player.Position = [System.TimeSpan]::FromSeconds({START_SECS})
    $player.Play()
    while ($player.Position.TotalSeconds -lt 238) {{
        Start-Sleep -Milliseconds 200
    }}
    """
    ps_file = os.path.join(os.path.dirname(VIDEO_PATH), "play_bg.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_code)

    proc = subprocess.Popen(
        ["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-File", ps_file],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return proc, ps_file

def get_colored_typewriter_line(lyric_text, char_count, default_color):
    # Keep break/system lines a single unified color
    if lyric_text.startswith("~~"):
        return f"{default_color}{lyric_text[:char_count]}{RESET}"
        
    word_colors = [CYAN, PINK, GREEN, YELLOW, BLUE, MAGENTA]
    words = lyric_text.split(" ")
    colored_result = []
    
    current_char_idx = 0
    for i, word in enumerate(words):
        color = word_colors[i % len(word_colors)]
        
        # Add space separator between words if not the first word
        if i > 0:
            if current_char_idx < char_count:
                colored_result.append(" ")
                current_char_idx += 1
            else:
                break
                
        word_len = len(word)
        if current_char_idx + word_len <= char_count:
            # Word is fully typed
            colored_result.append(f"{color}{word}{RESET}")
            current_char_idx += word_len
        elif current_char_idx < char_count:
            # Word is partially typed
            visible_part = word[:char_count - current_char_idx]
            colored_result.append(f"{color}{visible_part}{RESET}")
            current_char_idx = char_count
            break
        else:
            break
            
    return "".join(colored_result)

def draw_ui(song_time, active_lyric, active_color, char_count):
    total_duration = 238.0
    pct = min(1.0, song_time / total_duration)
    
    # Progress bar
    bar_width = 30
    filled = int(bar_width * pct)
    bar = "█" * filled + "░" * (bar_width - filled)
    
    min_el, sec_el = divmod(int(song_time), 60)
    min_tot, sec_tot = divmod(int(total_duration), 60)
    time_str = f"{min_el:02d}:{sec_el:02d} / {min_tot:02d}:{sec_tot:02d}"
    
    # Pulsing status text
    if int(time.time()) % 2 == 0:
        status_text = f"{GREEN}● PLAYING{RESET}"
    else:
        status_text = f"{DIM}{GREEN}● PLAYING{RESET}"

    # Typewriter lyric calculation with word-by-word coloring
    visible_lyric = get_colored_typewriter_line(active_lyric, char_count, active_color)
    
    # UI buffer assembly (Strict left margin alignment & static line count to prevent shifting)
    buf = []
    buf.append("\033[H")  # Home cursor to avoid screen flash
    
    # Line 1: Metadata Header
    buf.append(f"    {CYAN}Level Five{RESET}  {DIM}::{RESET}  {WHITE}Tumi (Official Single){RESET}  {DIM}[{RESET}{status_text}{DIM}]{RESET}\033[K")
    
    # Line 2: Empty Spacer
    buf.append(f"\033[K")
    
    # Line 3: Lyric Line (Main Focus)
    buf.append(f"    »  {visible_lyric}{RESET}\033[K")
    
    # Line 4: Empty Spacer
    buf.append(f"\033[K")
    
    # Line 5: Timeline Progress
    buf.append(f"    {time_str}  {DIM}[{RESET}{CYAN}{bar}{RESET}{DIM}]{RESET}\033[K\033[J")
    
    # Write to terminal window
    sys.stdout.write("\n".join(buf))
    sys.stdout.flush()

def main():
    # Windows ANSI Terminal initiation
    os.system('') 
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n  Initializing Cyber-HUD Level Five Player. Please wait...")
    audio_proc, ps_file = play_audio()
    
    time.sleep(1.2)
    start_time = time.time()
    song_end_time = 238.0 - START_SECS
    
    try:
        while True:
            elapsed = time.time() - start_time
            if elapsed >= song_end_time:
                break
                
            # Retrieve active lyric offset
            song_time = START_SECS + elapsed
            current_idx = -1
            for i, (offset, color, line) in enumerate(LYRICS):
                adjusted_offset = offset + TIME_OFFSET
                if song_time >= adjusted_offset:
                    current_idx = i
                else:
                    break
            
            # Determine lyrics and active times
            if current_idx == -1:
                active_lyric = "~~ Preparing playback... ~~"
                active_color = WHITE
                lyric_elapsed = 0.0
            else:
                active_lyric = LYRICS[current_idx][2]
                active_color = LYRICS[current_idx][1]
                lyric_start = LYRICS[current_idx][0] + TIME_OFFSET
                lyric_elapsed = song_time - lyric_start
            
            # Typewriter character index (approx 20 chars/sec)
            char_count = int(lyric_elapsed * 20)
            if "~~" in active_lyric: # Instantly print system/break labels
                char_count = len(active_lyric)
            
            # Draw the UI frame (20 FPS update rate)
            draw_ui(
                song_time = song_time,
                active_lyric = active_lyric,
                active_color = active_color,
                char_count = char_count
            )
            
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        try:
            audio_proc.terminate()
        except:
            pass
        try:
            if os.path.exists(ps_file):
                os.remove(ps_file)
        except:
            pass
        
        # Clear screen and display final goodbye
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n  {CYAN}LEVEL FIVE - TUMI{RESET}")
        print(f"  --------------------------------------------------")
        print(f"  {CYAN}Gaan shesh! Dhonnobad!{RESET}\n")

if __name__ == "__main__":
    main()
