import os
import shutil
import zipfile
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def generate_asistia_document():
    template_path = "plantilla_referencia.docx"
    output_path = "AsistIA_Doc_Final.docx"
    
    # Copiar plantilla base para preservar headers, footers, logos y estilos XML exactos
    shutil.copyfile(template_path, output_path)
    doc = Document(output_path)
    
    print("Base document loaded with", len(doc.paragraphs), "paragraphs.")
    
    # -------------------------------------------------------------
    # 1. ACTUALIZAR PORTADA (Párrafos 0 a 33)
    # -------------------------------------------------------------
    doc.paragraphs[3].text = "PRODUCTO SOFTWARE"
    doc.paragraphs[4].text = "SEMILLERO DE INVESTIGACIÓN EN INNOVACIÓN Y APLICACIÓN DE NUEVAS TECNOLOGÍAS - SIIANTEC"
    doc.paragraphs[5].text = "TÍTULO PROYECTO"
    
    doc.paragraphs[7].text = "SISTEMA DE ASISTENCIA INTELIGENTE Y CONVERSACIONAL BASADO EN INTELIGENCIA ARTIFICIAL GENERATIVA Y ARQUITECTURA RAG PARA LA ATENCIÓN Y ORIENTACIÓN INSTITUCIONAL DE LAS DIVISIONES DE TEINCO (ASISTIA)"
    
    doc.paragraphs[9].text = "LÍNEA DE INVESTIGACIÓN"
    doc.paragraphs[10].text = "DISCIPLINAS AL SERVICIO DE LA SOCIEDAD Y EL SECTOR PRODUCTIVO"
    
    doc.paragraphs[12].text = "INTEGRANTES"
    doc.paragraphs[13].text = "ESTEFANY CASTRO PEDROZO"
    doc.paragraphs[14].text = "ANDERSON ESTIVEN JIMENEZ AMAYA"
    doc.paragraphs[15].text = "" # Limpiar tercer integrante si no aplica o dejar espacio
    
    doc.paragraphs[17].text = "SEMESTRE VIII / NIVEL PROFESIONAL"
    
    doc.paragraphs[19].text = "DOCENTE LÍDER SEMILLERISTA VÍCTOR ALFONSO GUZMÁN BRAND"
    doc.paragraphs[20].text = "DOCENTES DE INVESTIGACIÓN VÍCTOR ALFONSO GUZMÁN BRAND"
    doc.paragraphs[21].text = "DOCENTE ASESOR / EVALUADOR: CARLOS RAMOS"
    
    doc.paragraphs[23].text = "PROGRAMA TECNOLOGÍA EN DESARROLLO DE SOFTWARE / INGENIERÍA DE SISTEMAS"
    doc.paragraphs[25].text = "INSTITUCIÓN"
    doc.paragraphs[26].text = "CORPORACIÓN TECNOLÓGICA INDUSTRIAL COLOMBIANA TEINCO"
    doc.paragraphs[29].text = "AÑO Y CIUDAD BOGOTÁ, D.C - 2026"
    
    # -------------------------------------------------------------
    # 2. ACTUALIZAR RESUMEN (Párrafos 34 a 50)
    # -------------------------------------------------------------
    # Parágrafo previo al resumen (Pág. 2)
    doc.paragraphs[34].text = "Resumen"
    doc.paragraphs[35].text = (
        "El presente proyecto de desarrollo de software describe el diseño, arquitectura, construcción, validación e "
        "implementación de AsistIA, una plataforma web integral basada en un asistente conversacional con Inteligencia "
        "Artificial Generativa bajo la arquitectura RAG (Retrieval-Augmented Generation). Su objetivo primordial es "
        "automatizar, centralizar y optimizar la canalización y atención de consultas institucionales formuladas por "
        "aspirantes, estudiantes regulares de diversas jornadas, egresados y cuerpo docente hacia las diferentes divisiones "
        "académico-administrativas de la Corporación Tecnológica Industrial Colombiana (TEINCO), tales como Admisiones y Mercadeo, "
        "Registro y Control Académico, Bienestar Institucional, Cartera y Financiación, y Coordinaciones Académicas de las "
        "tres facultades institucionales (Ingeniería y Tecnologías, Ciencias Económicas y Administrativas, y Diseño y "
        "Comunicación Digital). La plataforma mitiga la saturación histórica de los canales de comunicación tradicionales "
        "proporcionando respuestas inmediatas, contextualmente validadas y categorizadas las 24 horas del día."
    )
    
    doc.paragraphs[36].text = (
        "El alcance del software abarca desde la sanitización y anonimización de datos personales en cumplimiento riguroso de la "
        "Ley Estatutaria 1581 de 2012, hasta la sincronización con una arquitectura de persistencia desacoplada que indexa "
        "semánticamente el reglamento estudiantil, resoluciones de rectoría, derechos pecuniarios y calendarios académicos "
        "oficiales. Al momento en que el usuario formula una consulta en lenguaje natural, el sistema analiza la intención, "
        "identifica la dependencia responsable, recupera los fragmentos normativos concordantes mediante similitud semántica y "
        "construye una respuesta precisa, escalonada y verificada, anexando en cada interacción la ficha con los canales oficiales "
        "de contacto institucional. Este flujo de trabajo automatizado garantiza que la comunidad acceda a información fidedigna "
        "y exenta de alucinaciones sintéticas."
    )
    
    doc.paragraphs[39].text = (
        "Desde la perspectiva institucional y de gestión educativa, el proyecto representa una transferencia tecnológica de alto "
        "impacto que moderniza los servicios de atención al estudiante y fortalece la retención académica. La reducción del "
        "tiempo de respuesta a milisegundos no solo descongestiona los buzones de correo y conmutadores de las oficinas, sino que "
        "proporciona al cuerpo directivo un Panel Gerencial y de Monitoreo en tiempo real con tableros analíticos de demanda por "
        "dependencia, tasas de satisfacción estudiantil, control de acceso basado en roles (RBAC) con perfiles diferenciados de "
        "Super Administrador y Operario, y un módulo de ingesta documental automática de archivos PDF. En conclusión, AsistIA "
        "transforma la operatividad tradicional en un modelo de gestión inteligente basado en datos, alineando los servicios "
        "universitarios de TEINCO con los estándares de la educación 4.0."
    )
    
    doc.paragraphs[40].text = (
        "El objetivo del proyecto es desarrollar e implementar un sistema de información web y asistente conversacional inteligente "
        "que combine la arquitectura RAG con modelos de lenguaje generativo de última generación, facilitando la orientación precisa "
        "y continua de la comunidad académica hacia las dependencias de TEINCO, optimizando los tiempos de atención y suministrando "
        "herramientas de analítica y gobernanza de datos para la dirección institucional."
    )

    # -------------------------------------------------------------
    # 3. ACTUALIZAR TABLA DE ILUSTRACIONES (Párrafos 55 a 82)
    # -------------------------------------------------------------
    ilustraciones = [
        ("Ilustración 1 - Diagrama de Gantt con planificación y fases de AsistIA", "30"),
        ("Ilustración 2 - Matriz de requerimientos funcionales y no funcionales", "35"),
        ("Ilustración 3 - Modelo de información y persistencia relacional en SQLAlchemy", "37"),
        ("Ilustración 4 - Panel Gerencial (Dashboard) con métricas analíticas en tiempo real", "38"),
        ("Ilustración 5 - Interfaz de Atención Estudiantil con chat inteligente y clasificación", "39"),
        ("Ilustración 6 - Despliegue de respuestas estructuradas y escalonadas en el chat", "40"),
        ("Ilustración 7 - Gestión de Base de Conocimiento indexada y trámites manuales", "41"),
        ("Ilustración 8 - Módulo de Ingesta Automática de Documentos y Reglamentos en PDF", "42"),
        ("Ilustración 9 - Selector y conmutación en caliente de motores de IA Generativa", "43"),
        ("Ilustración 10 - Bitácora de Auditoría en Vivo con consultas sanitizadas Ley 1581", "44"),
        ("Ilustración 11 - Modal de Control de Acceso y Gestión de Funcionarios (RBAC)", "45"),
        ("Ilustración 12 - Matriz de resultados de casos de prueba funcionales ejecutados", "47")
    ]
    
    for idx, (titulo, pag) in enumerate(ilustraciones):
        p_target = 55 + idx
        if p_target < len(doc.paragraphs):
            doc.paragraphs[p_target].text = f"{titulo}\t{pag}"
            
    # Limpiar entradas sobrantes de ilustraciones si las hay
    for p_clear in range(55 + len(ilustraciones), 83):
        if p_clear < len(doc.paragraphs):
            doc.paragraphs[p_clear].text = ""

    # Guardar progreso preliminar
    doc.save(output_path)
    print("Cover, Summary, and Illustrations Table updated.")

if __name__ == "__main__":
    generate_asistia_document()
