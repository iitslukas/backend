import { Routes, Route } from 'react-router-dom'
import Gallery from './pages/Gallery'
import Chat from './pages/Chat'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Gallery />} />
      <Route path="/chat" element={<Chat />} />
    </Routes>
  )
}
