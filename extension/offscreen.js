// SoundPress Offscreen Audio Worker (Manifest V3)
// Plays polyphonic sound effects without being affected by webpage CSP or autoplay policies.

const POOL_SIZE = 12;
const audioPool = [];
let poolIndex = 0;

for (let i = 0; i < POOL_SIZE; i++) {
  audioPool.push(new Audio());
}

chrome.runtime.onMessage.addListener((message) => {
  if (message.type === "OFFSCREEN_PLAY" && message.file) {
    try {
      const audio = audioPool[poolIndex];
      poolIndex = (poolIndex + 1) % POOL_SIZE;

      audio.src = chrome.runtime.getURL(`sounds/${message.file}`);
      audio.volume = Math.max(0.0, Math.min(1.0, message.volume ?? 0.55));
      audio.currentTime = 0;
      audio.play().catch((err) => {
        console.warn("Audio playback failed:", err);
      });
    } catch (e) {
      console.warn("Offscreen audio error:", e);
    }
  }
});
