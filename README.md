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
- **Plays on ANY Keypress (Not Just Textboxes)**:
  - Supports letters, numbers, space, enter, backspace, arrow keys, function keys, and shortcuts anywhere on the page.
- **Integrated New Tab Search**: Opens a dedicated SoundPress New Tab search page (`Ctrl + T`) that immediately captures all search typing with zero setup!
- **Runs Inside Chrome Only**: SoundPress is **only active while Chrome is open** and immediately stops when Chrome is closed. No background processes remain on your system.
- **Zero-Latency Polyphonic Playback**: Powered by the Web Audio API buffer engine for instant, overlapping audio with zero lag.

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
6. Open any website (e.g. Google, Docs, Reddit, Wikipedia) or open a New Tab (`Ctrl + T`) and start typing to hear the sound effects!
7. Click the extension toolbar icon to change sounds, adjust volume, or turn on the multiple-sound randomizer.

> **Note**: The extension runs **exclusively inside Google Chrome**. When you close Chrome, SoundPress automatically terminates with no leftover background processes on your computer.

---

### Option 2: Chrome-Bound Companion (For Top Address Bar / Omnibox)

If you also want sound effects while typing in Chrome's **native top address bar (Omnibox)**:
1. Double-click `run-chrome-soundpress.bat`.
2. This companion is **strictly bound to Chrome**:
   - It **only** plays sounds when Google Chrome is the active foreground window.
   - It captures keystrokes in the top address bar, search bar, and everywhere in Chrome.
   - When you switch away from Chrome, it is completely silent.
   - The moment you close Chrome, it **automatically terminates and exits** itself!

---

### Option 3: Full Desktop Standalone App (.EXE)

If you want system-wide sound effects outside of Chrome:
1. Double-click `run.bat` (or run `dist\SoundPress.exe`).

---

### Option 4: Run via Python Desktop GUI

```bash
python app.py
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
- **Isolated to Chrome**: Only listens to keystrokes while Chrome is active.

---

## 📜 Sound Assets & License

- **Source Code**: Released under the [MIT License](LICENSE).
- **Generated Sounds**: Synthesized by `generate_sound.py` using Python's standard library math/wave modules (MIT).
- **Bundled Sounds**: Contributed sound effects included under permission; see [SOUND_ASSETS.md](SOUND_ASSETS.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
