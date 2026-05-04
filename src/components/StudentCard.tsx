import type { Student } from '../types'

interface Props {
  student: Student
  isActive: boolean
  delay?: number
  onToggle: () => void
  onChat: () => void
}

export default function StudentCard({ student, isActive, delay = 0, onToggle, onChat }: Props) {
  return (
    <div
      className={`card${isActive ? ' open' : ''}`}
      style={{ animationDelay: `${delay}ms` }}
      onClick={e => { if ((e.target as Element).closest('a,button')) return; onToggle() }}
    >
      <div className="av-ring">
        <img src={student.image} alt={student.meno} loading="lazy" />
        <div className="av-id">#{student.id}</div>
      </div>

      <div className="card-name">{student.meno} {student.priezvisko}</div>
      <div className="role-pill">✦ Študent</div>

      <div className="card-expand">
        <div className="exp-inner">
          <div className="drow"><span>Meno</span><strong>{student.meno}</strong></div>
          <div className="drow"><span>Priezvisko</span><strong>{student.priezvisko}</strong></div>
          <div className="drow"><span>ID</span><strong>#{student.id}</strong></div>
        </div>
      </div>

      <div className="card-foot">
        <button className="chat-btn" onClick={e => { e.stopPropagation(); onChat() }}>
          💬 Chatovať so študentom
        </button>
      </div>
    </div>
  )
}
