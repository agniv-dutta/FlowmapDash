import { useRef, useEffect, useState } from 'react';
import { Download, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';

interface ClickData {
  x: number;
  y: number;
  count: number;
  timestamp: string;
}

interface HeatmapCanvasProps {
  clickData: ClickData[];
  width?: number;
  height?: number;
}

export function HeatmapCanvas({ clickData, width = 800, height = 600 }: HeatmapCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [scale, setScale] = useState(1);
  const [panX, setPanX] = useState(0);
  const [panY, setPanY] = useState(0);
  const [hoveredClick, setHoveredClick] = useState<ClickData | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const maxClickCount = Math.max(...clickData.map(c => c.count), 1);
  const avgCount = clickData.reduce((sum, c) => sum + c.count, 0) / clickData.length || 0;

  const stats = {
    totalClicks: clickData.reduce((sum, c) => sum + c.count, 0),
    hotspots: clickData.filter(c => c.count > avgCount).length,
    coldspots: clickData.filter(c => c.count < avgCount / 2).length,
    avgClicksPerArea: Math.round(clickData.reduce((sum, c) => sum + c.count, 0) / clickData.length) || 0,
  };

  function getHeatColor(clickCount: number, maxClicks: number): { fill: string; stroke: string } {
    const intensity = clickCount / maxClicks;
    
    // Saturated teal gradient with high contrast
    if (intensity < 0.25) return { fill: 'rgba(100, 200, 200, 0.5)', stroke: 'rgba(30, 100, 100, 0.8)' };
    if (intensity < 0.5) return { fill: 'rgba(74, 180, 180, 0.7)', stroke: 'rgba(30, 100, 100, 0.9)' };
    if (intensity < 0.75) return { fill: 'rgba(42, 150, 150, 0.9)', stroke: 'rgba(20, 80, 80, 1)' };
    return { fill: 'rgba(30, 120, 120, 1)', stroke: 'rgba(10, 60, 60, 1)' };
  }

  const drawCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Apply transformations
    ctx.save();
    ctx.translate(panX, panY);
    ctx.scale(scale, scale);

    // Bright white background
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, width, height);

    // Draw subtle grid
    ctx.strokeStyle = '#E8E4E0';
    ctx.lineWidth = 1;
    const gridSize = 50;
    
    for (let x = 0; x <= width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    
    for (let y = 0; y <= height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Draw click dots with saturated colors and borders
    clickData.forEach(({ x, y, count }) => {
      const { fill, stroke } = getHeatColor(count, maxClickCount);
      ctx.fillStyle = fill;
      ctx.beginPath();
      ctx.arc(x, y, 8, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = stroke;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    });

    ctx.restore();
  };

  useEffect(() => {
    drawCanvas();
  }, [clickData, scale, panX, panY]);

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const mouseX = (e.clientX - rect.left - panX) / scale;
    const mouseY = (e.clientY - rect.top - panY) / scale;

    const hovered = clickData.find(click => {
      const dist = Math.hypot(click.x - mouseX, click.y - mouseY);
      return dist < 12;
    });

    setHoveredClick(hovered || null);

    if (isDragging) {
      setPanX(prev => prev + e.clientX - dragStart.x);
      setPanY(prev => prev + e.clientY - dragStart.y);
      setDragStart({ x: e.clientX, y: e.clientY });
    }
  };

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX, y: e.clientY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    setScale(prev => Math.max(0.5, Math.min(3, prev + (e.deltaY > 0 ? -0.1 : 0.1))));
  };

  const handleZoomIn = () => {
    setScale(prev => Math.min(3, prev + 0.2));
  };

  const handleZoomOut = () => {
    setScale(prev => Math.max(0.5, prev - 0.2));
  };

  const handleReset = () => {
    setScale(1);
    setPanX(0);
    setPanY(0);
  };

  const exportHeatmapData = () => {
    const csv = [
      ['X', 'Y', 'Clicks', 'Timestamp'],
      ...clickData.map(d => [d.x, d.y, d.count, d.timestamp]),
    ];
    const csvContent = csv.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `heatmap-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          <button
            onClick={handleZoomIn}
            className="flex items-center gap-2 px-3 py-2 text-sm border border-neutral-200 rounded-lg hover:bg-neutral-100"
          >
            <ZoomIn size={16} />
            Zoom In
          </button>
          <button
            onClick={handleZoomOut}
            className="flex items-center gap-2 px-3 py-2 text-sm border border-neutral-200 rounded-lg hover:bg-neutral-100"
          >
            <ZoomOut size={16} />
            Zoom Out
          </button>
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-3 py-2 text-sm border border-neutral-200 rounded-lg hover:bg-neutral-100"
          >
            <RotateCcw size={16} />
            Reset
          </button>
        </div>
        <button
          onClick={exportHeatmapData}
          className="flex items-center gap-2 px-3 py-2 text-sm border border-neutral-200 rounded-lg hover:bg-neutral-100"
        >
          <Download size={16} />
          Export CSV
        </button>
      </div>

      {/* Canvas */}
      <div className="relative border border-neutral-200 rounded-lg overflow-hidden">
        <canvas
          ref={canvasRef}
          width={width}
          height={height}
          className="cursor-crosshair"
          onMouseMove={handleMouseMove}
          onMouseDown={handleMouseDown}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onWheel={handleWheel}
        />
        
        {/* Tooltip */}
        {hoveredClick && (
          <div
            className="absolute bg-neutral-900 text-white text-xs rounded px-2 py-1 pointer-events-none"
            style={{
              left: `${hoveredClick.x * scale + panX + 10}px`,
              top: `${hoveredClick.y * scale + panY - 30}px`,
            }}
          >
            <div>Clicks: {hoveredClick.count}</div>
            <div>Time: {new Date(hoveredClick.timestamp).toLocaleTimeString()}</div>
          </div>
        )}

        {/* Scale indicator */}
        <div className="absolute bottom-2 right-2 bg-neutral-900 text-white text-xs rounded px-2 py-1">
          {Math.round(scale * 100)}%
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-neutral-50 border border-neutral-200 rounded-lg p-4">
          <div className="text-sm text-neutral-600">Total Clicks</div>
          <div className="text-2xl font-bold text-neutral-900">{stats.totalClicks}</div>
        </div>
        <div className="bg-neutral-50 border border-neutral-200 rounded-lg p-4">
          <div className="text-sm text-neutral-600">Hotspots</div>
          <div className="text-2xl font-bold text-accent-teal">{stats.hotspots}</div>
        </div>
        <div className="bg-neutral-50 border border-neutral-200 rounded-lg p-4">
          <div className="text-sm text-neutral-600">Coldspots</div>
          <div className="text-2xl font-bold text-neutral-400">{stats.coldspots}</div>
        </div>
        <div className="bg-neutral-50 border border-neutral-200 rounded-lg p-4">
          <div className="text-sm text-neutral-600">Avg/Area</div>
          <div className="text-2xl font-bold text-neutral-900">{stats.avgClicksPerArea}</div>
        </div>
      </div>
    </div>
  );
}
