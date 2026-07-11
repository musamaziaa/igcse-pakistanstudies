import { useState, useEffect, useRef } from 'react';
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
  Lightbulb
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

const API_BASE = "http://127.0.0.1:8000";

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
  // Full class strings (kept static so Tailwind does not purge them)
  card: string;
  iconWrap: string;
  heading: string;
  tagClass: string;
}

const SUBJECTS: Subject[] = [
  {
    key: 'islamiyat', name: 'Islamiyat', tagline: 'IGCSE LRN Global Board',
    icon: <BookOpen size={48} className="text-emerald-600" />,
    card: 'bg-emerald-50 border-emerald-200 hover:border-emerald-500',
    iconWrap: 'bg-emerald-100', heading: 'text-emerald-800',
    tagClass: 'bg-emerald-100 text-emerald-800',
  },
  {
    key: 'pak_studies', name: 'Pak Studies', tagline: 'IGCSE LRN Global Board',
    icon: <Map size={48} className="text-blue-600" />,
    card: 'bg-blue-50 border-blue-200 hover:border-blue-500',
    iconWrap: 'bg-blue-100', heading: 'text-blue-800',
    tagClass: 'bg-blue-100 text-blue-800',
  },
  {
    key: 'hospitality', name: 'Hospitality', tagline: 'IGCSE LRN Global Board',
    icon: <UtensilsCrossed size={48} className="text-amber-600" />,
    card: 'bg-amber-50 border-amber-200 hover:border-amber-500',
    iconWrap: 'bg-amber-100', heading: 'text-amber-800',
    tagClass: 'bg-amber-100 text-amber-800',
  },
  {
    key: 'cs', name: 'Computer Science', tagline: 'IGCSE LRN Global Board',
    icon: <Cpu size={48} className="text-slate-600" />,
    card: 'bg-slate-50 border-slate-200 hover:border-slate-500',
    iconWrap: 'bg-slate-100', heading: 'text-slate-800',
    tagClass: 'bg-slate-100 text-slate-800',
  },
  {
    key: 'ai', name: 'Artificial Intelligence', tagline: 'IGCSE LRN Global Board',
    icon: <BrainCircuit size={48} className="text-violet-600" />,
    card: 'bg-violet-50 border-violet-200 hover:border-violet-500',
    iconWrap: 'bg-violet-100', heading: 'text-violet-800',
    tagClass: 'bg-violet-100 text-violet-800',
  },
  {
    key: 'ict', name: 'ICT', tagline: 'IGCSE LRN Global Board',
    icon: <MonitorSmartphone size={48} className="text-rose-600" />,
    card: 'bg-rose-50 border-rose-200 hover:border-rose-500',
    iconWrap: 'bg-rose-100', heading: 'text-rose-800',
    tagClass: 'bg-rose-100 text-rose-800',
  },
];

