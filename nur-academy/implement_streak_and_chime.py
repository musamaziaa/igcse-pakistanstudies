import re

with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "r") as f:
    content = f.read()

# 1. Inject playSuccessChime and StreakFlame at the top after imports
components_to_inject = """

export const playSuccessChime = () => {
  try {
    const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const playNode = (freq: number, delay: number) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.value = freq;
      
      const startTime = ctx.currentTime + delay;
      gain.gain.setValueAtTime(0, startTime);
      gain.gain.linearRampToValueAtTime(0.2, startTime + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 1.5);
      
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(startTime);
      osc.stop(startTime + 1.5);
    };

    // A shimmering E major 9 chord
    playNode(659.25, 0);       // E5
    playNode(830.61, 0.04);    // G#5
    playNode(987.77, 0.08);    // B5
    playNode(1244.51, 0.12);   // D#6
    playNode(1479.98, 0.16);   // F#6
  } catch (e) {
    console.error("Audio playback failed", e);
  }
};

const StreakFlame = ({ streak }: { streak: number }) => {
  const intensity = Math.min(streak, 10) / 10;
  const isHigh = streak >= 7;
  const colorClass = streak === 0 ? 'text-slate-600' : isHigh ? 'text-emerald-500' : 'text-orange-500';
  const glowClass = streak === 0 ? '' : isHigh ? 'bg-emerald-500' : 'bg-orange-500';
  const duration = isHigh ? 1.5 : 2.5;

  return (
    <div className="relative mx-auto w-12 h-12 mb-2 flex items-center justify-center">
      {streak > 0 && (
        <motion.div
          animate={{ scale: [1, 1.2 + intensity * 0.3, 1], opacity: [0.3, 0.6 + intensity * 0.2, 0.3] }}
          transition={{ repeat: Infinity, duration, ease: 'easeInOut' }}
          className={`absolute inset-0 rounded-full blur-xl ${glowClass}`}
        />
      )}
      <motion.div
        animate={streak > 0 ? {
          y: [0, -2, 0],
          rotate: [-3, 3, -3],
          scale: [1, 1.05 + intensity * 0.1, 1]
        } : {}}
        transition={{ repeat: Infinity, duration: duration * 0.8, ease: 'easeInOut' }}
        className="relative z-10"
      >
        <Flame size={32} className={colorClass} strokeWidth={isHigh ? 2.5 : 2} />
      </motion.div>
    </div>
  );
};
"""

content = content.replace("export default function App() {", components_to_inject + "\nexport default function App() {")

# 2. Update the Flame icon in progress screen
old_flame_html = '<Flame size={28} className="mx-auto text-orange-500 mb-2" />'
new_flame_html = '<StreakFlame streak={progressData.stats.current_streak} />'
content = content.replace(old_flame_html, new_flame_html)

# 3. Update handleType to play chime
old_handle_type = """    if (val.length >= currentLineText.length) {
      if (activeLineIdx < memQueue[currentMemIdx].lines.length - 1) {
        setActiveLineIdx(activeLineIdx + 1);
        if (inputRef.current) inputRef.current.value = "";
      }
    }"""

new_handle_type = """    if (val.length >= currentLineText.length) {
      if (activeLineIdx < memQueue[currentMemIdx].lines.length - 1) {
        setActiveLineIdx(activeLineIdx + 1);
        if (inputRef.current) inputRef.current.value = "";
      } else if (val.length === currentLineText.length) {
        let typos = 0;
        memQueue[currentMemIdx].lines.forEach((line: string, i: number) => {
          const t = newTyped[i] || '';
          for (let c = 0; c < Math.min(t.length, line.length); c++) {
            if (t[c] !== line[c]) typos++;
          }
        });
        if (typos === 0) {
          playSuccessChime();
        }
      }
    }"""

content = content.replace(old_handle_type, new_handle_type)

with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "w") as f:
    f.write(content)
