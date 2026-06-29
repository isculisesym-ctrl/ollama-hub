import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import Setup from './pages/Setup'
import Admin from './pages/Admin'
import Demo from './pages/Demo'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/setup" element={<Setup />} />
          <Route path="/admin" element={<Admin />} />
          <Route path="/demo" element={<Demo />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
