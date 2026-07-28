import { useState } from 'react'
import { getShortestPath } from '../api.js'

// Lets the user type two phone numbers and see how they're connected,
// even if they never called each other directly. The result gets
// passed up to App, which highlights that path on the graph.
export default function PathFinder({ onPathFound }) {
  const [numberA, setNumberA] = useState("")
  const [numberB, setNumberB] = useState("")
  const [message, setMessage] = useState("")

  async function handleFindPath(event) {
    event.preventDefault()
    if (!numberA.trim() || !numberB.trim()) return

    try {
      const result = await getShortestPath(numberA.trim(), numberB.trim())
      if (result.connected) {
        onPathFound(result.path)
        setMessage(`Connected through ${result.path.length} number(s): ${result.path.join(" -> ")}`)
      } else {
        onPathFound([])
        setMessage("No connection found between these two numbers.")
      }
    } catch (err) {
      setMessage("Error: " + err.message)
    }
  }

  return (
    <form className="path-finder" onSubmit={handleFindPath}>
      <input
        type="text"
        placeholder="First number"
        value={numberA}
        onChange={(e) => setNumberA(e.target.value)}
      />
      <input
        type="text"
        placeholder="Second number"
        value={numberB}
        onChange={(e) => setNumberB(e.target.value)}
      />
      <button type="submit">Find Connection</button>
      {message && <p className="path-message">{message}</p>}
    </form>
  )
}
