// SoundPress Popup Controller (Manifest V3)

const SOUNDS = [
  { id: "gunshotjbudden", name: "Gunshot J Budden", file: "gunshotjbudden.mp3", type: "meme" },
  { id: "shotgun", name: "Shotgun", file: "shotgun.wav", type: "synth" },
  { id: "boing", name: "Cartoon Boing", file: "boing.wav", type: "synth" },
  { id: "beep", name: "Censor Beep", file: "beep.wav", type: "synth" },
  { id: "fart", name: "Dry Fart", file: "fart.wav", type: "synth" },
  { id: "pew", name: "Pew Pew", file: "pew.wav", type: "synth" },
  { id: "quack", name: "Quack", file: "quack.wav", type: "synth" },
  { id: "applepay", name: "Apple Pay", file: "applepay.mp3", type: "sfx" },
  { id: "movie_1", name: "Movie 1", file: "movie_1.mp3", type: "sfx" },
  { id: "rizz-sound-effect", name: "Rizz Sound Effect", file: "rizz-sound-effect.mp3", type: "meme" },
  { id: "wrong-answer-sound-effect", name: "Wrong Answer", file: "wrong-answer-sound-effect.mp3", type: "meme" },
  { id: "yes-lara-voice", name: "Yes Lara Voice", file: "yes-lara-voice.mp3", type: "meme" },
  { id: "shocked-sound-effect", name: "Shocked", file: "shocked-sound-effect.mp3", type: "meme" },
  { id: "punch_u4LmMsr", name: "Punch", file: "punch_u4LmMsr.mp3", type: "sfx" },
  { id: "maro-jump-sound-effect_1", name: "Maro Jump", file: "maro-jump-sound-effect_1.mp3", type: "sfx" },
  { id: "ding-sound-effect_2", name: "Ding", file: "ding-sound-effect_2.mp3", type: "sfx" },
  { id: "anime-ahh", name: "Anime Ahh", file: "anime-ahh.mp3", type: "meme" },
  { id: "67_SQlv2Xv", name: "67", file: "67_SQlv2Xv.mp3", type: "meme" }
];

let state = {
  armed: true,
  multiple_sounds: false,
  volume: 0.55,
  selected_sound_ids: ["gunshotjbudden"],
  key_count: 0
};

// DOM Elements
const armedToggle = document.getElementById("armedToggle");
const multipleToggle = document.getElementById("multipleToggle");
const selectAllBtn = document.getElementById("selectAllBtn");
const soundsContainer = document.getElementById("soundsContainer");
const volumeSelect = document.getElementById("volumeSelect");
const testSoundBtn = document.getElementById("testSoundBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const keyCounter = document.getElementById("keyCounter");

// Initialize Popup
document.addEventListener("DOMContentLoaded", async () => {
  const data = await chrome.storage.local.get(null);
  if (data.armed !== undefined) state.armed = data.armed;
  if (data.multiple_sounds !== undefined) state.multiple_sounds = data.multiple_sounds;
  if (data.volume !== undefined) state.volume = data.volume;
  if (data.selected_sound_ids && data.selected_sound_ids.length > 0) {
    state.selected_sound_ids = data.selected_sound_ids;
  }
  if (data.key_count !== undefined) state.key_count = data.key_count;

  updateUI();
  setupListeners();
});

function updateUI() {
  // Armed toggle
  armedToggle.checked = state.armed;
  if (state.armed) {
    statusDot.className = "dot";
    statusText.textContent = "Active in Chrome";
  } else {
    statusDot.className = "dot muted";
    statusText.textContent = "Muted (Sounds Disabled)";
  }

  // Multiple toggle & Select All button
  multipleToggle.checked = state.multiple_sounds;
  selectAllBtn.style.display = state.multiple_sounds ? "block" : "none";

  // Volume
  volumeSelect.value = String(state.volume);

  // Key counter
  keyCounter.textContent = `${state.key_count} keys`;

  // Render sounds list
  renderSoundsList();
}

function renderSoundsList() {
  soundsContainer.innerHTML = "";

  SOUNDS.forEach((sound) => {
    const isSelected = state.selected_sound_ids.includes(sound.id);
    const item = document.createElement("div");
    item.className = `sound-item ${isSelected ? "selected" : ""}`;

    const inputType = state.multiple_sounds ? "checkbox" : "radio";
    const input = document.createElement("input");
    input.type = inputType;
    input.name = "sound_selection";
    input.checked = isSelected;

    const title = document.createElement("span");
    title.className = "sound-title";
    title.textContent = sound.name;

    const badge = document.createElement("span");
    badge.className = "sound-badge";
    badge.textContent = sound.type.toUpperCase();

    item.appendChild(input);
    item.appendChild(title);
    item.appendChild(badge);

    item.addEventListener("click", (e) => {
      e.preventDefault();
      onSoundClick(sound.id);
    });

    soundsContainer.appendChild(item);
  });
}

async function onSoundClick(soundId) {
  if (state.multiple_sounds) {
    if (state.selected_sound_ids.includes(soundId)) {
      if (state.selected_sound_ids.length > 1) {
        state.selected_sound_ids = state.selected_sound_ids.filter((id) => id !== soundId);
      }
    } else {
      state.selected_sound_ids.push(soundId);
    }
  } else {
    state.selected_sound_ids = [soundId];
  }

  await chrome.storage.local.set({ selected_sound_ids: state.selected_sound_ids });
  renderSoundsList();
}

function setupListeners() {
  armedToggle.addEventListener("change", async () => {
    state.armed = armedToggle.checked;
    await chrome.storage.local.set({ armed: state.armed });
    updateUI();
  });

  multipleToggle.addEventListener("change", async () => {
    state.multiple_sounds = multipleToggle.checked;
    if (!state.multiple_sounds && state.selected_sound_ids.length > 1) {
      state.selected_sound_ids = [state.selected_sound_ids[0]];
    }
    await chrome.storage.local.set({
      multiple_sounds: state.multiple_sounds,
      selected_sound_ids: state.selected_sound_ids
    });
    updateUI();
  });

  selectAllBtn.addEventListener("click", async () => {
    if (state.multiple_sounds) {
      state.selected_sound_ids = SOUNDS.map((s) => s.id);
      await chrome.storage.local.set({ selected_sound_ids: state.selected_sound_ids });
      renderSoundsList();
    }
  });

  volumeSelect.addEventListener("change", async () => {
    state.volume = parseFloat(volumeSelect.value);
    await chrome.storage.local.set({ volume: state.volume });
  });

  testSoundBtn.addEventListener("click", () => {
    if (state.selected_sound_ids.length === 0) return;
    const randomId = state.selected_sound_ids[
      Math.floor(Math.random() * state.selected_sound_ids.length)
    ];
    const sound = SOUNDS.find((s) => s.id === randomId);
    if (!sound) return;

    const audio = new Audio(chrome.runtime.getURL(`sounds/${sound.file}`));
    audio.volume = state.volume;
    audio.play().catch((err) => console.warn("Test audio error:", err));
  });
}
