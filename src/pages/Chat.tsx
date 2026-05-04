import { useState, useEffect, useRef } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import type { Message } from '../types'

const OR_BASE = 'https://openrouter.ai/api/v1'

function systemPrompt(meno: string | null, priezvisko: string | null): string {
  if (meno && priezvisko) {
    return `Tvoje meno je ${meno} ${priezvisko}. Si skutočný človek a študent na škole. Odpovedaj ako tento študent s vlastnou osobnosťou. Odpovedaj stručne a priateľsky po slovensky. Používaj emoji. Nehovor, že si AI pokiaľ sa ťa to nevyslovene nespýtajú.`
  }
  return `Si priateľský a inteligentný AI asistent pre stránku Student Gallery.
Táto stránka zobrazuje nasledovných 10 študentov:
Peter Hruška, Jana Malá, Michal Kováč, Lucia Srnková, Marek Vysoký,
Ema Biela, Dávid Čierny, Simona Veselá, Jakub Dlhý, Katarína Šikovná.
Odpovedáš v slovenčine, ak sa pýtajú po slovensky. Ak po anglicky, odpovedáš po anglicky.
Si nápomocný, priateľský a stručný. Používaj emoji kde je to vhodné.`
}

function renderMd(t: string): string {
  return t
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/^#{1,3} (.+)$/gm, '<strong>$1</strong>')
    .replace(/^[-•] (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')
    .replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>')
    .replace(/^(.+)$/, '<p>$1</p>')
}

function timeStr() {
  return new Date().toLocaleTimeString('sk-SK', { hour: '2-digit', minute: '2-digit' })
}

export default function Chat() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const meno = params.get('meno')
  const priezvisko = params.get('priezvisko')
  const image = params.get('image')

  const [apiKey, setApiKey] = useState(() => localStorage.getItem('or_api_key') ?? '')
  const [keyInput, setKeyInput] = useState('')
  const [showModal, setShowModal] = useState(!localStorage.getItem('or_api_key'))
  const [keyError, setKeyError] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [typing, setTyping] = useState(false)
  const [freeModels, setFreeModels] = useState<string[]>([])
  const [modelIdx, setModelIdx] = useState(0)
  const msgsEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    fetch(`${OR_BASE}/models`)
      .then(r => r.json())
      .then(d => {
        const models: string[] = (d.data ?? [])
          .filter((m: { id: string; architecture?: { modality?: string } }) =>
            m.id.endsWith(':free') && m.architecture?.modality === 'text->text')
          .map((m: { id: string }) => m.id)
        setFreeModels(models.length ? models : ['meta-llama/llama-3.2-3b-instruct:free'])
      })
      .catch(() => setFreeModels(['meta-llama/llama-3.2-3b-instruct:free', 'google/gemma-2-9b-it:free']))
  }, [])

  useEffect(() => {
    msgsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, typing])

  function saveKey() {
    if (!keyInput.startsWith('sk-or-')) { setKeyError('Kľúč musí začínať s "sk-or-"'); return }
    localStorage.setItem('or_api_key', keyInput)
    setApiKey(keyInput)
    setShowModal(false)
    setKeyError('')
  }

  async function send(text: string) {
    const t = text.trim()
    if (!t) return
    if (!apiKey) { setShowModal(true); return }

    const userMsg: Message = { role: 'user', content: t, time: timeStr() }
    const nextMessages = [...messages, userMsg]
    setMessages(nextMessages)
    setInput('')
    setTyping(true)

    const history = nextMessages.map(m => ({
      role: m.role === 'ai' ? 'assistant' : 'user',
      content: m.content,
    }))

    const models = freeModels.length ? freeModels : ['meta-llama/llama-3.2-3b-instruct:free']
    let currentIdx = modelIdx

    for (let i = currentIdx; i < models.length; i++) {
      try {
        const res = await fetch(`${OR_BASE}/chat/completions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
          body: JSON.stringify({
            model: models[i],
            messages: [{ role: 'system', content: systemPrompt(meno, priezvisko) }, ...history],
            temperature: 0.85,
            max_tokens: 1024,
          }),
        })
        const d = await res.json().catch(() => ({}))
        if (!res.ok) {
          const errMsg: string = d?.error?.message ?? d?.error ?? ''
          const isModelErr = res.status === 404 || errMsg.toLowerCase().includes('no endpoints')
          if (isModelErr && i < models.length - 1) { currentIdx = i + 1; setModelIdx(i + 1); continue }
          throw new Error(`${res.status}: ${errMsg || JSON.stringify(d)}`)
        }
        setModelIdx(i)
        const reply: string = d.choices?.[0]?.message?.content ?? '(prázdna odpoveď)'
        setMessages(prev => [...prev, { role: 'ai', content: reply, time: timeStr() }])
        break
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : String(e)
        setMessages(prev => [...prev, { role: 'ai', content: `⚠️ ${msg}`, time: timeStr() }])
        break
      }
    }

    setTyping(false)
    inputRef.current?.focus()
  }

  return (
    <>
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-card">
            <div className="modal-icon">⚡</div>
            <h2>OpenRouter API kľúč</h2>
            <p>
              Zadarmo — žiadna kreditná karta.<br />
              Registruj sa na{' '}
              <a href="https://openrouter.ai" target="_blank" rel="noreferrer">openrouter.ai</a>,
              klikni na <strong>Keys</strong> a vytvor kľúč.<br /><br />
              Používa bezplatné AI modely (Llama, Mistral, Gemma).
            </p>
            <input
              className="key-input"
              type="password"
              placeholder="sk-or-…"
              value={keyInput}
              autoComplete="off"
              onChange={e => setKeyInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && saveKey()}
            />
            <button className="key-btn" onClick={saveKey}>Spustiť chat</button>
            {keyError && <div className="key-error">{keyError}</div>}
          </div>
        </div>
      )}

      <div className="chat-app">
        <header className="chat-header">
          <div className="h-avatar">
            {image ? <img src={decodeURIComponent(image)} alt="avatar" /> : '🤖'}
          </div>
          <div className="h-info">
            <h1>{meno && priezvisko ? `${meno} ${priezvisko}` : 'AI Asistent'}</h1>
            <div className="h-status"><span className="status-dot" /> Online</div>
          </div>
          <div className="h-actions">
            <button className="icon-btn" onClick={() => setMessages([])}>🗑 <span>Vymazať</span></button>
            <button className="icon-btn" onClick={() => { setKeyInput(apiKey); setShowModal(true) }}>🔑 <span>Kľúč</span></button>
            <button className="icon-btn" onClick={() => navigate('/')}>← Späť</button>
          </div>
        </header>

        <div className="msgs-list">
          {messages.length === 0 && (
            <div className="welcome">
              <div className="welcome-icon">✨</div>
              <h2>{meno ? `Ahoj! Som ${meno} ${priezvisko}` : 'Ahoj! Som váš AI asistent'}</h2>
              <p>
                {meno
                  ? 'Opýtaj sa ma čokoľvek. Budem chatovať ako tvoj spolužiak!'
                  : 'Opýtaj sa ma čokoľvek — pomôžem s otázkami, vysvetlím pojmy alebo si pokecáme.'}
              </p>
              <div className="chips">
                <button className="chip" onClick={() => send('Ako sa volajú študenti na tejto stránke?')}>👥 Kto sú študenti?</button>
                <button className="chip" onClick={() => send('Povedz mi vtip v slovenčine.')}>😄 Povedz vtip</button>
                <button className="chip" onClick={() => send('Čo je to API a na čo slúži?')}>🔌 Čo je API?</button>
                <button className="chip" onClick={() => send('Vysvetli mi, ako funguje Flask v Pythone.')}>🐍 Ako funguje Flask?</button>
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`msg-row ${m.role}`}>
              <div className="msg-av">{m.role === 'ai' ? '⚡' : '🧑'}</div>
              <div className="msg-col">
                {m.role === 'ai' ? (
                  <div className="bubble" dangerouslySetInnerHTML={{ __html: renderMd(m.content) }} />
                ) : (
                  <div className="bubble">{m.content}</div>
                )}
                <div className="msg-time">{m.time}</div>
              </div>
            </div>
          ))}

          {typing && (
            <div className="msg-row ai">
              <div className="typing-av">🤖</div>
              <div className="typing-bubble">
                <div className="dot" /><div className="dot" /><div className="dot" />
              </div>
            </div>
          )}
          <div ref={msgsEndRef} />
        </div>

        <div className="input-area">
          <div className="input-box">
            <textarea
              ref={inputRef}
              className="msg-input"
              rows={1}
              placeholder="Napíš správu…"
              value={input}
              onChange={e => {
                setInput(e.target.value)
                e.currentTarget.style.height = 'auto'
                e.currentTarget.style.height = Math.min(e.currentTarget.scrollHeight, 140) + 'px'
              }}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(input) }
              }}
            />
            <button className="send-btn" disabled={typing} onClick={() => send(input)}>↑</button>
          </div>
          <div className="input-hint">Enter — odoslať &nbsp;·&nbsp; Shift+Enter — nový riadok</div>
        </div>
      </div>
    </>
  )
}
