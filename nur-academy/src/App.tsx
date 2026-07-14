import { useState, useEffect, useRef, useCallback } from 'react';
import type { ReactNode } from 'react';
import { 
  Timer, 
  Bell, 
  Star, 
  ArrowLeft, 
  ArrowRight, 
  LayoutGrid, 
  Trophy, 
  LayoutDashboard, 
  BookOpen, 
  GraduationCap, 
  Settings,
  CheckCircle2,
  PlayCircle,
  ChevronRight,
  XCircle,
  Map,
  Search,
  UtensilsCrossed,
  Cpu,
  BrainCircuit,
  MonitorSmartphone,
  ClipboardList,
  Rocket,
  Lightbulb,
  LogOut,
  Flame,
  Clock,
  Calendar,
  Target,
  BarChart3
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { useGoogleLogin } from '@react-oauth/google';
import * as htmlToImage from 'html-to-image';

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

// --- Google Auth Types & Helpers ---
interface GoogleUser {
  sub: string;        // unique Google user ID
  name: string;       // display name
  email: string;
  picture: string;    // profile photo URL
}

const STORAGE_KEY = 'nur_academy_user';

function loadUser(): GoogleUser | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch { return null; }
}

function saveUser(user: GoogleUser) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(user));
}

function clearUser() {
  localStorage.removeItem(STORAGE_KEY);
}

interface MemCard {
  id: string;
  section?: string;
  category?: string;
  display_category?: string;
  group_id: string;
  group_label: string;
  title: string;
  arabic?: string;
  lines: string[];
  tier_label?: string;
}



interface Subject {
  key: string;
  name: string;
  tagline: string;
  icon: ReactNode;
  card: string;
  iconWrap: string;
  heading: string;
  tagClass: string;
  isLocked?: boolean;
  circleBg?: string;
}

const SUBJECTS: Subject[] = [
  {
    key: 'islamiyat', name: 'Islamiyat', tagline: 'IGCSE LRN Global Board',
    icon: <BookOpen size={48} className="text-emerald-400" />,
    card: 'bg-slate-900 border-slate-800 hover:border-emerald-500/50 hover:shadow-[0_0_30px_rgba(52,211,153,0.15)]',
    iconWrap: '', heading: 'text-slate-100',
    tagClass: 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20',
    circleBg: 'bg-emerald-600'
  },
  {
    key: 'pak_studies', name: 'Pak Studies', tagline: 'IGCSE LRN Global Board',
    icon: <Map size={48} className="text-blue-400" />,
    card: 'bg-slate-900 border-slate-800 hover:border-blue-500/50 hover:shadow-[0_0_30px_rgba(96,165,250,0.15)]',
    iconWrap: '', heading: 'text-slate-100',
    tagClass: 'bg-blue-500/10 text-blue-300 border border-blue-500/20',
    circleBg: 'bg-blue-600'
  },
  {
    key: 'hospitality', name: 'Hospitality', tagline: 'IGCSE LRN Global Board',
    icon: <UtensilsCrossed size={48} className="text-amber-400" />,
    card: 'bg-slate-900 border-slate-800 hover:border-amber-500/50 hover:shadow-[0_0_30px_rgba(245,158,11,0.15)]',
    iconWrap: '', heading: 'text-slate-100',
    tagClass: 'bg-amber-500/10 text-amber-300 border border-amber-500/20',
    circleBg: 'bg-amber-600'
  },
  {
    key: 'cs', name: 'Computer Science', tagline: 'IGCSE LRN Global Board',
    icon: <Cpu size={48} className="text-slate-400" />,
    card: 'bg-slate-900 border-slate-800 hover:border-slate-500/50 hover:shadow-[0_0_30px_rgba(148,163,184,0.15)]',
    iconWrap: '', heading: 'text-slate-100',
    tagClass: 'bg-slate-500/10 text-slate-300 border border-slate-500/20',
    circleBg: 'bg-slate-600'
  },
  {
    key: 'ai', name: 'Artificial Intelligence', tagline: 'IGCSE LRN Global Board',
    icon: <BrainCircuit size={48} className="text-violet-400" />,
    card: 'bg-slate-900 border-slate-800 hover:border-violet-500/50 hover:shadow-[0_0_30px_rgba(139,92,246,0.15)]',
    iconWrap: '', heading: 'text-slate-100',
    tagClass: 'bg-violet-500/10 text-violet-300 border border-violet-500/20',
    circleBg: 'bg-violet-600'
  },
  {
    key: 'ict', name: 'ICT', tagline: 'IGCSE LRN Global Board',
    icon: <MonitorSmartphone size={48} className="text-rose-400" />,
    card: 'bg-slate-900 border-slate-800 hover:border-rose-500/50 hover:shadow-[0_0_30px_rgba(243,64,121,0.15)]',
    iconWrap: '', heading: 'text-slate-100',
    tagClass: 'bg-rose-500/10 text-rose-300 border border-rose-500/20',
    circleBg: 'bg-rose-600'
  },
];



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

