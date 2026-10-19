#!/usr/bin/env python3
"""
SoundPress - A desktop application that plays a sound effect for every key press.
Supports Windows (native zero-dependency MCI audio + low-level keyboard hook)
and includes all 18 bundled meme and sound effects.
"""

import os
import sys
import json
import random
import ctypes
from ctypes import wintypes
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Win32 Constants & Types
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
winmm = ctypes.windll.winmm
mciSendStringW = winmm.mciSendStringW

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, wintypes.HINSTANCE, wintypes.DWORD]
user32.SetWindowsHookExW.restype = wintypes.HHOOK
user32.CallNextHookEx.argtypes = [wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
user32.CallNextHookEx.restype = ctypes.c_longlong
user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
user32.UnhookWindowsHookEx.restype = wintypes.BOOL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(
    os.environ.get("LOCALAPPDATA", BASE_DIR),
    "SoundPress",
    "settings.json"
)
CUSTOM_SOUNDS_DIR = os.path.join(
    os.environ.get("LOCALAPPDATA", BASE_DIR),
    "SoundPress",
    "CustomSounds"
)

# Bundled Sound Catalog (18 sounds matching original repository)
DEFAULT_ENTRIES = [
    ("gunshotjbudden", "Gunshot J Budden", os.path.join(BASE_DIR, "bundled-sounds", "gunshotjbudden.mp3")),
    ("shotgun", "Shotgun", os.path.join(BASE_DIR, "generated-sounds", "shotgun.wav")),
    ("boing", "Cartoon Boing", os.path.join(BASE_DIR, "generated-sounds", "boing.wav")),
    ("beep", "Censor Beep", os.path.join(BASE_DIR, "generated-sounds", "beep.wav")),
    ("fart", "Dry Fart", os.path.join(BASE_DIR, "generated-sounds", "fart.wav")),
    ("pew", "Pew Pew", os.path.join(BASE_DIR, "generated-sounds", "pew.wav")),
    ("quack", "Quack", os.path.join(BASE_DIR, "generated-sounds", "quack.wav")),
    ("applepay", "Apple Pay", os.path.join(BASE_DIR, "bundled-sounds", "applepay.mp3")),
    ("movie_1", "Movie 1", os.path.join(BASE_DIR, "bundled-sounds", "movie_1.mp3")),
    ("rizz-sound-effect", "Rizz Sound Effect", os.path.join(BASE_DIR, "bundled-sounds", "rizz-sound-effect.mp3")),
    ("wrong-answer-sound-effect", "Wrong Answer", os.path.join(BASE_DIR, "bundled-sounds", "wrong-answer-sound-effect.mp3")),
    ("yes-lara-voice", "Yes Lara Voice", os.path.join(BASE_DIR, "bundled-sounds", "yes-lara-voice.mp3")),
    ("shocked-sound-effect", "Shocked", os.path.join(BASE_DIR, "bundled-sounds", "shocked-sound-effect.mp3")),
    ("punch_u4LmMsr", "Punch", os.path.join(BASE_DIR, "bundled-sounds", "punch_u4LmMsr.mp3")),
    ("maro-jump-sound-effect_1", "Maro Jump", os.path.join(BASE_DIR, "bundled-sounds", "maro-jump-sound-effect_1.mp3")),
    ("ding-sound-effect_2", "Ding", os.path.join(BASE_DIR, "bundled-sounds", "ding-sound-effect_2.mp3")),
    ("anime-ahh", "Anime Ahh", os.path.join(BASE_DIR, "bundled-sounds", "anime-ahh.mp3")),
    ("67_SQlv2Xv", "67", os.path.join(BASE_DIR, "bundled-sounds", "67_SQlv2Xv.mp3"))
]


class PolyphonicSoundEngine:
    """Zero-dependency high-performance audio mixer using Windows MCI."""
    def __init__(self, max_voices=12):
        self.max_voices = max_voices
        self.voice_index = 0
        self.lock = threading.Lock()

    def play(self, filepath, volume=0.55):
        if not filepath or not os.path.exists(filepath):
            return
        abs_path = os.path.abspath(filepath)
        threading.Thread(target=self._play_worker, args=(abs_path, volume), daemon=True).start()

    def _play_worker(self, abs_path, volume):
        with self.lock:
            self.voice_index = (self.voice_index + 1) % self.max_voices
            alias = f"sp_voice_{self.voice_index}"

        # Close any previous audio stream on this alias channel
        mciSendStringW(f'close {alias}', None, 0, None)
        # Open the audio file
        ext = os.path.splitext(abs_path)[1].lower()
        type_hint = "type waveaudio" if ext == ".wav" else "type mpegvideo"
        open_cmd = f'open "{abs_path}" {type_hint} alias {alias}'
        res = mciSendStringW(open_cmd, None, 0, None)
        if res == 0:
            vol_val = int(max(0.0, min(1.0, volume)) * 1000)
            mciSendStringW(f'setaudio {alias} volume to {vol_val}', None, 0, None)
            mciSendStringW(f'play {alias} from 0', None, 0, None)

    def close_all(self):
        for i in range(self.max_voices):
            mciSendStringW(f'close sp_voice_{i}', None, 0, None)


class GlobalKeyboardHook:
    """Low-level Windows keyboard hook."""
    def __init__(self, on_key_down):
        self.on_key_down = on_key_down
        self.hook = None
        self.thread = None
        self.thread_id = None
        self.keep_running = True
        self.callback_ref = None

    def start(self):
        self.thread = threading.Thread(target=self._hook_loop, daemon=True)
        self.thread.start()

    def _hook_loop(self):
        self.thread_id = kernel32.GetCurrentThreadId()

        def _callback(nCode, wParam, lParam):
            if nCode >= 0 and (wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN):
                try:
                    self.on_key_down()
                except Exception:
                    pass
            return user32.CallNextHookEx(self.hook, nCode, wParam, lParam)

        self.callback_ref = HOOKPROC(_callback)
        self.hook = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self.callback_ref,
            0,
            0
        )
        if not self.hook:
            print(f"Warning: Failed to set keyboard hook (error: {kernel32.GetLastError()})")
            return

        msg = wintypes.MSG()
        while self.keep_running:
            res = user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)
            if res <= 0:
                break
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        if self.hook:
            user32.UnhookWindowsHookEx(self.hook)
            self.hook = None

    def stop(self):
        self.keep_running = False
        if self.thread_id:
            user32.PostThreadMessageW(self.thread_id, 0x0012, 0, 0)  # WM_QUIT


class SoundPressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SoundPress")
        self.root.geometry("560x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#F8F9FA")

        self.key_count = 0
        self.audio_engine = PolyphonicSoundEngine(max_voices=12)

        # Settings state
        self.armed_var = tk.BooleanVar(value=True)
        self.multiple_var = tk.BooleanVar(value=False)
        self.volume_var = tk.StringVar(value="Medium")
        self.selected_sound_ids = ["gunshotjbudden"]
        self.custom_sounds = []

        self.load_settings()
        self.build_sound_catalog()
        self.create_ui()

        # Keyboard hook
        self.hook = GlobalKeyboardHook(self.on_key_press)
        self.hook.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_sound_catalog(self):
        self.sounds = []
        for sid, name, path in DEFAULT_ENTRIES:
            if os.path.exists(path):
                self.sounds.append({"id": sid, "name": name, "path": path, "is_custom": False})

        for custom in self.custom_sounds:
            if os.path.exists(custom["path"]):
                self.sounds.append({"id": custom["id"], "name": custom["name"], "path": custom["path"], "is_custom": True})

        valid_ids = {s["id"] for s in self.sounds}
        self.selected_sound_ids = [sid for sid in self.selected_sound_ids if sid in valid_ids]
        if not self.selected_sound_ids and self.sounds:
            self.selected_sound_ids = [self.sounds[0]["id"]]

    def create_ui(self):
        # Header Container
        header_frame = tk.Frame(self.root, bg="#F8F9FA", padx=24, pady=16)
        header_frame.pack(fill="x")

        title_label = tk.Label(
            header_frame,
            text="🔊 SoundPress",
            font=("Segoe UI", 20, "bold"),
            bg="#F8F9FA",
            fg="#1A1A1A"
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="A sound effect for every key press · Windows & macOS",
            font=("Segoe UI", 10),
            bg="#F8F9FA",
            fg="#666666"
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # Status Card
        self.status_card = tk.Frame(self.root, bg="#E9ECEF", bd=0, padx=16, pady=12)
        self.status_card.pack(fill="x", padx=24, pady=(0, 14))

        status_title = tk.Label(
            self.status_card,
            text="● Keyboard Monitoring Active",
            font=("Segoe UI", 10, "bold"),
            bg="#E9ECEF",
            fg="#28A745"
        )
        status_title.pack(anchor="w")

        self.status_keys_label = tk.Label(
            self.status_card,
            text="Listening · 0 keys detected",
            font=("Segoe UI", 9),
            bg="#E9ECEF",
            fg="#495057"
        )
        self.status_keys_label.pack(anchor="w", pady=(2, 0))

        # Controls Row (Armed, Multiple sounds)
        controls_frame = tk.Frame(self.root, bg="#F8F9FA", padx=24)
        controls_frame.pack(fill="x", pady=(0, 10))

        armed_cb = tk.Checkbutton(
            controls_frame,
            text="Armed (Sound on keypress)",
            font=("Segoe UI", 10, "bold"),
            variable=self.armed_var,
            bg="#F8F9FA",
            activebackground="#F8F9FA",
            command=self.save_settings
        )
        armed_cb.pack(side="left")

        multiple_cb = tk.Checkbutton(
            controls_frame,
            text="Multiple sounds (Random mix)",
            font=("Segoe UI", 10),
            variable=self.multiple_var,
            bg="#F8F9FA",
            activebackground="#F8F9FA",
            command=self.on_multiple_toggle
        )
        multiple_cb.pack(side="left", padx=20)

        # Sounds Section Label
        sounds_header = tk.Frame(self.root, bg="#F8F9FA", padx=24)
        sounds_header.pack(fill="x", pady=(4, 6))

        tk.Label(
            sounds_header,
            text="Sounds",
            font=("Segoe UI", 12, "bold"),
            bg="#F8F9FA",
            fg="#1A1A1A"
        ).pack(side="left")

        tk.Label(
            sounds_header,
            text="(Select one, or check Multiple sounds to mix)",
            font=("Segoe UI", 9),
            bg="#F8F9FA",
            fg="#777777"
        ).pack(side="left", padx=8)

        # Sounds Listbox with Scrollbar
        list_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid")
        list_frame.pack(fill="both", expand=True, padx=24, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.sound_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.SINGLE,
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            height=10
        )
        self.sound_listbox.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        scrollbar.config(command=self.sound_listbox.yview)

        self.sound_listbox.bind("<<ListboxSelect>>", self.on_sound_select)
        self.populate_listbox()

        # Action Buttons Row
        btn_frame = tk.Frame(self.root, bg="#F8F9FA", padx=24)
        btn_frame.pack(fill="x", pady=(0, 12))

        add_btn = ttk.Button(btn_frame, text="Add Sounds…", command=self.add_custom_sound)
        add_btn.pack(side="left", padx=(0, 8))

        remove_btn = ttk.Button(btn_frame, text="Remove Sound", command=self.remove_custom_sound)
        remove_btn.pack(side="left", padx=(0, 8))

        self.select_all_btn = ttk.Button(btn_frame, text="Select All", command=self.select_all_sounds)
        self.select_all_btn.pack(side="right")
        self.update_select_all_state()

        # Bottom Controls: Volume & Test Sound
        bottom_frame = tk.Frame(self.root, bg="#F8F9FA", padx=24)
        bottom_frame.pack(fill="x", pady=(0, 16))

        tk.Label(
            bottom_frame,
            text="Volume:",
            font=("Segoe UI", 10),
            bg="#F8F9FA"
        ).pack(side="left", padx=(0, 6))

        vol_combo = ttk.Combobox(
            bottom_frame,
            textvariable=self.volume_var,
            values=["Loud (100%)", "Medium (55%)", "Quiet (20%)"],
            state="readonly",
            width=14
        )
        vol_combo.pack(side="left")
        vol_combo.bind("<<ComboboxSelected>>", lambda e: self.save_settings())

        test_btn = ttk.Button(
            bottom_frame,
            text="▶ Test Selected Sound",
            command=self.test_sound
        )
        test_btn.pack(side="right")

    def populate_listbox(self):
        self.sound_listbox.delete(0, tk.END)
        for i, sound in enumerate(self.sounds):
            is_sel = sound["id"] in self.selected_sound_ids
            marker = "☑ " if is_sel else "☐ "
            custom_tag = " (Custom)" if sound.get("is_custom") else ""
            self.sound_listbox.insert(tk.END, f"{marker}{sound['name']}{custom_tag}")
            if is_sel and not self.multiple_var.get():
                self.sound_listbox.selection_set(i)

    def on_sound_select(self, event):
        selection = self.sound_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        sound = self.sounds[idx]

        if self.multiple_var.get():
            if sound["id"] in self.selected_sound_ids:
                if len(self.selected_sound_ids) > 1:
                    self.selected_sound_ids.remove(sound["id"])
            else:
                self.selected_sound_ids.append(sound["id"])
        else:
            self.selected_sound_ids = [sound["id"]]

        self.populate_listbox()
        self.save_settings()

    def on_multiple_toggle(self):
        if not self.multiple_var.get() and len(self.selected_sound_ids) > 1:
            self.selected_sound_ids = [self.selected_sound_ids[0]]
        self.update_select_all_state()
        self.populate_listbox()
        self.save_settings()

    def update_select_all_state(self):
        if self.multiple_var.get():
            self.select_all_btn.state(["!disabled"])
        else:
            self.select_all_btn.state(["disabled"])

    def select_all_sounds(self):
        if self.multiple_var.get():
            self.selected_sound_ids = [s["id"] for s in self.sounds]
            self.populate_listbox()
            self.save_settings()

    def get_current_volume(self):
        v = self.volume_var.get()
        if "Loud" in v:
            return 1.0
        elif "Quiet" in v:
            return 0.20
        return 0.55

    def on_key_press(self):
        self.key_count += 1
        # Update counter on UI thread
        self.root.after(0, self.update_key_counter)

        if not self.armed_var.get() or not self.selected_sound_ids:
            return

        chosen_id = random.choice(self.selected_sound_ids)
        sound = next((s for s in self.sounds if s["id"] == chosen_id), None)
        if sound and os.path.exists(sound["path"]):
            self.audio_engine.play(sound["path"], self.get_current_volume())

    def update_key_counter(self):
        self.status_keys_label.config(text=f"Listening · {self.key_count} keys detected")

    def test_sound(self):
        if not self.selected_sound_ids:
            return
        chosen_id = random.choice(self.selected_sound_ids)
        sound = next((s for s in self.sounds if s["id"] == chosen_id), None)
        if sound and os.path.exists(sound["path"]):
            self.audio_engine.play(sound["path"], self.get_current_volume())

    def add_custom_sound(self):
        filetypes = [("Audio Files", "*.mp3 *.wav *.ogg *.aac *.m4a"), ("All Files", "*.*")]
        filenames = filedialog.askopenfilenames(title="Select Audio Files", filetypes=filetypes)
        if not filenames:
            return

        os.makedirs(CUSTOM_SOUNDS_DIR, exist_ok=True)
        added_any = False
        for path in filenames:
            try:
                base_name = os.path.basename(path)
                name_without_ext = os.path.splitext(base_name)[0]
                sound_id = f"custom_{int(random.random() * 1000000)}"
                dest_path = os.path.join(CUSTOM_SOUNDS_DIR, f"{sound_id}_{base_name}")
                with open(path, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())

                self.custom_sounds.append({
                    "id": sound_id,
                    "name": name_without_ext,
                    "path": dest_path
                })
                added_any = True
            except Exception as e:
                messagebox.showerror("Error Adding Sound", f"Could not add {base_name}: {e}")

        if added_any:
            self.build_sound_catalog()
            self.populate_listbox()
            self.save_settings()

    def remove_custom_sound(self):
        selection = self.sound_listbox.curselection()
        if not selection:
            messagebox.showinfo("Remove Sound", "Please select a custom sound from the list to remove.")
            return
        sound = self.sounds[selection[0]]
        if not sound.get("is_custom"):
            messagebox.showwarning("Cannot Remove", "Only user-added custom sounds can be removed.")
            return

        self.custom_sounds = [c for c in self.custom_sounds if c["id"] != sound["id"]]
        if sound["id"] in self.selected_sound_ids:
            self.selected_sound_ids.remove(sound["id"])
        try:
            if os.path.exists(sound["path"]):
                os.remove(sound["path"])
        except Exception:
            pass

        self.build_sound_catalog()
        self.populate_listbox()
        self.save_settings()

    def load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.armed_var.set(data.get("armed", True))
                    self.multiple_var.set(data.get("multiple_sounds", False))
                    self.volume_var.set(data.get("volume", "Medium"))
                    self.selected_sound_ids = data.get("selected_sound_ids", ["gunshotjbudden"])
                    self.custom_sounds = data.get("custom_sounds", [])
        except Exception:
            pass

    def save_settings(self):
        try:
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            data = {
                "armed": self.armed_var.get(),
                "multiple_sounds": self.multiple_var.get(),
                "volume": self.volume_var.get(),
                "selected_sound_ids": self.selected_sound_ids,
                "custom_sounds": self.custom_sounds
            }
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def on_close(self):
        self.hook.stop()
        self.audio_engine.close_all()
        self.save_settings()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SoundPressApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
