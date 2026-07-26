// api.js
//
// Every single call to our backend server lives in this one file.
// Keeping them all in one place means if the backend URL ever changes,
// or something breaks, there's only ONE place to look, not scattered
// across every component.

const BASE_URL = "http://127.0.0.1:8000"

/**
 * Uploads a CSV file to the backend and gets back the full graph data:
 * nodes, edges, and a summary of totals.
 */
export async function uploadCallRecords(file) {
  const formData = new FormData()
  formData.append("file", file)

  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || "Upload failed")
  }

  return response.json()
}

/**
 * Gets the most "important" phone numbers from the last uploaded data:
 * hub numbers (talk to the most people) and bridge numbers (connect
 * separate groups together).
 */
export async function getCentralNumbers() {
  const response = await fetch(`${BASE_URL}/central-numbers`)
  if (!response.ok) {
    throw new Error("Could not fetch central numbers")
  }
  return response.json()
}

/**
 * Finds the connection path between two phone numbers, even if they
 * never called each other directly.
 */
export async function getShortestPath(numberA, numberB) {
  const params = new URLSearchParams({ number_a: numberA, number_b: numberB })
  const response = await fetch(`${BASE_URL}/shortest-path?${params}`)
  if (!response.ok) {
    throw new Error("Could not fetch shortest path")
  }
  return response.json()
}
