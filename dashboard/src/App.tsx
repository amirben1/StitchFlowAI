import { useState, useRef, useMemo } from 'react'
import { motion, useReducedMotion } from 'motion/react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Environment } from '@react-three/drei'
import { ArrowRight } from '@phosphor-icons/react'
import agentData from './data.json'
import * as THREE from 'three'

// --- 3D Silk Fabric Component ---
function ChromeFabric() {
  const meshRef = useRef<THREE.Mesh>(null)
  
  // Create a high-res plane for the cloth simulation
  const geometry = useMemo(() => new THREE.PlaneGeometry(25, 25, 128, 128), [])
  const positions = geometry.attributes.position
  const initialPositions = useMemo(() => {
    const arr = new Float32Array(positions.count * 3)
    for (let i = 0; i < positions.count * 3; i++) arr[i] = positions.array[i]
    return arr
  }, [positions])

  useFrame((state) => {
    if (!meshRef.current) return
    const time = state.clock.getElapsedTime()
    const pos = meshRef.current.geometry.attributes.position

    // Gentle flowing cloth math
    for (let i = 0; i < pos.count; i++) {
      const ix = i * 3
      const iy = i * 3 + 1
      const iz = i * 3 + 2
      
      const x = initialPositions[ix]
      const y = initialPositions[iy]
      
      // Complex sine waves for organic fabric folds
      const waveX1 = Math.sin(x * 0.2 + time * 0.3) * 0.5
      const waveY1 = Math.sin(y * 0.3 + time * 0.2) * 0.5
      const waveXY = Math.sin((x + y) * 0.1 + time * 0.1) * 1.5
      
      pos.array[iz] = waveX1 + waveY1 + waveXY
    }
    
    pos.needsUpdate = true
    meshRef.current.geometry.computeVertexNormals()
  })

  return (
    <mesh ref={meshRef} rotation={[-Math.PI / 3, 0, 0]} position={[0, -2, -5]}>
      <primitive object={geometry} attach="geometry" />
      <meshStandardMaterial 
        color="#a1a1aa" 
        roughness={0.2} 
        metalness={0.9} 
        envMapIntensity={1.5}
        side={THREE.DoubleSide}
      />
    </mesh>
  )
}

function Scene() {
  const reduce = useReducedMotion()
  if (reduce) return null

  return (
    <div className="fixed inset-0 z-0 pointer-events-none opacity-[0.15]">
      <Canvas camera={{ position: [0, 5, 10], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 20, 10]} intensity={2} />
        <pointLight position={[-10, -10, -10]} intensity={1} color="#ffffff" />
        <Environment preset="studio" />
        <ChromeFabric />
      </Canvas>
      <div className="absolute inset-0 bg-gradient-to-t from-[#050505] via-transparent to-[#050505]" />
    </div>
  )
}

// --- Minimalist UI Components ---
function Reveal({ children, delay = 0, className = "" }: { children: React.ReactNode, delay?: number, className?: string }) {
  const reduce = useReducedMotion()
  return (
    <motion.div
      className={className}
      initial={reduce ? false : { opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay, ease: [0.2, 1, 0.4, 1] }}
    >
      {children}
    </motion.div>
  )
}

function StatCard({ label, value, subtext }: { label: string, value: string | number, subtext?: string }) {
  return (
    <div className="flex flex-col border-b border-zinc-800 pb-6 mb-6 last:border-0 last:mb-0 last:pb-0">
      <span className="text-[10px] tracking-[0.2em] font-mono text-zinc-500 uppercase mb-4">{label}</span>
      <div className="text-4xl lg:text-5xl tracking-tighter font-light text-zinc-100">{value}</div>
      {subtext && <div className="text-xs text-zinc-500 mt-2">{subtext}</div>}
    </div>
  )
}

