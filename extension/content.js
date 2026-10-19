// SoundPress Content Script (Manifest V3)
// Intercepts keydown events inside Chrome tabs and triggers low-latency Web Audio sound playback.

const SOUND_FILES = {
  "gunshotjbudden": "gunshotjbudden.mp3",
  "shotgun": "shotgun.wav",
  "boing": "boing.wav",
  "beep": "beep.wav",
  "fart": "fart.wav",
  "pew": "pew.wav",
  "quack": "quack.wav",
  "applepay": "applepay.mp3",
  "movie_1": "movie_1.mp3",
  "rizz-sound-effect": "rizz-sound-effect.mp3",
  "wrong-answer-sound-effect": "wrong-answer-sound-effect.mp3",
  "yes-lara-voice": "yes-lara-voice.mp3",
  "shocked-sound-effect": "shocked-sound-effect.mp3",
  "punch_u4LmMsr": "punch_u4LmMsr.mp3",
  "maro-jump-sound-effect_1": "maro-jump-sound-effect_1.mp3",
  "ding-sound-effect_2": "ding-sound-effect_2.mp3",
  "anime-ahh": "anime-ahh.mp3",
  "67_SQlv2Xv": "67_SQlv2Xv.mp3"
};

let currentSettings = {
  armed: true,
  multiple_sounds: false,
  volume: 0.55,
  selected_sound_ids: ["gunshotjbudden"]
};

// Web Audio API Polyphonic Audio Engine
let audioCtx = null;
const soundBuffers = {};

function getAudioContext() {
  if (!audioCtx) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (AudioContextClass) {
      audioCtx = new AudioContextClass();
    }
  }
  if (audioCtx && audioCtx.state === "suspended") {
    audioCtx.resume();
  }
  return audioCtx;
}

async function loadBuffer(filename) {
  if (soundBuffers[filename]) return soundBuffers[filename];
  try {
    const ctx = getAudioContext();
    if (!ctx) return null;
    const url = chrome.runtime.getURL(`sounds/${filename}`);
    const res = await fetch(url);
    const arrayBuffer = await res.arrayBuffer();
    const decoded = await ctx.decodeAudioData(arrayBuffer);
    soundBuffers[filename] = decoded;
    return decoded;
  } catch (err) {
    return null;
  }
}

// Preload the current default sounds
async function preloadCurrentSounds() {
  if (!currentSettings.selected_sound_ids) return;
  for (const id of currentSettings.selected_sound_ids) {
    const file = SOUND_FILES[id];
    if (file) loadBuffer(file);
  }
}

// Load initial settings
chrome.storage.local.get(["armed", "multiple_sounds", "volume", "selected_sound_ids"], (data) => {
  if (data.armed !== undefined) currentSettings.armed = data.armed;
  if (data.multiple_sounds !== undefined) currentSettings.multiple_sounds = data.multiple_sounds;
  if (data.volume !== undefined) currentSettings.volume = data.volume;
  if (data.selected_sound_ids && data.selected_sound_ids.length > 0) {
    currentSettings.selected_sound_ids = data.selected_sound_ids;
  }
  preloadCurrentSounds();
});

// Sync real-time settings changes from popup
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "local") {
    if (changes.armed) currentSettings.armed = changes.armed.newValue;
    if (changes.multiple_sounds) currentSettings.multiple_sounds = changes.multiple_sounds.newValue;
    if (changes.volume) currentSettings.volume = changes.volume.newValue;
    if (changes.selected_sound_ids) {
      currentSettings.selected_sound_ids = changes.selected_sound_ids.newValue;
      preloadCurrentSounds();
    }
  }
});

async function playSound(filename, volume) {
  try {
    const ctx = getAudioContext();
    if (!ctx) {
      // Fallback
      fallbackPlay(filename, volume);
      return;
    }

    let buffer = soundBuffers[filename];
    if (!buffer) {
      buffer = await loadBuffer(filename);
    }

    if (buffer) {
      const source = ctx.createBufferSource();
      source.buffer = buffer;
      const gain = ctx.createGain();
      gain.gain.value = Math.max(0.0, Math.min(1.0, volume));
      source.connect(gain);
      gain.connect(ctx.destination);
      source.start(0);
    } else {
      fallbackPlay(filename, volume);
    }
  } catch (err) {
    fallbackPlay(filename, volume);
  }
}

function fallbackPlay(filename, volume) {
  try {
    const audio = new Audio(chrome.runtime.getURL(`sounds/${filename}`));
    audio.volume = Math.max(0.0, Math.min(1.0, volume));
    audio.play().catch(() => {
      chrome.runtime.sendMessage({
        type: "PLAY_SOUND",
        file: filename,
        volume: volume
      }).catch(() => {});
    });
  } catch {
    chrome.runtime.sendMessage({
      type: "PLAY_SOUND",
      file: filename,
      volume: volume
    }).catch(() => {});
  }
}

// Global keydown event listener on window and document (capture phase)
function handleKeyEvent(e) {
  if (!currentSettings.armed) return;
  if (!currentSettings.selected_sound_ids || currentSettings.selected_sound_ids.length === 0) return;

  // Pick sound based on mode
  let soundId;
  if (currentSettings.multiple_sounds) {
    const ids = currentSettings.selected_sound_ids;
    soundId = ids[Math.floor(Math.random() * ids.length)];
  } else {
    soundId = currentSettings.selected_sound_ids[0];
  }

  const filename = SOUND_FILES[soundId] || "gunshotjbudden.mp3";
  playSound(filename, currentSettings.volume);

  // Send non-blocking key pressed notification for counter
  chrome.runtime.sendMessage({ type: "KEY_PRESSED" }).catch(() => {});
}

// Attach to both window and document to ensure events are captured anywhere on the page
window.addEventListener("keydown", handleKeyEvent, true);
document.addEventListener("keydown", handleKeyEvent, true);
