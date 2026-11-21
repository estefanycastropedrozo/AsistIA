import React from 'react';
import { MessageSquareText, BarChart3, ShieldCheck, Sparkles } from 'lucide-react';

interface NavbarProps {
  activeTab: 'chat' | 'admin';
  setActiveTab: (tab: 'chat' | 'admin') => void;
  onOpenPrivacy: () => void;
  isBackendHealthy: boolean;
  userRole: string;
  setUserRole: (role: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  onOpenPrivacy,
  isBackendHealthy
}) => {
  return (
    <header className="bg-white border-b border-slate-200 shadow-xs sticky top-0 z-40">
      {/* Línea sutil pastel superior */}
      <div className="h-1 bg-gradient-to-r from-blue-600 via-amber-500 to-blue-600 w-full" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo Oficial de TEINCO - Tamaño grande y legible */}
          <div className="flex items-center gap-3">
            <div className="p-1 bg-white rounded-xl">
              <img
                src="/teinco_logo.png"
                alt="TEINCO - Corporación Tecnológica Industrial Colombiana"
                className="h-12 w-auto max-w-[240px] sm:max-w-[280px] object-contain"
              />
            </div>

            <div className="hidden sm:flex items-center gap-2 pl-3 border-l border-slate-200">
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5">
                  <span className="font-extrabold text-sm text-slate-800 tracking-tight">AsistIA</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-amber-50 text-amber-800 rounded-md border border-amber-200 flex items-center gap-1">
                    <Sparkles className="w-2.5 h-2.5 text-amber-600" /> Virtual TEINCO
                  </span>
                </div>
                <span className="text-[11px] text-slate-500 font-medium">
                  Atención y Orientación Institucional
                </span>
              </div>
            </div>
          </div>

          {/* Selector de Vistas - Pasteles Suaves */}
          <div className="flex items-center gap-1.5 bg-slate-50 p-1 rounded-xl border border-slate-200">
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'chat'
                  ? 'bg-white text-blue-700 shadow-xs border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <MessageSquareText className="w-3.5 h-3.5 text-blue-600" />
              <span>Atención Estudiantil</span>
            </button>

            <button
              onClick={() => setActiveTab('admin')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeTab === 'admin'
                  ? 'bg-white text-blue-700 shadow-xs border border-slate-200/80'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
              }`}
            >
              <BarChart3 className="w-3.5 h-3.5 text-amber-600" />
              <span>Panel de Reportes</span>
            </button>
          </div>

          {/* Indicador de Estado y Ley 1581 */}
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-50 text-[11px] font-semibold text-emerald-800 border border-emerald-200">
              <span className={`w-2 h-2 rounded-full ${isBackendHealthy ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
              <span>{isBackendHealthy ? 'Servicio Activo' : 'Offline'}</span>
            </div>

            <button
              onClick={onOpenPrivacy}
              title="Aviso de Privacidad — Ley 1581 de 2012"
              className="px-2.5 py-1 rounded-lg text-slate-600 hover:text-blue-800 hover:bg-blue-50 border border-slate-200 transition-colors flex items-center gap-1.5 text-xs font-semibold"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
              <span className="hidden sm:inline text-[11px]">Ley 1581</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};
