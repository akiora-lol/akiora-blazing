import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout/Layout.jsx'
import { Welcome } from './pages/Welcome.js'
import './i18n.js'

function App() {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<Welcome />} />
                    <Route path="/champions" element={<div className="container mx-auto px-4 py-20"><h1 className="text-4xl font-bold text-glow-red">Champions</h1></div>} />
                    <Route path="/items" element={<div className="container mx-auto px-4 py-20"><h1 className="text-4xl font-bold text-glow-cyan">Items</h1></div>} />
                    <Route path="/builds" element={<div className="container mx-auto px-4 py-20"><h1 className="text-4xl font-bold text-glow-red">Builds</h1></div>} />
                </Routes>
            </Layout>
        </BrowserRouter>
    )
}

export default App
