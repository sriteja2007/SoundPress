// SoundPress Background Service Worker (Manifest V3)

const DEFAULT_SETTINGS = {
  armed: true,
  multiple_sounds: false,
  volume: 0.55,
  selected_sound_ids: ["gunshotjbudden"],
  key_count: 0
};

chrome.runtime.onInstalled.addListener(async () => {
  const existing = await chrome.storage.local.get(null);
  const toSet = {};
  for (const [key, value] of Object.entries(DEFAULT_SETTINGS)) {
    if (existing[key] === undefined) {
      toSet[key] = value;
    }
  }
  if (Object.keys(toSet).length > 0) {
    await chrome.storage.local.set(toSet);
  }
  updateBadge(existing.armed ?? true);
});

async function updateBadge(isArmed) {
  if (isArmed) {
    await chrome.action.setBadgeText({ text: "" });
  } else {
    await chrome.action.setBadgeText({ text: "OFF" });
    await chrome.action.setBadgeBackgroundColor({ color: "#6c757d" });
  }
}

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === "local" && changes.armed) {
    updateBadge(changes.armed.newValue);
  }
});

let creatingOffscreenPromise = null;

async function setupOffscreenDocument() {
  const existingContexts = await chrome.runtime.getContexts({
    contextTypes: ["OFFSCREEN_DOCUMENT"]
  });
  if (existingContexts.length > 0) return;

  if (creatingOffscreenPromise) {
    await creatingOffscreenPromise;
    return;
  }

  creatingOffscreenPromise = chrome.offscreen.createDocument({
    url: "offscreen.html",
    reasons: ["AUDIO_PLAYBACK"],
    justification: "Play keypress sound effects reliably across all web pages"
  });

  await creatingOffscreenPromise;
  creatingOffscreenPromise = null;
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "KEY_PRESSED") {
    (async () => {
      const data = await chrome.storage.local.get("key_count");
      const newCount = (data.key_count || 0) + 1;
      await chrome.storage.local.set({ key_count: newCount });
      sendResponse({ success: true, count: newCount });
    })();
    return true; // async sendResponse
  }

  if (message.type === "PLAY_SOUND") {
    (async () => {
      try {
        await setupOffscreenDocument();
        // Forward message to offscreen document
        chrome.runtime.sendMessage({
          type: "OFFSCREEN_PLAY",
          file: message.file,
          volume: message.volume
        });
        sendResponse({ success: true });
      } catch (err) {
        console.error("Offscreen play error:", err);
        sendResponse({ success: false, error: err.message });
      }
    })();
    return true;
  }
});
