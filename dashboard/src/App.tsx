import { useState, useRef, useMemo } from 'react'
import { motion, useReducedMotion, useScroll } from 'motion/react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Environment } from '@react-three/drei'
import { EffectComposer, Bloom, Vignette, Noise } from '@react-three/postprocessing'
import { ArrowRight, Cpu, TrendUp, Crosshair } from '@phosphor-icons/react'
import agentData from './data.json'
import * as THREE from 'three'

// --- 3D Scrollable Cinematic Fabric ---
function ChromeFabric({ scrollYProgress }: { scrollYProgress: any }) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  const geometry = useMemo(() => new THREE.PlaneGeometry(35, 35, 150, 150), [])
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
    
    // Get current scroll (0 to 1)
    const scroll = scrollYProgress.get()

    // 3D Effects tied to scroll
    meshRef.current.rotation.x = -Math.PI / 3 + scroll * 0.5
    meshRef.current.position.y = -2 + scroll * 3
    meshRef.current.position.z = -5 - scroll * 2

    // Flowing math
    for (let i = 0; i < pos.count; i++) {
      const ix = i * 3, iy = i * 3 + 1, iz = i * 3 + 2
      const x = initialPositions[ix], y = initialPositions[iy]
      
      const waveX1 = Math.sin(x * 0.2 + time * 0.3) * 0.5
      const waveY1 = Math.sin(y * 0.3 + time * 0.2) * 0.5
      const waveXY = Math.sin((x + y) * 0.1 + time * 0.1) * (1.5 + scroll * 2) // Intensity increases on scroll
      
      pos.array[iz] = waveX1 + waveY1 + waveXY
    }
    
    pos.needsUpdate = true
    meshRef.current.geometry.computeVertexNormals()
  })

  return (
    <mesh ref={meshRef}>
      <primitive object={geometry} attach="geometry" />
      <meshStandardMaterial 
        color="#a1a1aa" 
        roughness={0.15} 
        metalness={1.0} 
        envMapIntensity={2.5}
        side={THREE.DoubleSide}
      />
    </mesh>
  )
}

function Scene({ scrollYProgress }: { scrollYProgress: any }) {
  const reduce = useReducedMotion()
  if (reduce) return null

  return (
    <div className="fixed inset-0 z-0 pointer-events-none">
      <Canvas camera={{ position: [0, 5, 10], fov: 45 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 20, 10]} intensity={2} color="#ffffff" />
        <pointLight position={[-10, -10, -10]} intensity={1} color="#ffffff" />
        <Environment preset="studio" />
        <ChromeFabric scrollYProgress={scrollYProgress} />
        
        {/* Beauty Effects */}
        <EffectComposer>
          <Bloom luminanceThreshold={0.5} mipmapBlur intensity={0.8} />
          <Noise opacity={0.05} />
          <Vignette eskil={false} offset={0.1} darkness={1.1} />
        </EffectComposer>
      </Canvas>
      <div className="absolute inset-0 bg-gradient-to-b from-[#050505]/80 via-transparent to-[#050505] mix-blend-multiply" />
    </div>
  )
}

// --- Minimalist UI Components ---
function Reveal({ children, delay = 0, className = "" }: { children: React.ReactNode, delay?: number, className?: string }) {
  const reduce = useReducedMotion()
  return (
    <motion.div
      className={className}
      initial={reduce ? false : { opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.8, delay, ease: [0.2, 1, 0.4, 1] }}
    >
      {children}
    </motion.div>
  )
}

