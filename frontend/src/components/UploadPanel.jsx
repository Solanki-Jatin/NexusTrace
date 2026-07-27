import { useState } from 'react'
import { uploadCallRecords } from '../api.js'

// This component shows a file picker button. When the user selects a
// CSV file, it sends it to the backend and hands the result back up to
// the App component (via the onUploadSuccess function passed in as a prop).
export default function UploadPanel({ onUploadSuccess }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleFileChange(event) {
    const file = event.target.files[0]
    if (!file) return

    setLoading(true)
    setError(null)

    try {
      const data = await uploadCallRecords(file)
      onUploadSuccess(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-panel">
      <label className="upload-button">
        {loading ? "Analyzing..." : "Upload Call Records (CSV)"}
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          disabled={loading}
          style={{ display: "none" }}
        />
      </label>
      {error && <p className="error-text">{error}</p>}
    </div>
  )
}
