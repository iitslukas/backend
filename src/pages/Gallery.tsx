import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import StudentCard from '../components/StudentCard'
import type { Student } from '../types'

export default function Gallery() {
  const [students, setStudents] = useState<Student[]>([])
  const [search, setSearch] = useState('')
  const [activeId, setActiveId] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetch('/api')
      .then(r => { if (!r.ok) throw new Error(`Server vrátil ${r.status}`); return r.json() })
      .then((data: Student[]) => { setStudents(data); setLoading(false) })
      .catch((e: Error) => { setError(e.message); setLoading(false) })
  }, [])

  const filtered = search.trim()
    ? students.filter(s => `${s.meno} ${s.priezvisko}`.toLowerCase().includes(search.toLowerCase()))
    : students

  function goChat(s: Student) {
    navigate(`/chat?meno=${encodeURIComponent(s.meno)}&priezvisko=${encodeURIComponent(s.priezvisko)}&image=${encodeURIComponent(s.image)}`)
  }

  return (
    <div className="page">
      <div className="orb orb-1" /><div className="orb orb-2" /><div className="orb orb-3" />

      <section className="hero">
        <div className="badge"><span className="badge-dot" /> Live · Student Gallery</div>
        <h1>Zoznam Študentov</h1>
        <p className="sub">Klikni na kartu pre viac detailov &nbsp;·&nbsp; Chatuj s AI asistentom</p>
      </section>

      <div className="controls">
        <div className="search-wrap">
          <div className="search-box">
            <span className="si">🔍</span>
            <input
              id="searchBar" type="text"
              placeholder="Hľadaj podľa mena…"
              value={search}
              onChange={e => setSearch(e.target.value)}
              autoComplete="off"
            />
          </div>
        </div>
        <div className="stats-bar">
          <div className="stat-pill">Celkom &nbsp;<strong>{students.length || '—'}</strong></div>
          <div className="stat-pill">Zobrazených &nbsp;<strong>{loading ? '—' : filtered.length}</strong></div>
        </div>
      </div>

      <div className="grid">
        {loading && Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="sk-card">
            <div className="sk sk-av" /><div className="sk sk-nm" />
            <div className="sk sk-rl" /><div className="sk sk-btn" />
          </div>
        ))}

        {error && (
          <div className="error-state" style={{ gridColumn: '1/-1' }}>
            <div className="error-icon">⚠️</div>
            <div className="error-title">Nepodarilo sa načítať študentov</div>
            <div className="error-msg">{error}</div>
            <button className="retry-btn" onClick={() => window.location.reload()}>↺ Skúsiť znova</button>
          </div>
        )}

        {!loading && !error && filtered.map((s, i) => (
          <StudentCard
            key={s.id} student={s}
            isActive={activeId === s.id}
            delay={i * 55}
            onToggle={() => setActiveId(activeId === s.id ? null : s.id)}
            onChat={() => goChat(s)}
          />
        ))}

        {!loading && !error && filtered.length === 0 && students.length > 0 && (
          <div className="empty-state" style={{ gridColumn: '1/-1' }}>
            <div className="empty-icon">🔍</div>
            <div>Žiadny výsledok pre „<strong>{search}</strong>"</div>
          </div>
        )}
      </div>

      <footer>Student Gallery &nbsp;·&nbsp; 2026</footer>
      <button className="fab" onClick={() => navigate('/chat')}>✨ AI Chat</button>
    </div>
  )
}
