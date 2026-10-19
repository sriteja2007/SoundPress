#!/usr/bin/env python3
"""
SoundPress Chrome-Bound Companion
Listens for keypresses ONLY when Google Chrome is the active foreground window.
Works across the entire Chrome window: address bar / omnibox, search, tabs, webpages, DevTools!
Automatically exits the instant Google Chrome is closed.
"""

import os
import sys
import time
import json
import random
import ctypes
from ctypes import wintypes
import threading

# Win32 APIs & Constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

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

kernel32.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(
    os.environ.get("LOCALAPPDATA", BASE_DIR),
    "SoundPress",
    "settings.json"
)

SOUND_FILES = [
    os.path.join(BASE_DIR, "bundled-sounds", "gunshotjbudden.mp3"),
    os.path.join(BASE_DIR, "generated-sounds", "shotgun.wav"),
    os.path.join(BASE_DIR, "generated-sounds", "boing.wav"),
    os.path.join(BASE_DIR, "generated-sounds", "beep.wav"),
    os.path.join(BASE_DIR, "generated-sounds", "fart.wav"),
    os.path.join(BASE_DIR, "generated-sounds", "pew.wav"),
    os.path.join(BASE_DIR, "generated-sounds", "quack.wav"),
    os.path.join(BASE_DIR, "bundled-sounds", "applepay.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "movie_1.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "rizz-sound-effect.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "wrong-answer-sound-effect.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "yes-lara-voice.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "shocked-sound-effect.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "punch_u4LmMsr.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "maro-jump-sound-effect_1.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "ding-sound-effect_2.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "anime-ahh.mp3"),
    os.path.join(BASE_DIR, "bundled-sounds", "67_SQlv2Xv.mp3")
]

class ChromeAudioPlayer:
    def __init__(self, max_voices=12):
        self.max_voices = max_voices
        self.voice_index = 0
        self.lock = threading.Lock()

    def play(self, filepath, volume=0.55):
        if not os.path.exists(filepath):
            return
        threading.Thread(target=self._play_worker, args=(os.path.abspath(filepath), volume), daemon=True).start()

    def _play_worker(self, abs_path, volume):
        with self.lock:
            self.voice_index = (self.voice_index + 1) % self.max_voices
            alias = f"sp_chr_{self.voice_index}"

        mciSendStringW(f'close {alias}', None, 0, None)
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
            mciSendStringW(f'close sp_chr_{i}', None, 0, None)


def is_chrome_foreground():
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return False
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if not pid.value:
        return False

    hProcess = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
    if not hProcess:
        return False

    buf = ctypes.create_unicode_buffer(1024)
    size = wintypes.DWORD(len(buf))
    success = kernel32.QueryFullProcessImageNameW(hProcess, 0, buf, ctypes.byref(size))
    kernel32.CloseHandle(hProcess)

    if success:
        proc_name = os.path.basename(buf.value).lower()
        return "chrome" in proc_name
    return False


def is_chrome_running():
    # Enumerate processes or check snapshot
    # Fast check via CreateToolhelp32Snapshot
    TH32CS_SNAPPROCESS = 0x00000002
    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ('dwSize', wintypes.DWORD),
            ('cntUsage', wintypes.DWORD),
            ('th32ProcessID', wintypes.DWORD),
            ('th32DefaultHeapID', ctypes.POINTER(wintypes.ULONG)),
            ('th32ModuleID', wintypes.DWORD),
            ('cntThreads', wintypes.DWORD),
            ('th32ParentProcessID', wintypes.DWORD),
            ('pcPriClassBase', wintypes.LONG),
            ('dwFlags', wintypes.DWORD),
            ('szExeFile', wintypes.WCHAR * 260)
        ]

    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == -1:
        return False

    pe = PROCESSENTRY32W()
    pe.dwSize = ctypes.sizeof(PROCESSENTRY32W)
    found = False
    if kernel32.Process32FirstW(snapshot, ctypes.byref(pe)):
        while True:
            if pe.szExeFile.lower() == "chrome.exe":
                found = True
                break
            if not kernel32.Process32NextW(snapshot, ctypes.byref(pe)):
                break
    kernel32.CloseHandle(snapshot)
    return found


def main():
    print("=" * 60)
    print("  SoundPress Chrome-Bound Companion")
    print("  Active ONLY when Google Chrome is the foreground window.")
    print("  Captures: address bar, search, tabs, webpages, DevTools.")
    print("  Automatically closes when Google Chrome exits.")
    print("=" * 60)

    # Check if Chrome is currently running
    if not is_chrome_running():
        print("\nNotice: Google Chrome is not currently open.")
        print("Waiting for Google Chrome to start...")
        while not is_chrome_running():
            time.sleep(1)
        print("Google Chrome detected! SoundPress is now active.")
    else:
        print("Google Chrome is running. SoundPress is active.")

    audio_player = ChromeAudioPlayer()
    selected_sound = SOUND_FILES[0]  # Gunshot J Budden default
    if not os.path.exists(selected_sound):
        # Fallback to any existing sound in SOUND_FILES
        for s in SOUND_FILES:
            if os.path.exists(s):
                selected_sound = s
                break

    keep_running = True
    main_thread_id = kernel32.GetCurrentThreadId()

    def on_key_down():
        # ONLY play if Chrome is the active foreground window
        if is_chrome_foreground():
            audio_player.play(selected_sound, 0.55)

    def hook_loop():
        def _callback(nCode, wParam, lParam):
            if nCode >= 0 and (wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN):
                try:
                    on_key_down()
                except Exception:
                    pass
            return user32.CallNextHookEx(hook, nCode, wParam, lParam)

        cb_ref = HOOKPROC(_callback)
        hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, cb_ref, 0, 0)
        if not hook:
            print("Failed to install keyboard hook.")
            return

        msg = wintypes.MSG()
        while keep_running:
            res = user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)
            if res <= 0:
                break
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

        if hook:
            user32.UnhookWindowsHookEx(hook)

    hook_thread = threading.Thread(target=hook_loop, daemon=True)
    hook_thread.start()

    # Chrome Watchdog: polls Chrome process state
    try:
        while True:
            time.sleep(1.5)
            if not is_chrome_running():
                print("\n[SoundPress] Google Chrome has been closed.")
                print("[SoundPress] Auto-terminating now. Goodbye!")
                break
    except KeyboardInterrupt:
        pass
    finally:
        keep_running = False
        user32.PostThreadMessageW(main_thread_id, 0x0012, 0, 0)
        audio_player.close_all()


if __name__ == "__main__":
    main()
