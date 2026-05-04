export interface Student {
  id: number
  meno: string
  priezvisko: string
  image: string
}

export interface Message {
  role: 'user' | 'ai'
  content: string
  time: string
}