// --- Main App ---
export default function App() {
  const [approvedIds, setApprovedIds] = useState<Set<string>>(new Set())

  const toggleApproval = (id: string) => {
    setApprovedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const handleExecute = () => {
    alert(`Executing PO for ${approvedIds.size} items. Syncing to ERP...`)
  }

  return (
    <div className="min-h-[100dvh] bg-[#050505] text-zinc-100 font-sans selection:bg-zinc-100 selection:text-black relative">
      
      {/* 3D Fabric Background */}
      <Scene />

      {/* Foreground UI */}
      <div className="relative z-10 flex flex-col min-h-[100dvh]">
        
        {/* Minimal Navigation */}
        <nav className="p-8 flex items-center justify-between mix-blend-difference">
          <div className="text-xs font-mono tracking-widest uppercase">STITCHFLOW // LOGISTICS</div>
          <div className="flex items-center gap-2 text-xs font-mono text-zinc-500 uppercase tracking-widest">
            <span>SYNC: {new Date(agentData.last_updated).toISOString().split('T')[1].slice(0, 5)}</span>
          </div>
        </nav>

        <main className="flex-1 max-w-[1600px] w-full mx-auto px-8 lg:px-16 py-12 lg:py-24 grid grid-cols-1 lg:grid-cols-12 gap-16 lg:gap-24">
          
          {/* Left Column: Editorial Hero & Stats */}
          <div className="lg:col-span-5 flex flex-col justify-between">
            <div className="mb-24">
              <Reveal>
                <h1 className="text-6xl md:text-8xl tracking-tighter font-light leading-[0.9] mb-8 text-zinc-100">
                  Supply<br/>Chain<br/><span className="text-zinc-600">Audit.</span>
                </h1>
              </Reveal>
              <Reveal delay={0.1}>
                <p className="text-zinc-400 max-w-sm leading-relaxed text-sm">
                  Autonomous procurement analysis. 
                  Evaluating local inventory velocity against global trend indices. 
                  Capital and spatial limits strictly enforced.
                </p>
              </Reveal>
            </div>

            <Reveal delay={0.2}>
              <div className="border border-zinc-800 p-8 bg-[#0a0a0a]/80 backdrop-blur-md">
                <StatCard 
                  label="Available Capital" 
                  value={`${(agentData.budget_remaining_tnd / 1000).toFixed(1)}k`} 
                  subtext="TND Reserve"
                />
                <StatCard 
                  label="Warehouse Volume" 
                  value={`${agentData.capacity_remaining_m3}`} 
                  subtext="Cubic Meters Remaining"
                />
              </div>
            </Reveal>
          </div>

          {/* Right Column: High-Density List */}
          <div className="lg:col-span-7 pt-4">
            <Reveal delay={0.3}>
              <div className="flex items-center justify-between mb-8 pb-4 border-b border-zinc-800">
                <h2 className="text-[10px] font-mono tracking-[0.2em] text-zinc-500 uppercase">Recommended Operations</h2>
                <span className="text-[10px] font-mono tracking-[0.2em] text-zinc-500">{agentData.recommendations.length} ITEMS</span>
              </div>
            </Reveal>

            <div className="flex flex-col gap-px bg-zinc-800 border border-zinc-800">
              {agentData.recommendations.map((rec, index) => {
                const isApproved = approvedIds.has(rec.id);
                return (
                  <Reveal key={rec.id} delay={0.4 + (index * 0.05)}>
                    <div 
                      className={`group relative bg-[#050505] p-6 lg:p-8 transition-all duration-300 flex flex-col md:flex-row gap-8 justify-between items-start md:items-center
                        ${isApproved ? 'bg-zinc-100 text-[#050505]' : 'hover:bg-[#0a0a0a]'}`}
                    >
                      {/* Item Details */}
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          <span className={`text-[10px] font-mono tracking-widest ${isApproved ? 'text-black' : 'text-zinc-500'} uppercase`}>
                            {rec.id}
                          </span>
                          <span className={`px-2 py-0.5 text-[9px] font-mono tracking-widest uppercase border 
                            ${rec.action === 'PROCURE' 
                              ? (isApproved ? 'border-black text-black' : 'border-zinc-700 text-zinc-300') 
                              : (isApproved ? 'border-black text-black' : 'border-zinc-700 text-zinc-500')}`}
                          >
                            {rec.action}
                          </span>
                        </div>
                        <h3 className="text-xl md:text-2xl font-light tracking-tight mb-3 pr-4">{rec.name}</h3>
                        <p className={`text-xs leading-relaxed max-w-md ${isApproved ? 'text-zinc-800' : 'text-zinc-500'}`}>
                          {rec.reasoning}
                        </p>
                      </div>

                      {/* Math & Button */}
                      <div className="flex flex-col md:items-end gap-6 shrink-0 md:w-48">
                        <div className="grid grid-cols-2 md:text-right gap-x-8 gap-y-2">
                          <span className={`text-[9px] font-mono tracking-widest uppercase ${isApproved ? 'text-zinc-600' : 'text-zinc-600'}`}>QTY</span>
                          <span className={`text-xs font-mono ${isApproved ? 'text-black' : 'text-zinc-300'}`}>{rec.quantity || '-'}</span>
                          
                          <span className={`text-[9px] font-mono tracking-widest uppercase ${isApproved ? 'text-zinc-600' : 'text-zinc-600'}`}>COST</span>
                          <span className={`text-xs font-mono ${isApproved ? 'text-black' : 'text-zinc-300'}`}>{rec.cost_tnd ? `${rec.cost_tnd.toLocaleString()} TND` : '-'}</span>
                        </div>

                        <button 
                          onClick={() => toggleApproval(rec.id)}
                          className={`w-full md:w-auto px-6 py-3 text-[10px] font-mono tracking-[0.2em] uppercase transition-all duration-300 border
                            ${isApproved 
                              ? 'bg-black text-white border-black' 
                              : 'bg-transparent text-zinc-100 border-zinc-700 hover:border-zinc-300 hover:bg-zinc-100 hover:text-black'}`}
                        >
                          {isApproved ? 'Approved' : 'Authorize'}
                        </button>
                      </div>
                    </div>
                  </Reveal>
                )
              })}
            </div>
          </div>
        </main>

        {/* Floating Action Bar */}
        {approvedIds.size > 0 && (
          <motion.div 
            initial={{ y: 100 }}
            animate={{ y: 0 }}
            className="sticky bottom-0 border-t border-zinc-800 bg-[#050505] p-6 lg:p-8 flex items-center justify-between mix-blend-difference"
          >
            <div className="font-mono text-xs tracking-widest text-zinc-500 uppercase">
              <span className="text-zinc-100">{approvedIds.size}</span> Orders Ready
            </div>
            <button 
              onClick={handleExecute}
              className="flex items-center gap-3 bg-zinc-100 text-[#050505] px-8 py-4 text-xs font-mono tracking-[0.2em] font-bold hover:bg-white active:scale-95 transition-transform"
            >
              EXECUTE TO ERP
              <ArrowRight weight="bold" />
            </button>
          </motion.div>
        )}
      </div>
    </div>
  )
}
