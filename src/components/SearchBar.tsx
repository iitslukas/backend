interface Props {
  value: string
  onChange: (v: string) => void
}

export default function SearchBar({ value, onChange }: Props) {
  return (
    <div className="search-wrap">
      <div className="search-inner">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          className="search-input"
          placeholder="Hľadaj podľa mena..."
          value={value}
          onChange={e => onChange(e.target.value)}
          autoComplete="off"
        />
      </div>
    </div>
  )
}
