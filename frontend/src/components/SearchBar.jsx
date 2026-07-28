import { useState } from 'react'

// A simple text input where the user types a phone number, and we tell
// the parent (App) which node to focus/highlight on the graph.
export default function SearchBar({ onSearch }) {
  const [value, setValue] = useState("")

  function handleSubmit(event) {
    event.preventDefault()
    if (value.trim()) {
      onSearch(value.trim())
    }
  }

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Search a phone number..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <button type="submit">Search</button>
    </form>
  )
}
