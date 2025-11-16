import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'
import Dashboard from './views/Dashboard'
import Locations from './views/Locations'

function App() {
  return (
    <Router>
      <nav style={{
        padding: '1rem',
        background: '#1a1a1a',
        marginBottom: '2rem',
        display: 'flex',
        gap: '1rem'
      }}>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Dashboard</Link>
        <Link to="/locations" style={{ color: 'white', textDecoration: 'none' }}>Locations</Link>
        <Link to="/factions" style={{ color: 'white', textDecoration: 'none' }}>Factions</Link>
        <Link to="/characters" style={{ color: 'white', textDecoration: 'none' }}>Characters</Link>
        <Link to="/timeline" style={{ color: 'white', textDecoration: 'none' }}>Timeline</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/locations" element={<Locations />} />
        <Route path="/factions" element={<div className="container"><h1>Factions</h1><p>Coming soon...</p></div>} />
        <Route path="/characters" element={<div className="container"><h1>Characters</h1><p>Coming soon...</p></div>} />
        <Route path="/timeline" element={<div className="container"><h1>Timeline</h1><p>Coming soon...</p></div>} />
      </Routes>
    </Router>
  )
}

export default App
