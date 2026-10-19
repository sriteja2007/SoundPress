# SoundPress 🔊

A desktop application that plays a sound effect whenever you press a key on your keyboard. Runs on Windows and macOS.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey.svg)](#how-to-run)

---

## 🚀 Features

- **18 Bundled Sound Effects**:
  - **Procedural Synthesized Waves**: Shotgun, Cartoon Boing, Censor Beep, Dry Fart, Pew Pew, Quack.
  - **Popular Effects & Memes**: Gunshot J Budden, Apple Pay, Movie 1, Rizz Sound Effect, Wrong Answer, Yes Lara Voice, Shocked, Punch, Maro Jump, Ding, Anime Ahh, 67.
- **Sound Playback Modes**:
  - **Single Sound**: Consistent feedback on every keystroke.
  - **Multiple Sounds (Random Mix)**: Randomly chooses among your checked sounds on every keypress.
- **Custom Sound Import**: Add your own `.wav` and `.mp3` audio files with one click.
- **Volume Settings**: Quick selection for Loud (100%), Medium (55%), and Quiet (20%).
- **Armed Switch**: Quickly silence or reactivate sound effects without quitting the application.
- **Keystroke Counter**: Displays real-time detected key events so you know the listener is active.
- **Zero-Latency Polyphonic Playback**: Handles rapid typing (e.g. 100+ WPM) without audio clipping or stuttering.
- **System Tray Support**: Minimizes to the Windows system tray / notification area to run unobtrusively in the background.

---

## 🕹️ How to Run

### Method 1: One-Click Quick Run (Windows Standalone .EXE)

If you have the pre-built portable executable in `dist/`:
1. Double-click `run.bat` (or run `dist\SoundPress.exe`).
2. The application opens immediately—no installation or .NET runtime needed!

> **Note**: If `dist\SoundPress.exe` is not yet downloaded on your system, you can fetch it with one command:
> ```powershell
> .\download-windows-binary.ps1
> ```

---

### Method 2: Run via Python (Cross-Platform, Zero External Dependencies)

SoundPress includes a native Python application (`app.py`) built with Tkinter, Windows low-level keyboard hooks, and multi-voice MCI audio mixing.

```bash
python app.py
```
Or simply double-click `run.bat` (it automatically falls back to Python if `dist\SoundPress.exe` is absent).

**Requirements**:
- Python 3.10+ (using standard libraries).

---

### Method 3: Build from C# Source (.NET 10 SDK)

To build the self-contained single-file Windows executable yourself:

```powershell
# 1. Generate synthesized WAV sounds
python generate_sound.py

# 2. Build and publish with .NET 10
.\windows\build.ps1
```

The resulting standalone executable will be written to `dist/SoundPress.exe`.

---

### Method 4: Build on macOS (Swift)

Requires macOS 12+, Swift Command Line Tools, and Python 3:

```bash
# Generate sounds and build DMG package
./build-dmg.sh
```

The resulting `.dmg` will be placed in `dist/`.
> *macOS permissions note*: Grant **Input Monitoring** and **Accessibility** permissions in **System Settings → Privacy & Security**.

---

## 🎛️ Controls & UI Guide

| Control | Description |
|---|---|
| **Armed** | Checkbox that enables or disables sound playback when typing. |
| **Multiple sounds** | When enabled, randomly plays one of the selected checked sounds on each keypress. |
| **Sound List** | Click to select sounds. In single mode, selecting a sound activates it. In multiple mode, check all sounds you want to mix. |
| **Add Sounds…** | Open file dialog to import custom `.mp3` or `.wav` audio files. |
| **Remove Sound** | Removes a previously imported custom sound. |
| **Volume** | Choose Loud (100%), Medium (55%), or Quiet (20%). |
| **Test Selected Sound** | Plays the selected sound immediately without typing. |
| **Close Window** | Keeps the application running in the Windows Notification Area / System Tray. Double-click the tray icon to restore or right-click to quit. |

---

## 🔒 Privacy & Safety

SoundPress responds only to global key-down events to trigger sound playback.
- **No Keystroke Logging**: SoundPress **does not** record, save, or transmit the keys you press or text you type.
- **Offline**: SoundPress makes **zero network requests** during operation.
- All configuration settings and custom sound files are stored strictly locally in your user profile.

---

## 📜 Sound Assets & License

- **Source Code**: Released under the [MIT License](LICENSE).
- **Generated Sounds**: Synthesized by `generate_sound.py` using Python's standard library math/wave modules (MIT).
- **Bundled Sounds**: Contributed sound effects included under permission; see [SOUND_ASSETS.md](SOUND_ASSETS.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
