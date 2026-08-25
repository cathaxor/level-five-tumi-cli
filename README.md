# Level Five – Tumi CLI

A Python-based CLI lyric player for **Level Five — Tumi**.

The project provides synchronized lyric playback directly in the terminal, along with tools for lyric calibration, media duration detection, and playback analysis.

## Features

* Terminal-based lyric player
* Synchronized `.lrc` lyrics
* Local media playback
* Lyric timing calibration
* Playback analysis
* Media duration detection
* Lightweight Python implementation
* Windows support

## Project Structure

```text
Level Five - Tumi/
│
├── play_tumi.py
├── calibrate_tumi.py
├── analyze_tumi.py
├── get_duration.ps1
├── Level Five - Tumi.lrc
├── LEVEL-FIVE-TUMI-Official.mp4
└── README.md
```

## Requirements

* Windows 10 / 11
* Python 3.9+
* PowerShell
* Local copy of the media file

Check Python:

```powershell
python --version
```

Check PowerShell:

```powershell
$PSVersionTable.PSVersion
```

## Usage

### Play

Start the CLI lyric player:

```powershell
python play_tumi.py
```

The player starts the media and displays the synchronized lyrics in the terminal.

### Calibrate Lyrics

If the lyrics are early or late:

```powershell
python calibrate_tumi.py
```

Use the calibration tool to fine-tune synchronization between the `.lrc` lyrics and the media.

### Analyze Playback

Run the analysis utility:

```powershell
python analyze_tumi.py
```

This can be used to inspect the media/lyric timing and help identify synchronization issues.

### Get Media Duration

Run the PowerShell utility:

```powershell
.\get_duration.ps1
```

This utility helps retrieve the duration of the local media file.

## Lyrics

The project uses an LRC lyric file:

```text
Level Five - Tumi.lrc
```

LRC timestamps determine when each lyric line appears during playback.

Example:

```text
[00:12.50] Lyric line
[00:17.20] Another lyric line
```

## Media

The original media file is kept locally:

```text
LEVEL-FIVE-TUMI-Official.mp4
```

Large media files should not normally be committed to GitHub.

Recommended `.gitignore` entries:

```gitignore
*.mp4
*.mp3
*.wav
*.m4a
*.flac
__pycache__/
*.pyc
```

## Installation

Clone the repository:

```powershell
git clone https://github.com/cathaxor/level-five-tumi-cli.git
cd level-five-tumi-cli
```

Then run:

```powershell
python play_tumi.py
```

## Workflow

```text
Media
  │
  ├── analyze_tumi.py
  │
  ├── get_duration.ps1
  │
  ▼
Lyric Timing
  │
  ├── calibrate_tumi.py
  │
  ▼
Level Five - Tumi.lrc
  │
  ▼
play_tumi.py
  │
  ▼
Terminal Lyric Playback
```

## Author

**Abdur Rahaman Abdulla**

Instagram: **[@abdulla_trzz](https://instagram.com/abdulla_trzz)**

## License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for details.
