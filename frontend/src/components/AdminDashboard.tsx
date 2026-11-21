import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  TrendingUp,
  Clock,
  ThumbsUp,
  Download,
  Search,
  Building2,
  Users,
  Settings,
  Plus,
  Trash2,
  RefreshCw,
  Sliders,
  CheckCircle2,
  KeyRound,
  FileSpreadsheet,
  Lock,
  LogOut,
  Upload,
  FileText,
  AlertCircle,
  ExternalLink,
  Shield,
  Sparkles,
  Info,
  Pencil,
  ShieldCheck,
  UserPlus
} from 'lucide-react';
import { AnalyticsOverview, KnowledgeArticle, RuntimeSettings, AdminUser } from '../types';

export const AdminDashboard: React.FC = () => {
  // Estado de autenticación administrativa
  const [adminToken, setAdminToken] = useState<string | null>(() => {
    return sessionStorage.getItem('asistia_admin_token');
  });
  const [adminUser, setAdminUser] = useState<any>(() => {
    const saved = sessionStorage.getItem('asistia_admin_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loginEmail, setLoginEmail] = useState('admin@teinco.edu.co');
  const [loginPassword, setLoginPassword] = useState('Teinco2026*');
  const [loginError, setLoginError] = useState('');
  const [isLoggingIn, setIsLoggingIn] = useState(false);

  // Estados de datos
  const [metrics, setMetrics] = useState<AnalyticsOverview | null>(null);
  const [knowledgeList, setKnowledgeList] = useState<KnowledgeArticle[]>([]);
  const [settingsData, setSettingsData] = useState<RuntimeSettings | null>(null);
  const [usersList, setUsersList] = useState<AdminUser[]>([]);
  const [activeSubTab, setActiveSubTab] = useState<'analytics' | 'knowledge' | 'settings' | 'users'>('analytics');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDivisionFilter, setSelectedDivisionFilter] = useState('all');
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Formulario nuevo usuario institucional
  const [showAddUserModal, setShowAddUserModal] = useState(false);
  const [newUser, setNewUser] = useState({
    email: '',
    full_name: '',
    password: '',
    role: 'Operario'
  });
  const [userError, setUserError] = useState('');
  const [userSuccess, setUserSuccess] = useState('');

  // Formulario nuevo artículo de conocimiento
  const [showAddArticleModal, setShowAddArticleModal] = useState(false);
  const [newArticle, setNewArticle] = useState({
    division: 'Admisiones y Mercadeo',
    category: 'General',
    title: '',
    content: '',
    keywords: '',
    contact_email: 'admisiones@teinco.edu.co',
    contact_phone: '+57 601 7433200',
    office_location: 'Sede Principal Calle 57 No. 9-28',
    schedule: 'Lunes a Viernes 7:00 a.m. a 10:00 p.m.'
  });

  // Formulario editar artículo existente
  const [showEditArticleModal, setShowEditArticleModal] = useState(false);
  const [editArticle, setEditArticle] = useState<KnowledgeArticle | null>(null);

  // Estado para subida de PDF
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [pdfDivision, setPdfDivision] = useState('Registro y Control');
  const [isUploadingPdf, setIsUploadingPdf] = useState(false);
  const [pdfUploadSuccess, setPdfUploadSuccess] = useState<string | null>(null);
  const [pdfUploadError, setPdfUploadError] = useState<string | null>(null);

  // Formulario de configuración de IA
  const [aiProvider, setAiProvider] = useState('local_rag');
  const [openaiKey, setOpenaiKey] = useState('');
  const [geminiKey, setGeminiKey] = useState('');
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoggingIn(true);
    setLoginError('');

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: loginEmail, password: loginPassword })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Credenciales incorrectas');

      sessionStorage.setItem('asistia_admin_token', data.token);
      sessionStorage.setItem('asistia_admin_user', JSON.stringify(data.user));
      setAdminToken(data.token);
      setAdminUser(data.user);
      loadData(data.token);
    } catch (err: any) {
      setLoginError(err.message || 'Error al iniciar sesión');
    } finally {
      setIsLoggingIn(false);
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('asistia_admin_token');
    sessionStorage.removeItem('asistia_admin_user');
    setAdminToken(null);
    setAdminUser(null);
  };

  const loadData = async (token?: string) => {
    setIsRefreshing(true);
    try {
      const authHeader = (token || adminToken) ? { 'Authorization': `Bearer ${token || adminToken}` } : {};

      const requests: Promise<Response>[] = [
        fetch('/api/admin/metrics', { headers: authHeader }),
        fetch('/api/admin/knowledge-base', { headers: authHeader }),
        fetch('/api/admin/settings', { headers: authHeader })
      ];

      // Verificar si es SuperAdmin para cargar el directorio de usuarios
      const effectiveUser = token ? JSON.parse(sessionStorage.getItem('asistia_admin_user') || '{}') : adminUser;
      if (effectiveUser?.role === 'SuperAdmin') {
        requests.push(fetch('/api/admin/users', { headers: authHeader }));
      }

      const results = await Promise.all(requests);

      if (results[0].ok) setMetrics(await results[0].json());
      if (results[1].ok) setKnowledgeList(await results[1].json());
      if (results[2].ok) {
        const s = await results[2].json();
        setSettingsData(s);
        setAiProvider(s.AI_PROVIDER || 'local_rag');
      }
      if (results[3] && results[3].ok) {
        setUsersList(await results[3].json());
      }
    } catch (e) {
      console.error('Error cargando analíticas:', e);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setUserError('');
    setUserSuccess('');
    try {
      const res = await fetch('/api/admin/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${adminToken}`
        },
        body: JSON.stringify(newUser)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al registrar funcionario');

      setUserSuccess(`Funcionario ${data.full_name} (${data.email}) registrado exitosamente.`);
      setNewUser({ email: '', full_name: '', password: '', role: 'Operario' });
      setShowAddUserModal(false);
      loadData();
      setTimeout(() => setUserSuccess(''), 4000);
    } catch (err: any) {
      setUserError(err.message || 'Error registrando funcionario');
    }
  };

  const handleDeleteUser = async (userId: number, userFullName: string) => {
    if (!confirm(`¿Estás seguro de desvincular a ${userFullName}? Esta acción revocará de inmediato sus credenciales de acceso a AsistIA.`)) return;
    try {
      const res = await fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${adminToken}` }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error al eliminar funcionario');
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  useEffect(() => {
    if (adminToken) {
      loadData();
      const interval = setInterval(() => loadData(), 20000);
      return () => clearInterval(interval);
    }
  }, [adminToken]);

  const handleSaveSettings = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/admin/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${adminToken}`
        },
        body: JSON.stringify({
          AI_PROVIDER: aiProvider,
          OPENAI_API_KEY: openaiKey,
          GEMINI_API_KEY: geminiKey
        })
      });
      if (res.ok) {
        setSaveSuccess(true);
        setTimeout(() => setSaveSuccess(false), 3000);
        loadData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleUploadPdf = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pdfFile) return;

    setIsUploadingPdf(true);
    setPdfUploadSuccess(null);
    setPdfUploadError(null);

    const formData = new FormData();
    formData.append('file', pdfFile);
    formData.append('division', pdfDivision);

    try {
      const res = await fetch('/api/admin/upload-pdf', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${adminToken}`
        },
        body: formData
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Error procesando archivo');

      setPdfUploadSuccess(data.message);
      setPdfFile(null);
      loadData();
    } catch (err: any) {
      setPdfUploadError(err.message || 'Error al subir el archivo');
    } finally {
      setIsUploadingPdf(false);
    }
  };

  const handleCreateArticle = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newArticle.title || !newArticle.content) return;

    try {
      const res = await fetch('/api/admin/knowledge-base', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${adminToken}`
        },
        body: JSON.stringify(newArticle)
      });
      if (res.ok) {
        setShowAddArticleModal(false);
        setNewArticle({
          division: 'Admisiones y Mercadeo',
          category: 'General',
          title: '',
          content: '',
          keywords: '',
          contact_email: 'admisiones@teinco.edu.co',
          contact_phone: '+57 601 7433200',
          office_location: 'Sede Principal Calle 57 No. 9-28',
          schedule: 'Lunes a Viernes 7:00 a.m. a 10:00 p.m.'
        });
        loadData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteArticle = async (id: number) => {
    if (!confirm('¿Eliminar este artículo institucional? El motor RAG se actualizará automáticamente.')) return;
    try {
      const res = await fetch(`/api/admin/knowledge-base/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${adminToken}` }
      });
      if (res.ok) loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleStartEdit = (article: KnowledgeArticle) => {
    setEditArticle({ ...article });
    setShowEditArticleModal(true);
  };

  const handleUpdateArticle = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editArticle) return;
    try {
      const res = await fetch(`/api/admin/knowledge-base/${editArticle.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${adminToken}`
        },
        body: JSON.stringify(editArticle)
      });
      if (res.ok) {
        setShowEditArticleModal(false);
        setEditArticle(null);
        loadData();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleClearHistory = async () => {
    if (!confirm('¿Estás seguro de reiniciar el historial de consultas de prueba? Esto pondrá los contadores en cero para una nueva sesión limpia.')) return;
    try {
      const res = await fetch('/api/admin/clear-history', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${adminToken}` }
      });
      if (res.ok) loadData();
    } catch (err) {
      console.error(err);
    }
  };

  // Filtrado de auditoría
  const filteredInteractions = (metrics?.recent_interactions || []).filter(item => {
    const matchesDiv = selectedDivisionFilter === 'all' || item.detected_division === selectedDivisionFilter;
    const matchesSearch =
      searchQuery === '' ||
      item.user_query.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.ai_reply.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.user_role.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDiv && matchesSearch;
  });

  // PANTALLA DE LOGIN SI NO HAY SESIÓN ACTIVA
  if (!adminToken) {
    return (
      <div className="max-w-md mx-auto px-4 py-12 animate-fade-in">
        <div className="bg-white/95 backdrop-blur-md p-8 rounded-3xl border border-slate-200/90 shadow-xl space-y-6">
          <div className="text-center space-y-3">
            <img src="/teinco_logo.png" alt="TEINCO" className="h-12 mx-auto object-contain" />
            <div>
              <h2 className="text-xl font-black text-slate-900 tracking-tight">Portal Administrativo</h2>
              <p className="text-xs text-slate-500 font-medium mt-0.5">Monitoreo y Analítica de AsistIA TEINCO</p>
            </div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-900 text-[11px] font-bold">
              <Lock className="w-3.5 h-3.5 text-amber-600" />
              <span>Acceso Restringido a Coordinadores</span>
            </div>
          </div>

          {loginError && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs font-semibold flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{loginError}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Correo Institucional
              </label>
              <input
                type="email"
                required
                value={loginEmail}
                onChange={e => setLoginEmail(e.target.value)}
                placeholder="admin@teinco.edu.co"
                className="w-full px-3.5 py-2.5 text-xs rounded-xl border border-slate-300 focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
                Contraseña
              </label>
              <input
                type="password"
                required
                value={loginPassword}
                onChange={e => setLoginPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 text-xs rounded-xl border border-slate-300 focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
              />
            </div>

            <button
              type="submit"
              disabled={isLoggingIn}
              className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition-colors shadow-sm disabled:opacity-50"
            >
              {isLoggingIn ? 'Verificando...' : 'Ingresar al Panel'}
            </button>
          </form>

          <div className="p-3 bg-blue-50/80 rounded-xl border border-blue-200/80 text-[11px] text-blue-900 space-y-1">
            <span className="font-bold flex items-center gap-1">
              <Info className="w-3.5 h-3.5 text-blue-600" /> Credenciales de demostración para jurados:
            </span>
            <p><strong>Usuario:</strong> <code>admin@teinco.edu.co</code></p>
            <p><strong>Clave:</strong> <code>Teinco2026*</code></p>
          </div>
        </div>
      </div>
    );
  }

  // PANTALLA PRINCIPAL DEL DASHBOARD (AUTENTICADO)
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 space-y-5 animate-fade-in">
      
      {/* Cabecera del Panel con Usuario y Cerrar Sesión */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white/95 backdrop-blur-md p-4 sm:p-5 rounded-2xl border border-slate-200/90 shadow-sm">
        <div className="flex items-center gap-3">
          <img src="/teinco_logo.png" alt="TEINCO" className="h-10 w-auto object-contain hidden sm:block" />
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">Panel Gerencial y Monitoreo</h1>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
                En Vivo
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2 mt-0.5">
              <p className="text-xs text-slate-500">
                Sesión activa: <strong className="text-blue-900">{adminUser?.name || 'Coordinación TEINCO'}</strong> ({adminUser?.email})
              </p>
              <span className={`px-2 py-0.5 rounded-md text-[10px] font-black uppercase tracking-wider ${
                adminUser?.role === 'SuperAdmin'
                  ? 'bg-purple-100 text-purple-900 border border-purple-200'
                  : 'bg-emerald-100 text-emerald-900 border border-emerald-200'
              }`}>
                {adminUser?.role === 'SuperAdmin' ? '👑 Super Administrador' : '👤 Operario / Supervisor'}
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => loadData()}
            disabled={isRefreshing}
            className="p-2 rounded-xl border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors"
            title="Refrescar datos"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </button>

          <a
            href="/api/admin/export-csv"
            download
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-all text-xs font-bold shadow-xs"
          >
            <FileSpreadsheet className="w-4 h-4 text-emerald-300" />
            <span>Exportar CSV</span>
          </a>

          <button
            onClick={handleClearHistory}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-200 border border-slate-200 text-xs font-bold transition-all"
            title="Reiniciar contador de consultas de prueba"
          >
            <Trash2 className="w-4 h-4 text-slate-400" />
            <span className="hidden sm:inline">Limpiar Pruebas</span>
          </button>

          <button
            onClick={handleLogout}
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-100 text-slate-700 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-200 border border-slate-200 text-xs font-bold transition-all"
            title="Cerrar sesión"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Salir</span>
          </button>
        </div>
      </div>

      {/* Tarjetas KPI Superiores con Gradientes Pasteles */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="bg-gradient-to-br from-blue-50/90 to-indigo-50/50 p-4.5 rounded-2xl border border-blue-200/80 shadow-xs flex items-center gap-3.5">
          <div className="w-11 h-11 rounded-xl bg-white text-blue-700 flex items-center justify-center shrink-0 shadow-2xs border border-blue-200">
            <BarChart3 className="w-5 h-5" />
          </div>
          <div>
            <p className="text-[10px] font-bold text-blue-900 uppercase tracking-wider">Consultas Atendidas</p>
            <h3 className="text-xl font-black text-slate-900 mt-0.5">{metrics?.total_queries ?? 0}</h3>
            <p className="text-[10px] text-emerald-700 font-semibold flex items-center gap-1 mt-0.5">
              <TrendingUp className="w-3 h-3 text-emerald-600" /> Atención 24/7 en línea
            </p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-emerald-50/90 to-teal-50/50 p-4.5 rounded-2xl border border-emerald-200/80 shadow-xs flex items-center gap-3.5">
          <div className="w-11 h-11 rounded-xl bg-white text-emerald-700 flex items-center justify-center shrink-0 shadow-2xs border border-emerald-200">
            <ThumbsUp className="w-5 h-5" />
          </div>
          <div>
            <p className="text-[10px] font-bold text-emerald-900 uppercase tracking-wider">Satisfacción Estudiantil</p>
            <h3 className="text-xl font-black text-slate-900 mt-0.5">{metrics?.satisfaction_rate ?? 100}%</h3>
            <p className="text-[10px] text-emerald-800 font-medium mt-0.5">
              {metrics?.positive_feedback ?? 0} valoraciones positivas
            </p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-amber-50/90 to-orange-50/50 p-4.5 rounded-2xl border border-amber-200/80 shadow-xs flex items-center gap-3.5">
          <div className="w-11 h-11 rounded-xl bg-white text-amber-700 flex items-center justify-center shrink-0 shadow-2xs border border-amber-200">
            <Clock className="w-5 h-5" />
          </div>
          <div>
            <p className="text-[10px] font-bold text-amber-900 uppercase tracking-wider">Tiempo Promedio</p>
            <h3 className="text-xl font-black text-slate-900 mt-0.5">{metrics?.avg_response_time_ms ?? 0} ms</h3>
            <p className="text-[10px] text-amber-800 font-semibold mt-0.5">
              Meta institucional &lt; 2000 ms
            </p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-50/90 to-violet-50/50 p-4.5 rounded-2xl border border-purple-200/80 shadow-xs flex items-center gap-3.5">
          <div className="w-11 h-11 rounded-xl bg-white text-purple-700 flex items-center justify-center shrink-0 shadow-2xs border border-purple-200">
            <Users className="w-5 h-5" />
          </div>
          <div>
            <p className="text-[10px] font-bold text-purple-900 uppercase tracking-wider">Sesiones Únicas</p>
            <h3 className="text-xl font-black text-slate-900 mt-0.5">{metrics?.total_sessions ?? 0}</h3>
            <p className="text-[10px] text-purple-800 font-medium mt-0.5">
              Estudiantes, aspirantes y docentes
            </p>
          </div>
        </div>

      </div>

      {/* Pestañas de Navegación del Panel */}
      <div className="flex border-b border-slate-200 space-x-3 bg-white/70 p-1.5 rounded-xl">
        <button
          onClick={() => setActiveSubTab('analytics')}
          className={`px-3 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
            activeSubTab === 'analytics'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
          }`}
        >
          <BarChart3 className="w-4 h-4" />
          <span>Analítica y Auditoría</span>
        </button>

        <button
          onClick={() => setActiveSubTab('knowledge')}
          className={`px-3 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
            activeSubTab === 'knowledge'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
          }`}
        >
          <Building2 className="w-4 h-4" />
          <span>Base de Conocimiento y PDFs ({knowledgeList.length})</span>
        </button>

        <button
          onClick={() => setActiveSubTab('settings')}
          className={`px-3 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
            activeSubTab === 'settings'
              ? 'bg-blue-600 text-white shadow-xs'
              : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
          }`}
        >
          <Settings className="w-4 h-4" />
          <span>Motor de IA Generativa</span>
        </button>

        {adminUser?.role === 'SuperAdmin' && (
          <button
            onClick={() => setActiveSubTab('users')}
            className={`px-3 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
              activeSubTab === 'users'
                ? 'bg-purple-600 text-white shadow-xs'
                : 'text-purple-700 hover:text-purple-900 hover:bg-purple-50'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Gestión de Funcionarios ({usersList.length})</span>
          </button>
        )}
      </div>

      {/* VISTA 1: ANALÍTICA Y AUDITORÍA */}
      {activeSubTab === 'analytics' && (
        <div className="space-y-5">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            
            <div className="lg:col-span-2 bg-white/95 p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-black text-slate-900">Demanda por División Institucional</h3>
                  <p className="text-xs text-slate-500">Distribución de preguntas dirigidas hacia las diferentes áreas de TEINCO</p>
                </div>
                <Building2 className="w-5 h-5 text-blue-600" />
              </div>

              <div className="space-y-3 pt-2">
                {metrics && Object.keys(metrics.queries_by_division).length > 0 ? (
                  Object.entries(metrics.queries_by_division).map(([division, count]) => {
                    const total = metrics.total_queries || 1;
                    const percent = Math.round((count / total) * 100);
                    return (
                      <div key={division} className="space-y-1">
                        <div className="flex justify-between text-xs font-semibold text-slate-700">
                          <span className="flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full bg-blue-600" />
                            {division}
                          </span>
                          <span className="text-slate-500">
                            {count} consultas ({percent}%)
                          </span>
                        </div>
                        <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                          <div
                            className="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                            style={{ width: `${percent}%` }}
                          />
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <p className="text-sm text-slate-400 py-6 text-center">No hay registros de consultas aún.</p>
                )}
              </div>
            </div>

            <div className="bg-white/95 p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-4">
              <div>
                <h3 className="text-sm font-black text-slate-900">Perfil de la Comunidad</h3>
                <p className="text-xs text-slate-500">Usuarios que interactúan con AsistIA</p>
              </div>

              <div className="space-y-2.5 pt-2">
                {metrics && Object.keys(metrics.queries_by_role).length > 0 ? (
                  Object.entries(metrics.queries_by_role).map(([role, count]) => {
                    const total = metrics.total_queries || 1;
                    const percent = Math.round((count / total) * 100);
                    return (
                      <div key={role} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-200/70">
                        <div className="capitalize font-bold text-xs text-slate-800">
                          {role}
                        </div>
                        <div className="text-right">
                          <div className="text-xs font-bold text-blue-700">{count} consultas</div>
                          <div className="text-[10px] text-slate-400">{percent}% del total</div>
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <p className="text-sm text-slate-400 py-6 text-center">Esperando interacciones...</p>
                )}
              </div>
            </div>

          </div>

          {/* Bitácora de Auditoría */}
          <div className="bg-white/95 p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-black text-slate-900">Bitácora de Auditoría de Consultas</h3>
                <p className="text-xs text-slate-500">
                  Registro anonimizado en tiempo real (Protección de identidad Ley 1581 de 2012)
                </p>
              </div>

              <div className="flex items-center gap-2">
                <div className="relative">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    placeholder="Buscar en bitácora..."
                    className="pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-blue-600"
                  />
                </div>

                <select
                  value={selectedDivisionFilter}
                  onChange={e => setSelectedDivisionFilter(e.target.value)}
                  className="text-xs py-1.5 px-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-blue-600"
                >
                  <option value="all">Todas las dependencias</option>
                  <option value="Admisiones y Mercadeo">Admisiones</option>
                  <option value="Registro y Control">Registro y Control</option>
                  <option value="Bienestar Institucional">Bienestar</option>
                  <option value="Cartera y Financiación">Cartera</option>
                  <option value="Coordinación Académica">Coordinación</option>
                  <option value="Soporte y Sistemas">Sistemas</option>
                </select>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-600 uppercase font-bold border-y border-slate-200">
                  <tr>
                    <th className="py-2.5 px-3">Hora</th>
                    <th className="py-2.5 px-3">Rol</th>
                    <th className="py-2.5 px-3">Consulta (Sanitizada)</th>
                    <th className="py-2.5 px-3">División Detectada</th>
                    <th className="py-2.5 px-3">Confianza</th>
                    <th className="py-2.5 px-3">Tiempo</th>
                    <th className="py-2.5 px-3">Satisfacción</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredInteractions.map(item => (
                    <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                      <td className="py-2.5 px-3 text-slate-500 whitespace-nowrap">
                        {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </td>
                      <td className="py-2.5 px-3">
                        <span className="capitalize px-2 py-0.5 rounded-md bg-slate-100 font-semibold text-slate-700">
                          {item.user_role}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 max-w-xs truncate text-slate-800 font-medium" title={item.user_query}>
                        {item.user_query}
                      </td>
                      <td className="py-2.5 px-3 whitespace-nowrap">
                        <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-blue-50 text-blue-800 border border-blue-200">
                          {item.detected_division}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-emerald-700 font-bold whitespace-nowrap">
                        {Math.round(item.confidence_score * 100)}%
                      </td>
                      <td className="py-2.5 px-3 text-slate-500 whitespace-nowrap">
                        {item.response_time_ms} ms
                      </td>
                      <td className="py-2.5 px-3 whitespace-nowrap">
                        {item.is_helpful === true ? (
                          <span className="text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Útil</span>
                        ) : item.is_helpful === false ? (
                          <span className="text-rose-700 font-bold bg-rose-50 px-2 py-0.5 rounded border border-rose-200">No útil</span>
                        ) : (
                          <span className="text-slate-400">Sin calificar</span>
                        )}
                      </td>
                    </tr>
                  ))}
                  {filteredInteractions.length === 0 && (
                    <tr>
                      <td colSpan={7} className="text-center py-8 text-slate-400">
                        No se encontraron registros de auditoría que coincidan con la búsqueda.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* VISTA 2: BASE DE CONOCIMIENTO Y SUBIDA DE PDFS */}
      {activeSubTab === 'knowledge' && (
        <div className="space-y-5">
          
          {/* Subida de Documentos PDF */}
          <div className="bg-white/95 p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-4">
            <div>
              <h3 className="text-sm font-black text-slate-900 flex items-center gap-2">
                <Upload className="w-4 h-4 text-amber-600" />
                Ingesta Automática de Documentos y Reglamentos en PDF
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Carga circulares, reglamentos o calendarios oficiales en formato PDF. El sistema extraerá el texto, lo fragmentará y lo indexará automáticamente en el motor RAG.
              </p>
            </div>

            {pdfUploadSuccess && (
              <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-semibold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>{pdfUploadSuccess}</span>
              </div>
            )}

            {pdfUploadError && (
              <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl text-xs font-semibold flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>{pdfUploadError}</span>
              </div>
            )}

            <form onSubmit={handleUploadPdf} className="grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Dependencia Responsable
                </label>
                <select
                  value={pdfDivision}
                  onChange={e => setPdfDivision(e.target.value)}
                  className="w-full px-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:border-blue-600 bg-white"
                >
                  <option value="Registro y Control">Registro y Control</option>
                  <option value="Admisiones y Mercadeo">Admisiones y Mercadeo</option>
                  <option value="Bienestar Institucional">Bienestar Institucional</option>
                  <option value="Cartera y Financiación">Cartera y Financiación</option>
                  <option value="Coordinación Académica">Coordinación Académica</option>
                  <option value="Soporte y Sistemas">Soporte y Sistemas</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">
                  Seleccionar Archivo PDF (.pdf)
                </label>
                <input
                  type="file"
                  accept=".pdf"
                  required
                  onChange={e => setPdfFile(e.target.files?.[0] || null)}
                  className="w-full text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer border border-slate-300 rounded-xl p-1"
                />
              </div>

              <button
                type="submit"
                disabled={!pdfFile || isUploadingPdf}
                className="py-2.5 px-4 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs transition-colors shadow-xs disabled:opacity-50 flex items-center justify-center gap-1.5"
              >
                <Upload className="w-4 h-4" />
                <span>{isUploadingPdf ? 'Extrayendo e Indexando...' : 'Indexar Documento en RAG'}</span>
              </button>
            </form>
          </div>

          {/* Lista de Artículos */}
          <div className="bg-white/95 p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="text-sm font-black text-slate-900">Base de Conocimiento Indexada ({knowledgeList.length} secciones)</h3>
                <p className="text-xs text-slate-500">Documentación consultada por AsistIA para generar respuestas oficiales</p>
              </div>
              <button
                onClick={() => setShowAddArticleModal(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-all text-xs font-bold shadow-xs"
              >
                <Plus className="w-4 h-4" /> Nuevo Trámite Manual
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              {knowledgeList.map(art => (
                <div key={art.id} className="bg-slate-50/70 p-4 rounded-2xl border border-slate-200/80 shadow-2xs flex flex-col justify-between space-y-2">
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-blue-50 text-blue-800 border border-blue-200">
                        {art.division}
                      </span>
                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => handleStartEdit(art)}
                          className="text-slate-400 hover:text-blue-600 p-1 rounded transition-colors"
                          title="Editar trámite"
                        >
                          <Pencil className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDeleteArticle(art.id)}
                          className="text-slate-400 hover:text-rose-600 p-1 rounded transition-colors"
                          title="Eliminar artículo"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                    <h4 className="font-bold text-xs text-slate-900 mb-1">{art.title}</h4>
                    <p className="text-xs text-slate-600 leading-relaxed line-clamp-3">
                      {art.content}
                    </p>
                  </div>

                  <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between text-[10px] text-slate-400 font-medium">
                    <span>{art.category}</span>
                    <span className="truncate max-w-[160px] text-blue-700">{art.contact_email}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

      {/* VISTA 3: CONFIGURACIÓN MOTOR DE IA Y GUÍA GEMINI */}
      {activeSubTab === 'settings' && (
        <div className="max-w-3xl mx-auto space-y-5">
          
          {/* Guía Visual: Cómo obtener la clave gratuita de Google Gemini */}
          <div className="bg-gradient-to-br from-blue-50 via-indigo-50/50 to-amber-50/30 p-5 rounded-3xl border border-blue-200/80 shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-amber-500" />
                <h3 className="text-sm font-black text-blue-950">
                  ¿Cómo obtener tu clave gratuita de Google Gemini en 2 minutos?
                </h3>
              </div>
              <a
                href="https://aistudio.google.com/app/apikey"
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1 px-3 py-1 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition-colors shadow-2xs"
              >
                <span>Abrir Google AI Studio</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              Google ofrece acceso <strong>100% gratuito</strong> a Gemini 1.5 Flash sin pedir tarjetas de crédito. Sigue estos 3 pasos:
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div className="p-3 bg-white rounded-2xl border border-blue-100 shadow-2xs space-y-1">
                <div className="font-extrabold text-blue-700 flex items-center gap-1.5">
                  <span className="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center text-[11px]">1</span>
                  Inicia Sesión
                </div>
                <p className="text-[11px] text-slate-500 leading-snug">
                  Entra a Google AI Studio con tu cuenta habitual de Gmail.
                </p>
              </div>

              <div className="p-3 bg-white rounded-2xl border border-blue-100 shadow-2xs space-y-1">
                <div className="font-extrabold text-amber-700 flex items-center gap-1.5">
                  <span className="w-5 h-5 rounded-full bg-amber-100 flex items-center justify-center text-[11px]">2</span>
                  Crear API Key
                </div>
                <p className="text-[11px] text-slate-500 leading-snug">
                  Haz clic en el botón azul <strong>"Create API Key"</strong> y selecciona un proyecto.
                </p>
              </div>

              <div className="p-3 bg-white rounded-2xl border border-blue-100 shadow-2xs space-y-1">
                <div className="font-extrabold text-emerald-700 flex items-center gap-1.5">
                  <span className="w-5 h-5 rounded-full bg-emerald-100 flex items-center justify-center text-[11px]">3</span>
                  Pega y Guarda
                </div>
                <p className="text-[11px] text-slate-500 leading-snug">
                  Copia tu clave (empieza por <code>AIza...</code>), pégala abajo y dale a <strong>Guardar</strong>.
                </p>
              </div>
            </div>
          </div>

          {/* Formulario de Configuración del Motor */}
          <div className="bg-white/95 p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-5">
            <div>
              <h3 className="text-base font-black text-slate-900 flex items-center gap-2">
                <Sliders className="w-5 h-5 text-blue-600" />
                Selector del Motor de IA Generativa
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Puedes cambiar el motor en tiempo de ejecución sin reiniciar el servidor.
              </p>
            </div>

            {saveSuccess && (
              <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-semibold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Configuración guardada y aplicada en caliente exitosamente.</span>
              </div>
            )}

            <form onSubmit={handleSaveSettings} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                  Motor de Inferencia
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div
                    onClick={() => setAiProvider('local_rag')}
                    className={`p-3.5 rounded-2xl border-2 cursor-pointer transition-all ${
                      aiProvider === 'local_rag'
                        ? 'border-blue-600 bg-blue-50/60 shadow-xs'
                        : 'border-slate-200 hover:border-slate-300 bg-white'
                    }`}
                  >
                    <div className="font-bold text-xs text-slate-900">RAG Semántico Local</div>
                    <p className="text-[11px] text-slate-500 mt-0.5">100% gratuito, offline, latencia &lt; 5 ms.</p>
                  </div>

                  <div
                    onClick={() => setAiProvider('gemini')}
                    className={`p-3.5 rounded-2xl border-2 cursor-pointer transition-all ${
                      aiProvider === 'gemini'
                        ? 'border-blue-600 bg-blue-50/60 shadow-xs'
                        : 'border-slate-200 hover:border-slate-300 bg-white'
                    }`}
                  >
                    <div className="font-bold text-xs text-slate-900 flex items-center gap-1">
                      <span>Google Gemini</span>
                      <span className="text-[9px] bg-amber-100 text-amber-800 px-1 py-0.2 rounded font-black">Gratis</span>
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5">Gemini 1.5 Flash. Máxima fluidez natural.</p>
                  </div>

                  <div
                    onClick={() => setAiProvider('openai')}
                    className={`p-3.5 rounded-2xl border-2 cursor-pointer transition-all ${
                      aiProvider === 'openai'
                        ? 'border-blue-600 bg-blue-50/60 shadow-xs'
                        : 'border-slate-200 hover:border-slate-300 bg-white'
                    }`}
                  >
                    <div className="font-bold text-xs text-slate-900">OpenAI GPT-4o</div>
                    <p className="text-[11px] text-slate-500 mt-0.5">Modelo GPT-4o-mini institucional.</p>
                  </div>
                </div>
              </div>

              {aiProvider === 'gemini' && (
                <div className="space-y-1">
                  <label className="block text-xs font-bold text-slate-700">Google Gemini API Key</label>
                  <div className="relative">
                    <KeyRound className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                    <input
                      type="password"
                      value={geminiKey}
                      onChange={e => setGeminiKey(e.target.value)}
                      placeholder={settingsData?.HAS_GEMINI_KEY ? `Configurada: ${settingsData.GEMINI_API_KEY_MASKED}` : 'Pega tu clave AIza...'}
                      className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:border-blue-600"
                    />
                  </div>
                </div>
              )}

              {aiProvider === 'openai' && (
                <div className="space-y-1">
                  <label className="block text-xs font-bold text-slate-700">OpenAI API Key</label>
                  <div className="relative">
                    <KeyRound className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                    <input
                      type="password"
                      value={openaiKey}
                      onChange={e => setOpenaiKey(e.target.value)}
                      placeholder={settingsData?.HAS_OPENAI_KEY ? `Configurada: ${settingsData.OPENAI_API_KEY_MASKED}` : 'sk-...'}
                      className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-300 focus:outline-none focus:border-blue-600"
                    />
                  </div>
                </div>
              )}

              <div className="pt-2 flex justify-end">
                <button
                  type="submit"
                  className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl transition-all shadow-xs"
                >
                  Guardar Configuración de IA
                </button>
              </div>
            </form>
          </div>

        </div>
      )}

      {/* VISTA 4: GESTIÓN DE FUNCIONARIOS Y ROLES (RBAC - EXCLUSIVO SUPERADMIN) */}
      {activeSubTab === 'users' && adminUser?.role === 'SuperAdmin' && (
        <div className="space-y-5 animate-fade-in">
          {userSuccess && (
            <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>{userSuccess}</span>
            </div>
          )}

          {userError && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-800 rounded-xl text-xs font-bold flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
              <span>{userError}</span>
            </div>
          )}

          <div className="bg-white/95 p-6 rounded-2xl border border-slate-200/90 shadow-xs space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-base font-black text-slate-900 flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-purple-600" />
                  Control de Funcionarios y Permisos Institucionales (RBAC)
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Módulo exclusivo de Rectoría y Vicerrectoría. Permite registrar nuevos coordinadores o desvincular al personal saliente.
                </p>
              </div>

              <button
                onClick={() => setShowAddUserModal(true)}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs transition-all shadow-xs"
              >
                <UserPlus className="w-4 h-4" />
                <span>+ Nuevo Funcionario</span>
              </button>
            </div>

            {/* Tabla de Usuarios */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                    <th className="py-3 px-3">Funcionario</th>
                    <th className="py-3 px-3">Correo Institucional</th>
                    <th className="py-3 px-3">Rol / Nivel de Acceso</th>
                    <th className="py-3 px-3">Estado</th>
                    <th className="py-3 px-3">Fecha de Registro</th>
                    <th className="py-3 px-3 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
                  {usersList.map(u => {
                    const isSelf = u.email.toLowerCase() === adminUser?.email?.toLowerCase();
                    return (
                      <tr key={u.id} className="hover:bg-slate-50/80 transition-colors">
                        <td className="py-3 px-3 font-bold text-slate-900 flex items-center gap-2">
                          <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-black ${
                            u.role === 'SuperAdmin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                          }`}>
                            {u.full_name.charAt(0)}
                          </div>
                          <span>{u.full_name}</span>
                          {isSelf && (
                            <span className="text-[10px] text-purple-600 font-extrabold">(Tú)</span>
                          )}
                        </td>
                        <td className="py-3 px-3 text-slate-600 font-mono text-[11px]">{u.email}</td>
                        <td className="py-3 px-3">
                          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-bold ${
                            u.role === 'SuperAdmin'
                              ? 'bg-purple-50 text-purple-800 border border-purple-200'
                              : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                          }`}>
                            {u.role === 'SuperAdmin' ? 'Super Administrador (Rectoría)' : 'Operario / Consultas'}
                          </span>
                        </td>
                        <td className="py-3 px-3">
                          <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-700">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                            Activo
                          </span>
                        </td>
                        <td className="py-3 px-3 text-slate-500 text-[11px]">
                          {new Date(u.created_at).toLocaleDateString()}
                        </td>
                        <td className="py-3 px-3 text-right">
                          <button
                            onClick={() => handleDeleteUser(u.id, u.full_name)}
                            disabled={isSelf}
                            className={`p-1.5 rounded-lg border transition-colors ${
                              isSelf
                                ? 'opacity-30 cursor-not-allowed border-slate-200 text-slate-400'
                                : 'hover:bg-rose-50 text-slate-400 hover:text-rose-600 border-slate-200'
                            }`}
                            title={isSelf ? 'No puedes eliminar tu propia cuenta activa' : 'Desvincular funcionario'}
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}


      {/* Modal para Agregar Artículo Manual */}
      {showAddArticleModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-200">
            <h3 className="text-base font-black text-slate-900 mb-3">
              Registrar Trámite Manual en Base de Conocimiento
            </h3>
            <form onSubmit={handleCreateArticle} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Dependencia</label>
                <select
                  value={newArticle.division}
                  onChange={e => setNewArticle({ ...newArticle, division: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300"
                >
                  <option value="Admisiones y Mercadeo">Admisiones y Mercadeo</option>
                  <option value="Registro y Control">Registro y Control</option>
                  <option value="Bienestar Institucional">Bienestar Institucional</option>
                  <option value="Cartera y Financiación">Cartera y Financiación</option>
                  <option value="Coordinación Académica">Coordinación Académica</option>
                  <option value="Soporte y Sistemas">Soporte y Sistemas</option>
                </select>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Título</label>
                <input
                  type="text"
                  required
                  placeholder="Ej. Trámite de Paz y Salvo"
                  value={newArticle.title}
                  onChange={e => setNewArticle({ ...newArticle, title: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Contenido Normativo</label>
                <textarea
                  required
                  rows={4}
                  placeholder="Describe los pasos y requisitos..."
                  value={newArticle.content}
                  onChange={e => setNewArticle({ ...newArticle, content: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddArticleModal(false)}
                  className="px-4 py-2 border border-slate-300 rounded-xl font-bold text-slate-600 hover:bg-slate-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl"
                >
                  Guardar en RAG
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para Editar Artículo Existente */}
      {showEditArticleModal && editArticle && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <h3 className="text-base font-black text-slate-900 flex items-center gap-2">
                <Pencil className="w-4 h-4 text-blue-600" />
                Editar Trámite Institucional
              </h3>
              <button
                type="button"
                onClick={() => setShowEditArticleModal(false)}
                className="text-slate-400 hover:text-slate-700 text-xs font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleUpdateArticle} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Dependencia Responsable</label>
                <select
                  value={editArticle.division}
                  onChange={e => setEditArticle({ ...editArticle, division: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300"
                >
                  <option value="Admisiones y Mercadeo">Admisiones y Mercadeo</option>
                  <option value="Registro y Control">Registro y Control</option>
                  <option value="Bienestar Institucional">Bienestar Institucional</option>
                  <option value="Cartera y Financiación">Cartera y Financiación</option>
                  <option value="Coordinación Académica">Coordinación Académica</option>
                  <option value="Soporte y Sistemas">Soporte y Sistemas</option>
                </select>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Título del Trámite</label>
                <input
                  type="text"
                  required
                  value={editArticle.title}
                  onChange={e => setEditArticle({ ...editArticle, title: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300 font-semibold"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Categoría</label>
                <input
                  type="text"
                  value={editArticle.category}
                  onChange={e => setEditArticle({ ...editArticle, category: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Contenido Normativo y Pasos</label>
                <textarea
                  required
                  rows={6}
                  value={editArticle.content}
                  onChange={e => setEditArticle({ ...editArticle, content: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300 leading-relaxed font-normal"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowEditArticleModal(false)}
                  className="px-4 py-2 border border-slate-300 rounded-xl font-bold text-slate-600 hover:bg-slate-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-xs"
                >
                  Actualizar y Sincronizar en RAG
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para Registrar Nuevo Funcionario (RBAC) */}
      {showAddUserModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <h3 className="text-base font-black text-slate-900 flex items-center gap-2">
                <UserPlus className="w-4 h-4 text-purple-600" />
                Registrar Nuevo Funcionario Institucional
              </h3>
              <button
                type="button"
                onClick={() => setShowAddUserModal(false)}
                className="text-slate-400 hover:text-slate-700 text-xs font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateUser} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Nombre Completo y Cargo</label>
                <input
                  type="text"
                  required
                  placeholder="Ej: Dra. Sandra Milena Pérez - Vicerrectora"
                  value={newUser.full_name}
                  onChange={e => setNewUser({ ...newUser, full_name: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300 font-medium"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Correo Electrónico Institucional</label>
                <input
                  type="email"
                  required
                  placeholder="funcionario@teinco.edu.co"
                  value={newUser.email}
                  onChange={e => setNewUser({ ...newUser, email: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300 font-medium"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Contraseña Inicial</label>
                <input
                  type="password"
                  required
                  placeholder="Mínimo 6 caracteres"
                  value={newUser.password}
                  onChange={e => setNewUser({ ...newUser, password: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300"
                />
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Rol y Nivel de Privilegios</label>
                <select
                  value={newUser.role}
                  onChange={e => setNewUser({ ...newUser, role: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-300 font-bold"
                >
                  <option value="Operario">Operario / Supervisor (Consultas, Métricas y Reglamentos)</option>
                  <option value="SuperAdmin">Super Administrador (Rectoría / Vicerrectoría - Control Total)</option>
                </select>
                <p className="text-[10px] text-slate-500 mt-1">
                  * Los <strong>Operarios</strong> pueden consultar métricas y subir reglamentos, pero NO tienen permisos para crear ni eliminar personal.
                </p>
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddUserModal(false)}
                  className="px-4 py-2 border border-slate-300 rounded-xl font-bold text-slate-600 hover:bg-slate-50"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow-xs"
                >
                  Vincular Funcionario
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
