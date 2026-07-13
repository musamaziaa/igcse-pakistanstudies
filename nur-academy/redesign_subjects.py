import re

with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "r") as f:
    content = f.read()

# Update Subject Interface
old_interface = """interface Subject {
  key: string;
  name: string;
  tagline: string;
  icon: ReactNode;
  card: string;
  iconWrap: string;
  heading: string;
  tagClass: string;
  isLocked?: boolean;
}"""

new_interface = """interface Subject {
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
}"""

content = content.replace(old_interface, new_interface)

# Update SUBJECTS array
old_subjects_pattern = r"const SUBJECTS: Subject\[\] = \[\n(.*?)\n\];"
new_subjects = """const SUBJECTS: Subject[] = [
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
];"""
content = re.sub(r'const SUBJECTS: Subject\[\] = \[\n.*?\n\];', new_subjects, content, flags=re.DOTALL)

# Update Rendering Logic
old_render = """              {/* Active Subjects */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto w-full mb-8">
                {SUBJECTS.filter((s: Subject) => !s.isLocked).map((subject: Subject) => (
                  <button key={subject.key} onClick={() => { setActiveSubject(subject.key); setView('dashboard'); }} className={`text-left p-8 rounded-3xl border border-slate-800 transition-all flex flex-col group relative overflow-hidden ${subject.card}`}>
                    <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-white/5 to-transparent rounded-full -translate-y-32 translate-x-32 group-hover:scale-110 transition-transform duration-500 pointer-events-none" />
                    <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform shadow-inner ${subject.iconWrap}`}>
                      {subject.icon}
                    </div>
                    <h3 className={`text-2xl font-bold ${subject.heading}`}>{subject.name}</h3>
                    <p className="mt-2 text-slate-400 font-medium">{subject.tagline}</p>
                    <div className="mt-8 flex items-center text-emerald-400 font-bold text-sm uppercase tracking-wider group-hover:translate-x-2 transition-transform">
                      Enter Subject <ChevronRight size={18} className="ml-1" />
                    </div>
                  </button>
                ))}
              </div>"""

new_render = """              {/* Active Subjects */}
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
              </div>"""

if "Active Subjects" in content:
    content = re.sub(r'\{\/\* Active Subjects \*\/\}.*?<\/div>', new_render, content, flags=re.DOTALL)

with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "w") as f:
    f.write(content)
