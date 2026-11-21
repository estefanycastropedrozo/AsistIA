import React from 'react';
import { ShieldCheck, X, FileText, CheckCircle2 } from 'lucide-react';

interface PrivacyModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const PrivacyModal: React.FC<PrivacyModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl border border-slate-100 relative max-h-[90vh] overflow-y-auto">
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-teinco-primary">Política de Protección de Datos Personales</h3>
            <p className="text-xs text-slate-500 font-medium">Cumplimiento Ley Estatutaria 1581 de 2012 — República de Colombia</p>
          </div>
        </div>

        <div className="space-y-4 text-sm text-slate-600 leading-relaxed border-t border-slate-100 pt-4">
          <div className="bg-blue-50/70 border border-blue-100 rounded-xl p-3.5 flex gap-3 text-blue-900">
            <FileText className="w-5 h-5 text-blue-700 shrink-0 mt-0.5" />
            <p className="text-xs">
              <strong>Corporación Tecnológica Industrial Colombiana (TEINCO):</strong> AsistIA implementa mecanismos automáticos de anonimización y disociación de información personal en cada interacción.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-slate-800 mb-1 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> 1. Anonimización de Consultas
            </h4>
            <p>
              Números de identificación (Cédulas de Ciudadanía, Tarjetas de Identidad), números telefónicos privados y correos personales son filtrados y enmascarados antes de cualquier procesamiento o almacenamiento.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-slate-800 mb-1 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> 2. Finalidad del Tratamiento
            </h4>
            <p>
              Las interacciones son utilizadas exclusivamente con fines académicos, estadísticos y de mejoramiento continuo de la atención institucional, sin compartir información sensible con terceros.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-slate-800 mb-1 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> 3. Seguridad y Confidencialidad
            </h4>
            <p>
              El sistema opera bajo los lineamientos de la Ley 1273 de 2009 (Delitos Informáticos), garantizando la integridad, disponibilidad y confidencialidad de la base de conocimiento y los registros de servicio.
            </p>
          </div>
        </div>

        <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2.5 bg-teinco-primary text-white font-medium text-sm rounded-xl hover:bg-teinco-secondary transition-all shadow-sm"
          >
            Entendido y Acepto
          </button>
        </div>
      </div>
    </div>
  );
};