// --- Main App ---
export default function App() {
  const { scrollYProgress } = useScroll()
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

  const agentIcons = [Cpu, TrendUp, Crosshair]

  return (
    <div className="min-h-[100dvh] bg-[#050505] text-zinc-100 font-sans selection:bg-zinc-100 selection:text-black relative">
      
      {/* 3D Fabric Background tied to scroll */}
      <Scene scrollYProgress={scrollYProgress} />

      {/* Foreground UI */}
      <div className="relative z-10 flex flex-col min-h-[100dvh]">
        
        {/* Navigation */}
        <nav className="px-8 py-6 flex items-center justify-between bg-[#050505]/90 backdrop-blur-xl border-b border-zinc-800 sticky top-0 z-50">
          <div className="text-sm font-mono tracking-widest font-bold text-white uppercase">STITCHFLOW // LOGISTICS</div>
          <div className="flex items-center gap-2 text-xs font-mono font-bold text-zinc-400 uppercase tracking-widest">
            <span>SYNC: {new Date(agentData.last_updated).toISOString().split('T')[1].slice(0, 5)}</span>
          </div>
        </nav>

        <main className="flex-1 max-w-[1400px] w-full mx-auto px-6 lg:px-16 pt-24 pb-48">
          
          {/* Hero Section */}
          <div className="min-h-[80vh] flex flex-col justify-center mb-32">
            <Reveal>
              <h1 className="text-7xl md:text-[9rem] tracking-tighter font-light leading-[0.85] mb-12 text-zinc-100 mix-blend-difference">
                Supply<br/>Chain<br/><span className="text-zinc-600">Audit.</span>
              </h1>
            </Reveal>
            <Reveal delay={0.2}>
              <div className="grid grid-cols-2 gap-12 max-w-2xl border-l border-zinc-800 pl-8">
                <div>
                  <div className="text-[10px] font-mono tracking-[0.2em] text-zinc-500 uppercase mb-2">Capital Reserve</div>
                  <div className="text-4xl font-light">{(agentData.budget_remaining_tnd / 1000).toFixed(1)}k <span className="text-sm text-zinc-500">TND</span></div>
                </div>
                <div>
                  <div className="text-[10px] font-mono tracking-[0.2em] text-zinc-500 uppercase mb-2">Warehouse Vol.</div>
                  <div className="text-4xl font-light">{agentData.capacity_remaining_m3} <span className="text-sm text-zinc-500">m³</span></div>
                </div>
              </div>
            </Reveal>
          </div>

          {/* AI Agents Work Showcase */}
          <div className="mb-48">
            <Reveal>
              <h2 className="text-[10px] font-mono tracking-[0.2em] text-zinc-500 uppercase mb-12 border-b border-zinc-800 pb-4">
                Multi-Agent Intelligence Network
              </h2>
            </Reveal>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {agentData.agent_summaries.map((agent, i) => {
                const Icon = agentIcons[i]
                return (
                  <Reveal key={i} delay={i * 0.15}>
                    <div className="border border-zinc-800 p-8 bg-[#050505]/50 backdrop-blur-md hover:bg-zinc-900 transition-colors duration-500 h-full flex flex-col">
                      <Icon className="w-8 h-8 text-zinc-100 mb-8" weight="light" />
                      <h3 className="text-xl font-light tracking-tight mb-2">{agent.agent_name}</h3>
                      <p className="text-[10px] font-mono tracking-[0.1em] text-zinc-500 uppercase mb-6">{agent.role_description}</p>
                      <p className="text-sm text-zinc-400 leading-relaxed mt-auto border-t border-zinc-800 pt-6">
                        {agent.findings_summary}
                      </p>
                    </div>
                  </Reveal>
                )
              })}
            </div>
          </div>

          {/* Recommendations List */}
          <div>
            <Reveal>
              <div className="flex items-center justify-between mb-12 pb-4 border-b border-zinc-800">
                <h2 className="text-[10px] font-mono tracking-[0.2em] text-zinc-500 uppercase">Computed Procurement Orders</h2>
                <span className="text-[10px] font-mono tracking-[0.2em] text-zinc-500">{agentData.recommendations.length} ITEMS</span>
              </div>
            </Reveal>

            <div className="flex flex-col gap-2">
              {agentData.recommendations.map((rec) => {
                const isApproved = approvedIds.has(rec.id);
                return (
                  <Reveal key={rec.id} delay={0.1}>
                    <div 
                      className={`group relative border p-6 lg:p-8 transition-all duration-500 flex flex-col md:flex-row gap-8 justify-between items-start md:items-center
                        ${isApproved 
                          ? 'border-zinc-100 bg-zinc-100 text-[#050505] shadow-[0_0_50px_rgba(255,255,255,0.1)]' 
                          : 'border-zinc-800 bg-[#050505]/80 hover:bg-[#0a0a0a] backdrop-blur-md'}`}
                    >
                      {/* Item Details */}
                      <div className="flex-1">
                        <div className="flex items-center gap-4 mb-4">
                          <span className={`text-[10px] font-mono tracking-widest ${isApproved ? 'text-black' : 'text-zinc-500'} uppercase`}>
                            {rec.id}
                          </span>
                          <span className={`px-3 py-1 text-[9px] font-mono tracking-widest uppercase border 
                            ${rec.action === 'PROCURE' 
                              ? (isApproved ? 'border-black text-black' : 'border-zinc-700 text-zinc-300') 
                              : (isApproved ? 'border-black text-black' : 'border-zinc-700 text-zinc-500')}`}
                          >
                            {rec.action}
                          </span>
                        </div>
                        <h3 className="text-2xl md:text-3xl font-light tracking-tight mb-4 pr-4">{rec.name}</h3>
                        <p className={`text-sm leading-relaxed max-w-2xl ${isApproved ? 'text-zinc-800' : 'text-zinc-400'}`}>
                          {rec.reasoning}
                        </p>
                      </div>

                      {/* Math & Button */}
                      <div className="flex flex-col md:items-end gap-8 shrink-0 md:w-56">
                        <div className="grid grid-cols-2 md:text-right gap-x-8 gap-y-3 w-full">
                          <span className={`text-[10px] font-mono tracking-widest uppercase ${isApproved ? 'text-zinc-600' : 'text-zinc-600'}`}>QTY</span>
                          <span className={`text-sm font-mono ${isApproved ? 'text-black' : 'text-zinc-300'}`}>{rec.quantity || '-'}</span>
                          
                          <span className={`text-[10px] font-mono tracking-widest uppercase ${isApproved ? 'text-zinc-600' : 'text-zinc-600'}`}>COST</span>
                          <span className={`text-sm font-mono ${isApproved ? 'text-black' : 'text-zinc-300'}`}>{rec.cost_tnd ? `${rec.cost_tnd.toLocaleString()} TND` : '-'}</span>
                        </div>

                        <button 
                          onClick={() => toggleApproval(rec.id)}
                          className={`w-full px-8 py-4 text-[10px] font-mono tracking-[0.2em] uppercase transition-all duration-300 border
                            ${isApproved 
                              ? 'bg-black text-white border-black hover:bg-zinc-900' 
                              : 'bg-transparent text-zinc-100 border-zinc-600 hover:border-zinc-100 hover:bg-zinc-100 hover:text-black'}`}
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
            className="fixed bottom-0 left-0 right-0 border-t border-zinc-800 bg-[#050505]/90 backdrop-blur-xl p-6 lg:p-8 flex items-center justify-between z-50"
          >
            <div className="font-mono text-xs tracking-widest text-zinc-500 uppercase pl-4 lg:pl-12">
              <span className="text-zinc-100">{approvedIds.size}</span> Orders Ready
            </div>
            <button 
              onClick={handleExecute}
              className="flex items-center gap-3 bg-zinc-100 text-[#050505] px-10 py-4 text-xs font-mono tracking-[0.2em] font-bold hover:bg-white active:scale-95 transition-transform mr-4 lg:mr-12"
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
