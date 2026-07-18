import { useState } from 'react'
import { motion, useReducedMotion } from 'motion/react'
import { CheckCircle, Warning, Package, CurrencyDollar, TrendUp } from '@phosphor-icons/react'
import agentData from './data.json'

// --- Components ---

function StaggerReveal({ children, delay = 0 }: { children: React.ReactNode, delay?: number }) {
  const reduce = useReducedMotion()
  return (
    <motion.div
      initial={reduce ? false : { opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  )
}

function Metric({ label, value, icon: Icon }: { label: string, value: string | number, icon: any }) {
  return (
    <div className="border border-zinc-800 bg-zinc-900/50 p-6 flex flex-col justify-between h-full">
      <div className="flex items-center justify-between mb-8">
        <span className="text-sm tracking-wide text-zinc-400 font-mono uppercase">{label}</span>
        <Icon className="w-5 h-5 text-zinc-500" />
      </div>
      <div className="text-4xl tracking-tighter">{value}</div>
    </div>
  )
}

function ActionBadge({ action }: { action: string }) {
  if (action === "PROCURE") {
    return (
      <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-mono font-medium text-emerald-400 bg-emerald-400/10 border border-emerald-400/20">
        <CheckCircle weight="fill" /> PROCURE
      </span>
    )
  }
  return (
    <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-mono font-medium text-amber-400 bg-amber-400/10 border border-amber-400/20">
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
    <div className="min-h-[100dvh] bg-zinc-950 text-zinc-100 selection:bg-accent selection:text-white">
      
      {/* Navigation */}
      <nav className="h-16 border-b border-zinc-900 flex items-center justify-between px-6 lg:px-12">
        <div className="flex items-center gap-2 font-mono text-sm tracking-wide text-zinc-300">
          <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
          STITCHFLOW.AI // AUTONOMOUS AGENT
        </div>
        <div className="text-xs font-mono text-zinc-500 hidden sm:block">
          LAST SYNC: {new Date(agentData.last_updated).toLocaleString()}
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 lg:px-12 pt-16 pb-32">
        
        {/* Hero Section */}
        <section className="mb-20">
          <StaggerReveal>
            <h1 className="text-4xl md:text-5xl lg:text-6xl tracking-tighter leading-none mb-6 max-w-4xl">
              Procurement orders generated.
              <br />
              <span className="text-zinc-500">Awaiting human authorization.</span>
            </h1>
          </StaggerReveal>
          
          <StaggerReveal delay={0.1}>
            <p className="text-zinc-400 max-w-[60ch] leading-relaxed text-lg">
              The AI orchestration team has completed market analysis. 
              Below are the optimized purchase orders prioritizing current high-velocity trends while strictly maintaining our capital and warehouse constraints.
            </p>
          </StaggerReveal>
        </section>

        {/* Global Metrics (Bento-ish row) */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-16">
          <StaggerReveal delay={0.2}>
            <Metric 
              label="Remaining Capital" 
              value={`${agentData.budget_remaining_tnd.toLocaleString()} TND`} 
              icon={CurrencyDollar} 
            />
          </StaggerReveal>
          <StaggerReveal delay={0.3}>
            <Metric 
              label="Available Warehouse Cap" 
              value={`${agentData.capacity_remaining_m3} m³`} 
              icon={Package} 
            />
          </StaggerReveal>
        </section>

        {/* Recommendations List */}
        <section>
          <StaggerReveal delay={0.4}>
            <div className="flex items-center justify-between mb-6 border-b border-zinc-900 pb-4">
              <h2 className="text-sm font-mono tracking-wide text-zinc-500 uppercase">Agent Recommendations</h2>
              <span className="text-sm font-mono text-zinc-500">{agentData.recommendations.length} ITEMS</span>
            </div>
          </StaggerReveal>

          <div className="grid gap-4">
            {agentData.recommendations.map((rec, index) => (
              <StaggerReveal key={rec.id} delay={0.5 + (index * 0.05)}>
                <div 
                  className={`border p-6 transition-colors duration-200 flex flex-col md:flex-row md:items-center justify-between gap-6
                    ${approvedIds.has(rec.id) ? 'border-accent bg-accent/5' : 'border-zinc-800 bg-zinc-900/20 hover:border-zinc-700'}`}
                >
                  
                  {/* Left block: Identity & Reasoning */}
                  <div className="flex-1 space-y-4">
                    <div className="flex items-center gap-3">
                      <ActionBadge action={rec.action} />
                      <span className="font-mono text-sm text-zinc-500">{rec.id}</span>
                    </div>
                    
                    <div>
                      <h3 className="text-xl font-medium tracking-tight mb-2">{rec.name}</h3>
                      <p className="text-zinc-400 text-sm leading-relaxed max-w-[75ch] flex items-start gap-2">
                        <TrendUp className="w-4 h-4 mt-0.5 text-zinc-500 shrink-0" />
                        {rec.reasoning}
                      </p>
                    </div>
                  </div>

                  {/* Right block: Math & Action */}
                  <div className="flex flex-col md:items-end gap-6 shrink-0 md:w-64">
                    <div className="grid grid-cols-2 md:text-right gap-x-8 gap-y-1">
                      <span className="text-xs font-mono text-zinc-500">QTY</span>
                      <span className="text-sm font-mono">{rec.quantity > 0 ? rec.quantity : '-'}</span>
                      
                      <span className="text-xs font-mono text-zinc-500">COST</span>
                      <span className="text-sm font-mono">{rec.cost_tnd > 0 ? `${rec.cost_tnd.toLocaleString()} TND` : '-'}</span>
                      
                      <span className="text-xs font-mono text-zinc-500">VOL</span>
                      <span className="text-sm font-mono">{rec.volume_m3 > 0 ? `${rec.volume_m3} m³` : '-'}</span>
                    </div>

                    <button 
                      onClick={() => toggleApproval(rec.id)}
                      className={`px-4 py-2 text-sm font-medium transition-transform active:scale-95 border
                        ${approvedIds.has(rec.id) 
                          ? 'bg-accent text-white border-accent' 
                          : 'bg-transparent text-zinc-300 border-zinc-700 hover:border-zinc-500 hover:text-white'}`}
                    >
                      {approvedIds.has(rec.id) ? 'AUTHORIZED' : 'AUTHORIZE'}
                    </button>
                  </div>

                </div>
              </StaggerReveal>
            ))}
          </div>

          {/* Floating Action Bar */}
          {approvedIds.size > 0 && (
            <motion.div 
              initial={{ y: 100, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="fixed bottom-8 left-1/2 -translate-x-1/2 bg-zinc-900 border border-zinc-800 p-4 shadow-2xl flex items-center gap-6 z-50"
            >
              <div className="font-mono text-sm">
                <span className="text-accent">{approvedIds.size}</span> item(s) approved
              </div>
              <button 
                onClick={handleExecute}
                className="bg-zinc-100 text-zinc-950 px-6 py-2 text-sm font-medium hover:bg-white active:scale-95 transition-all"
              >
                EXECUTE ORDER
              </button>
            </motion.div>
          )}

        </section>
      </main>
    </div>
  )
}
