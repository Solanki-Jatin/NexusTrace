# NexusTrace — Complete Project Roadmap Checklist

A single place to track everything, from today's progress to the final submission.

---

## ✅ V1 — Foundation (Core Engine)

### Setup & Data
- [x] Create GitHub repo, initial README
- [x] Add `.gitignore`
- [x] Write synthetic CDR data generator (`generate_data.py`)
- [x] Generate sample dataset with planted suspect cluster (`call_records.csv`)
- [x] Add `requirements.txt`

### Core Analysis Engine
- [x] Build graph construction logic (CSV → nodes & weighted edges)
- [x] Implement community/cluster detection (Louvain method)
- [x] Implement centrality scoring (find "hub" and "bridge" numbers)
- [x] Implement shortest-path search between two numbers
- [x] Save analysis output as JSON for frontend use (`graph_output.json`)
- [x] Test that planted suspect cluster is actually detected correctly

### Backend API
- [x] Set up FastAPI project structure
- [x] Endpoint: upload a CSV file
- [x] Endpoint: return graph + cluster data as JSON
- [x] Endpoint: shortest path between two given numbers
- [x] Endpoint: get top central/hub numbers
- [x] Basic error handling (bad file format, empty file, etc.)
- [x] Test API endpoints manually (Postman or browser)

### Frontend (not started yet)
- [ ] Set up React project
- [ ] File upload component
- [ ] Connect upload to backend API
- [ ] Render graph visually (react-force-graph or D3)
- [ ] Color nodes by cluster
- [ ] Size nodes by importance/centrality
- [ ] Click a node → highlight its direct connections
- [ ] Search bar to find a specific number
- [ ] Select two numbers → show shortest path highlighted on graph
- [ ] Basic responsive styling (doesn't need to be fancy, just clean)

### Demo Prep
- [ ] Design a "realistic" final demo dataset (clear story, obvious cluster, a couple of interesting hub numbers)
- [ ] Write a 2-minute demo script (what to click, what to say)
- [ ] Record demo video/GIF
- [ ] Add demo video/GIF to README
- [ ] Take screenshots for README
- [ ] Update README: mark v1 checklist items as done, fill in "Getting Started" instructions properly
- [ ] Add team member names to README

### V1 Wrap-up
- [ ] Full run-through test (fresh clone → install → run → upload data → see results) to make sure nothing's broken
- [ ] Tag this version in Git as `v1.0` (optional but professional touch)

---

## 🚀 V2 — Timeline

- [ ] Add date-range filter to the graph (show only calls within a chosen time window)
- [ ] Build a timeline slider UI component
- [ ] Detect calling pattern spikes/drops around specific dates
- [ ] Highlight "sudden activity change" numbers automatically
- [ ] Update backend to support time-filtered queries
- [ ] Update README roadmap table, mark v2 as current

---

## 🌍 V3 — Geo

- [ ] Add tower location data to synthetic dataset generator
- [ ] Build geo-clustering logic (which numbers are physically near each other over time)
- [ ] Add a map view to frontend (Leaflet.js or Google Maps embed)
- [ ] Plot movement patterns per number over time
- [ ] Cross-reference geo-clusters with call-based clusters (do they match?)

---

## 🔗 V4 — Fusion

- [ ] Design synthetic IPDR (internet/app usage) dataset structure
- [ ] Build IPDR data generator
- [ ] Extend graph model to support multiple data source types (calls + internet usage)
- [ ] Merge/correlate CDR + IPDR into one unified view
- [ ] Update frontend to toggle between data source views

---

## 📡 V5 — Signal (Anomaly Detection)

- [ ] Define what "normal" calling behavior looks like (baseline)
- [ ] Implement simple anomaly detection (sudden change in call frequency/pattern per number)
- [ ] Flag anomalous numbers in the UI
- [ ] Tune sensitivity to avoid false-positive spam
- [ ] Document limitations honestly (this is a heuristic, not certain proof)

---