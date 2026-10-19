// SoundPress Content Script (Manifest V3)
// Intercepts keydown events inside Chrome tabs and triggers low-latency sound playback.

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

// Load initial settings
chrome.storage.local.get(["armed", "multiple_sounds", "volume", "selected_sound_ids"], (data) => {
  if (data.armed !== undefined) currentSettings.armed = data.armed;
  if (data.multiple_sounds !== undefined) currentSettings.multiple_sounds = data.multiple_sounds;
  if (data.volume !== undefined) currentSettings.volume = data.volume;
  if (data.selected_sound_ids && data.selected_sound_ids.length > 0) {
    currentSettings.selected_sound_ids = data.selected_sound_ids;
  }
});

// Sync real-time settings changes from popup
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "local") {
    if (changes.armed) currentSettings.armed = changes.armed.newValue;
    if (changes.multiple_sounds) currentSettings.multiple_sounds = changes.multiple_sounds.newValue;
    if (changes.volume) currentSettings.volume = changes.volume.newValue;
    if (changes.selected_sound_ids) currentSettings.selected_sound_ids = changes.selected_sound_ids.newValue;
  }
});

// Polyphonic local audio cache
const localPool = [];
const POOL_MAX = 8;
let poolIndex = 0;
for (let i = 0; i < POOL_MAX; i++) {
  localPool.push(new Audio());
}

function playAudio(filename, volume) {
  try {
    const audio = localPool[poolIndex];
    poolIndex = (poolIndex + 1) % POOL_MAX;
    audio.src = chrome.runtime.getURL(`sounds/${filename}`);
    audio.volume = Math.max(0.0, Math.min(1.0, volume));
    audio.currentTime = 0;
    const promise = audio.play();
    if (promise !== undefined) {
      promise.catch(() => {
        // Fallback to offscreen document if page CSP or autoplay restricts Audio element
        chrome.runtime.sendMessage({
          type: "PLAY_SOUND",
          file: filename,
          volume: volume
        });
      });
    }
  } catch {
    chrome.runtime.sendMessage({
      type: "PLAY_SOUND",
      file: filename,
      volume: volume
    });
  }
}

// Global keydown event listener
window.addEventListener("keydown", (e) => {
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
  playAudio(filename, currentSettings.volume);

  // Send non-blocking key pressed notification for counter
  chrome.runtime.sendMessage({ type: "KEY_PRESSED" }).catch(() => {});
}, true);
