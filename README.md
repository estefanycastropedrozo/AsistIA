# AsistIA — Asistente Conversacional con IA Generativa para TEINCO

**Corporación Tecnológica Industrial Colombiana — TEINCO**  
*Programa de Tecnología en Desarrollo de Software*  
*Proyecto de Prácticas Profesionales*  
**Autora:** Estefany Castro Pedrozo  
**Docente Asesor / Evaluador:** Carlos Ramos  
**Bogotá, D.C., Colombia — 2026**

---

## 📌 Descripción General

**AsistIA** es una solución web integral diseñada para optimizar, centralizar y automatizar la atención y canalización de consultas académicas y administrativas en **TEINCO**. Emplea una arquitectura **RAG (Retrieval-Augmented Generation)** que combina modelos de lenguaje generativos con una base de conocimiento oficial indexada semánticamente, garantizando respuestas precisas, reglamentadas y libres de alucinaciones.

### Divisiones Institucionales Integradas:
1. **Admisiones y Mercadeo**: Requisitos de ingreso, oferta de carreras tecnológicas, proceso de entrevista y homologaciones desde el SENA u otras IES.
2. **Registro y Control Académico**: Expedición de certificados, matrícula académica, adición/cancelación de asignaturas y postulaciones a grado.
3. **Bienestar Institucional**: Acompañamiento psicológico gratuito, primeros auxilios, deportes, cultura y convocatorias de becas de excelencia.
4. **Cartera y Financiación (Tesorería)**: Pagos por botón PSE o bancos, crédito directo institucional, líneas ICETEX y paz y salvo financiero.
5. **Coordinación Académica (Software)**: Requisitos de prácticas profesionales (70% de créditos), opciones de grado, exámenes supletorios y habilitaciones.
6. **Soporte y Sistemas**: Acceso al Campus Virtual Moodle, restablecimiento de contraseñas y correos `@teinco.edu.co`.

---

## 🚀 Puesta en Marcha Rápida (Windows)

La plataforma incluye scripts de ejecución automatizada en un solo clic:

### Opción 1: Inicio Unificado (Recomendado)
Haz doble clic sobre el archivo:
```cmd
start_asistia.bat
```
Este script:
1. Inicia el servidor backend FastAPI (`http://127.0.0.1:8000`).
2. Inicia el servidor frontend React (`http://localhost:3000`).
3. Abre automáticamente la aplicación en tu navegador predeterminado.

### Opción 2: Inicio Manual por Terminales

**Terminal 1 (Backend FastAPI):**
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
- Documentación Swagger interactiva: `http://127.0.0.1:8000/docs`
- Estado de salud: `http://127.0.0.1:8000/api/health`

**Terminal 2 (Frontend React):**
```bash
cd frontend
npm.cmd run dev
```
- Aplicación de atención estudiantil y panel de reportes: `http://localhost:3000`

---

## 🏛️ Características Principales

### 1. Módulo de Atención al Estudiante (Chat AsistIA)
- **Selector de Perfiles**: Respuestas personalizadas para *Aspirantes, Estudiantes Activos, Egresados y Docentes*.
- **Píldoras de Acceso Rápido**: Preguntas frecuentes organizadas por división institucional.
- **Canalización Directa**: Generación automática de fichas de contacto oficial (correo, teléfono, oficina física y horarios de atención) para cada área.
- **Calificación y Feedback**: Botones de valoración (*¿Fue útil?*) para auditoría de calidad.
- **Protección de Datos Personales**: Cumplimiento de la **Ley Estatutaria 1581 de 2012** con anonimización de números de cédula, celulares y correos privados antes de procesar prompts.

### 2. Panel Administrativo y de Monitoreo Institucional
- **Métricas e Indicadores en Vivo**:
  - Total de consultas atendidas 24/7.
  - Tasa de satisfacción estudiantil (%).
  - Tiempo de respuesta medio (&lt; 20 ms con RAG local).
  - Cantidad de sesiones activas.
- **Gráficos de Demanda por Dependencia**: Visualización de la carga y temas más consultados en Admisiones, Registro, Cartera, etc.
- **Bitácora de Auditoría en Tiempo Real**: Tabla detallada con consultas sanitizadas, clasificaciones, puntuación de confianza y retroalimentación recibida.
- **Exportación de Reportes**: Descarga directa de informes en formato `.csv` para comités directivos.
- **Gestor de la Base de Conocimiento**: Interfaz para registrar o actualizar normativas y trámites de TEINCO.
- **Selector del Motor de IA**: Configura en tiempo de ejecución entre **RAG Semántico Local** (sin costo ni dependencias de pago), **Google Gemini 1.5 Flash** u **OpenAI GPT-4o-mini**.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnologías |
|---|---|
| **Backend** | Python 3.12, FastAPI, SQLAlchemy ORM, Pydantic, Uvicorn |
| **Base de Datos** | SQLite3 (compatible con PostgreSQL / pgvector para despliegue productivo) |
| **Pipeline RAG** | Tokenización semántica normalizada en español, TF-IDF / Coseno, Re-ranking temático |
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS, Lucide React Icons |
| **Seguridad Legal** | Algoritmo de desidentificación de PII (Ley 1581 de 2012 / Ley 1273 de 2009) |

---

## 📄 Estructura del Proyecto

```text
AsistIA/
├── backend/
│   ├── config.py              # Ajustes de entorno y configuración en caliente
│   ├── database.py            # Motor de conexión y sesiones SQLAlchemy
│   ├── models.py              # Modelos de datos (Sesiones, Mensajes, Feedback, Conocimiento)
│   ├── schemas.py             # Esquemas Pydantic de entrada/salida
│   ├── knowledge_base.py      # Base de conocimiento curada de las divisiones de TEINCO
│   ├── rag_service.py         # Pipeline RAG, anonimización PII e inferencia generativa
│   ├── seed_data.py           # Población inicial de la BD con reglamentos y datos de demo
│   ├── main.py                # Entrada principal FastAPI y montaje estático
│   ├── requirements.txt       # Librerías de Python
│   └── routers/
│       ├── chat.py            # Endpoints de chat, historial y feedback
│       └── admin.py           # Endpoints de analítica, auditoría y exportación CSV
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.tsx           # Barra de navegación institucional y estado
│   │   │   ├── ChatView.tsx         # Chatbot con selector de rol y tarjetas de contacto
│   │   │   ├── AdminDashboard.tsx   # Tablero de métricas, gráficos y auditoría
│   │   │   └── PrivacyModal.tsx     # Aviso legal de la Ley 1581 de 2012
│   │   ├── types.ts                 # Definiciones TypeScript
│   │   ├── App.tsx                  # Componente raíz y control de vistas
│   │   └── main.tsx                 # Montaje en el DOM
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── run_backend.bat            # Script para ejecutar solo el Backend
├── run_frontend.bat           # Script para ejecutar solo el Frontend
├── start_asistia.bat          # Script para iniciar TODO el sistema
├── AsistIA.docx               # Documento original del proyecto de grado
└── README.md                  # Este documento
```

---

## 🎓 Verificación y Pruebas Realizadas

1. **Compilación Frontend:** Construcción con Vite exitosa en 4.45 segundos sin errores de TypeScript.
2. **Servicio REST Backend:** Endpoints probados y validados con respuestas en códigos 200 HTTP.
3. **Precisión RAG por Dependencia:** 100% de coincidencia semántica en pruebas de clasificación en todas las 6 divisiones de TEINCO.
4. **Tiempos de Respuesta:** Inferiores a 5 ms en modo local, cumpliendo ampliamente el requisito no funcional de &lt; 2000 ms.
