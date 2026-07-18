import { useState, useRef } from 'react'
import { motion, useReducedMotion } from 'motion/react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Environment, Float, MeshDistortMaterial, Stars } from '@react-three/drei'
import { CheckCircle, Warning, Package, CurrencyDollar, TrendUp, Lightning } from '@phosphor-icons/react'
import agentData from './data.json'
import * as THREE from 'three'

// --- 3D Background Component ---
function AbstractNodes() {
  const group = useRef<THREE.Group>(null)

  useFrame((state) => {
    if (group.current) {
      group.current.rotation.y = state.clock.getElapsedTime() * 0.05
      group.current.rotation.z = state.clock.getElapsedTime() * 0.02
    }
  })

  return (
    <group ref={group}>
      <Float speed={1.5} rotationIntensity={0.5} floatIntensity={1}>
        <mesh position={[0, 0, -5]}>
          <torusKnotGeometry args={[3, 0.8, 128, 32]} />
          <MeshDistortMaterial
            color="#0284c7"
            emissive="#0ea5e9"
            emissiveIntensity={0.5}
            envMapIntensity={2}
            clearcoat={1}
            clearcoatRoughness={0.1}
            metalness={0.9}
            roughness={0.1}
            distort={0.4}
            speed={2}
          />
        </mesh>
      </Float>
      {/* Background glowing particles/stars */}
      <Stars radius={50} depth={50} count={3000} factor={3} saturation={1} fade speed={1} />
    </group>
  )
}

function Scene() {
  const reduce = useReducedMotion()
  if (reduce) return null // No 3D for reduced motion

  return (
    <div className="fixed inset-0 z-0 pointer-events-none opacity-40">
      <Canvas camera={{ position: [0, 0, 10], fov: 45 }}>
        <ambientLight intensity={0.2} />
        <directionalLight position={[10, 10, 5]} intensity={1} color="#0284c7" />
        <pointLight position={[-10, -10, -5]} intensity={0.5} color="#0ea5e9" />
        <Environment preset="city" />
        <AbstractNodes />
      </Canvas>
      {/* Optional: Add the stunning generated image as an overlay to blend with 3D */}
      <div 
        className="absolute inset-0 bg-[url('/hero-bg.jpg')] bg-cover bg-center opacity-30 mix-blend-screen"
        style={{ filter: 'contrast(1.2)' }}
      />
      <div className="absolute inset-0 bg-gradient-to-b from-zinc-950/20 via-zinc-950/80 to-zinc-950" />
    </div>
  )
}

