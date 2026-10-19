// SoundPress New Tab Audio & Search Controller

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

let settings = {
  armed: true,
  multiple_sounds: false,
  volume: 0.55,
  selected_sound_ids: ["gunshotjbudden"]
};

// Web Audio API engine
let audioCtx = null;
const audioBuffers = {};

function getAudioContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === "suspended") {
    audioCtx.resume();
  }
  return audioCtx;
}

async function getSoundBuffer(filename) {
  if (audioBuffers[filename]) return audioBuffers[filename];
  try {
    const ctx = getAudioContext();
    const resp = await fetch(chrome.runtime.getURL(`sounds/${filename}`));
    const arrayBuffer = await resp.arrayBuffer();
    const decoded = await ctx.decodeAudioData(arrayBuffer);
    audioBuffers[filename] = decoded;
    return decoded;
  } catch (e) {
    return null;
  }
}

async function playKeySound(filename, volume) {
  try {
    const ctx = getAudioContext();
    const buffer = await getSoundBuffer(filename);
    if (!buffer) return;

    const source = ctx.createBufferSource();
    source.buffer = buffer;
    const gainNode = ctx.createGain();
    gainNode.gain.value = Math.max(0.0, Math.min(1.0, volume));
    source.connect(gainNode);
    gainNode.connect(ctx.destination);
    source.start(0);
  } catch (err) {
    console.warn("Newtab audio playback error:", err);
  }
}

// Load settings and update UI badges
async function loadSettings() {
  const data = await chrome.storage.local.get(null);
  if (data.armed !== undefined) settings.armed = data.armed;
  if (data.multiple_sounds !== undefined) settings.multiple_sounds = data.multiple_sounds;
  if (data.volume !== undefined) settings.volume = data.volume;
  if (data.selected_sound_ids && data.selected_sound_ids.length > 0) {
    settings.selected_sound_ids = data.selected_sound_ids;
  }

  const statusBadge = document.getElementById("statusBadge");
  const soundNameBadge = document.getElementById("soundNameBadge");
  if (statusBadge) {
    statusBadge.textContent = settings.armed ? "🔊 SoundPress: Armed" : "🔇 SoundPress: Muted";
    statusBadge.style.color = settings.armed ? "#34D399" : "#94A3B8";
  }
  if (soundNameBadge) {
    soundNameBadge.textContent = settings.multiple_sounds
      ? "Sound: Multiple (Random Mix)"
      : `Sound: ${settings.selected_sound_ids[0] || "Gunshot"}`;
  }
}

chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "local") {
    loadSettings();
  }
});

// Capture ANY key pressed on the New Tab page (in the search input, or anywhere on the page!)
window.addEventListener("keydown", (e) => {
  if (!settings.armed || !settings.selected_sound_ids.length) return;

  let soundId;
  if (settings.multiple_sounds) {
    soundId = settings.selected_sound_ids[
      Math.floor(Math.random() * settings.selected_sound_ids.length)
    ];
  } else {
    soundId = settings.selected_sound_ids[0];
  }

  const filename = SOUND_FILES[soundId] || "gunshotjbudden.mp3";
  playKeySound(filename, settings.volume);

  chrome.runtime.sendMessage({ type: "KEY_PRESSED" }).catch(() => {});
}, true);

// Focus search box automatically
document.addEventListener("DOMContentLoaded", () => {
  loadSettings();
  const input = document.getElementById("searchInput");
  if (input) input.focus();
});
