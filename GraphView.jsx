import { useRef, useMemo, useCallback } from 'react'
import ForceGraph2D from 'react-force-graph-2d'

// A set of distinct colors, one per cluster number. If there are more
// clusters than colors, it just wraps around and reuses them.
const CLUSTER_COLORS = [
  "#3b82f6", "#ef4444", "#22c55e", "#f59e0b",
  "#a855f7", "#06b6d4", "#ec4899", "#84cc16",
]

function colorForCluster(clusterId) {
  return CLUSTER_COLORS[clusterId % CLUSTER_COLORS.length]
}

// This component takes the raw {nodes, edges} data from the backend and
// draws it as an interactive, force-directed graph (dots that naturally
// spread out and connect with lines, like a real network diagram).
export default function GraphView({ graphData, hubScores, highlightedPath, onNodeClick }) {
  const fgRef = useRef()

  // react-force-graph expects "links" instead of "edges", and expects
  // node/link objects in a specific shape, so we convert our API data
  // into that shape here.
  const data = useMemo(() => {
    if (!graphData) return { nodes: [], links: [] }

    return {
      nodes: graphData.nodes.map((n) => ({
        id: n.id,
        cluster: n.cluster,
        hubScore: hubScores?.[n.id] || 0,
      })),
      links: graphData.edges.map((e) => ({
        source: e.source,
        target: e.target,
        weight: e.weight,
      })),
    }
  }, [graphData, hubScores])

  // Figures out if a node is part of the currently highlighted shortest
  // path (so we can draw it differently, e.g. bright yellow ring).
  const isHighlighted = useCallback(
    (nodeId) => highlightedPath?.includes(nodeId),
    [highlightedPath]
  )

  // Draws each node manually as a circle, this gives us full control
  // over size (bigger = more "important" per hub score) and color
  // (grouped by cluster).
  const paintNode = useCallback((node, ctx) => {
    const baseSize = 4
    const sizeBoost = node.hubScore * 12 // important nodes get bigger
    const radius = baseSize + sizeBoost

    ctx.beginPath()
    ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI)
    ctx.fillStyle = colorForCluster(node.cluster)
    ctx.fill()

    if (isHighlighted(node.id)) {
      ctx.strokeStyle = "#facc15"
      ctx.lineWidth = 2.5
      ctx.stroke()
    }
  }, [isHighlighted])

  if (!graphData) {
    return (
      <div className="graph-placeholder">
        Upload a call records file to see the network.
      </div>
    )
  }

  return (
    <ForceGraph2D
      ref={fgRef}
      graphData={data}
      nodeId="id"
      nodeCanvasObject={paintNode}
      nodePointerAreaPaint={(node, color, ctx) => {
        ctx.beginPath()
        ctx.arc(node.x, node.y, 8, 0, 2 * Math.PI)
        ctx.fillStyle = color
        ctx.fill()
      }}
      linkWidth={(link) => Math.min(link.weight / 3, 4)}
      linkColor={(link) => {
        const bothHighlighted =
          isHighlighted(link.source.id || link.source) &&
          isHighlighted(link.target.id || link.target)
        return bothHighlighted ? "#facc15" : "rgba(150,150,150,0.4)"
      }}
      onNodeClick={(node) => onNodeClick?.(node.id)}
      cooldownTicks={100}
    />
  )
}