// --- UI Components ---
function StaggerReveal({ children, delay = 0, className = "" }: { children: React.ReactNode, delay?: number, className?: string }) {
  const reduce = useReducedMotion()
  return (
    <motion.div
      className={className}
      initial={reduce ? false : { opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  )
}

function PremiumMetric({ label, value, subtext, icon: Icon }: { label: string, value: string | number, subtext?: string, icon: any }) {
  return (
    <div className="relative group overflow-hidden border border-white/5 bg-zinc-900/30 backdrop-blur-xl p-8 rounded-none h-full">
      <div className="absolute inset-0 bg-gradient-to-b from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
      <div className="relative z-10 flex flex-col justify-between h-full gap-8">
        <div className="flex items-start justify-between">
          <span className="text-xs tracking-[0.2em] text-zinc-400 font-mono uppercase">{label}</span>
          <div className="p-2 bg-black/40 rounded-full border border-white/5">
            <Icon className="w-4 h-4 text-accent" />
          </div>
        </div>
        <div>
          <div className="text-5xl font-light tracking-tighter text-white mb-2">{value}</div>
          {subtext && <div className="text-sm font-mono text-emerald-400">{subtext}</div>}
        </div>
      </div>
    </div>
  )
}

function ActionBadge({ action }: { action: string }) {
  if (action === "PROCURE") {
    return (
      <span className="inline-flex items-center gap-1.5 px-3 py-1 text-[10px] font-mono tracking-widest text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-full backdrop-blur-md">
        <CheckCircle weight="fill" /> PROCURE
      </span>
    )
  }
  return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1 text-[10px] font-mono tracking-widest text-amber-400 bg-amber-500/10 border border-amber-500/20 rounded-full backdrop-blur-md">
      <Warning weight="fill" /> CLEARANCE
    </span>
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
    <div className="min-h-[100dvh] bg-zinc-950 text-zinc-100 selection:bg-accent selection:text-white relative overflow-hidden font-sans">
      
      {/* 3D Canvas Background */}
      <Scene />

      {/* Foreground UI */}
      <div className="relative z-10">
        
        {/* Navigation */}
        <nav className="h-20 border-b border-white/5 flex items-center justify-between px-6 lg:px-12 backdrop-blur-sm bg-zinc-950/50 sticky top-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent/20 rounded flex items-center justify-center border border-accent/30 shadow-[0_0_15px_rgba(2,132,199,0.3)]">
              <Lightning weight="bold" className="text-accent w-5 h-5" />
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] tracking-[0.2em] font-mono text-zinc-500 uppercase">System Status</span>
              <span className="text-sm tracking-widest font-medium">STITCHFLOW // OS</span>
            </div>
          </div>
          <div className="text-[10px] tracking-[0.2em] font-mono text-zinc-500 uppercase flex items-center gap-2">
            <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(16,185,129,0.5)]" />
            LIVE SYNC • {new Date(agentData.last_updated).toISOString().split('T')[1].slice(0, 8)}
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-6 lg:px-12 pt-24 pb-40">
          
          {/* Hero Section */}
          <section className="mb-32">
            <StaggerReveal>
              <div className="inline-block px-3 py-1 mb-8 border border-white/10 rounded-full backdrop-blur-md bg-white/5">
                <span className="text-[10px] tracking-[0.2em] font-mono text-zinc-400 uppercase">Agent Intelligence Report Generated</span>
              </div>
            </StaggerReveal>
            <StaggerReveal delay={0.1}>
              <h1 className="text-5xl md:text-7xl tracking-tighter font-light leading-[1.1] mb-8 max-w-4xl bg-gradient-to-br from-white via-zinc-200 to-zinc-600 bg-clip-text text-transparent">
                Procurement optimized. <br />
                Awaiting human override.
              </h1>
            </StaggerReveal>
            <StaggerReveal delay={0.2}>
              <p className="text-zinc-400 max-w-[65ch] leading-relaxed text-lg font-light border-l border-accent/50 pl-6 ml-1">
                The MAS orchestration team has computed optimal supply-chain flows based on raw ERP data and live web signals. Physical warehouse constraints and active capital reserves have been strictly enforced.
              </p>
            </StaggerReveal>
          </section>

          {/* Global Metrics (Bento Grid) */}
          <section className="grid grid-cols-1 md:grid-cols-2 gap-px bg-white/5 p-px mb-24 backdrop-blur-xl rounded-2xl overflow-hidden shadow-2xl">
            <StaggerReveal delay={0.3} className="h-full">
              <PremiumMetric 
                label="Available Capital Reserve" 
                value={`${(agentData.budget_remaining_tnd / 1000).toFixed(1)}k TND`} 
                subtext="Sufficient for Q3 Procurement"
                icon={CurrencyDollar} 
              />
            </StaggerReveal>
            <StaggerReveal delay={0.4} className="h-full">
              <PremiumMetric 
                label="Warehouse Spatial Capacity" 
                value={`${agentData.capacity_remaining_m3} m³`} 
                subtext="64% Utilized"
                icon={Package} 
              />
            </StaggerReveal>
          </section>

          {/* Recommendations List */}
          <section>
            <StaggerReveal delay={0.5}>
              <div className="flex items-center justify-between mb-8 pb-4">
                <h2 className="text-xs font-mono tracking-[0.2em] text-zinc-500 uppercase">Recommended Operations</h2>
                <div className="h-px bg-gradient-to-r from-zinc-800 to-transparent flex-1 ml-6" />
              </div>
            </StaggerReveal>

            <div className="grid gap-4">
              {agentData.recommendations.map((rec, index) => {
                const isApproved = approvedIds.has(rec.id);
                return (
                  <StaggerReveal key={rec.id} delay={0.6 + (index * 0.05)}>
                    <div 
                      className={`group relative overflow-hidden backdrop-blur-xl border transition-all duration-500 flex flex-col lg:flex-row lg:items-center justify-between gap-8 p-6 lg:p-8
                        ${isApproved 
                          ? 'border-accent/50 bg-accent/[0.03] shadow-[0_0_30px_rgba(2,132,199,0.1)]' 
                          : 'border-white/5 bg-zinc-900/30 hover:bg-zinc-900/50 hover:border-white/10'}`}
                    >
                      {/* Left block: Identity & Reasoning */}
                      <div className="flex-1 space-y-5">
                        <div className="flex items-center gap-4">
                          <ActionBadge action={rec.action} />
                          <span className="font-mono text-[10px] tracking-widest text-zinc-500 uppercase">{rec.id}</span>
                        </div>
                        
                        <div>
                          <h3 className="text-2xl font-light tracking-tight text-zinc-100 mb-3">{rec.name}</h3>
                          <p className="text-zinc-400 text-sm leading-relaxed max-w-[80ch] flex items-start gap-3">
                            <TrendUp className="w-4 h-4 mt-0.5 text-accent shrink-0" />
                            {rec.reasoning}
                          </p>
                        </div>
                      </div>

                      {/* Right block: Math & Action */}
                      <div className="flex flex-col lg:items-end gap-8 shrink-0 lg:w-72">
                        <div className="grid grid-cols-2 lg:text-right gap-x-12 gap-y-2">
                          <span className="text-[10px] font-mono tracking-widest text-zinc-500 uppercase">QTY</span>
                          <span className="text-sm font-mono text-zinc-300">{rec.quantity > 0 ? rec.quantity.toLocaleString() : '-'}</span>
                          
                          <span className="text-[10px] font-mono tracking-widest text-zinc-500 uppercase">COST</span>
                          <span className="text-sm font-mono text-zinc-300">{rec.cost_tnd > 0 ? `${rec.cost_tnd.toLocaleString()} TND` : '-'}</span>
                          
                          <span className="text-[10px] font-mono tracking-widest text-zinc-500 uppercase">VOL</span>
                          <span className="text-sm font-mono text-zinc-300">{rec.volume_m3 > 0 ? `${rec.volume_m3} m³` : '-'}</span>
                        </div>

                        <button 
                          onClick={() => toggleApproval(rec.id)}
                          className={`relative overflow-hidden w-full lg:w-auto px-8 py-3 text-xs font-mono tracking-[0.2em] transition-all duration-300 border backdrop-blur-md
                            ${isApproved 
                              ? 'bg-accent/10 text-accent border-accent/50 hover:bg-accent/20' 
                              : 'bg-white/5 text-zinc-300 border-white/10 hover:border-white/30 hover:bg-white/10 hover:text-white'}`}
                        >
                          {isApproved ? 'AUTHORIZED' : 'AUTHORIZE_OS'}
                        </button>
                      </div>
                    </div>
                  </StaggerReveal>
                )
              })}
            </div>
          </section>
        </main>

        {/* Floating Action Bar */}
        {approvedIds.size > 0 && (
          <motion.div 
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="fixed bottom-0 left-0 right-0 border-t border-accent/30 bg-zinc-950/80 backdrop-blur-2xl z-50 p-6 shadow-[0_-20px_50px_rgba(2,132,199,0.1)]"
          >
            <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className="w-2 h-2 bg-accent rounded-full animate-pulse" />
                <div className="font-mono text-xs tracking-widest text-zinc-400 uppercase">
                  <span className="text-accent">{approvedIds.size}</span> Items queued for PO generation
                </div>
              </div>
              <button 
                onClick={handleExecute}
                className="bg-zinc-100 text-zinc-950 px-8 py-3 text-xs font-mono tracking-[0.2em] font-bold hover:bg-white active:scale-95 transition-all shadow-[0_0_20px_rgba(255,255,255,0.2)]"
              >
                EXECUTE ORDER PO_
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}
