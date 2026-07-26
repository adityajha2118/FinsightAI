import Link from "next/link";
import { Activity, LayoutDashboard, Github } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-white selection:bg-blue-500/30">
      {/* Top Navigation */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-br from-blue-500 to-blue-700 shadow-lg shadow-blue-500/20">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">FinSight AI</h1>
            <p className="text-[10px] text-blue-400 font-semibold tracking-widest uppercase">
              Enterprise
            </p>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
          <Link href="#overview" className="hover:text-white transition-colors">Overview</Link>
          <Link href="#features" className="hover:text-white transition-colors">Platform Features</Link>
          <Link href="#architecture" className="hover:text-white transition-colors">Architecture</Link>
        </div>

        <div className="flex items-center gap-4">
          <a href="https://github.com/adityajha2118/FinsightAI" target="_blank" rel="noopener noreferrer" className="text-sm font-medium text-slate-300 hover:text-white flex items-center gap-2 transition-colors">
            <Github className="w-4 h-4" />
            GitHub
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-8 pt-20 pb-32 grid lg:grid-cols-2 gap-16 items-center">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold tracking-wide uppercase mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            Enterprise Fintech Analytics
          </div>
          
          <h2 className="text-5xl lg:text-7xl font-extrabold tracking-tight mb-8 leading-[1.1]">
            Customer <br />
            Intelligence, <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">
              Reimagined.
            </span>
          </h2>
          
          <p className="text-lg text-slate-400 mb-10 max-w-xl leading-relaxed">
            FinSight AI simulates how American Express analyzes customer behavior — 
            predicting churn, detecting compliance risk, and surfacing decision intelligence 
            for every level of the organization using production-grade machine learning.
          </p>

          <div className="flex flex-wrap items-center gap-4">
            <Link 
              href="/dashboard" 
              className="inline-flex items-center gap-2 px-6 py-3.5 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-lg shadow-lg shadow-blue-500/25 transition-all hover:-translate-y-0.5"
            >
              <LayoutDashboard className="w-4 h-4" />
              Explore Dashboard
            </Link>
            <a 
              href="https://github.com/adityajha2118/FinsightAI"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3.5 bg-slate-800 hover:bg-slate-700 text-white text-sm font-semibold rounded-lg border border-slate-700 transition-all"
            >
              View Architecture
            </a>
          </div>
        </div>

        {/* CSS Credit Card Illustration */}
        <div className="relative perspective-1000">
          <div className="relative w-full max-w-[500px] mx-auto aspect-[1.586/1] rounded-2xl bg-gradient-to-br from-blue-600 via-blue-700 to-slate-900 shadow-2xl p-8 flex flex-col justify-between overflow-hidden border border-white/10 transform rotate-y-[-10deg] rotate-x-[5deg] hover:rotate-y-0 hover:rotate-x-0 transition-transform duration-700 group">
            
            {/* Card Background Patterns */}
            <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_50%_0%,rgba(255,255,255,0.2),transparent_70%)]" />
            <div className="absolute -right-20 -top-20 w-64 h-64 bg-blue-400 rounded-full mix-blend-overlay blur-3xl opacity-50 group-hover:opacity-70 transition-opacity" />
            
            {/* Card Header */}
            <div className="relative flex justify-between items-start z-10">
              <div className="text-white font-black tracking-widest text-xl opacity-90">
                AMEX
              </div>
              {/* Contactless Icon */}
              <div className="flex flex-col gap-1 opacity-70">
                <div className="w-1.5 h-1.5 rounded-full bg-white ml-auto" />
                <div className="w-2.5 h-1.5 rounded-full border-t-2 border-white ml-auto" />
                <div className="w-3.5 h-2 rounded-full border-t-2 border-white ml-auto" />
                <div className="w-4.5 h-2.5 rounded-full border-t-2 border-white ml-auto" />
              </div>
            </div>

            {/* Abstract Centered Logo / EMV Chip */}
            <div className="relative flex flex-col items-center justify-center gap-2 z-10">
               <div className="w-16 h-16 rounded-full border border-white/20 flex items-center justify-center bg-white/5 backdrop-blur-sm">
                 <div className="w-12 h-12 rounded-full border border-white/40 flex items-center justify-center">
                   <div className="w-8 h-4 bg-white/60 rounded-full" />
                 </div>
               </div>
            </div>

            {/* Card Footer */}
            <div className="relative flex justify-between items-end z-10">
              <div>
                <p className="text-white/60 text-xs font-semibold tracking-widest uppercase mb-1">Authorized User</p>
                <p className="text-white text-lg font-medium tracking-widest">FINSIGHT AI PLATFORM</p>
              </div>
              
              {/* Gold Chip */}
              <div className="w-12 h-9 rounded bg-gradient-to-br from-yellow-300 to-yellow-600 flex overflow-hidden opacity-90">
                 <div className="flex-1 border-r border-yellow-700/30" />
                 <div className="flex-1 flex flex-col">
                   <div className="flex-1 border-b border-yellow-700/30" />
                   <div className="flex-1" />
                 </div>
              </div>
            </div>
          </div>
          
          {/* Decorative glows behind card */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full bg-blue-500/20 blur-[100px] -z-10 rounded-full" />
        </div>
      </main>

      {/* Metrics Bar */}
      <div className="border-t border-slate-800 bg-slate-900/50 backdrop-blur-xl py-12">
        <div className="max-w-7xl mx-auto px-8 grid grid-cols-2 md:grid-cols-4 gap-8 divide-x divide-slate-800">
          <div className="text-center px-4">
            <p className="text-4xl font-bold text-white mb-2">100k+</p>
            <p className="text-xs font-bold text-slate-500 tracking-widest uppercase">Customers Analyzed</p>
          </div>
          <div className="text-center px-4">
            <p className="text-4xl font-bold text-white mb-2">100%</p>
            <p className="text-xs font-bold text-slate-500 tracking-widest uppercase">Cloud Deployed</p>
          </div>
          <div className="text-center px-4">
            <p className="text-4xl font-bold text-white mb-2">5</p>
            <p className="text-xs font-bold text-slate-500 tracking-widest uppercase">Analytics Modules</p>
          </div>
          <div className="text-center px-4">
            <p className="text-4xl font-bold text-white mb-2">XGBoost</p>
            <p className="text-xs font-bold text-slate-500 tracking-widest uppercase">ML Predictions</p>
          </div>
        </div>
      </div>
    </div>
  );
}