export default function App() {
  const [view, setView] = useState<'subject_selection' | 'dashboard' | 'exam' | 'memorize' | 'project_guide' | 'prep_session' | 'progress'>('subject_selection');
  const [activeSubject, setActiveSubject] = useState<string | null>(null);
  const [guide, setGuide] = useState<any>(null);
  const [prepSessions, setPrepSessions] = useState<any[]>([]);
  const [activeSession, setActiveSession] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState("");

  // --- Auth State ---
  const [user, setUser] = useState<GoogleUser | null>(loadUser);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const studentName = user?.name || 'Guest';

  const googleLogin = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      try {
        const res = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
          headers: { Authorization: `Bearer ${tokenResponse.access_token}` },
        });
        const profile = await res.json();
        const gUser: GoogleUser = {
          sub: profile.sub,
          name: profile.name,
          email: profile.email,
          picture: profile.picture,
        };
        saveUser(gUser);
        setUser(gUser);
        // Sync profile to backend
        fetch(`${API_BASE}/api/users/${profile.sub}/profile`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: profile.name, email: profile.email, picture: profile.picture }),
        }).catch(() => {});
      } catch (err) {
        console.error('Failed to fetch Google profile:', err);
      }
    },
    onError: (err) => console.error('Google login error:', err),
  });

  const handleLogout = useCallback(() => {
    clearUser();
    setUser(null);
    setShowUserMenu(false);
  }, []);

  const requireLogin = (action: () => void) => {
    if (!user) {
      if (confirm('Sign in with Google to save your progress. Sign in now?')) {
        googleLogin();
      }
      return;
    }
    action();
  };
  
  // Exam State
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentQIdx, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [revealed, setRevealed] = useState<Record<number, boolean>>({});

  // Memorize State
  const [memData, setMemData] = useState<MemCard[]>([]);
  const [selectedGroups, setSelectedGroups] = useState<string[]>([]);
  const [memQueue, setMemQueue] = useState<MemCard[]>([]);
  const [currentMemIdx, setCurrentMemIdx] = useState(0);
  const [typedLines, setTypedLines] = useState<string[]>([]);
  const [activeLineIdx, setActiveLineIdx] = useState(0);
  const [isMemStarted, setIsMemStarted] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const [toast, setToast] = useState<{message: string, type: 'error' | 'success'} | null>(null);

  const showToast = (message: string, type: 'error' | 'success' = 'error') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  // Progress Tracking State
  const [cardStartTime, setCardStartTime] = useState<number>(0);
  const [cardStats, setCardStats] = useState<Array<{card_id: string, title: string, lines_total: number, lines_completed: number, accuracy_pct: number, typo_count: number, time_seconds: number}>>([]);
  const [sessionStartTime, setSessionStartTime] = useState<number>(0);
  const [examStartTime, setExamStartTime] = useState<number>(0);
  const [examElapsed, setExamElapsed] = useState<number>(0);
  const [progressData, setProgressData] = useState<any>(null);
  const [selectedDay, setSelectedDay] = useState<string | null>(null);
  const [sessionResult, setSessionResult] = useState<{
    type: 'memorize' | 'exam';
    subject: string;
    accuracy: number;
    timeSec: number;
    cardsCompleted?: number;
    cardsTotal?: number;
    score?: number;
    totalMarks?: number;
    percentage?: number;
    cardDetails?: Array<{title: string; accuracy_pct: number; typo_count: number; time_seconds: number}>;
  } | null>(null);

  const shareOnWhatsApp = async () => {
    if (!sessionResult) return;
    const card = document.getElementById('session-result-card');
    if (!card) {
      alert("Could not generate image.");
      return;
    }

    try {
      showToast("Generating image...", "success");
      // Temporarily hide things if we wanted, but the card only wraps the content, not buttons
      const blob = await htmlToImage.toBlob(card, {
        backgroundColor: '#020617', // slate-950
        pixelRatio: 2,
        style: { transform: 'none' }, // prevent scale weirdness
        filter: (node: HTMLElement) => {
          if (node.tagName === 'IMG' && (node as HTMLImageElement).src?.includes('googleusercontent.com')) {
            return false; // Skip fetching Google PFP for the screenshot to avoid 429 crashes
          }
          return true;
        }
      });

      if (!blob) return;
      const subjectName = SUBJECTS.find((s: Subject) => s.key === sessionResult.subject)?.name || sessionResult.subject;
      const text = `🚀 Just finished my ${subjectName} session on Nur Academy!`;
      
      const file = new File([blob], 'nur-academy-result.png', { type: 'image/png' });

      if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
          await navigator.share({
            text: text,
            files: [file]
          });
          return;
        } catch (e) {
          console.error("Web Share failed:", e);
        }
      }
      
      // Fallback: copy to clipboard or download, then open WhatsApp
      try {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ]);
        alert("📋 Image copied to your clipboard!\n\nWhatsApp Web does not allow images to be attached via links automatically. When WhatsApp opens, please press Ctrl+V (or Right-Click -> Paste) in the chat box to attach your screenshot!");
      } catch {
        // If clipboard fails, just download
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'nur-academy-result.png';
        a.click();
        URL.revokeObjectURL(url);
        alert("🖼️ Image downloaded to your computer!\n\nWhatsApp Web does not allow images to be attached via links automatically. When WhatsApp opens, please drag and drop the downloaded image into the chat box!");
      }
      
      const encoded = encodeURIComponent(text);
      window.open(`https://wa.me/?text=${encoded}`, '_blank');

    } catch (err) {
      console.error(err);
      showToast('Failed to generate screenshot.');
    }
  };

  const fmtTime = (s: number) => { const h = Math.floor(s / 3600); const m = Math.floor((s % 3600) / 60); return h > 0 ? `${h}h ${m}m` : `${m}m`; };
  const fmtTimer = (s: number) => { const m = Math.floor(s / 60); const sec = s % 60; return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`; };

  // Fetch optional Paper 2 / practical project guide when subject changes
  useEffect(() => {
    if (!activeSubject) { setGuide(null); return; }
    setGuide(null);
    fetch(`${API_BASE}/api/${activeSubject}/project_guide`)
      .then(res => res.ok ? res.json() : null)
      .then(data => setGuide(data))
      .catch(() => setGuide(null));
  }, [activeSubject]);

  // Fetch optional Paper 2 preparation sessions (step-by-step practical walkthroughs) when subject changes
  useEffect(() => {
    if (!activeSubject) { setPrepSessions([]); setActiveSession(null); return; }
    setPrepSessions([]);
    setActiveSession(null);
    fetch(`${API_BASE}/api/${activeSubject}/prep_sessions`)
      .then(res => res.ok ? res.json() : null)
      .then(data => setPrepSessions(data?.sessions ?? []))
      .catch(() => setPrepSessions([]));
  }, [activeSubject]);

  // Fetch Memorize Data when subject changes
  useEffect(() => {
    if (!activeSubject) return;
    const fetchData = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/${activeSubject}/memorize`);
        if (!res.ok) throw new Error("Could not fetch memorize data");
        const data = await res.json();
        if (data.cards) {
          setMemData(data.cards);
        } else {
          console.warn("API returned no cards:", data);
          setMemData([]);
        }
      } catch (err) {
        console.error("API Connection Error:", err);
        setMemData([]);
      }
    };
    fetchData();
  }, [activeSubject]);

  // Auto-scroll to active line in Memorize view
  useEffect(() => {
    const activeEl = document.getElementById(`mem-line-${activeLineIdx}`);
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [activeLineIdx]);

  // Exam timer interval
  useEffect(() => {
    if (view !== 'exam' || questions.length === 0 || examStartTime === 0) return;
    const interval = setInterval(() => {
      setExamElapsed(Math.round((Date.now() - examStartTime) / 1000));
    }, 1000);
    return () => clearInterval(interval);
  }, [view, questions.length, examStartTime]);

  // Fetch progress data
  useEffect(() => {
    if (view === 'progress' && user && activeSubject) {
      fetch(`${API_BASE}/api/users/${user.sub}/${activeSubject}/progress`)
        .then(r => r.ok ? r.json() : null)
        .then(d => { if (d) setProgressData(d); })
        .catch(() => {});
    }
  }, [view, user, activeSubject]);

  // --- Exam Logic ---
  const startExam = async () => {
    if (!activeSubject) return;
    try {
      const res = await fetch(`${API_BASE}/api/${activeSubject}/exam/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_name: studentName, n_questions: 10 })
      });
      
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Failed to generate exam");
      }

      if (!data.questions || data.questions.length === 0) {
        throw new Error("No questions found in the question bank.");
      }

      setQuestions(data.questions);
      setCurrentQuestion(0);
      setAnswers({});
      setRevealed({});
      setExamStartTime(Date.now());
      setExamElapsed(0);
      setView('exam');
    } catch (err: any) {
      alert(`⚠️ Error: ${err.message}`);
    }
  };

  const submitExam = async () => {
    if (!activeSubject) return;
    const realTime = Math.round((Date.now() - examStartTime) / 1000);
    const endpoint = user
      ? `${API_BASE}/api/users/${user.sub}/${activeSubject}/exam/evaluate`
      : `${API_BASE}/api/${activeSubject}/exam/evaluate`;
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_name: studentName, questions, answers, time_taken: realTime })
      });
      const data = await res.json();
      setExamStartTime(0);
      setSessionResult({
        type: 'exam',
        subject: activeSubject,
        accuracy: data.percentage ?? 0,
        timeSec: realTime,
        score: data.score,
        totalMarks: data.total,
        percentage: data.percentage,
      });
      setView('session_result');
    } catch {
      alert("Failed to submit exam.");
    }
  };

  // --- Memorize Logic ---
  const toggleGroup = (groupId: string) => {
    setSelectedGroups(prev => prev.includes(groupId) ? prev.filter(g => g !== groupId) : [...prev, groupId]);
  };

  const startMemorize = () => {
    const queue = memData.filter(c => selectedGroups.includes(c.group_id));
    if (queue.length === 0) return alert("Select at least one topic!");
    setMemQueue(queue);
    setCurrentMemIdx(0);
    resetCard(queue[0]);
    setCardStats([]);
    setCardStartTime(Date.now());
    setSessionStartTime(Date.now());
    setIsMemStarted(true);
  };

  const resetCard = (card: any) => {
    setTypedLines(new Array(card.lines.length).fill(""));
    setActiveLineIdx(0);
  };

  const handleType = (val: string) => {
    const currentLineText = memQueue[currentMemIdx].lines[activeLineIdx];
    const newTyped = [...typedLines];
    newTyped[activeLineIdx] = val;
    setTypedLines(newTyped);

    if (val.length >= currentLineText.length) {
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
    }
  };

  const captureCardStats = () => {
    const card = memQueue[currentMemIdx];
    let totalChars = 0, correctChars = 0, typos = 0;
    card.lines.forEach((line: string, i: number) => {
      const typed = typedLines[i] || '';
      for (let c = 0; c < line.length; c++) {
        totalChars++;
        if (c < typed.length) {
          if (typed[c] === line[c]) correctChars++;
          else typos++;
        }
      }
    });
    const accuracy = totalChars > 0 ? Math.round((correctChars / totalChars) * 1000) / 10 : 0;
    const timeSec = Math.round((Date.now() - cardStartTime) / 1000);
    return {
      card_id: card.id,
      title: card.title,
      lines_total: card.lines.length,
      lines_completed: card.lines.length,
      accuracy_pct: accuracy,
      typo_count: typos,
      time_seconds: timeSec,
    };
  };

  const nextCard = () => {
    const stats = captureCardStats();
    const newCardStats = [...cardStats, stats];
    setCardStats(newCardStats);
    if (currentMemIdx < memQueue.length - 1) {
      const nextIdx = currentMemIdx + 1;
      setCurrentMemIdx(nextIdx);
      resetCard(memQueue[nextIdx]);
      setCardStartTime(Date.now());
      if (inputRef.current) inputRef.current.value = "";
    } else {
      finishMemorizeWith(newCardStats);
    }
  };

  const finishMemorizeWith = async (allCardStats: typeof cardStats) => {
    if (!activeSubject) return;
    const totalTime = Math.round((Date.now() - sessionStartTime) / 1000);
    const accArr = allCardStats.map(c => c.accuracy_pct);
    const overallAcc = accArr.length > 0 ? Math.round((accArr.reduce((a, b) => a + b, 0) / accArr.length) * 10) / 10 : 0;
    const endpoint = user
      ? `${API_BASE}/api/users/${user.sub}/${activeSubject}/memorize-attempt`
      : `${API_BASE}/api/students/${studentName}/${activeSubject}/memorize-attempt`;
    const body = user ? {
      groups_selected: selectedGroups,
      cards: allCardStats,
      cards_completed: memQueue.length,
      cards_total: memQueue.length,
      total_time_seconds: totalTime,
      overall_accuracy_pct: overallAcc,
    } : {
      groups_selected: selectedGroups,
      cards_completed: memQueue.length,
      cards_total: memQueue.length,
    };
    await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).catch(() => {});
    setIsMemStarted(false);
    setSessionResult({
      type: 'memorize',
      subject: activeSubject,
      accuracy: overallAcc,
      timeSec: totalTime,
      cardsCompleted: memQueue.length,
      cardsTotal: memQueue.length,
      cardDetails: allCardStats.map(c => ({
        title: c.title,
        accuracy_pct: c.accuracy_pct,
        typo_count: c.typo_count,
        time_seconds: c.time_seconds,
      })),
    });
    setView('session_result');
  };

  const finishMemorize = async () => {
    const stats = captureCardStats();
    const allCardStats = [...cardStats, stats];
    await finishMemorizeWith(allCardStats);
  };

  const currentMemCard = memQueue[currentMemIdx];
  const allLinesDone = currentMemCard && activeLineIdx === currentMemCard.lines.length - 1 && typedLines[activeLineIdx].length >= currentMemCard.lines[activeLineIdx].length;

  return (
    <div className="min-h-screen pb-24 flex flex-col bg-slate-950 text-slate-200 font-sans selection:bg-emerald-500/30">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-slate-900/80 backdrop-blur-md border-b border-slate-800 z-50 px-4 md:px-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-black text-emerald-400 tracking-tight italic flex items-center gap-2">
            <div className="w-8 h-8 bg-emerald-500/20 rounded-lg flex items-center justify-center border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.2)]"><Rocket size={18} className="text-emerald-400" /></div>
            NUR ACADEMY
          </h1>
          {activeSubject && (
             <button onClick={() => { setActiveSubject(null); setView('subject_selection'); setIsMemStarted(false); setQuestions([]); }} className="text-sm font-bold text-slate-400 hover:text-emerald-400 flex items-center gap-1 bg-slate-800/50 hover:bg-slate-800 px-3 py-1.5 rounded-full transition-colors border border-slate-700/50 hover:border-emerald-500/30">
               <ArrowLeft size={16} /> Subjects
             </button>
          )}
        </div>
        <div className="flex items-center gap-3">
          {user ? (
            <div className="relative">
              <button onClick={() => setShowUserMenu(!showUserMenu)} className="flex items-center gap-2 hover:opacity-80 transition-opacity">
                <img src={user.picture} alt={user.name} className="w-9 h-9 rounded-full border-2 border-emerald-500 object-cover shadow-[0_0_10px_rgba(16,185,129,0.3)]" referrerPolicy="no-referrer" />
                <span className="hidden md:block text-sm font-bold text-slate-200">{user.name}</span>
              </button>
              {showUserMenu && (
                <div className="absolute right-0 top-12 bg-slate-900 border border-slate-700 rounded-xl shadow-xl shadow-black/50 p-2 min-w-[200px] z-[60]">
                  <div className="px-3 py-2 border-b border-slate-800 mb-1">
                    <p className="font-bold text-sm text-white">{user.name}</p>
                    <p className="text-xs text-slate-400">{user.email}</p>
                  </div>
                  <button onClick={handleLogout} className="w-full text-left px-3 py-2 text-sm font-medium text-rose-400 hover:bg-rose-500/10 hover:text-rose-300 rounded-lg flex items-center gap-2 transition-colors">
                    <LogOut size={16} /> Sign out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button onClick={() => googleLogin()} className="flex items-center gap-2 px-4 py-2 bg-slate-800 border border-slate-700 rounded-full hover:border-emerald-500/50 hover:bg-slate-700 hover:shadow-[0_0_15px_rgba(16,185,129,0.15)] transition-all text-sm font-bold text-slate-200">
              <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59a14.5 14.5 0 0 1 0-9.18l-7.98-6.19a24.04 24.04 0 0 0 0 21.56l7.98-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>
              Sign in
            </button>
          )}
        </div>
      </header>

      <main className="mt-24 flex-1 w-full max-w-7xl mx-auto px-4 md:px-8">
        <AnimatePresence mode="wait">
          {view === 'subject_selection' && (
            <motion.div key="subject_selection" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-8 mt-12">
              <div className="text-center mb-10">
                <h2 className="text-4xl md:text-5xl font-black text-white mb-4 tracking-tight drop-shadow-md">Master your IGCSEs.</h2>
                <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto">AI-powered, interactive learning designed specifically for the LRN Global Board.</p>
              </div>
              
                            {/* Active Subjects */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto w-full mb-8">
                {SUBJECTS.filter((s: Subject) => !s.isLocked).map((subject: Subject, idx: number) => (
                  <button key={subject.key} onClick={() => { setActiveSubject(subject.key); setView('dashboard'); }} className={`text-left p-8 rounded-2xl border transition-all flex flex-col group relative overflow-hidden ${subject.card}`}>
                    {/* Corner Circle with Number */}
                    <div className={`absolute -top-12 -right-12 w-32 h-32 rounded-full transition-transform duration-500 group-hover:scale-110 flex items-end justify-start p-8 font-black text-3xl text-white shadow-lg ${subject.circleBg}`}>
                       <span className="leading-none tracking-tight">0{idx + 1}</span>
                    </div>
                    
                    {/* Bare Icon */}
                    <div className="mb-6 group-hover:scale-110 transition-transform origin-left">
                      {subject.icon}
                    </div>
                    
                    <h3 className={`text-2xl font-bold mt-2 ${subject.heading}`}>{subject.name}</h3>
                    <p className="mt-4 text-slate-400 font-medium text-sm leading-relaxed flex-1">{subject.tagline}</p>
                    
                    <div className="mt-8 flex items-center text-slate-300 font-bold text-sm uppercase tracking-wider group-hover:translate-x-2 transition-transform">
                      Enter Subject <ChevronRight size={18} className="ml-1" />
                    </div>
                  </button>
                ))}
              </div>


              {/* Locked Subjects */}
              {SUBJECTS.filter((s: Subject) => s.isLocked).length > 0 && (
              <div className="max-w-4xl mx-auto w-full">
                <div className="flex items-center gap-4 mb-6">
                  <div className="h-px bg-slate-800 flex-1" />
                  <span className="text-sm font-bold text-slate-400 uppercase tracking-wider">Coming Soon</span>
                  <div className="h-px bg-slate-800 flex-1" />
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {SUBJECTS.filter((s: Subject) => s.isLocked).map((subject: Subject) => (
                    <div key={subject.key} className="p-5 rounded-2xl border border-slate-800/50 bg-slate-900/50 flex flex-col items-center justify-center text-center opacity-60 backdrop-blur-sm">
                      <div className="text-slate-400 mb-3 grayscale">
                        {subject.icon}
                      </div>
                      <h3 className="text-sm font-bold text-slate-300">{subject.name}</h3>
                    </div>
                  ))}
                </div>
              </div>
              )}
            </motion.div>
          )}

          {view === 'dashboard' && (
            <motion.div key="dash" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-10 mt-6 max-w-5xl mx-auto w-full">
              <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-slate-800">
                <div>
                  <div className="flex items-center gap-3 mb-4">
                    <span className={`px-3 py-1 rounded-full font-bold uppercase tracking-wider text-xs ${SUBJECTS.find((s: Subject) => s.key === activeSubject)?.tagClass ?? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}`}>
                      {SUBJECTS.find((s: Subject) => s.key === activeSubject)?.name ?? activeSubject}
                    </span>
                  </div>
                  <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">Assalam-o-Alaikum, <span className="text-emerald-400">{user?.name || studentName}</span>!</h2>
                  <p className="mt-2 text-slate-400 text-lg">What would you like to focus on today?</p>
                </div>
              </div>

              {!user && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-2xl p-4 flex items-start gap-4">
                  <div className="bg-amber-500/20 p-2 rounded-lg text-amber-400">
                    <LogOut size={20} className="rotate-180" />
                  </div>
                  <div>
                    <h4 className="text-amber-400 font-bold">Browsing as Guest</h4>
                    <p className="text-amber-400/80 text-sm mt-1 leading-relaxed">Your progress will not be permanently saved. Sign in with Google to unlock Practice Exams and keep track of your learning streaks.</p>
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <DashboardCard icon={<GraduationCap size={28} className="text-emerald-400" />} color="emerald" title="Practice Exam" desc="Test your knowledge with random questions." action={startExam} locked={!user} />
                <DashboardCard icon={<BookOpen size={28} className="text-blue-400" />} color="blue" title="Memorize Topics" desc="Interactive character-by-character typing practice." action={() => setView('memorize')} />
                {guide && (
                  <DashboardCard icon={<ClipboardList size={28} className="text-violet-400" />} color="violet" title={guide.title || "Paper 2 Guide"} desc="Paper 2 format, what's assessed, and a step-by-step preparation plan." action={() => setView('project_guide')} />
                )}
                {prepSessions.map((sess: any, i: number) => (
                  <DashboardCard
                    key={sess.id ?? i}
                    icon={<Rocket size={28} className="text-indigo-400" />}
                    color="indigo"
                    title={sess.title}
                    desc={sess.subtitle}
                    action={() => { setActiveSession(sess); setView('prep_session'); }}
                  />
                ))}
              </div>
            </motion.div>
          )}

          {view === 'exam' && questions.length > 0 && (
            <motion.div key="exam" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              <div className="lg:col-span-8 flex flex-col gap-6">
                {/* Exam Timer */}
                <div className="flex items-center justify-center gap-3 bg-slate-900 border border-slate-800 rounded-2xl px-6 py-3">
                  <Clock size={20} className="text-emerald-400" />
                  <span className="text-2xl font-mono font-bold text-white">{fmtTimer(examElapsed)}</span>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                  {(() => {
                    const q = questions[currentQIdx];
                    const isMcq = q.options && Object.keys(q.options).length > 0;
                    return (
                      <>
                        <div className="flex flex-wrap items-center justify-center gap-2 mb-4">
                          {q.section && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-400 text-xs font-bold uppercase tracking-wide">Section {q.section}{q.section_title ? `: ${q.section_title}` : ''}</span>}
                          {q.topic_title && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-400 text-xs font-bold uppercase tracking-wide">{q.topic_title}</span>}
                          {q.marks && <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-400 text-xs font-bold uppercase tracking-wide">{q.marks} {q.marks === 1 ? 'mark' : 'marks'}</span>}
                        </div>
                        <h2 className="text-2xl font-bold text-center mb-10">{q.question}</h2>
                        {isMcq ? (
                          <div className="grid gap-4">
                            {Object.entries(q.options).map(([key, text]: [any, any]) => (
                              <button key={key} onClick={() => setAnswers({...answers, [currentQIdx]: key})} className={`w-full text-left p-4 rounded-xl border-2 flex items-center justify-between transition-all ${answers[currentQIdx] === key ? 'border-emerald-500 bg-emerald-900/30' : 'border-slate-800 bg-slate-900 border-b-4 border-slate-700 hover:bg-slate-800'}`}>
                                <span className="font-medium">{key}. {text}</span>
                                {answers[currentQIdx] === key && <CheckCircle2 className="text-emerald-400" />}
                              </button>
                            ))}
                          </div>
                        ) : (
                          <div className="grid gap-4">
                            <textarea
                              value={answers[currentQIdx] || ""}
                              onChange={(e) => setAnswers({...answers, [currentQIdx]: e.target.value})}
                              placeholder="Type your answer here..."
                              className="w-full min-h-[160px] p-4 bg-slate-900/50 border border-slate-800 rounded-xl outline-none focus:border-emerald-500 focus:bg-slate-900 transition-all resize-y"
                            />
                            <button onClick={() => setRevealed({...revealed, [currentQIdx]: !revealed[currentQIdx]})} className="self-start text-sm font-bold text-emerald-400 hover:text-emerald-400 flex items-center gap-1">
                              {revealed[currentQIdx] ? 'Hide model answer' : 'Show model answer'}
                            </button>
                            {revealed[currentQIdx] && q.model_answer && (
                              <div className="p-4 bg-emerald-950/20 border border-emerald-500/20 border-2 border-emerald-100 rounded-xl">
                                <p className="text-xs font-bold uppercase tracking-wide text-emerald-400 mb-2">Model Answer</p>
                                <p className="text-slate-300 whitespace-pre-line leading-relaxed">{q.model_answer}</p>
                              </div>
                            )}
                          </div>
                        )}
                      </>
                    );
                  })()}
                </div>
                <div className="flex justify-between">
                  <button disabled={currentQIdx === 0} onClick={() => setCurrentQuestion(currentQIdx - 1)} className="px-8 py-3 rounded-xl border border-slate-800 bg-slate-900 text-slate-300 hover:bg-slate-800 hover:text-white font-bold transition-all disabled:opacity-50">Previous</button>
                  {currentQIdx === questions.length - 1 ? <button onClick={submitExam} className="px-12 py-3 rounded-xl bg-emerald-600 text-white font-bold border-b-4 border-emerald-800">Submit</button> : <button onClick={() => setCurrentQuestion(currentQIdx + 1)} className="px-12 py-3 rounded-xl bg-emerald-600 text-white font-bold border-b-4 border-emerald-800">Next</button>}
                </div>
              </div>
              <aside className="lg:col-span-4 bg-slate-900 border border-slate-800 rounded-3xl p-6 h-fit sticky top-24">
                <div className="grid grid-cols-5 gap-2">{questions.map((_, i) => <button key={i} onClick={() => setCurrentQuestion(i)} className={`aspect-square rounded-lg flex items-center justify-center font-bold text-sm ${answers[i] ? 'bg-emerald-600 text-white' : i === currentQIdx ? 'border border-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)] bg-emerald-500/10 text-emerald-400' : 'bg-slate-900 border border-slate-800 text-slate-400 hover:bg-slate-800 hover:text-slate-200'}`}>{i + 1}</button>)}</div>
              </aside>
            </motion.div>
          )}

          {view === 'memorize' && (
             <motion.div key="mem" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
               {!isMemStarted ? (
                 <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm max-w-2xl mx-auto">
                   <h2 className="text-2xl font-bold mb-4">Select Topics to Memorize</h2>
                   <div className="relative mb-6">
                     <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                     <input 
                       type="text" 
                       placeholder="Search topics..." 
                       value={searchQuery}
                       onChange={(e) => setSearchQuery(e.target.value)}
                       className="w-full pl-12 pr-4 py-3 bg-slate-900/50 border border-slate-800 rounded-xl outline-none focus:border-emerald-500 focus:bg-slate-900 transition-all"
                     />
                   </div>
                   <div className="grid gap-4 mb-8 max-h-[50vh] overflow-y-auto pr-2">
                     {Array.from(new Set(memData.map(c => c.tier_label || "Other Topics"))).map(tierLabel => {
                       const groupsInTier = Array.from(new Set(memData.filter(c => (c.tier_label || "Other Topics") === tierLabel).map(c => c.group_id)))
                         .map((groupId: string) => ({
                           id: groupId,
                           label: memData.find(c => c.group_id === groupId)?.group_label || ""
                         }))
                         .filter(group => group.label.toLowerCase().includes(searchQuery.toLowerCase()));
                       
                       if (groupsInTier.length === 0) return null;

                       return (
                         <div key={tierLabel} className="mb-2">
                           <h3 className="text-lg font-bold text-emerald-400 mb-3 border-b-2 border-emerald-100 pb-2">{tierLabel}</h3>
                           <div className="grid gap-3">
                             {groupsInTier.map(group => (
                               <label key={group.id} className="flex items-center gap-3 p-4 bg-slate-900/50 border border-slate-800/80 rounded-xl cursor-pointer hover:bg-emerald-950/20 hover:border-emerald-500/40 transition-all">
                                 <input type="checkbox" checked={selectedGroups.includes(group.id)} onChange={() => toggleGroup(group.id)} className="w-5 h-5 accent-emerald-600" />
                                 <span className="font-medium">{group.label}</span>
                               </label>
                             ))}
                           </div>
                         </div>
                       );
                     })}
                     {memData.length === 0 && <p className="text-slate-400 italic">No topics available for {activeSubject}.</p>}
                     {memData.length > 0 && Array.from(new Set(memData.map(c => c.group_id))).filter(groupId => (memData.find(c => c.group_id === groupId)?.group_label || "").toLowerCase().includes(searchQuery.toLowerCase())).length === 0 && (
                       <p className="text-slate-400 italic text-center py-4">No topics match your search.</p>
                     )}
                   </div>
                   <button onClick={startMemorize} className="w-full py-4 bg-emerald-600 text-white font-bold rounded-xl border-b-4 border-emerald-800">Start Session</button>
                 </div>
               ) : (
                 <div className="flex flex-col gap-6 w-full max-w-4xl mx-auto">
                    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                      <h3 className="text-emerald-400 font-bold mb-4 text-center">{currentMemCard.title}</h3>
                      {currentMemCard.arabic && (
                        <div className="text-3xl font-serif text-right mb-8 bg-emerald-950/20 border border-emerald-500/20 p-6 rounded-2xl border-r-4 border-emerald-600 leading-loose" dir="rtl">
                          {currentMemCard.arabic}
                        </div>
                      )}
                      <div className="flex flex-col gap-3 mb-8 max-h-[50vh] overflow-y-auto pr-2 scroll-smooth">
                        {currentMemCard.lines.map((line: string, i: number) => {
                          const typed = typedLines[i] || "";
                          const isActive = i === activeLineIdx && !allLinesDone;
                          return (
                            <div key={i} id={`mem-line-${i}`} className={`p-3 rounded-xl transition-all ${isActive ? 'bg-emerald-950/20 border border-emerald-500/20 border-l-4 border-emerald-600 shadow-inner' : ''}`}>
                              <div className="text-lg flex flex-wrap gap-[0px]">
                                {line.split("").map((char, charIdx) => {
                                  let color = "text-slate-400"; // Darkened from slate-300
                                  if (charIdx < typed.length) {
                                    color = typed[charIdx] === char ? "text-emerald-400 font-bold" : "text-red-500 bg-red-100 rounded-[2px]";
                                  } else if (isActive && charIdx === typed.length) {
                                    color = "text-emerald-400 border-l-2 border-emerald-600 animate-pulse font-black";
                                  }
                                  return <span key={charIdx} className={color}>{char === " " ? "\u00A0" : char}</span>;
                                })}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                      {!allLinesDone ? (
                        <input 
                          autoFocus
                          value={typedLines[activeLineIdx] || ""}
                          className="w-full p-4 text-lg border-2 border-emerald-500 rounded-xl outline-none bg-slate-900 text-white font-mono shadow-[0_0_15px_rgba(16,185,129,0.1)] focus:ring-2 ring-emerald-500/20"
                          placeholder="Type the highlighted line exactly as shown..."
                          onChange={(e) => handleType(e.target.value)}
                        />
                      ) : (
                        <button onClick={nextCard} className="w-full py-4 bg-emerald-600 text-white font-bold rounded-xl border-b-4 border-emerald-800 flex items-center justify-center gap-2">
                          {currentMemIdx < memQueue.length - 1 ? "Next Card" : "Finish Session"}
                          <ChevronRight size={20} />
                        </button>
                      )}
                    </div>
                  </div>
               )}
             </motion.div>
          )}

          {view === 'project_guide' && guide && (
            <motion.div key="guide" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-4xl mx-auto flex flex-col gap-6">
              {/* Header */}
              <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                <span className="inline-block px-4 py-1.5 rounded-full bg-violet-100 text-violet-800 font-bold uppercase tracking-wider text-xs mb-4">Practical Coursework</span>
                <h2 className="text-3xl font-bold text-white">{guide.title}</h2>
                {guide.subtitle && <p className="mt-2 text-slate-400 font-medium">{guide.subtitle}</p>}
                {guide.intro && <p className="mt-4 text-slate-400 leading-relaxed">{guide.intro}</p>}
              </div>

              {/* Overview facts */}
              {guide.overview && guide.overview.length > 0 && (
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">At a Glance</h3>
                  <div className="grid gap-3">
                    {guide.overview.map((row: any, i: number) => (
                      <div key={i} className="grid grid-cols-1 sm:grid-cols-3 gap-1 sm:gap-4 py-2 border-b border-slate-100 last:border-0">
                        <span className="font-bold text-slate-300">{row.label}</span>
                        <span className="sm:col-span-2 text-slate-400">{row.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Components + mark scheme */}
              {guide.components && guide.components.map((comp: any, i: number) => (
                <div key={i} className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <h3 className="text-xl font-bold text-white">{comp.name}</h3>
                    {comp.marks != null && <span className="shrink-0 px-3 py-1 rounded-full bg-violet-100 text-violet-700 text-sm font-bold">{comp.marks} marks</span>}
                  </div>
                  {comp.summary && <p className="text-slate-400 mb-4">{comp.summary}</p>}
                  {comp.criteria && (
                    <div className="grid gap-2">
                      {comp.criteria.map((c: any, j: number) => (
                        <div key={j} className="flex items-center justify-between gap-4 p-3 bg-slate-900/40 border border-slate-800 rounded-xl">
                          <span className="text-slate-300">{c.criterion}</span>
                          {c.marks != null && <span className="shrink-0 font-bold text-slate-400 text-sm">{c.marks}</span>}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {/* Approved tools */}
              {guide.tools && guide.tools.length > 0 && (
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">Approved Tools</h3>
                  <ul className="grid gap-2">
                    {guide.tools.map((t: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-400"><Cpu size={18} className="text-violet-500 mt-0.5 shrink-0" />{t}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Step-by-step plan */}
              {guide.steps && guide.steps.length > 0 && (
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">How to Prepare</h3>
                  <div className="grid gap-4">
                    {guide.steps.map((step: any, i: number) => (
                      <div key={i} className="p-4 bg-slate-900/40 border border-slate-800 rounded-xl border-l-4 border-violet-400">
                        <h4 className="font-bold text-white mb-1">{step.title}</h4>
                        <p className="text-slate-400 leading-relaxed">{step.detail}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Submission checklist */}
              {guide.submission && guide.submission.length > 0 && (
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">What to Submit</h3>
                  <ul className="grid gap-2">
                    {guide.submission.map((item: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-400"><CheckCircle2 size={18} className="text-emerald-500 mt-0.5 shrink-0" />{item}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Tips */}
              {guide.tips && guide.tips.length > 0 && (
                <div className="bg-violet-50 border-2 border-violet-100 rounded-3xl p-8">
                  <h3 className="text-lg font-bold text-violet-800 mb-4">Examiner Tips</h3>
                  <ul className="grid gap-2">
                    {guide.tips.map((tip: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-300"><Star size={18} className="text-violet-500 mt-0.5 shrink-0" />{tip}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button onClick={() => setView('dashboard')} className="self-start px-8 py-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 hover:text-white font-bold text-slate-300 flex items-center gap-2 transition-all">
                <ArrowLeft size={18} /> Back to Dashboard
              </button>
            </motion.div>
          )}

          {view === 'prep_session' && activeSession && (
            <motion.div key="prep" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-4xl mx-auto flex flex-col gap-6">
              {/* Header */}
              <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
                <span className="inline-block px-4 py-1.5 rounded-full bg-indigo-950/40 border border-indigo-500/20 text-indigo-400 font-bold uppercase tracking-wider text-xs mb-4">Paper 2 - Hands-on Walkthrough</span>
                <h2 className="text-3xl font-bold text-white">{activeSession.title}</h2>
                {activeSession.subtitle && <p className="mt-2 text-slate-400 font-medium">{activeSession.subtitle}</p>}
                <div className="flex flex-wrap gap-2 mt-4">
                  {activeSession.project_name && <span className="px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 text-sm font-bold">{activeSession.project_name}</span>}
                  {activeSession.difficulty && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-400 text-sm font-semibold">{activeSession.difficulty}</span>}
                  {activeSession.duration && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-400 text-sm font-semibold">{activeSession.duration}</span>}
                </div>
                {activeSession.intro && <p className="mt-4 text-slate-400 leading-relaxed">{activeSession.intro}</p>}
              </div>

              {/* Overview facts */}
              {activeSession.overview && activeSession.overview.length > 0 && (
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-indigo-400 mb-4 border-b-2 border-indigo-100 pb-2">At a Glance</h3>
                  <div className="grid gap-3">
                    {activeSession.overview.map((row: any, i: number) => (
                      <div key={i} className="grid grid-cols-1 sm:grid-cols-3 gap-1 sm:gap-4 py-2 border-b border-slate-100 last:border-0">
                        <span className="font-bold text-slate-300">{row.label}</span>
                        <span className="sm:col-span-2 text-slate-400">{row.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* What you need */}
              {activeSession.materials && activeSession.materials.length > 0 && (
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-indigo-400 mb-4 border-b-2 border-indigo-100 pb-2">Before You Start - What You Need</h3>
                  <ul className="grid gap-2">
                    {activeSession.materials.map((m: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-400"><CheckCircle2 size={18} className="text-indigo-500 mt-0.5 shrink-0" />{m}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Step-by-step walkthrough */}
              {activeSession.steps && activeSession.steps.map((step: any, i: number) => (
                <div key={i} className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <div className="flex items-start gap-4 mb-4">
                    <div className="shrink-0 w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold">{i + 1}</div>
                    <div>
                      <h3 className="text-xl font-bold text-white">{step.title}</h3>
                      {step.detail && <p className="mt-1 text-slate-400 leading-relaxed">{step.detail}</p>}
                    </div>
                  </div>
                  {step.illustration && (
                    <div
                      className="mb-4 rounded-2xl overflow-hidden border border-slate-800 bg-slate-50 [&_svg]:block [&_svg]:w-full [&_svg]:h-auto"
                      dangerouslySetInnerHTML={{ __html: step.illustration }}
                    />
                  )}
                  {step.substeps && step.substeps.length > 0 && (
                    <ol className="grid gap-2.5 mb-4">
                      {step.substeps.map((ss: string, j: number) => (
                        <li key={j} className="flex items-start gap-3 text-slate-300">
                          <span className="shrink-0 mt-0.5 w-6 h-6 rounded-full bg-indigo-950/40 border border-indigo-500/20 text-indigo-700 text-xs font-bold flex items-center justify-center">{j + 1}</span>
                          <span className="leading-relaxed">{ss}</span>
                        </li>
                      ))}
                    </ol>
                  )}
                  {step.tip && (
                    <div className="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-xl">
                      <Lightbulb size={18} className="text-amber-500 mt-0.5 shrink-0" />
                      <p className="text-slate-300 text-sm leading-relaxed"><span className="font-bold text-amber-700">Tip: </span>{step.tip}</p>
                    </div>
                  )}
                </div>
              ))}

              {/* Evidence checklist */}
              {activeSession.evidence && activeSession.evidence.length > 0 && (
                <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-indigo-400 mb-4 border-b-2 border-indigo-100 pb-2">Evidence to Collect for Paper 2</h3>
                  <ul className="grid gap-2">
                    {activeSession.evidence.map((e: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-400"><CheckCircle2 size={18} className="text-emerald-500 mt-0.5 shrink-0" />{e}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Ethics note */}
              {activeSession.ethics_note && (
                <div className="bg-rose-50 border-2 border-rose-100 rounded-3xl p-6 sm:p-8">
                  <h3 className="text-lg font-bold text-rose-800 mb-2">Don't Forget: Ethics</h3>
                  <p className="text-slate-300 leading-relaxed">{activeSession.ethics_note}</p>
                </div>
              )}

              {/* Next up */}
              {activeSession.next_up && (
                <div className="bg-indigo-50 border-2 border-indigo-100 rounded-3xl p-6 sm:p-8">
                  <h3 className="text-lg font-bold text-indigo-400 mb-2 flex items-center gap-2"><Rocket size={18} /> What's Next</h3>
                  <p className="text-slate-300 leading-relaxed">{activeSession.next_up}</p>
                </div>
              )}

              <button onClick={() => setView('dashboard')} className="self-start px-8 py-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 hover:text-white font-bold text-slate-300 flex items-center gap-2 transition-all">
                <ArrowLeft size={18} /> Back to Dashboard
              </button>
            </motion.div>
          )}

          {view === 'session_result' && sessionResult && (
            <motion.div key="session_result" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="w-full max-w-2xl mx-auto flex flex-col gap-6 items-center text-center">
              
              {/* Snapshot wrapper */}
              <div id="session-result-card" className="w-full flex flex-col gap-6 items-center p-8 bg-slate-950 rounded-[2rem] border border-slate-800 shadow-2xl relative overflow-hidden">
                
                {/* Background ambient glow */}
                <div className="absolute top-0 inset-x-0 h-32 bg-gradient-to-b from-emerald-500/10 to-transparent pointer-events-none" />

                {/* User info */}
                {user && (
                  <div className="flex items-center gap-3 bg-slate-900 border border-slate-800 px-5 py-2 rounded-full shadow-sm z-10">
                    <img src={user.picture} alt={user.name} className="w-7 h-7 rounded-full border border-emerald-500/50 object-cover" referrerPolicy="no-referrer" />
                    <span className="text-sm font-bold text-slate-300">{user.name}</span>
                  </div>
                )}

                {/* Trophy / Celebration */}
                <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 200, damping: 15 }} className="w-24 h-24 rounded-full bg-emerald-500/10 border-2 border-emerald-500/30 flex items-center justify-center shadow-[0_0_40px_rgba(16,185,129,0.2)] z-10">
                  <Trophy size={48} className="text-emerald-400" />
                </motion.div>

                <h2 className="text-3xl font-black text-white z-10">
                  {sessionResult.type === 'memorize' ? 'Memorize Session Complete!' : 'Exam Submitted!'}
                </h2>
                <p className="text-slate-400 text-lg -mt-4 z-10">Great work! Here are your results:</p>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-4 w-full mt-2 z-10">
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-center">
                    <Target size={24} className="mx-auto text-blue-400 mb-2" />
                    <p className="text-2xl font-black text-white">{sessionResult.accuracy}%</p>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">Accuracy</p>
                  </div>
                  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-center">
                    <Clock size={24} className="mx-auto text-amber-400 mb-2" />
                    <p className="text-2xl font-black text-white">{fmtTimer(sessionResult.timeSec)}</p>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">Time Taken</p>
                  </div>
                  {sessionResult.type === 'exam' && (
                    <div className="col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 text-center">
                      <GraduationCap size={24} className="mx-auto text-emerald-400 mb-2" />
                      <p className="text-2xl font-black text-white">{sessionResult.score} / {sessionResult.totalMarks}</p>
                      <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">Score</p>
                    </div>
                  )}
                  {sessionResult.type === 'memorize' && (
                    <div className="col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-5 text-center">
                      <BookOpen size={24} className="mx-auto text-emerald-400 mb-2" />
                      <p className="text-2xl font-black text-white">{sessionResult.cardsCompleted} / {sessionResult.cardsTotal}</p>
                      <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">Cards Completed</p>
                    </div>
                  )}
                </div>

                {/* Card Breakdown for Memorize */}
                {sessionResult.type === 'memorize' && sessionResult.cardDetails && sessionResult.cardDetails.length > 0 && (
                  <div className="w-full bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left z-10">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-wide mb-3">Card Breakdown</h3>
                    <div className="grid gap-2">
                      {sessionResult.cardDetails.map((c, i) => (
                        <div key={i} className="flex items-center justify-between p-3 bg-slate-950 rounded-xl border border-slate-800/50">
                          <span className="text-sm font-medium text-slate-300 truncate flex-1 mr-3">{c.title}</span>
                          <div className="flex items-center gap-3 text-xs font-bold shrink-0">
                            <span className={c.accuracy_pct >= 90 ? 'text-emerald-400' : c.accuracy_pct >= 70 ? 'text-amber-400' : 'text-red-400'}>{c.accuracy_pct}%</span>
                            <span className="text-slate-500">{c.typo_count} typos</span>
                            <span className="text-slate-500">{c.time_seconds}s</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3 w-full mt-2">
                <button
                  onClick={shareOnWhatsApp}
                  className="flex-1 flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-bold text-white transition-all shadow-lg"
                  style={{ backgroundColor: '#25D366' }}
                >
                  <svg viewBox="0 0 24 24" className="w-5 h-5 fill-white"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.5-5.729-1.45L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.825 1.451 5.436 0 9.86-4.37 9.864-9.799.002-2.63-1.023-5.101-2.885-6.966a9.9 9.9 0 00-6.98-2.879c-5.443 0-9.866 4.372-9.87 9.802 0 1.714.453 3.39 1.31 4.887l-.994 3.63 3.73-.976zm10.743-6.195c-.297-.15-1.758-.867-2.03-.966-.273-.1-.472-.15-.672.15-.2.3-.775.966-.95 1.165-.175.2-.35.225-.647.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.2.05-.373-.025-.523-.075-.15-.672-1.62-.922-2.215-.242-.584-.487-.504-.672-.513l-.573-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414-.074-.124-.272-.198-.57-.347z"/></svg>
                  Share on WhatsApp
                </button>
                <button
                  onClick={() => { setSessionResult(null); setView('dashboard'); }}
                  className="flex-1 px-6 py-3.5 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 font-bold text-slate-300 flex items-center justify-center gap-2 transition-all"
                >
                  <ArrowLeft size={18} /> Back to Dashboard
                </button>
              </div>
            </motion.div>
          )}

          {view === 'progress' && user && activeSubject && (
            <motion.div key="progress" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-5xl mx-auto flex flex-col gap-6">
              <h2 className="text-3xl font-bold text-white">Your Progress</h2>

              {/* Summary Stats */}
              {progressData?.stats && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 text-center">
                    <StreakFlame streak={progressData.stats.current_streak} />
                    <p className="text-3xl font-black text-white">{progressData.stats.current_streak}</p>
                    <p className="text-sm font-bold text-slate-400 uppercase tracking-wide">Day Streak</p>
                  </div>
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 text-center">
                    <BookOpen size={28} className="mx-auto text-emerald-500 mb-2" />
                    <p className="text-3xl font-black text-white">{progressData.stats.total_sessions}</p>
                    <p className="text-sm font-bold text-slate-400 uppercase tracking-wide">Sessions</p>
                  </div>
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 text-center">
                    <Target size={28} className="mx-auto text-blue-500 mb-2" />
                    <p className="text-3xl font-black text-white">{progressData.stats.avg_accuracy}%</p>
                    <p className="text-sm font-bold text-slate-400 uppercase tracking-wide">Accuracy</p>
                  </div>
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 text-center">
                    <Clock size={28} className="mx-auto text-violet-500 mb-2" />
                    <p className="text-3xl font-black text-white">{fmtTime(progressData.stats.total_time_seconds)}</p>
                    <p className="text-sm font-bold text-slate-400 uppercase tracking-wide">Total Time</p>
                  </div>
                </div>
              )}

              {/* Calendar Heatmap */}
              {progressData && (() => {
                const today = new Date();
                const days: {date: string, count: number}[] = [];
                for (let i = 182; i >= 0; i--) {
                  const d = new Date(today);
                  d.setDate(d.getDate() - i);
                  const ds = d.toISOString().slice(0, 10);
                  let count = 0;
                  (progressData.memorize_log || []).forEach((e: any) => { if (e.date?.slice(0, 10) === ds) count++; });
                  (progressData.exam_log || []).forEach((e: any) => { if (e.date?.slice(0, 10) === ds) count++; });
                  days.push({ date: ds, count });
                }
                // Pad start so first column starts on Sunday
                const firstDow = new Date(days[0].date).getDay();
                const padded = Array.from({ length: firstDow }, () => null as null | typeof days[0]);
                const allCells = [...padded, ...days];
                const weeks: (null | typeof days[0])[][] = [];
                for (let i = 0; i < allCells.length; i += 7) {
                  weeks.push(allCells.slice(i, i + 7));
                }
                // Transpose: 7 rows x N columns
                const maxWeeks = weeks.length;
                const rows = Array.from({ length: 7 }, (_, row) =>
                  weeks.map(week => week[row] ?? null)
                );
                const colorFor = (count: number) => {
                  if (count === 0) return 'bg-slate-900 border border-slate-800/50';
                  if (count === 1) return 'bg-emerald-200';
                  if (count <= 3) return 'bg-emerald-400';
                  return 'bg-emerald-600';
                };
                return (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-sm">
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><Calendar size={20} /> Activity Calendar</h3>
                    <div className="overflow-x-auto">
                      <div className="inline-grid gap-[3px]" style={{ gridTemplateColumns: `repeat(${maxWeeks}, 1fr)`, gridTemplateRows: 'repeat(7, 1fr)' }}>
                        {rows.flat().map((cell, idx) => (
                          <button
                            key={idx}
                            onClick={() => cell && setSelectedDay(selectedDay === cell.date ? null : cell.date)}
                            title={cell ? `${cell.date}: ${cell.count} session(s)` : ''}
                            className={`w-3.5 h-3.5 rounded-sm transition-all ${cell ? `${colorFor(cell.count)} hover:ring-2 hover:ring-emerald-400 ${selectedDay === cell.date ? 'ring-2 ring-emerald-600' : ''}` : 'bg-transparent'}`}
                          />
                        ))}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 mt-3 text-xs text-slate-400">
                      <span>Less</span>
                      <span className="w-3 h-3 rounded-sm bg-slate-900 border border-slate-800/50" />
                      <span className="w-3 h-3 rounded-sm bg-emerald-200" />
                      <span className="w-3 h-3 rounded-sm bg-emerald-400" />
                      <span className="w-3 h-3 rounded-sm bg-emerald-600" />
                      <span>More</span>
                    </div>
                  </div>
                );
              })()}

              {/* Day Detail Panel */}
              {selectedDay && progressData && (() => {
                const memSessions = (progressData.memorize_log || []).filter((e: any) => e.date?.slice(0, 10) === selectedDay);
                const examSessions = (progressData.exam_log || []).filter((e: any) => e.date?.slice(0, 10) === selectedDay);
                if (memSessions.length === 0 && examSessions.length === 0) return (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-sm">
                    <p className="text-slate-400 italic">No activity on {selectedDay}</p>
                  </div>
                );
                const fmtDate = (iso: string) => {
                  try {
                    const d = new Date(iso);
                    return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
                      + ' at ' + d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
                  } catch { return iso; }
                };
                return (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-sm">
                    <h3 className="text-lg font-bold text-white mb-4">{new Date(selectedDay + 'T00:00:00').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}</h3>
                    <div className="grid gap-5">
                      {memSessions.map((s: any, i: number) => {
                        const isComplete = s.cards_completed >= s.cards_total;
                        return (
                          <div key={`m${i}`} className="bg-slate-900/50 rounded-2xl border-l-4 border-emerald-600 overflow-hidden">
                            {/* Session header */}
                            <div className="p-4 flex items-center gap-3">
                              <BookOpen size={22} className="text-emerald-400 shrink-0" />
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <p className="font-bold text-white">Memorize Session</p>
                                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${isComplete ? 'bg-emerald-100 text-emerald-400' : 'bg-amber-100 text-amber-700'}`}>
                                    {isComplete ? '✓ Completed' : '✗ Incomplete'}
                                  </span>
                                </div>
                                <p className="text-sm text-slate-400">{fmtDate(s.date)}</p>
                                <div className="flex items-center gap-4 mt-1 text-sm text-slate-400">
                                  <span className="flex items-center gap-1"><Clock size={14} /> {fmtTime(s.total_time_seconds || 0)}</span>
                                  <span>{s.cards_completed}/{s.cards_total} card(s)</span>
                                  {s.overall_accuracy_pct != null && <span className="font-bold text-emerald-400">{s.overall_accuracy_pct}% accuracy</span>}
                                </div>
                              </div>
                            </div>
                            {/* Per-card breakdown */}
                            {s.cards && s.cards.length > 0 && (
                              <div className="border-t border-slate-800 px-4 py-3">
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-2">Card Results</p>
                                <div className="grid gap-2">
                                  {s.cards.map((card: any, ci: number) => (
                                    <div key={ci} className="flex items-center gap-3 px-3 py-2 bg-slate-800 rounded-lg">
                                      <div className="flex-1 min-w-0">
                                        <p className="font-semibold text-sm text-slate-300 truncate">{card.title}</p>
                                        <p className="text-xs text-slate-400">{card.lines_completed}/{card.lines_total} lines</p>
                                      </div>
                                      <div className="flex items-center gap-3 text-xs shrink-0">
                                        <span className={`font-bold ${card.accuracy_pct >= 90 ? 'text-emerald-400' : card.accuracy_pct >= 70 ? 'text-amber-600' : 'text-red-500'}`}>
                                          {card.accuracy_pct}%
                                        </span>
                                        {card.typo_count > 0 && <span className="text-red-400">{card.typo_count} typo{card.typo_count !== 1 ? 's' : ''}</span>}
                                        <span className="text-slate-400">{fmtTime(card.time_seconds || 0)}</span>
                                      </div>
                                      {/* Accuracy bar */}
                                      <div className="w-16 h-1.5 bg-slate-800 rounded-full overflow-hidden shrink-0">
                                        <div className={`h-full rounded-full ${card.accuracy_pct >= 90 ? 'bg-emerald-950/20 border border-emerald-500/200' : card.accuracy_pct >= 70 ? 'bg-amber-400' : 'bg-red-400'}`} style={{ width: `${Math.min(card.accuracy_pct, 100)}%` }} />
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                      {examSessions.map((s: any, i: number) => (
                        <div key={`e${i}`} className="bg-slate-900/50 rounded-2xl border-l-4 border-blue-600 overflow-hidden">
                          {/* Session header */}
                          <div className="p-4 flex items-center gap-3">
                            <GraduationCap size={22} className="text-blue-400 shrink-0" />
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 flex-wrap">
                                <p className="font-bold text-white">Exam Attempt</p>
                                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${s.percentage >= 70 ? 'bg-emerald-100 text-emerald-400' : s.percentage >= 50 ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700'}`}>
                                  {s.score}/{s.total} ({s.percentage}%)
                                </span>
                              </div>
                              <p className="text-sm text-slate-400">{fmtDate(s.date)}</p>
                              <div className="flex items-center gap-4 mt-1 text-sm text-slate-400">
                                <span className="flex items-center gap-1"><Clock size={14} /> {fmtTime(s.time_taken || 0)}</span>
                              </div>
                            </div>
                          </div>
                          {/* Per-question breakdown */}
                          {s.question_results && s.question_results.length > 0 && (
                            <div className="border-t border-slate-800 px-4 py-3">
                              <p className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-2">Question Results</p>
                              <div className="grid gap-1.5">
                                {s.question_results.map((qr: any, qi: number) => (
                                  <div key={qi} className={`flex items-center gap-3 px-3 py-2 rounded-lg ${qr.correct ? 'bg-emerald-950/20 border border-emerald-500/20' : 'bg-red-950/20 border border-red-500/20'}`}>
                                    <span className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 text-xs font-bold ${qr.correct ? 'bg-emerald-950/20 border border-emerald-500/200 text-white' : 'bg-red-400 text-white'}`}>
                                      {qr.correct ? '✓' : '✗'}
                                    </span>
                                    <div className="flex-1 min-w-0">
                                      <p className="text-sm text-slate-300 truncate">{qr.question?.slice(0, 80)}{(qr.question?.length || 0) > 80 ? '...' : ''}</p>
                                      {qr.topic && <p className="text-xs text-slate-400">{qr.topic}</p>}
                                    </div>
                                    {!qr.correct && (
                                      <div className="text-xs text-right shrink-0">
                                        <p className="text-red-500">Your: {qr.student_answer || '—'}</p>
                                        <p className="text-emerald-400">Ans: {String(qr.correct_answer).slice(0, 30)}</p>
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })()}

              {/* Topic Mastery Tracker */}
              {progressData && memData.length > 0 && (() => {
                const groups = Array.from(new Set(memData.map(c => c.group_id)));
                const mastery = groups.map(gid => {
                  const card = memData.find(c => c.group_id === gid);
                  const label = card?.group_label || gid;
                  // Find all card attempts for any card in this group
                  const cardIds = memData.filter(c => c.group_id === gid).map(c => c.id);
                  let attempts = 0;
                  let accSum = 0;
                  let lastDate = '';
                  (progressData.memorize_log || []).forEach((session: any) => {
                    (session.cards || []).forEach((ca: any) => {
                      if (cardIds.includes(ca.card_id)) {
                        attempts++;
                        accSum += ca.accuracy_pct || 0;
                        if (session.date > lastDate) lastDate = session.date;
                      }
                    });
                  });
                  const avgAcc = attempts > 0 ? Math.round(accSum / attempts * 10) / 10 : 0;
                  const completions = cardIds.length > 0 ? Math.floor(attempts / cardIds.length) : 0;
                  return { gid, label, attempts, avgAcc, lastDate, completions };
                });
                mastery.sort((a, b) => b.attempts - a.attempts || a.lastDate.localeCompare(b.lastDate));
                return (
                  <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-sm">
                    <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2"><BarChart3 size={20} /> Topic Mastery</h3>
                    <div className="grid gap-3">
                      {mastery.map(t => (
                        <div key={t.gid} className="p-4 bg-slate-900/40 border border-slate-800 rounded-xl">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-bold text-slate-300">{t.label}</span>
                            <span className="text-xs text-slate-400">
                              {t.attempts > 0 ? `Completed ${t.completions}x • ${t.avgAcc}% acc` : 'Not practiced'}
                            </span>
                          </div>
                          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                            <div className={`h-full rounded-full transition-all ${t.avgAcc >= 90 ? 'bg-emerald-950/20 border border-emerald-500/200' : t.avgAcc >= 70 ? 'bg-amber-400' : t.avgAcc > 0 ? 'bg-red-400' : 'bg-slate-200'}`} style={{ width: `${Math.min(t.avgAcc, 100)}%` }} />
                          </div>
                          {t.lastDate && <p className="text-xs text-slate-400 mt-1">Last: {t.lastDate.slice(0, 10)}</p>}
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })()}

              <button onClick={() => setView('dashboard')} className="self-start px-8 py-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 hover:text-white font-bold text-slate-300 flex items-center gap-2 transition-all">
                <ArrowLeft size={18} /> Back to Dashboard
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {activeSubject && (
        <nav className="fixed bottom-0 left-0 right-0 h-20 bg-slate-900/90 backdrop-blur-md border-t border-slate-800 flex justify-around items-center z-50 px-2 pb-safe">
          <NavButton icon={<LayoutDashboard size={24} />} label="Dash" active={view === 'dashboard'} onClick={() => {setView('dashboard'); setIsMemStarted(false);}} />
          <NavButton icon={<BookOpen size={24} />} label="Memorize" active={view === 'memorize'} onClick={() => {
            if (view === 'memorize') {
              if (!isMemStarted && selectedGroups.length > 0) {
                startMemorize();
              } else {
                setIsMemStarted(false);
              }
            } else {
              setView('memorize');
            }
          }} />
          <NavButton icon={<Trophy size={24} />} label="Progress" active={view === 'progress'} onClick={() => { if (user) { setView('progress'); setIsMemStarted(false); } else { requireLogin(() => setView('progress')); }}} />
          <NavButton icon={<GraduationCap size={24} />} label="Exams" active={view === 'exam'} onClick={() => {setView('exam'); setIsMemStarted(false);}} />
        </nav>
      )}
      
      {/* Toast Notification */}
      <AnimatePresence>
        {toast && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.9 }}
            className={`fixed bottom-24 right-4 sm:right-8 sm:bottom-8 p-4 rounded-2xl shadow-2xl border flex items-center gap-3 z-[100] max-w-sm ${
              toast.type === 'error' ? 'bg-red-950/90 border-red-800/50 text-red-200' : 'bg-emerald-950/90 border-emerald-800/50 text-emerald-200'
            } backdrop-blur-md`}
          >
            {toast.type === 'error' ? <XCircle size={24} className="text-red-400 shrink-0" /> : <CheckCircle2 size={24} className="text-emerald-400 shrink-0" />}
            <span className="font-bold text-sm leading-snug">{toast.message}</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function DashboardCard({ icon, color, title, desc, action, locked }: any) {
  const styles: any = {
    emerald: { card: 'border-emerald-500/20 hover:border-emerald-400 hover:shadow-[0_0_30px_rgba(52,211,153,0.15)]', wrap: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400', btn: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/20' },
    blue: { card: 'border-blue-500/20 hover:border-blue-400 hover:shadow-[0_0_30px_rgba(96,165,250,0.15)]', wrap: 'bg-blue-500/10 border-blue-500/20 text-blue-400', btn: 'bg-blue-500/10 text-blue-400 border-blue-500/30 hover:bg-blue-500/20' },
    violet: { card: 'border-violet-500/20 hover:border-violet-400 hover:shadow-[0_0_30px_rgba(139,92,246,0.15)]', wrap: 'bg-violet-500/10 border-violet-500/20 text-violet-400', btn: 'bg-violet-500/10 text-violet-400 border-violet-500/30 hover:bg-violet-500/20' },
    indigo: { card: 'border-indigo-500/20 hover:border-indigo-400 hover:shadow-[0_0_30px_rgba(99,102,241,0.15)]', wrap: 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400', btn: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30 hover:bg-indigo-500/20' },
  };
  const s = styles[color] || styles.emerald;
  return (
    <div className={`bg-slate-900/50 p-8 rounded-3xl border border-slate-800/80 backdrop-blur-sm transition-all group relative overflow-hidden flex flex-col ${s.card}`}>
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-white/5 to-transparent rounded-full -translate-y-16 translate-x-16 group-hover:scale-110 transition-transform duration-500 pointer-events-none" />
      <div className={`w-14 h-14 rounded-2xl flex items-center justify-center border mb-6 ${s.wrap}`}>{icon}</div>
      <h3 className="text-2xl font-bold mb-2 text-white">{title}</h3>
      <p className="text-slate-400 mb-8 flex-1">{desc}</p>
      <button onClick={locked ? undefined : action} className={`w-full py-3.5 font-bold rounded-xl border flex items-center justify-center gap-2 transition-all ${locked ? 'bg-slate-800/50 text-slate-500 border-slate-700 cursor-not-allowed' : s.btn}`}>
        {locked ? "Sign in to unlock" : <><PlayCircle size={18} /> Start</>}
      </button>
    </div>
  );
}

function NavButton({ icon, label, active = false, onClick }: any) {
  return (
    <button onClick={onClick} className={`flex flex-col items-center justify-center gap-1 transition-all ${active ? 'text-emerald-400 scale-110 drop-shadow-[0_0_8px_rgba(52,211,153,0.5)]' : 'text-slate-400 hover:text-slate-300'}`}>
      {icon} <span className="text-[10px] font-black uppercase">{label}</span>
    </button>
  );
}
