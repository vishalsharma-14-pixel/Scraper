export default function SparklineChart({
  values,
  width = 320,
  height = 80,
}: {
  values: number[]
  width?: number
  height?: number
}) {
  if (values.length < 2) {
    return <p className="text-sm text-gray-400">Not enough data points yet.</p>
  }

  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1
  const padding = 6

  const points = values.map((value, index) => {
    const x = padding + (index / (values.length - 1)) * (width - padding * 2)
    const y = height - padding - ((value - min) / range) * (height - padding * 2)
    return `${x.toFixed(1)},${y.toFixed(1)}`
  })

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="text-blue-500">
      <polyline points={points.join(' ')} fill="none" stroke="currentColor" strokeWidth={2} />
      {points.map((point, index) => {
        const [x, y] = point.split(',')
        return <circle key={index} cx={x} cy={y} r={2.5} fill="currentColor" />
      })}
    </svg>
  )
}
