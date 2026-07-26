import { useState } from 'react'
import UploadPanel from './components/UploadPanel.jsx'
import GraphView from './components/GraphView.jsx'
import SearchBar from './components/SearchBar.jsx'
import PathFinder from './components/PathFinder.jsx'
import { getCentralNumbers } from './api.js'

// This is the main "control center" component. It holds all the shared
// data (the graph, the important numbers, the highlighted path) and
// passes pieces of it down to each smaller component that needs it.
export default function App() {
  const [graphData, setGraphData] = useState(null)
  const [summary, setSummary] = useState(null)
  const [centralData, setCentralData] = useState(null)
  const [highlightedPath, setHighlightedPath] = useState([])
  const [searchedNode, setSearchedNode] = useState(null)

  // Called after a file is successfully uploaded and analyzed.
  async function handleUploadSuccess(data) {
    setGraphData(data)
    setSummary(data.summary)
    setHighlightedPath([])

    // once we have a graph, also fetch the "important numbers" list
    try {
      const central = await getCentralNumbers()
      setCentralData(central)
    } catch (err) {
      console.error("Could not load central numbers:", err)
    }
  }

  // Turns the top_hub_numbers list into a simple {number: score} lookup,
  // so GraphView can quickly check "how important is this node" while drawing.
  const hubScores = {}
  if (centralData) {
    centralData.top_hub_numbers.forEach((entry) => {
      hubScores[entry.number] = entry.score
    })
  }

  function handleSearch(number) {
    setSearchedNode(number)
    setHighlightedPath([number])
  }

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1>NexusTrace</h1>
        <p>Upload call records to find suspect networks automatically.</p>
      </header>

      <div className="app-body">
        <aside className="sidebar">
          <UploadPanel onUploadSuccess={handleUploadSuccess} />

          {summary && (
            <div className="summary-box">
              <p><strong>{summary.total_nodes}</strong> phone numbers</p>
              <p><strong>{summary.total_edges}</strong> connections</p>
              <p><strong>{summary.total_clusters}</strong> clusters found</p>
            </div>
          )}

          {graphData && (
            <>
              <SearchBar onSearch={handleSearch} />
              <PathFinder onPathFound={setHighlightedPath} />
            </>
          )}

          {centralData && (
            <div className="central-numbers-box">
              <h3>Top Hub Numbers</h3>
              <ul>
                {centralData.top_hub_numbers.map((entry) => (
                  <li key={entry.number}>{entry.number} ({entry.score})</li>
                ))}
              </ul>
            </div>
          )}
        </aside>

        <main className="graph-container">
          <GraphView
            graphData={graphData}
            hubScores={hubScores}
            highlightedPath={highlightedPath}
            onNodeClick={(id) => setHighlightedPath([id])}
          />
        </main>
      </div>
    </div>
  )
}
