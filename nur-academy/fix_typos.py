with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "r") as f:
    content = f.read()

# Fix the min-h-screen container
content = content.replace('selection:bg-emerald-950/20 border border-emerald-500/200/30', 'selection:bg-emerald-500/30')

# Fix NUR ACADEMY logo wrapper
content = content.replace('bg-emerald-950/20 border border-emerald-500/200/20 rounded-lg flex items-center justify-center border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.2)]', 'bg-emerald-500/20 rounded-lg flex items-center justify-center border border-emerald-500/30 shadow-[0_0_15px_rgba(16,185,129,0.2)]')

# Fix Active Subject TagClass fallback
content = content.replace("bg-emerald-950/20 border border-emerald-500/200/10 text-emerald-400 border border-emerald-500/20", "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20")

# Fix Exam active button
content = content.replace("shadow-[0_0_10px_rgba(16,185,129,0.3)] bg-emerald-950/20 border border-emerald-500/200/10 text-emerald-400", "shadow-[0_0_10px_rgba(16,185,129,0.3)] bg-emerald-500/10 text-emerald-400")

# Fix DashboardCard emerald style
content = content.replace("wrap: 'bg-emerald-950/20 border border-emerald-500/200/10 border-emerald-500/20 text-emerald-400'", "wrap: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'")
content = content.replace("btn: 'bg-emerald-950/20 border border-emerald-500/200/10 text-emerald-400 border-emerald-500/30 hover:bg-emerald-950/20 border border-emerald-500/200/20'", "btn: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/20'")

with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "w") as f:
    f.write(content)
