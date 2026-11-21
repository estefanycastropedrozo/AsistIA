import React, { useState, useEffect, useRef } from 'react';
import {
  Send,
  Sparkles,
  User,
  Clock,
  ThumbsUp,
  ThumbsDown,
  Building2,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Copy,
  Check,
  RotateCcw,
  BookOpen,
  MessageCircle,
  GraduationCap,
  PanelLeftClose,
  PanelLeftOpen,
  PanelRightClose,
  PanelRightOpen,
  HelpCircle,
  ShieldCheck,
  ExternalLink,
  ChevronRight,
  ArrowRight
} from 'lucide-react';
import { ChatMessageItem, DivisionContactInfo } from '../types';

interface ChatViewProps {
  userRole: string;
  setUserRole: (role: string) => void;
}

export const ChatView: React.FC<ChatViewProps> = ({ userRole, setUserRole }) => {
  const [messages, setMessages] = useState<ChatMessageItem[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionToken, setSessionToken] = useState<string>('');
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [activeDivisionFilter, setActiveDivisionFilter] = useState<string>('all');
  const [divisionsData, setDivisionsData] = useState<DivisionContactInfo[]>([]);

  // Estados de los paneles laterales (abiertos por defecto en pantalla grande)
  const [showLeftPanel, setShowLeftPanel] = useState(true);
  const [showRightPanel, setShowRightPanel] = useState(true);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Mapeo de estilos cromáticos pasteles por dependencia institucional
  const divisionMeta: Record<string, { bg: string; border: string; text: string; badge: string; iconColor: string; desc: string }> = {
    'all': {
      bg: 'bg-indigo-50/90',
      border: 'border-indigo-200',
      text: 'text-indigo-900',
      badge: 'bg-indigo-100 text-indigo-800',
      iconColor: 'text-indigo-600',
      desc: 'Todas las áreas académicas y administrativas'
    },
    'Admisiones y Mercadeo': {
      bg: 'bg-sky-50/90',
      border: 'border-sky-200',
      text: 'text-sky-900',
      badge: 'bg-sky-100 text-sky-800',
      iconColor: 'text-sky-600',
      desc: 'Inscripciones, costos, homologaciones y carreras'
    },
    'Registro y Control': {
      bg: 'bg-blue-50/90',
      border: 'border-blue-200',
      text: 'text-blue-900',
      badge: 'bg-blue-100 text-blue-800',
      iconColor: 'text-blue-600',
      desc: 'Certificados, notas, matrículas y grados'
    },
    'Bienestar Institucional': {
      bg: 'bg-emerald-50/90',
      border: 'border-emerald-200',
      text: 'text-emerald-900',
      badge: 'bg-emerald-100 text-emerald-800',
      iconColor: 'text-emerald-600',
      desc: 'Psicología gratuita, deportes, cultura y becas'
    },
    'Cartera y Financiación': {
      bg: 'bg-amber-50/90',
      border: 'border-amber-200',
      text: 'text-amber-900',
      badge: 'bg-amber-100 text-amber-800',
      iconColor: 'text-amber-600',
      desc: 'Pagos PSE, bancos, cuotas y créditos ICETEX'
    },
    'Coordinación Académica': {
      bg: 'bg-purple-50/90',
      border: 'border-purple-200',
      text: 'text-purple-900',
      badge: 'bg-purple-100 text-purple-800',
      iconColor: 'text-purple-600',
      desc: 'Opciones de grado (proyecto, diplomado, prácticas) y pensum'
    },
    'Soporte y Sistemas': {
      bg: 'bg-teal-50/90',
      border: 'border-teal-200',
      text: 'text-teal-900',
      badge: 'bg-teal-100 text-teal-800',
      iconColor: 'text-teal-600',
      desc: 'Campus Virtual Moodle, correos y portal Q10'
    },
    'General': {
      bg: 'bg-slate-50',
      border: 'border-slate-200',
      text: 'text-slate-800',
      badge: 'bg-slate-100 text-slate-700',
      iconColor: 'text-blue-600',
      desc: 'Orientación institucional general'
    }
  };

  useEffect(() => {
    let token = localStorage.getItem('asistia_session_token');
    if (!token) {
      token = crypto.randomUUID();
      localStorage.setItem('asistia_session_token', token);
    }
    setSessionToken(token);

    fetch(`/api/chat/history/${token}`)
      .then(res => res.json())
      .then(data => {
        if (data.messages && data.messages.length > 0) {
          setMessages(data.messages);
        } else {
          setMessages([
            {
              sender: 'assistant',
              content:
                '¡Hola! Te doy una cordial bienvenida a **AsistIA**, el asistente virtual institucional de la **Corporación Tecnológica Industrial Colombiana (TEINCO)**.\n\n' +
                'Estoy aquí para orientarte en tus consultas de **Admisiones, Registro y Control Académico, Cartera, Bienestar Institucional y Coordinación de Software**.\n\n' +
                'Puedes seleccionar una dependencia en el panel izquierdo, un trámite en el panel derecho o escribir directamente tu consulta abajo.',
              detected_division: 'General',
              confidence_score: 1.0,
              response_time_ms: 5,
              sources: ['Normativa Oficial TEINCO']
            }
          ]);
        }
      })
      .catch(() => {
        setMessages([
          {
            sender: 'assistant',
            content:
              '¡Hola! Te doy la bienvenida a **AsistIA**, el asistente institucional de **TEINCO**. ¿En qué trámite o consulta te puedo colaborar hoy?',
            detected_division: 'General',
            confidence_score: 1.0,
            response_time_ms: 5
          }
        ]);
      });

    fetch('/api/chat/divisions')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setDivisionsData(data);
        }
      })
      .catch(err => console.error('Error cargando divisiones:', err));
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (customMessage?: string) => {
    const textToSend = (customMessage || inputText).trim();
    if (!textToSend || isLoading) return;

    setInputText('');

    const userMessage: ChatMessageItem = {
      sender: 'user',
      content: textToSend,
      created_at: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_token: sessionToken,
          message: textToSend,
          user_role: userRole
        })
      });

      if (!response.ok) throw new Error('Error al procesar la respuesta');

      const data = await response.json();

      const assistantMessage: ChatMessageItem = {
        id: data.message_id,
        sender: 'assistant',
        content: data.reply,
        detected_division: data.detected_division,
        confidence_score: data.confidence_score,
        response_time_ms: data.response_time_ms,
        sources: data.sources,
        division_contact: data.division_contact,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [
        ...prev,
        {
          sender: 'assistant',
          content:
            '⚠️ En este momento no fue posible conectar con el servidor. Puedes escribir a **coordinacionregistroycontrol@teinco.edu.co** o comunicarte al PBX **+57 601 7433200**.',
          detected_division: 'Registro y Control'
        }
      ]);
    } finally {
      setIsLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  const handleFeedback = async (messageId: number, isHelpful: boolean) => {
    try {
      await fetch('/api/chat/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_id: messageId,
          is_helpful: isHelpful
        })
      });

      setMessages(prev =>
        prev.map(msg =>
          msg.id === messageId
            ? { ...msg, feedback: { is_helpful: isHelpful } }
            : msg
        )
      );
    } catch (err) {
      console.error('Error enviando feedback:', err);
    }
  };

  const handleCopyText = (content: string, id: number) => {
    navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleResetChat = () => {
    if (confirm('¿Deseas reiniciar la conversación con AsistIA?')) {
      const newToken = crypto.randomUUID();
      localStorage.setItem('asistia_session_token', newToken);
      setSessionToken(newToken);
      setMessages([
        {
          sender: 'assistant',
          content:
            '¡Hola nuevamente! Sesión renovada. ¿En qué trámite o consulta de **TEINCO** te puedo colaborar?',
          detected_division: 'General',
          confidence_score: 1.0,
          response_time_ms: 5
        }
      ]);
    }
  };

  const formatContent = (text: string) => {
    // 1. Escalonar pasos inline si vienen juntos como 1) ... 2) ... o 1. ... 2. ...
    let processedText = text;
    if (/(1[\)\.]\s+.*?2[\)\.])/.test(processedText)) {
      processedText = processedText
        .replace(/(\s*:\s*|\.\s+)(1[\)\.])\s*/g, ':\n\n1. ')
        .replace(/(\s+)(\d+)\)\s*/g, '\n$2. ')
        .replace(/(\s+)(\d+)\.(?!\d)\s*/g, '\n$2. ');
    }

    const lines = processedText.split('\n');
    return lines.map((line, idx) => {
      // Helper para formatear negritas (**texto**)
      const renderFormatted = (str: string) => {
        return str.split(/(\*\*.*?\*\*)/g).map((part, pIdx) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return (
              <strong key={pIdx} className="font-extrabold text-slate-900">
                {part.slice(2, -2)}
              </strong>
            );
          }
          return part;
        });
      };

      const trimmed = line.trim();

      // Pasos numerados escalonados (1. o 1) ...) evitando decimales
      const numMatch = trimmed.match(/^(\d+)(?:\)|\.(?!\d))\s+(.*)/);
      if (numMatch) {
        const stepNum = numMatch[1];
        const stepText = numMatch[2];
        return (
          <div
            key={idx}
            className="flex items-start gap-3 my-2 p-2.5 rounded-xl bg-blue-50/50 border border-blue-100 hover:border-blue-300 hover:bg-blue-50/80 transition-all shadow-2xs"
          >
            <span className="w-5 h-5 rounded-md bg-gradient-to-br from-blue-600 to-indigo-600 text-white font-black text-[11px] flex items-center justify-center shrink-0 shadow-2xs mt-0.5">
              {stepNum}
            </span>
            <div className="text-slate-800 text-xs sm:text-sm leading-relaxed">
              {renderFormatted(stepText)}
            </div>
          </div>
        );
      }

      // Viñetas con estilo institucional
      if (trimmed.startsWith('• ') || trimmed.startsWith('- ')) {
        const bulletText = trimmed.replace(/^[•\-]\s+/, '');
        return (
          <div key={idx} className="flex items-start gap-2.5 my-1.5 pl-1.5">
            <span className="w-2 h-2 rounded-full bg-amber-500 shrink-0 mt-2 shadow-2xs" />
            <div className="text-slate-700 text-xs sm:text-sm leading-relaxed">
              {renderFormatted(bulletText)}
            </div>
          </div>
        );
      }

      // Citas / Alertas
      if (trimmed.startsWith('> ')) {
        return (
          <blockquote
            key={idx}
            className="border-l-3 border-amber-400 bg-amber-50/70 p-2.5 rounded-r-lg my-2 text-slate-800 text-xs sm:text-sm"
          >
            {renderFormatted(trimmed.slice(2))}
          </blockquote>
        );
      }

      // Separador
      if (trimmed === '---') {
        return <hr key={idx} className="my-2.5 border-slate-200" />;
      }

      // Párrafo normal
      return (
        <p key={idx} className={trimmed === '' ? 'h-1.5' : 'my-1 text-xs sm:text-sm leading-relaxed text-slate-800'}>
          {renderFormatted(line)}
        </p>
      );
    });
  };

  return (
    <div className="w-full max-w-[1700px] mx-auto px-2 sm:px-4 py-3 h-[calc(100vh-5.5rem)] flex gap-3 overflow-hidden">
      
      {/* ============================================================== */}
      {/* PANEL LATERAL IZQUIERDO: DIRECTORIO DE DEPENDENCIAS TEINCO     */}
      {/* ============================================================== */}
      {showLeftPanel && (
        <aside className="hidden lg:flex flex-col w-72 shrink-0 bg-white/95 backdrop-blur-md rounded-2xl border border-slate-200/90 shadow-sm p-3.5 space-y-3 overflow-hidden animate-fade-in">
          
          {/* Cabecera del Panel Izquierdo */}
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center font-bold border border-blue-200">
                <Building2 className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Dependencias</h3>
                <p className="text-[10px] text-slate-400 font-medium">Directorio Oficial TEINCO</p>
              </div>
            </div>

            <button
              onClick={() => setShowLeftPanel(false)}
              className="p-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
              title="Ocultar panel"
            >
              <PanelLeftClose className="w-4 h-4" />
            </button>
          </div>

          {/* Lista de Dependencias en Tarjetas Pasteles Suaves */}
          <div className="flex-1 overflow-y-auto space-y-2 pr-1">
            <button
              onClick={() => setActiveDivisionFilter('all')}
              className={`w-full text-left p-2.5 rounded-xl border transition-all text-xs flex items-center justify-between ${
                activeDivisionFilter === 'all'
                  ? 'bg-blue-600 text-white border-blue-700 shadow-xs'
                  : 'bg-indigo-50/80 border-indigo-200/80 text-indigo-950 hover:bg-indigo-100/80'
              }`}
            >
              <div className="flex items-center gap-2">
                <Sparkles className={`w-4 h-4 ${activeDivisionFilter === 'all' ? 'text-white' : 'text-amber-500'}`} />
                <span className="font-bold">Todas las Dependencias</span>
              </div>
              <ChevronRight className={`w-3.5 h-3.5 opacity-60 ${activeDivisionFilter === 'all' ? 'text-white' : ''}`} />
            </button>

            {divisionsData.map(div => {
              const meta = divisionMeta[div.division_name] || divisionMeta['General'];
              const isSelected = activeDivisionFilter === div.division_name;

              return (
                <div
                  key={div.division_name}
                  onClick={() => {
                    setActiveDivisionFilter(div.division_name);
                    if (div.sample_queries && div.sample_queries.length > 0) {
                      handleSendMessage(div.sample_queries[0]);
                    }
                  }}
                  className={`p-2.5 rounded-xl border transition-all cursor-pointer text-xs space-y-1 ${
                    isSelected
                      ? 'bg-blue-600 text-white border-blue-700 shadow-xs'
                      : `${meta.bg} ${meta.border} hover:shadow-2xs hover:scale-[1.01]`
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5 font-bold">
                      <Building2 className={`w-3.5 h-3.5 ${isSelected ? 'text-white' : meta.iconColor}`} />
                      <span className={isSelected ? 'text-white' : meta.text}>{div.division_name}</span>
                    </div>
                  </div>
                  <p className={`text-[11px] leading-tight line-clamp-1 ${isSelected ? 'text-blue-100' : 'text-slate-500'}`}>
                    {meta.desc}
                  </p>
                </div>
              );
            })}
          </div>

          {/* Pie del Panel Izquierdo con Logo de TEINCO */}
          <div className="pt-2 border-t border-slate-100 flex items-center justify-center bg-slate-50/60 p-2 rounded-xl">
            <img src="/teinco_logo.png" alt="TEINCO" className="h-7 w-auto object-contain" />
          </div>

        </aside>
      )}

      {/* ============================================================== */}
      {/* PANEL CENTRAL: CHAT Y CONVERSACIÓN PRINCIPAL                   */}
      {/* ============================================================== */}
      <main className="flex-1 flex flex-col bg-white/90 backdrop-blur-md rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden min-w-0">
        
        {/* Barra Superior del Chat: Perfil, Periodo y Botones Desplegables */}
        <div className="px-4 py-2.5 border-b border-slate-200/80 bg-white/95 flex flex-wrap items-center justify-between gap-2.5">
          
          <div className="flex items-center gap-2">
            {!showLeftPanel && (
              <button
                onClick={() => setShowLeftPanel(true)}
                className="p-1.5 rounded-lg text-slate-500 hover:text-blue-700 hover:bg-slate-100 transition-colors"
                title="Mostrar directorio de dependencias"
              >
                <PanelLeftOpen className="w-4 h-4" />
              </button>
            )}

            <div className="flex items-center gap-1.5">
              <span className="text-[11px] uppercase tracking-wider font-extrabold text-slate-500 hidden sm:inline">Perfil:</span>
              <div className="flex gap-1 bg-slate-100/90 p-0.5 rounded-lg text-xs font-semibold">
                {[
                  { id: 'estudiante', label: 'Estudiante', color: 'bg-blue-50 text-blue-800 border-blue-300', active: 'bg-blue-600 text-white' },
                  { id: 'aspirante', label: 'Aspirante', color: 'bg-amber-50 text-amber-800 border-amber-300', active: 'bg-amber-600 text-white' },
                  { id: 'egresado', label: 'Egresado', color: 'bg-purple-50 text-purple-800 border-purple-300', active: 'bg-purple-600 text-white' },
                  { id: 'docente', label: 'Docente', color: 'bg-teal-50 text-teal-800 border-teal-300', active: 'bg-teal-600 text-white' }
                ].map(r => (
                  <button
                    key={r.id}
                    onClick={() => setUserRole(r.id)}
                    className={`px-2.5 py-1 rounded-md text-xs font-bold transition-all border ${
                      userRole === r.id
                        ? `${r.active} border-transparent shadow-xs`
                        : `${r.color} hover:opacity-90`
                    }`}
                  >
                    {r.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="hidden xl:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-blue-50/80 border border-blue-200 text-[11px] font-bold text-blue-800">
              <GraduationCap className="w-3.5 h-3.5 text-blue-600" />
              <span>Periodo 2026-1</span>
            </div>

            <button
              onClick={handleResetChat}
              className="text-xs text-slate-600 hover:text-blue-700 flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-slate-200 hover:bg-slate-50 transition-colors font-medium shadow-2xs"
              title="Nueva conversación"
            >
              <RotateCcw className="w-3.5 h-3.5 text-slate-500" />
              <span className="hidden sm:inline">Nueva Consulta</span>
            </button>

            {!showRightPanel && (
              <button
                onClick={() => setShowRightPanel(true)}
                className="p-1.5 rounded-lg text-slate-500 hover:text-amber-700 hover:bg-slate-100 transition-colors"
                title="Mostrar canales oficiales y trámites"
              >
                <PanelRightOpen className="w-4 h-4" />
              </button>
            )}
          </div>

        </div>

        {/* Hilo de Conversación */}
        <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3.5">
          {messages.map((msg, index) => {
            const isUser = msg.sender === 'user';
            const meta = divisionMeta[msg.detected_division || 'General'] || divisionMeta['General'];

            return (
              <div
                key={index}
                className={`flex gap-3 max-w-[95%] sm:max-w-[88%] ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
              >
                {/* Avatar */}
                <div
                  className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 shadow-xs border ${
                    isUser
                      ? 'bg-gradient-to-br from-blue-700 to-blue-600 text-white border-blue-800'
                      : 'bg-white border-slate-200 p-0.5'
                  }`}
                >
                  {isUser ? (
                    <span className="text-xs font-bold uppercase">{userRole.slice(0, 2)}</span>
                  ) : (
                    <img src="/teinco_logo.png" alt="TEINCO" className="w-8 h-8 object-contain" />
                  )}
                </div>

                {/* Burbuja */}
                <div
                  className={`rounded-2xl p-4 text-xs sm:text-sm leading-relaxed border shadow-xs ${
                    isUser
                      ? 'bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-600 text-white border-blue-700 rounded-tr-xs'
                      : 'bg-white text-slate-800 border-slate-200/90 rounded-tl-xs'
                  }`}
                >
                  {/* Cabecera del Asistente */}
                  {!isUser && msg.detected_division && msg.detected_division !== 'General' && (
                    <div className="flex flex-wrap items-center justify-between gap-2 pb-2 mb-2 border-b border-slate-100">
                      <span className={`px-2.5 py-0.5 rounded-lg text-[11px] font-bold border flex items-center gap-1 ${meta.bg} ${meta.text} ${meta.border}`}>
                        <Building2 className={`w-3 h-3 ${meta.iconColor}`} /> {msg.detected_division}
                      </span>

                      <div className="flex items-center gap-2 text-[10px] text-slate-400 font-medium">
                        {msg.response_time_ms && (
                          <span className="flex items-center gap-0.5 text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">
                            <Clock className="w-3 h-3 text-amber-600" />
                            {msg.response_time_ms} ms
                          </span>
                        )}
                        <button
                          onClick={() => handleCopyText(msg.content, msg.id || index)}
                          className="p-1 hover:text-slate-700 rounded transition-colors"
                          title="Copiar texto"
                        >
                          {copiedId === (msg.id || index) ? (
                            <Check className="w-3.5 h-3.5 text-emerald-600" />
                          ) : (
                            <Copy className="w-3.5 h-3.5" />
                          )}
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Texto */}
                  <div className="space-y-1">
                    {formatContent(msg.content)}
                  </div>

                  {/* Ficha Oficial de Contacto */}
                  {!isUser && msg.division_contact && (
                    <div className="mt-3 p-3.5 rounded-2xl bg-gradient-to-r from-amber-50/70 via-orange-50/30 to-blue-50/40 border-l-4 border-amber-500 border-y border-r border-amber-200/80 text-slate-800 space-y-2.5 shadow-2xs">
                      <div className="font-bold text-blue-900 flex items-center justify-between text-xs">
                        <span className="flex items-center gap-1.5 font-extrabold">
                          <Building2 className="w-4 h-4 text-amber-600" />
                          Canales Oficiales — {msg.division_contact.division_name}
                        </span>
                        <span className="text-[10px] font-bold text-emerald-800 bg-emerald-100/80 px-2 py-0.5 rounded-md border border-emerald-300">
                          Atención Presencial y Virtual
                        </span>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] pt-1">
                        <a
                          href={`mailto:${msg.division_contact.email}`}
                          className="flex items-center gap-2 p-2 rounded-xl bg-white border border-blue-200/80 hover:border-blue-500 text-blue-800 transition-colors font-semibold truncate shadow-2xs"
                        >
                          <Mail className="w-3.5 h-3.5 text-blue-600 shrink-0" />
                          <span className="truncate">{msg.division_contact.email}</span>
                        </a>

                        <a
                          href="https://wa.me/573013337956"
                          target="_blank"
                          rel="noreferrer"
                          className="flex items-center gap-2 p-2 rounded-xl bg-emerald-50 border border-emerald-300 hover:bg-emerald-100 text-emerald-900 transition-colors font-bold shadow-2xs"
                        >
                          <MessageCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                          <span>WhatsApp: 301 333 7956</span>
                        </a>

                        <div className="flex items-center gap-2 p-2 rounded-xl bg-white/80 border border-slate-200 text-slate-700">
                          <Phone className="w-3.5 h-3.5 text-slate-600 shrink-0" />
                          <span>PBX Bogotá: +57 601 7433200</span>
                        </div>

                        <div className="flex items-center gap-2 p-2 rounded-xl bg-amber-50/80 border border-amber-200 text-amber-900 font-medium">
                          <Calendar className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                          <span>Lun a Vie 7am-10pm | Sáb 7am-4pm</span>
                        </div>

                        <div className="flex items-start gap-2 p-2 rounded-xl bg-white/80 border border-slate-200 text-slate-700 sm:col-span-2">
                          <MapPin className="w-3.5 h-3.5 text-rose-500 shrink-0 mt-0.5" />
                          <span>{msg.division_contact.office}</span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Feedback */}
                  {!isUser && msg.id && (
                    <div className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                      <span className="flex items-center gap-1 font-medium text-slate-500">
                        <BookOpen className="w-3 h-3 text-blue-500" />
                        Reglamento TEINCO
                      </span>

                      <div>
                        {msg.feedback ? (
                          <span className="text-emerald-700 font-semibold flex items-center gap-1 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                            <Check className="w-3 h-3" /> ¡Gracias por calificar!
                          </span>
                        ) : (
                          <div className="flex items-center gap-1.5 text-slate-500 font-medium">
                            <span>¿Fue útil?</span>
                            <button
                              onClick={() => handleFeedback(msg.id!, true)}
                              className="p-1 hover:text-emerald-700 hover:bg-emerald-50 rounded transition-colors"
                              title="Respuesta útil"
                            >
                              <ThumbsUp className="w-3.5 h-3.5" />
                            </button>
                            <button
                              onClick={() => handleFeedback(msg.id!, false)}
                              className="p-1 hover:text-rose-700 hover:bg-rose-50 rounded transition-colors"
                              title="No resolvió mi duda"
                            >
                              <ThumbsDown className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {isLoading && (
            <div className="flex gap-3 max-w-[80%] mr-auto">
              <div className="w-9 h-9 rounded-xl bg-white border border-slate-200 p-0.5 flex items-center justify-center shrink-0">
                <img src="/teinco_logo.png" alt="TEINCO" className="w-8 h-8 object-contain animate-pulse" />
              </div>
              <div className="bg-white rounded-2xl p-3 border border-slate-200 shadow-2xs flex items-center gap-2 text-xs text-slate-600">
                <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce" />
                <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce [animation-delay:0.2s]" />
                <span className="w-2 h-2 rounded-full bg-amber-500 animate-bounce [animation-delay:0.4s]" />
                <span className="ml-1 font-semibold text-blue-900">Consultando reglamentos de TEINCO...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Barra de Entrada de Consulta */}
        <div className="p-3 border-t border-slate-200/80 bg-white/95">
          {/* Píldoras Rápidas Pasteles sobre el input */}
          <div className="flex gap-1.5 overflow-x-auto scrollbar-none mb-2 py-0.5 text-[11px]">
            {[
              { label: '📝 Certificados de Notas', q: '¿Cómo solicito un certificado oficial de notas y cuánto tarda?', color: 'bg-blue-50 text-blue-800 border-blue-200 hover:bg-blue-100' },
              { label: '💳 Pagos PSE y Cuotas', q: '¿Cuáles son los medios de pago disponibles y opciones de cuotas?', color: 'bg-amber-50 text-amber-800 border-amber-200 hover:bg-amber-100' },
              { label: '🎓 Opciones y Modos de Grado', q: '¿Cuáles son las opciones y modalidades de grado en TEINCO (proyecto de software, diplomado o prácticas)?', color: 'bg-purple-50 text-purple-800 border-purple-200 hover:bg-purple-100' },
              { label: '🧠 Psicología Gratuita', q: '¿Cómo puedo agendar una consulta psicológica en bienestar?', color: 'bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100' }
            ].map((chip, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(chip.q)}
                className={`px-2.5 py-1 rounded-lg border whitespace-nowrap transition-colors font-bold shadow-2xs ${chip.color}`}
              >
                {chip.label}
              </button>
            ))}
          </div>

          <form
            onSubmit={e => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="relative flex items-center bg-white border border-slate-300 rounded-xl shadow-xs focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-100 transition-all"
          >
            <input
              ref={inputRef}
              type="text"
              value={inputText}
              onChange={e => setInputText(e.target.value)}
              placeholder="Escribe tu consulta sobre admisiones, pagos, certificados, notas o bienestar..."
              className="w-full pl-4 pr-12 py-3 text-xs sm:text-sm bg-transparent focus:outline-none placeholder:text-slate-400 font-medium"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!inputText.trim() || isLoading}
              className="absolute right-2 p-2 rounded-lg bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white disabled:opacity-30 transition-all shadow-xs"
              title="Enviar mensaje"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

          <p className="text-[10px] text-center text-slate-400 mt-1 flex items-center justify-center gap-1">
            <GraduationCap className="w-3 h-3 text-slate-400" />
            Corporación Tecnológica Industrial Colombiana (TEINCO) • AsistIA 2026
          </p>
        </div>

      </main>

      {/* ============================================================== */}
      {/* PANEL LATERAL DERECHO: CANALES OFICIALES Y TRÁMITES RÁPIDOS    */}
      {/* ============================================================== */}
      {showRightPanel && (
        <aside className="hidden xl:flex flex-col w-80 shrink-0 bg-white/95 backdrop-blur-md rounded-2xl border border-slate-200/90 shadow-sm p-3.5 space-y-3 overflow-y-auto animate-fade-in">
          
          {/* Cabecera del Panel Derecho */}
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center font-bold border border-amber-200">
                <HelpCircle className="w-4 h-4 text-amber-600" />
              </div>
              <div>
                <h3 className="text-xs font-black text-slate-900 uppercase tracking-wider">Centro de Ayuda</h3>
                <p className="text-[10px] text-slate-400 font-medium">Canales y Trámites Rápidos</p>
              </div>
            </div>

            <button
              onClick={() => setShowRightPanel(false)}
              className="p-1 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition-colors"
              title="Ocultar panel"
            >
              <PanelRightClose className="w-4 h-4" />
            </button>
          </div>

          {/* Tarjeta 1: Atención Oficial Inmediata */}
          <div className="p-3 rounded-2xl bg-gradient-to-br from-amber-50/80 via-orange-50/40 to-blue-50/50 border border-amber-200/80 space-y-2 shadow-2xs">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-black text-blue-900 uppercase tracking-wider">Atención Registro y Control</span>
              <span className="text-[9px] font-bold bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded">Oficial</span>
            </div>

            <a
              href="https://wa.me/573013337956"
              target="_blank"
              rel="noreferrer"
              className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs transition-colors shadow-2xs"
            >
              <MessageCircle className="w-4 h-4" />
              <span>Chatear por WhatsApp</span>
            </a>

            <a
              href="mailto:coordinacionregistroycontrol@teinco.edu.co"
              className="w-full flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-xl bg-white border border-blue-200 hover:border-blue-500 text-blue-800 font-semibold text-[11px] transition-colors"
            >
              <Mail className="w-3.5 h-3.5 text-blue-600" />
              <span className="truncate">Enviar Correo Institucional</span>
            </a>

            <div className="text-[11px] text-slate-600 space-y-1 pt-1 border-t border-amber-200/50">
              <div className="flex items-center gap-1.5">
                <Phone className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                <span className="font-semibold text-slate-800">PBX: +57 601 7433200</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                <span>Lun a Vie: 7:00am a 10:00pm</span>
              </div>
              <div className="flex items-start gap-1.5">
                <MapPin className="w-3.5 h-3.5 text-rose-500 shrink-0 mt-0.5" />
                <span className="text-[10px]">Calle 57 # 9-28 / Av. Caracas # 57-41</span>
              </div>
            </div>
          </div>

          {/* Tarjeta 2: Trámites con 1 Clic */}
          <div className="space-y-2 pt-1">
            <span className="text-[11px] font-black text-slate-700 uppercase tracking-wider block">Trámites en 1 Clic</span>
            <div className="space-y-1.5">
              {[
                { title: 'Solicitar Certificado de Estudio', q: '¿Cuáles son los pasos para solicitar certificado de estudio?', color: 'border-blue-200 hover:bg-blue-50/60' },
                { title: 'Pago con Botón PSE o Bancos', q: '¿Cómo pagar el semestre mediante PSE o bancos autorizados?', color: 'border-amber-200 hover:bg-amber-50/60' },
                { title: 'Opciones y Modos de Grado', q: '¿Cuáles son las opciones de grado disponibles en TEINCO (proyecto, diplomado, prácticas)?', color: 'border-purple-200 hover:bg-purple-50/60' },
                { title: 'Requisitos para Postularse a Grado', q: '¿Cuáles son los requisitos completos para graduarme?', color: 'border-emerald-200 hover:bg-emerald-50/60' }
              ].map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(item.q)}
                  className={`w-full text-left p-2 rounded-xl border bg-white transition-all text-[11px] font-semibold text-slate-700 flex items-center justify-between group ${item.color}`}
                >
                  <span className="group-hover:text-blue-700 transition-colors">{item.title}</span>
                  <ArrowRight className="w-3 h-3 text-slate-400 group-hover:text-blue-600 transition-transform group-hover:translate-x-0.5" />
                </button>
              ))}
            </div>
          </div>

          {/* Tarjeta 3: Cumplimiento y Seguridad de Datos */}
          <div className="mt-auto p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-[10px] text-slate-500 space-y-1">
            <div className="flex items-center gap-1.5 font-bold text-slate-700">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>Gobernanza de Datos</span>
            </div>
            <p>
              Tus consultas se procesan bajo anonimización estricta conforme a la Ley Estatutaria 1581 de 2012.
            </p>
          </div>

        </aside>
      )}

    </div>
  );
};
