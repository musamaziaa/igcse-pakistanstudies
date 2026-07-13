with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "r") as f:
    content = f.read()

# 1. Add WhatsApp state variables
state_injection = """  const [selectedDay, setSelectedDay] = useState<string | null>(null);
  const [whatsappNumber, setWhatsappNumber] = useState('');
  const [whatsappEnabled, setWhatsappEnabled] = useState(false);
  const [isSavingSettings, setIsSavingSettings] = useState(false);

  const saveWhatsappSettings = async () => {
    if (!user) return;
    setIsSavingSettings(true);
    try {
      const res = await fetch(`${API_BASE}/api/users/${user.sub}/profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: user.name,
          email: user.email,
          picture: user.picture,
          whatsapp_number: whatsappNumber,
          whatsapp_enabled: whatsappEnabled
        })
      });
      if (res.ok) {
        alert("WhatsApp settings saved successfully!");
      }
    } catch (err) {
      console.error(err);
      alert("Failed to save settings.");
    } finally {
      setIsSavingSettings(false);
    }
  };"""

content = content.replace("  const [selectedDay, setSelectedDay] = useState<string | null>(null);", state_injection)

# 2. Update progress fetch callback to set state from profile
old_fetch_progress = """.then(d => { if (d) setProgressData(d); })"""
new_fetch_progress = """.then(d => {
          if (d) {
            setProgressData(d);
            if (d.profile) {
              setWhatsappNumber(d.profile.whatsapp_number || '');
              setWhatsappEnabled(d.profile.whatsapp_enabled || false);
            }
          }
        })"""

content = content.replace(old_fetch_progress, new_fetch_progress)

# 3. Add Settings Card into Progress View
old_back_button = """              <button onClick={() => setView('dashboard')} className="self-start px-8 py-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 hover:text-white font-bold text-slate-300 flex items-center gap-2 transition-all">"""

whatsapp_settings_card = """              {/* WhatsApp Reports Settings */}
              <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-sm">
                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                  <svg viewBox="0 0 24 24" className="w-5 h-5 fill-emerald-400"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.5-5.729-1.45L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.825 1.451 5.436 0 9.86-4.37 9.864-9.799.002-2.63-1.023-5.101-2.885-6.966a9.9 9.9 0 00-6.98-2.879c-5.443 0-9.866 4.372-9.87 9.802 0 1.714.453 3.39 1.31 4.887l-.994 3.63 3.73-.976zm10.743-6.195c-.297-.15-1.758-.867-2.03-.966-.273-.1-.472-.15-.672.15-.2.3-.775.966-.95 1.165-.175.2-.35.225-.647.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.2.05-.373-.025-.523-.075-.15-.672-1.62-.922-2.215-.242-.584-.487-.504-.672-.513l-.573-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414-.074-.124-.272-.198-.57-.347z"/></svg>
                  WhatsApp Progress Reports
                </h3>
                <p className="text-slate-400 text-sm mb-4 leading-relaxed">
                  Send automated study session updates (streaks, accuracy, time taken) automatically to a phone number. Perfect for keeping parents in the loop.
                </p>
                <div className="grid gap-4 max-w-md">
                  <div className="flex flex-col gap-1.5">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">WhatsApp Phone Number</label>
                    <input
                      type="text"
                      placeholder="e.g. +923001234567"
                      value={whatsappNumber}
                      onChange={(e) => setWhatsappNumber(e.target.value)}
                      className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-slate-200 text-sm focus:border-emerald-500/50 focus:outline-none transition-colors"
                    />
                  </div>
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      id="whatsapp_enabled"
                      checked={whatsappEnabled}
                      onChange={(e) => setWhatsappEnabled(e.target.checked)}
                      className="w-4 h-4 rounded border-slate-800 text-emerald-500 focus:ring-emerald-500/20 bg-slate-950"
                    />
                    <label htmlFor="whatsapp_enabled" className="text-sm font-medium text-slate-300 cursor-pointer select-none">
                      Enable automatic WhatsApp updates
                    </label>
                  </div>
                  <button
                    onClick={saveWhatsappSettings}
                    disabled={isSavingSettings}
                    className="self-start px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm rounded-xl transition-all shadow-[0_0_15px_rgba(16,185,129,0.2)] disabled:opacity-50"
                  >
                    {isSavingSettings ? 'Saving...' : 'Save WhatsApp Settings'}
                  </button>
                </div>
              </div>

              <button onClick={() => setView('dashboard')} className="self-start px-8 py-3 rounded-xl border border-slate-800 bg-slate-900 hover:bg-slate-800 hover:text-white font-bold text-slate-300 flex items-center gap-2 transition-all">"""

content = content.replace(old_back_button, whatsapp_settings_card)

with open("/home/muz/Documents/igcse-pakistanstudies/nur-academy/src/App.tsx", "w") as f:
    f.write(content)
