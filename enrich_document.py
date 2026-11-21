import docx
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_complete_document():
    doc = Document("AsistIA.docx")

    # Localizar el índice del Capítulo 8
    target_idx = -1
    for i, p in enumerate(doc.paragraphs):
        if "Cap" in p.text and "8" in p.text:
            target_idx = i
            break

    if target_idx == -1:
        print("No se encontró el Capítulo 8.")
        return

    # Contenido detallado para el Capítulo 8
    sections = [
        ("Capítulo 8: Especificaciones Técnicas y de Diseño", "Heading 1"),
        (
            "El presente capítulo describe de forma exhaustiva los requerimientos de ingeniería de software, el diseño de la arquitectura computacional, el modelo relacional de datos y las especificaciones de despliegue para la plataforma AsistIA en la Corporación Tecnológica Industrial Colombiana (TEINCO).",
            "Normal"
        ),
        ("8.1 Requerimientos del Sistema", "Heading 2"),
        (
            "Los requerimientos fueron estructurados bajo la metodología ágil Scrum, considerando las necesidades directas de los usuarios finales (estudiantes, aspirantes, egresados y docentes) y del personal administrativo de las diversas dependencias de TEINCO.",
            "Normal"
        ),
        ("8.1.1 Requisitos Funcionales (RF)", "Heading 3"),
        ("• RF-01 (Atención Conversacional Continua): El sistema debe proporcionar una interfaz conversacional web disponible las 24 horas del día, los 7 días de la semana, capaz de recibir consultas en lenguaje natural.", "Normal"),
        ("• RF-02 (Canalización por Dependencia): La plataforma debe clasificar automáticamente la intención del usuario y dirigir la orientación hacia una de las 6 dependencias oficiales de TEINCO: Admisiones y Mercadeo, Registro y Control Académico, Bienestar Institucional, Cartera y Financiación, Coordinación Académica o Soporte y Sistemas.", "Normal"),
        ("• RF-03 (Generación Aumentada por Recuperación - RAG): El sistema debe consultar la base de conocimiento institucional previamente curada (reglamentos, calendarios, trámites) para construir respuestas veraces y exentas de alucinaciones.", "Normal"),
        ("• RF-04 (Entrega de Datos de Contacto Oficial): En cada respuesta orientativa, el sistema debe anexar una ficha con los canales oficiales de la dependencia involucrada (correo institucional, teléfono, ubicación física y horario de atención).", "Normal"),
        ("• RF-05 (Personalización por Rol de Usuario): El aplicativo debe permitir al usuario seleccionar su perfil institucional (Estudiante Activo, Aspirante, Egresado o Docente), adaptando el tono y los detalles normativos de la respuesta.", "Normal"),
        ("• RF-06 (Módulo de Retroalimentación y Calidad): Cada respuesta del asistente debe incluir un mecanismo de calificación binaria (útil / no útil) y opción de comentarios para medir la percepción de calidad del servicio.", "Normal"),
        ("• RF-07 (Anonimización de Datos Personales - Ley 1581): El núcleo backend debe filtrar y enmascarar automáticamente números de documentos de identidad, números telefónicos privados y correos personales antes de cualquier persistencia o envío a modelos LLM.", "Normal"),
        ("• RF-08 (Tablero Administrativo de Métricas): El panel administrativo debe presentar indicadores clave de rendimiento (KPIs) en tiempo real: volumen total de consultas, porcentaje de satisfacción, tiempos de respuesta y distribución de demanda por división institucional.", "Normal"),
        ("• RF-09 (Bitácora de Auditoría en Tiempo Real): La plataforma debe registrar cada interacción en una bitácora institucional anonimizada con búsqueda y filtrado por división y rol.", "Normal"),
        ("• RF-10 (Exportación de Informes Gerenciales): El sistema debe permitir al cuerpo directivo exportar la bitácora de interacciones en formato de valores separados por comas (.csv) para su análisis en comités de gestión.", "Normal"),
        ("• RF-11 (Gestión Dinámica de Conocimiento): Los administradores de TEINCO deben poder registrar, consultar y actualizar artículos de trámites en la base de datos con reindexación automática del motor RAG.", "Normal"),
        ("• RF-12 (Interoperabilidad de Modelos de Lenguaje): El sistema debe permitir conmutar en caliente entre un motor RAG semántico local offline, Google Gemini 1.5 Flash y OpenAI GPT-4o-mini según la disponibilidad de credenciales.", "Normal"),

        ("8.1.2 Requisitos No Funcionales (RNF)", "Heading 3"),
        ("• RNF-01 (Tiempo de Respuesta): El tiempo de procesamiento y entrega de respuestas en el motor RAG local no debe exceder los 2.000 milisegundos (2 segundos) bajo condiciones normales de red.", "Normal"),
        ("• RNF-02 (Disponibilidad y Concurrencia): La arquitectura debe soportar múltiples solicitudes concurrentes mediante el paradigma asíncrono ASGI implementado en FastAPI y Uvicorn.", "Normal"),
        ("• RNF-03 (Seguridad y Privacidad): Se garantiza la conformidad con la Ley 1581 de 2012 y Ley 1273 de 2009, aplicando desidentificación estricta de tokens de sesión y no almacenamiento de credenciales en texto plano.", "Normal"),
        ("• RNF-04 (Diseño Responsivo e Intuitivo): La interfaz de usuario desarrollada en React y Tailwind CSS debe adaptarse fluidamente a dispositivos móviles, tabletas y computadores de escritorio.", "Normal"),
        ("• RNF-05 (Identidad Visual Institucional): El entorno gráfico debe reflejar la paleta de colores y línea gráfica de TEINCO (azul marino #0B2545, dorado #D97706 y blanco puro).", "Normal"),
        ("• RNF-06 (Modularidad y Mantenibilidad): El código fuente debe estructurarse siguiendo patrones de arquitectura limpia y separación de responsabilidades (Routers, Modelos, Esquemas, Servicios y Base de Datos).", "Normal"),
        ("• RNF-07 (Portabilidad de Persistencia): El acceso a datos mediante SQLAlchemy ORM debe garantizar portabilidad inmediata sobre SQLite para desarrollo local y migración sin fricción hacia PostgreSQL con la extensión pgvector.", "Normal"),

        ("8.2 Arquitectura del Sistema y Especificaciones de Despliegue", "Heading 2"),
        (
            "AsistIA adopta un patrón arquitectónico desacoplado Cliente-Servidor (Decoupled Client-Server Architecture) soportado por APIs RESTful asíncronas y canalización de Recuperación Aumentada por Generación (RAG).",
            "Normal"
        ),
        ("8.2.1 Componentes de la Arquitectura", "Heading 3"),
        (
            "1. Capa de Presentación (Frontend): Construida sobre React 18, Vite y TypeScript, estructurada en componentes modulares (Navbar, ChatView, AdminDashboard, PrivacyModal). Emplea Tailwind CSS para el diseño responsivo e iconos vectoriales de Lucide React.\n"
            "2. Capa de Servicios y Lógica de Negocio (Backend): Desarrollada en Python 3.12 con el framework FastAPI. Implementa controladores REST divididos en dos enrutadores principales: '/api/chat' (orientado al estudiante) y '/api/admin' (orientado a la administración institucional).\n"
            "3. Pipeline RAG y Motor Vectorial: Módulo que implementa normalización léxica en español, extracción de n-gramas, vectorización TF-IDF con ponderación IDF logarítmica y cálculo de similitud de coseno, complementado con un clasificador heurístico de dependencias y re-ranking contextual.\n"
            "4. Capa de Persistencia y Modelado Relacional: Gestionada por SQLAlchemy 2.0 ORM. Estructura cuatro entidades relacionales fundamentales:\n"
            "   a) ConversationSession: Almacena el identificador único UUID de sesión, rol del usuario, marcas de tiempo y auditoría temporal.\n"
            "   b) ChatMessage: Persiste las interacciones (emisor, texto sanitizado, división institucional detectada, índice de confianza, tiempo de respuesta en ms y fuentes reglamentarias citadas).\n"
            "   c) MessageFeedback: Vincula la calificación de satisfacción otorgada por los estudiantes (utilidad y comentarios cualitativos).\n"
            "   d) KnowledgeArticle: Contiene la documentación reglamentaria oficial de TEINCO catalogada por división, categoría, palabras clave y canales de atención directa.",
            "Normal"
        ),
        ("8.2.2 Estrategia de Cumplimiento Legal (Ley Estatutaria 1581 de 2012)", "Heading 3"),
        (
            "En cumplimiento del marco legal colombiano, AsistIA implementa una función de desidentificación previa a la inferencia (sanitize_pii), la cual localiza mediante expresiones regulares patrones correspondientes a números de identificación ciudadana, líneas celulares y correos no corporativos, sustituyéndolos por etiquetas neutras ([DOCUMENTO_PROTEGIDO], [CELULAR_PROTEGIDO]). De esta manera, ninguna información sensible de los miembros de la comunidad TEINCO es expuesta ante modelos externos de inteligencia artificial ni queda grabada en registros planos.",
            "Normal"
        ),
        ("8.2.3 Guía de Despliegue y Puesta en Marcha", "Heading 3"),
        (
            "El sistema cuenta con empaquetamiento y scripts de ejecución automatizada para entornos Windows:\n"
            "• start_asistia.bat: Inicializa de manera sincronizada el backend FastAPI en el puerto 8000, el frontend React en el puerto 3000 y apertura el navegador web predeterminado.\n"
            "• run_backend.bat: Arranca el servidor de aplicaciones ASGI con recarga automática y acceso a la consola interactiva Swagger UI en 'http://127.0.0.1:8000/docs'.\n"
            "• run_frontend.bat: Despliega el servidor de desarrollo Vite con proxy inverso para enrutamiento transparente hacia los microservicios backend.",
            "Normal"
        )
    ]

    # Reemplazar párrafos 63 y 64 con el contenido enriquecido
    # Insertamos las secciones
    # Eliminamos el párrafo 64 y 63 viejos
    p_to_del_1 = doc.paragraphs[target_idx + 1] # "Requerimientos del Sistema"
    p_to_del_2 = doc.paragraphs[target_idx + 2] # "Arquitectura del Sistema y Especificaciones de Despliegue"
    p_to_del_1.text = ""
    p_to_del_2.text = ""

    # Crear un nuevo documento ensamblado
    new_doc = Document()

    # Copiar estilos y márgenes básicos
    for section in doc.sections:
        for new_sec in new_doc.sections:
            new_sec.top_margin = section.top_margin
            new_sec.bottom_margin = section.bottom_margin
            new_sec.left_margin = section.left_margin
            new_sec.right_margin = section.right_margin

    for i, p in enumerate(doc.paragraphs):
        if i == target_idx:
            # Insertar todo el capítulo 8 enriquecido
            for text_block, style_name in sections:
                p_new = new_doc.add_paragraph()
                p_new.text = text_block
                if "Heading 1" in style_name:
                    p_new.style = "Heading 1"
                elif "Heading 2" in style_name:
                    p_new.style = "Heading 2"
                elif "Heading 3" in style_name:
                    p_new.style = "Heading 3"
                else:
                    p_new.style = "Normal"
        elif i == target_idx + 1 or i == target_idx + 2:
            continue
        else:
            p_new = new_doc.add_paragraph(p.text)
            p_new.style = p.style.name if p.style else "Normal"

    new_doc.save("AsistIA_Documento_Completo.docx")
    print("Documento completo generado exitosamente: AsistIA_Documento_Completo.docx")

if __name__ == "__main__":
    build_complete_document()