export default function App() {
  const [view, setView] = useState<'subject_selection' | 'dashboard' | 'exam' | 'memorize' | 'project_guide' | 'prep_session'>('subject_selection');
  const [activeSubject, setActiveSubject] = useState<string | null>(null);
  const [guide, setGuide] = useState<any>(null);
  const [prepSessions, setPrepSessions] = useState<any[]>([]);
  const [activeSession, setActiveSession] = useState<any>(null);
  const [studentName, setStudentName] = useState("Baba");
  const [searchQuery, setSearchQuery] = useState("");
  
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
      setView('exam');
    } catch (err: any) {
      alert(`⚠️ Error: ${err.message}`);
    }
  };

  const submitExam = async () => {
    if (!activeSubject) return;
    await fetch(`${API_BASE}/api/${activeSubject}/exam/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ student_name: studentName, questions, answers, time_taken: 300 })
    });
    alert("Exam Submitted!");
    setView('dashboard');
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
      }
    }
  };

  const nextCard = () => {
    if (currentMemIdx < memQueue.length - 1) {
      const nextIdx = currentMemIdx + 1;
      setCurrentMemIdx(nextIdx);
      resetCard(memQueue[nextIdx]);
      if (inputRef.current) inputRef.current.value = "";
    } else {
      finishMemorize();
    }
  };

  const finishMemorize = async () => {
    if (!activeSubject) return;
    await fetch(`${API_BASE}/api/students/${studentName}/${activeSubject}/memorize-attempt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        groups_selected: selectedGroups,
        cards_completed: memQueue.length,
        cards_total: memQueue.length
      })
    });
    alert("Great job! Memorization session completed.");
    setIsMemStarted(false);
    setView('dashboard');
  };

  const currentMemCard = memQueue[currentMemIdx];
  const allLinesDone = currentMemCard && activeLineIdx === currentMemCard.lines.length - 1 && typedLines[activeLineIdx].length >= currentMemCard.lines[activeLineIdx].length;

  return (
    <div className="min-h-screen pb-24 flex flex-col bg-slate-50">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b-2 border-slate-200 z-50 px-4 md:px-8 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-black text-emerald-600 tracking-tight italic">NUR ACADEMY</h1>
          {activeSubject && (
             <button onClick={() => { setActiveSubject(null); setView('subject_selection'); setIsMemStarted(false); setQuestions([]); }} className="text-sm font-bold text-slate-500 hover:text-emerald-600 flex items-center gap-1 bg-slate-100 px-3 py-1 rounded-full">
               <ArrowLeft size={16} /> Subjects
             </button>
          )}
        </div>
        <div className="w-9 h-9 rounded-full bg-emerald-100 border-2 border-emerald-600 flex items-center justify-center">
             <span className="font-bold text-emerald-700">{studentName[0]}</span>
        </div>
      </header>

      <main className="mt-24 flex-1 w-full max-w-7xl mx-auto px-4 md:px-8">
        <AnimatePresence mode="wait">
          {view === 'subject_selection' && (
            <motion.div key="subject_selection" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-8">
              <h2 className="text-3xl font-bold text-slate-800 text-center mb-8">Select Your Subject</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto w-full">
                {SUBJECTS.map((subject: Subject) => (
                  <div key={subject.key} onClick={() => { setActiveSubject(subject.key); setView('dashboard'); }} className={`cursor-pointer p-12 rounded-3xl border-2 shadow-sm transition-all flex flex-col items-center justify-center text-center group ${subject.card}`}>
                    <div className={`w-24 h-24 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform ${subject.iconWrap}`}>
                      {subject.icon}
                    </div>
                    <h3 className={`text-3xl font-bold ${subject.heading}`}>{subject.name}</h3>
                    <p className="mt-2 text-slate-500 font-medium">{subject.tagline}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {view === 'dashboard' && (
            <motion.div key="dash" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid gap-8">
              <div className="flex items-center gap-3 mb-2">
                <span className={`px-4 py-1.5 rounded-full font-bold uppercase tracking-wider text-sm ${SUBJECTS.find(s => s.key === activeSubject)?.tagClass ?? 'bg-emerald-100 text-emerald-800'}`}>
                  {SUBJECTS.find(s => s.key === activeSubject)?.name ?? activeSubject}
                </span>
              </div>
              <h2 className="text-3xl font-bold text-slate-800">Assalam-o-Alaikum, {studentName}!</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <DashboardCard icon={<GraduationCap size={32} />} color="emerald" title="Practice Exam" desc="Test your knowledge with random questions." action={startExam} />
                <DashboardCard icon={<BookOpen size={32} />} color="amber" title="Memorize Topics" desc="Interactive character-by-character typing practice." action={() => setView('memorize')} />
                {guide && (
                  <DashboardCard icon={<ClipboardList size={32} />} color="violet" title={guide.title || "Paper 2 Guide"} desc="Paper 2 format, what's assessed, and a step-by-step preparation plan." action={() => setView('project_guide')} />
                )}
                {prepSessions.map((sess: any, i: number) => (
                  <DashboardCard
                    key={sess.id ?? i}
                    icon={<Rocket size={32} />}
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
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                  {(() => {
                    const q = questions[currentQIdx];
                    const isMcq = q.options && Object.keys(q.options).length > 0;
                    return (
                      <>
                        <div className="flex flex-wrap items-center justify-center gap-2 mb-4">
                          {q.section && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600 text-xs font-bold uppercase tracking-wide">Section {q.section}{q.section_title ? `: ${q.section_title}` : ''}</span>}
                          {q.topic_title && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600 text-xs font-bold uppercase tracking-wide">{q.topic_title}</span>}
                          {q.marks && <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-xs font-bold uppercase tracking-wide">{q.marks} {q.marks === 1 ? 'mark' : 'marks'}</span>}
                        </div>
                        <h2 className="text-2xl font-bold text-center mb-10">{q.question}</h2>
                        {isMcq ? (
                          <div className="grid gap-4">
                            {Object.entries(q.options).map(([key, text]: [any, any]) => (
                              <button key={key} onClick={() => setAnswers({...answers, [currentQIdx]: key})} className={`w-full text-left p-4 rounded-xl border-2 flex items-center justify-between transition-all ${answers[currentQIdx] === key ? 'border-emerald-600 bg-emerald-50' : 'border-slate-200 bg-white border-b-4 border-slate-300'}`}>
                                <span className="font-medium">{key}. {text}</span>
                                {answers[currentQIdx] === key && <CheckCircle2 className="text-emerald-600" />}
                              </button>
                            ))}
                          </div>
                        ) : (
                          <div className="grid gap-4">
                            <textarea
                              value={answers[currentQIdx] || ""}
                              onChange={(e) => setAnswers({...answers, [currentQIdx]: e.target.value})}
                              placeholder="Type your answer here..."
                              className="w-full min-h-[160px] p-4 bg-slate-50 border-2 border-slate-200 rounded-xl outline-none focus:border-emerald-500 focus:bg-white transition-all resize-y"
                            />
                            <button onClick={() => setRevealed({...revealed, [currentQIdx]: !revealed[currentQIdx]})} className="self-start text-sm font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
                              {revealed[currentQIdx] ? 'Hide model answer' : 'Show model answer'}
                            </button>
                            {revealed[currentQIdx] && q.model_answer && (
                              <div className="p-4 bg-emerald-50 border-2 border-emerald-100 rounded-xl">
                                <p className="text-xs font-bold uppercase tracking-wide text-emerald-700 mb-2">Model Answer</p>
                                <p className="text-slate-700 whitespace-pre-line leading-relaxed">{q.model_answer}</p>
                              </div>
                            )}
                          </div>
                        )}
                      </>
                    );
                  })()}
                </div>
                <div className="flex justify-between">
                  <button disabled={currentQIdx === 0} onClick={() => setCurrentQuestion(currentQIdx - 1)} className="px-8 py-3 rounded-xl border-2 border-slate-200 bg-white font-bold disabled:opacity-50">Previous</button>
                  {currentQIdx === questions.length - 1 ? <button onClick={submitExam} className="px-12 py-3 rounded-xl bg-emerald-600 text-white font-bold border-b-4 border-emerald-800">Submit</button> : <button onClick={() => setCurrentQuestion(currentQIdx + 1)} className="px-12 py-3 rounded-xl bg-emerald-600 text-white font-bold border-b-4 border-emerald-800">Next</button>}
                </div>
              </div>
              <aside className="lg:col-span-4 bg-white border-2 border-slate-200 rounded-3xl p-6 h-fit sticky top-24">
                <div className="grid grid-cols-5 gap-2">{questions.map((_, i) => <button key={i} onClick={() => setCurrentQuestion(i)} className={`aspect-square rounded-lg flex items-center justify-center font-bold text-sm ${answers[i] ? 'bg-emerald-600 text-white' : i === currentQIdx ? 'border-2 border-emerald-600' : 'bg-slate-50 text-slate-300'}`}>{i + 1}</button>)}</div>
              </aside>
            </motion.div>
          )}

          {view === 'memorize' && (
             <motion.div key="mem" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
               {!isMemStarted ? (
                 <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm max-w-2xl mx-auto">
                   <h2 className="text-2xl font-bold mb-4">Select Topics to Memorize</h2>
                   <div className="relative mb-6">
                     <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                     <input 
                       type="text" 
                       placeholder="Search topics..." 
                       value={searchQuery}
                       onChange={(e) => setSearchQuery(e.target.value)}
                       className="w-full pl-12 pr-4 py-3 bg-slate-50 border-2 border-slate-200 rounded-xl outline-none focus:border-emerald-500 focus:bg-white transition-all"
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
                           <h3 className="text-lg font-bold text-emerald-800 mb-3 border-b-2 border-emerald-100 pb-2">{tierLabel}</h3>
                           <div className="grid gap-3">
                             {groupsInTier.map(group => (
                               <label key={group.id} className="flex items-center gap-3 p-4 bg-slate-50 rounded-xl cursor-pointer hover:bg-emerald-50 transition-colors">
                                 <input type="checkbox" checked={selectedGroups.includes(group.id)} onChange={() => toggleGroup(group.id)} className="w-5 h-5 accent-emerald-600" />
                                 <span className="font-medium">{group.label}</span>
                               </label>
                             ))}
                           </div>
                         </div>
                       );
                     })}
                     {memData.length === 0 && <p className="text-slate-500 italic">No topics available for {activeSubject}.</p>}
                     {memData.length > 0 && Array.from(new Set(memData.map(c => c.group_id))).filter(groupId => (memData.find(c => c.group_id === groupId)?.group_label || "").toLowerCase().includes(searchQuery.toLowerCase())).length === 0 && (
                       <p className="text-slate-500 italic text-center py-4">No topics match your search.</p>
                     )}
                   </div>
                   <button onClick={startMemorize} className="w-full py-4 bg-emerald-600 text-white font-bold rounded-xl border-b-4 border-emerald-800">Start Session</button>
                 </div>
               ) : (
                 <div className="flex flex-col gap-6 w-full max-w-4xl mx-auto">
                    <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                      <h3 className="text-emerald-700 font-bold mb-4 text-center">{currentMemCard.title}</h3>
                      {currentMemCard.arabic && (
                        <div className="text-3xl font-serif text-right mb-8 bg-emerald-50 p-6 rounded-2xl border-r-4 border-emerald-600 leading-loose" dir="rtl">
                          {currentMemCard.arabic}
                        </div>
                      )}
                      <div className="flex flex-col gap-3 mb-8 max-h-[50vh] overflow-y-auto pr-2 scroll-smooth">
                        {currentMemCard.lines.map((line: string, i: number) => {
                          const typed = typedLines[i] || "";
                          const isActive = i === activeLineIdx && !allLinesDone;
                          return (
                            <div key={i} id={`mem-line-${i}`} className={`p-3 rounded-xl transition-all ${isActive ? 'bg-emerald-50 border-l-4 border-emerald-600 shadow-inner' : ''}`}>
                              <div className="text-lg flex flex-wrap gap-[0px]">
                                {line.split("").map((char, charIdx) => {
                                  let color = "text-slate-400"; // Darkened from slate-300
                                  if (charIdx < typed.length) {
                                    color = typed[charIdx] === char ? "text-emerald-700 font-bold" : "text-red-500 bg-red-100 rounded-[2px]";
                                  } else if (isActive && charIdx === typed.length) {
                                    color = "text-emerald-800 border-l-2 border-emerald-600 animate-pulse font-black";
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
                          className="w-full p-4 text-lg border-2 border-emerald-600 rounded-xl outline-none focus:ring-4 ring-emerald-100 bg-white"
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
              <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                <span className="inline-block px-4 py-1.5 rounded-full bg-violet-100 text-violet-800 font-bold uppercase tracking-wider text-xs mb-4">Practical Coursework</span>
                <h2 className="text-3xl font-bold text-slate-800">{guide.title}</h2>
                {guide.subtitle && <p className="mt-2 text-slate-500 font-medium">{guide.subtitle}</p>}
                {guide.intro && <p className="mt-4 text-slate-600 leading-relaxed">{guide.intro}</p>}
              </div>

              {/* Overview facts */}
              {guide.overview && guide.overview.length > 0 && (
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">At a Glance</h3>
                  <div className="grid gap-3">
                    {guide.overview.map((row: any, i: number) => (
                      <div key={i} className="grid grid-cols-1 sm:grid-cols-3 gap-1 sm:gap-4 py-2 border-b border-slate-100 last:border-0">
                        <span className="font-bold text-slate-700">{row.label}</span>
                        <span className="sm:col-span-2 text-slate-600">{row.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Components + mark scheme */}
              {guide.components && guide.components.map((comp: any, i: number) => (
                <div key={i} className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <h3 className="text-xl font-bold text-slate-800">{comp.name}</h3>
                    {comp.marks != null && <span className="shrink-0 px-3 py-1 rounded-full bg-violet-100 text-violet-700 text-sm font-bold">{comp.marks} marks</span>}
                  </div>
                  {comp.summary && <p className="text-slate-500 mb-4">{comp.summary}</p>}
                  {comp.criteria && (
                    <div className="grid gap-2">
                      {comp.criteria.map((c: any, j: number) => (
                        <div key={j} className="flex items-center justify-between gap-4 p-3 bg-slate-50 rounded-xl">
                          <span className="text-slate-700">{c.criterion}</span>
                          {c.marks != null && <span className="shrink-0 font-bold text-slate-500 text-sm">{c.marks}</span>}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {/* Approved tools */}
              {guide.tools && guide.tools.length > 0 && (
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">Approved Tools</h3>
                  <ul className="grid gap-2">
                    {guide.tools.map((t: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-600"><Cpu size={18} className="text-violet-500 mt-0.5 shrink-0" />{t}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Step-by-step plan */}
              {guide.steps && guide.steps.length > 0 && (
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">How to Prepare</h3>
                  <div className="grid gap-4">
                    {guide.steps.map((step: any, i: number) => (
                      <div key={i} className="p-4 bg-slate-50 rounded-xl border-l-4 border-violet-400">
                        <h4 className="font-bold text-slate-800 mb-1">{step.title}</h4>
                        <p className="text-slate-600 leading-relaxed">{step.detail}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Submission checklist */}
              {guide.submission && guide.submission.length > 0 && (
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-violet-800 mb-4 border-b-2 border-violet-100 pb-2">What to Submit</h3>
                  <ul className="grid gap-2">
                    {guide.submission.map((item: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-600"><CheckCircle2 size={18} className="text-emerald-500 mt-0.5 shrink-0" />{item}</li>
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
                      <li key={i} className="flex items-start gap-3 text-slate-700"><Star size={18} className="text-violet-500 mt-0.5 shrink-0" />{tip}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button onClick={() => setView('dashboard')} className="self-start px-8 py-3 rounded-xl border-2 border-slate-200 bg-white font-bold text-slate-600 flex items-center gap-2">
                <ArrowLeft size={18} /> Back to Dashboard
              </button>
            </motion.div>
          )}

          {view === 'prep_session' && activeSession && (
            <motion.div key="prep" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-4xl mx-auto flex flex-col gap-6">
              {/* Header */}
              <div className="bg-white border-2 border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm">
                <span className="inline-block px-4 py-1.5 rounded-full bg-indigo-100 text-indigo-800 font-bold uppercase tracking-wider text-xs mb-4">Paper 2 - Hands-on Walkthrough</span>
                <h2 className="text-3xl font-bold text-slate-800">{activeSession.title}</h2>
                {activeSession.subtitle && <p className="mt-2 text-slate-500 font-medium">{activeSession.subtitle}</p>}
                <div className="flex flex-wrap gap-2 mt-4">
                  {activeSession.project_name && <span className="px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 text-sm font-bold">{activeSession.project_name}</span>}
                  {activeSession.difficulty && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600 text-sm font-semibold">{activeSession.difficulty}</span>}
                  {activeSession.duration && <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-600 text-sm font-semibold">{activeSession.duration}</span>}
                </div>
                {activeSession.intro && <p className="mt-4 text-slate-600 leading-relaxed">{activeSession.intro}</p>}
              </div>

              {/* Overview facts */}
              {activeSession.overview && activeSession.overview.length > 0 && (
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-indigo-800 mb-4 border-b-2 border-indigo-100 pb-2">At a Glance</h3>
                  <div className="grid gap-3">
                    {activeSession.overview.map((row: any, i: number) => (
                      <div key={i} className="grid grid-cols-1 sm:grid-cols-3 gap-1 sm:gap-4 py-2 border-b border-slate-100 last:border-0">
                        <span className="font-bold text-slate-700">{row.label}</span>
                        <span className="sm:col-span-2 text-slate-600">{row.value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* What you need */}
              {activeSession.materials && activeSession.materials.length > 0 && (
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-indigo-800 mb-4 border-b-2 border-indigo-100 pb-2">Before You Start - What You Need</h3>
                  <ul className="grid gap-2">
                    {activeSession.materials.map((m: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-600"><CheckCircle2 size={18} className="text-indigo-500 mt-0.5 shrink-0" />{m}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Step-by-step walkthrough */}
              {activeSession.steps && activeSession.steps.map((step: any, i: number) => (
                <div key={i} className="bg-white border-2 border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <div className="flex items-start gap-4 mb-4">
                    <div className="shrink-0 w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold">{i + 1}</div>
                    <div>
                      <h3 className="text-xl font-bold text-slate-800">{step.title}</h3>
                      {step.detail && <p className="mt-1 text-slate-600 leading-relaxed">{step.detail}</p>}
                    </div>
                  </div>
                  {step.illustration && (
                    <div
                      className="mb-4 rounded-2xl overflow-hidden border border-slate-200 bg-slate-50 [&_svg]:block [&_svg]:w-full [&_svg]:h-auto"
                      dangerouslySetInnerHTML={{ __html: step.illustration }}
                    />
                  )}
                  {step.substeps && step.substeps.length > 0 && (
                    <ol className="grid gap-2.5 mb-4">
                      {step.substeps.map((ss: string, j: number) => (
                        <li key={j} className="flex items-start gap-3 text-slate-700">
                          <span className="shrink-0 mt-0.5 w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center">{j + 1}</span>
                          <span className="leading-relaxed">{ss}</span>
                        </li>
                      ))}
                    </ol>
                  )}
                  {step.tip && (
                    <div className="flex items-start gap-3 p-4 bg-amber-50 border border-amber-200 rounded-xl">
                      <Lightbulb size={18} className="text-amber-500 mt-0.5 shrink-0" />
                      <p className="text-slate-700 text-sm leading-relaxed"><span className="font-bold text-amber-700">Tip: </span>{step.tip}</p>
                    </div>
                  )}
                </div>
              ))}

              {/* Evidence checklist */}
              {activeSession.evidence && activeSession.evidence.length > 0 && (
                <div className="bg-white border-2 border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm">
                  <h3 className="text-lg font-bold text-indigo-800 mb-4 border-b-2 border-indigo-100 pb-2">Evidence to Collect for Paper 2</h3>
                  <ul className="grid gap-2">
                    {activeSession.evidence.map((e: string, i: number) => (
                      <li key={i} className="flex items-start gap-3 text-slate-600"><CheckCircle2 size={18} className="text-emerald-500 mt-0.5 shrink-0" />{e}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Ethics note */}
              {activeSession.ethics_note && (
                <div className="bg-rose-50 border-2 border-rose-100 rounded-3xl p-6 sm:p-8">
                  <h3 className="text-lg font-bold text-rose-800 mb-2">Don't Forget: Ethics</h3>
                  <p className="text-slate-700 leading-relaxed">{activeSession.ethics_note}</p>
                </div>
              )}

              {/* Next up */}
              {activeSession.next_up && (
                <div className="bg-indigo-50 border-2 border-indigo-100 rounded-3xl p-6 sm:p-8">
                  <h3 className="text-lg font-bold text-indigo-800 mb-2 flex items-center gap-2"><Rocket size={18} /> What's Next</h3>
                  <p className="text-slate-700 leading-relaxed">{activeSession.next_up}</p>
                </div>
              )}

              <button onClick={() => setView('dashboard')} className="self-start px-8 py-3 rounded-xl border-2 border-slate-200 bg-white font-bold text-slate-600 flex items-center gap-2">
                <ArrowLeft size={18} /> Back to Dashboard
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {activeSubject && (
        <nav className="fixed bottom-0 left-0 right-0 h-20 bg-white border-t-2 border-slate-200 flex justify-around items-center z-50">
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
          <NavButton icon={<GraduationCap size={24} />} label="Exams" active={view === 'exam'} onClick={() => {setView('exam'); setIsMemStarted(false);}} />
        </nav>
      )}
    </div>
  );
}

function DashboardCard({ icon, color, title, desc, action }: any) {
  // Full static class strings so Tailwind does not purge them.
  const styles: any = {
    emerald: { card: 'hover:border-emerald-500', wrap: 'bg-emerald-100 text-emerald-600', btn: 'bg-emerald-600 border-emerald-800' },
    amber: { card: 'hover:border-amber-500', wrap: 'bg-amber-100 text-amber-600', btn: 'bg-amber-500 border-amber-700' },
    violet: { card: 'hover:border-violet-500', wrap: 'bg-violet-100 text-violet-600', btn: 'bg-violet-600 border-violet-800' },
    indigo: { card: 'hover:border-indigo-500', wrap: 'bg-indigo-100 text-indigo-600', btn: 'bg-indigo-600 border-indigo-800' },
  };
  const s = styles[color] || styles.emerald;
  return (
    <div className={`bg-white p-8 rounded-3xl border-2 border-slate-200 shadow-sm transition-all group ${s.card}`}>
      <div className={`${s.wrap} w-16 h-16 rounded-2xl flex items-center justify-center mb-6`}>{icon}</div>
      <h3 className="text-2xl font-bold mb-2 text-slate-800">{title}</h3>
      <p className="text-slate-500 mb-8">{desc}</p>
      <button onClick={action} className={`w-full py-4 text-white font-bold rounded-xl border-b-4 flex items-center justify-center gap-2 ${s.btn}`}>
        <PlayCircle size={20} /> Start
      </button>
    </div>
  );
}

function NavButton({ icon, label, active = false, onClick }: any) {
  return (
    <button onClick={onClick} className={`flex flex-col items-center justify-center gap-1 transition-all ${active ? 'text-emerald-600 scale-110' : 'text-slate-400'}`}>
      {icon} <span className="text-[10px] font-black uppercase">{label}</span>
    </button>
  );
}
