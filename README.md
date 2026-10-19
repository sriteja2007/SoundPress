# SoundPress 🔊

A keyboard sound effects application that plays sound effects whenever you type. Available as a **Google Chrome Extension (Manifest V3)** and as a standalone desktop app for Windows & macOS.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Extension%20MV3-brightgreen.svg)](#option-1-google-chrome-extension-recommended)
[![Platform](https://img.shields.io/badge/Platform-Chrome%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](#how-to-run)

---

## 🚀 Features

- **18 Bundled Sound Effects**:
  - **Procedural Synthesized Waves**: Shotgun, Cartoon Boing, Censor Beep, Dry Fart, Pew Pew, Quack.
  - **Popular Effects & Memes**: Gunshot J Budden, Apple Pay, Movie 1, Rizz Sound Effect, Wrong Answer, Yes Lara Voice, Shocked, Punch, Maro Jump, Ding, Anime Ahh, 67.
- **Sound Playback Modes**:
  - **Single Sound**: Consistent feedback on every keystroke.
  - **Multiple Sounds (Random Mix)**: Randomly chooses among your checked sounds on every keypress.
- **Volume Settings**: Quick selection for Loud (100%), Medium (55%), and Quiet (20%).
- **Armed Switch**: Quickly silence or reactivate sound effects without quitting the application.
- **Runs Inside Chrome Only**: When running as a Chrome Extension, SoundPress is **only active while Chrome is open** and immediately stops when Chrome is closed. No background processes remain on your system.
- **Zero-Latency Polyphonic Playback**: Handles rapid typing (e.g. 100+ WPM) without audio clipping or stuttering.

---

## 🕹️ How to Run

### Option 1: Google Chrome Extension (Recommended)

Load SoundPress directly into Google Chrome in Developer Mode:

1. Open Google Chrome and enter `chrome://extensions` in the address bar (or go to **Menu ⋮ → Extensions → Manage Extensions**).
2. Enable **"Developer mode"** via the toggle switch in the top-right corner.
3. Click the **"Load unpacked"** button in the top-left corner.
4. Select the **`extension`** folder from this project:
   ```
   H:\Projects\SoundPress\extension
   ```
5. **Done!** The SoundPress icon (🔊) will appear in your Chrome toolbar.
6. Open any website (e.g. Google, Docs, Reddit, Wikipedia) and start typing to hear the sound effects!
7. Click the extension toolbar icon to change sounds, adjust volume, or turn on the multiple-sound randomizer.

> **Note**: As requested, the extension is active **only inside Google Chrome**. When you close Chrome, SoundPress automatically terminates with no leftover background processes on your computer.

---

### Option 2: One-Click Quick Run (Windows Standalone .EXE)

If you want system-wide sound effects outside of Chrome:
1. Double-click `run.bat` (or run `dist\SoundPress.exe`).
2. The application opens immediately—no installation or .NET runtime needed!

---

### Option 3: Run via Python (Cross-Platform)

SoundPress also includes a native Python application (`app.py`) built with Tkinter:

```bash
python app.py
```

---

### Option 4: Build from Source

- **Windows (.NET 10)**:
  ```powershell
  python generate_sound.py
  .\windows\build.ps1
  ```
- **macOS (Swift)**:
  ```bash
  ./build-dmg.sh
  ```

---

## 🎛️ Extension Controls

| Control | Description |
|---|---|
| **Armed** | Toggle switch that enables or disables sound playback when typing. |
| **Multiple sounds** | When enabled, randomly plays one of the selected checked sounds on each keypress. |
| **Sound List** | Click to select sounds. In single mode, selecting a sound activates it. In multiple mode, check all sounds you want to mix. |
| **Volume** | Choose Loud (100%), Medium (55%), or Quiet (20%). |
| **Test Sound** | Plays the selected sound immediately without typing. |

---

## 🔒 Privacy & Safety

- **No Keystroke Logging**: SoundPress **never** records, saves, or transmits the keys you press or text you type.
- **Completely Offline**: SoundPress makes **zero network requests** and transmits zero data.
- **Isolated to Chrome**: Only listens to keystrokes inside web page tabs while Chrome is open.

---

## 📜 Sound Assets & License

- **Source Code**: Released under the [MIT License](LICENSE).
- **Generated Sounds**: Synthesized by `generate_sound.py` using Python's standard library math/wave modules (MIT).
- **Bundled Sounds**: Contributed sound effects included under permission; see [SOUND_ASSETS.md](SOUND_ASSETS.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
