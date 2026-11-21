import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()
    
    # Page setup - normal margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)
        
    # Color palette
    NAVY = RGBColor(15, 76, 129)      # #0F4C81 - Institucional TEINCO
    SLATE = RGBColor(51, 65, 85)     # #334155
    AMBER = RGBColor(217, 119, 6)    # #D97706
    GRAY_BG = "F8FAFC"
    HEADER_BG = "0F4C81"
    
    # Header Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = title.add_run("CORPORACIÓN TECNOLÓGICA INDUSTRIAL COLOMBIANA - TEINCO\n")
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = SLATE
    
    r_main = title.add_run("SISTEMA DE ASISTENCIA INTELIGENTE (AsistIA)\n")
    r_main.font.size = Pt(18)
    r_main.font.bold = True
    r_main.font.color.rgb = NAVY
    
    r_doc = title.add_run("GUÍA OFICIAL DE RECOLECCIÓN Y FORMALIZACIÓN DE INFORMACIÓN INSTITUCIONAL 2026\n")
    r_doc.font.size = Pt(13)
    r_doc.font.bold = True
    r_doc.font.color.rgb = AMBER
    
    r_desc = title.add_run("Instrumento de Captura por Dependencias para Precisión del Asistente Virtual")
    r_desc.font.size = Pt(10)
    r_desc.font.italic = True
    r_desc.font.color.rgb = SLATE
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Metadata Box Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Proyecto / Sistema:", "AsistIA TEINCO - Asistente de IA Basado en RAG (Recuperación y Generación)"),
        ("Objetivo del Instrumento:", "Estandarizar y recopilar datos oficiales directos de los líderes de área para eliminar ambigüedades."),
        ("Responsable Técnico:", "Equipo de Desarrollo de Software / Opción de Grado TEINCO"),
        ("Destinatarios:", "Rectoría, Vicerrectoría, Registro y Control, Admisiones, Cartera, Bienestar y Decanaturas.")
    ]
    for idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.2)
        cell_v.width = Inches(4.3)
        
        pk = cell_k.paragraphs[0]
        rk = pk.add_run(k)
        rk.font.bold = True
        rk.font.size = Pt(9.5)
        rk.font.color.rgb = NAVY
        
        pv = cell_v.paragraphs[0]
        rv = pv.add_run(v)
        rv.font.size = Pt(9.5)
        rv.font.color.rgb = SLATE
        
        set_cell_background(cell_k, "F1F5F9")
        set_cell_background(cell_v, GRAY_BG)
        set_cell_margins(cell_k, 60, 60, 100, 100)
        set_cell_margins(cell_v, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)
    
    # 1. Introducción
    h1 = doc.add_heading("1. Justificación y Propósito del Documento", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    for run in h1.runs:
        run.font.color.rgb = NAVY
        run.font.size = Pt(14)
        
    p1 = doc.add_paragraph(
        "El presente instrumento técnico tiene como finalidad orientar a los directores, coordinadores y jefes de cada dependencia "
        "de la Corporación Tecnológica Industrial Colombiana (TEINCO) en el suministro formal de reglamentos, calendarios, tarifas y procedimientos. "
        "Dado que AsistIA opera mediante la arquitectura RAG (Retrieval-Augmented Generation), el motor de inteligencia artificial "
        "basa el 100% de sus respuestas exclusivamente en la información verídica que la institución alimenta en su base de conocimiento. "
        "De este modo, se garantiza una atención veraz, oportuna y sin alucinaciones para estudiantes, egresados y aspirantes."
    )
    p1.paragraph_format.line_spacing = 1.15
    p1.paragraph_format.space_after = Pt(10)
    
    # 2. Instrucciones Generales
    h2 = doc.add_heading("2. Mecanismo de Formalización y Carga al Sistema", level=1)
    for run in h2.runs:
        run.font.color.rgb = NAVY
        run.font.size = Pt(14)
        
    p2 = doc.add_paragraph(
        "Cada líder de área puede entregar la información solicitada en dos formatos admitidos por el sistema:\n"
        "• Formato Documental Oficial (Recomendado): Documentos PDF expedidos por la institución (Resoluciones de Rectoría, Acuerdos de Consejo Directivo, Manual de Convivencia, Manual de Derechos Pecuniarios, Calendario Académico aprobado).\n"
        "• Ficha de Trámite Directa: Diligenciar el cuestionario estandarizado que se detalla en las siguientes secciones para que el Operario o Super Administrador lo incorpore en el módulo de 'Nuevo Trámite Manual' del Panel Gerencial de AsistIA."
    )
    p2.paragraph_format.line_spacing = 1.15
    p2.paragraph_format.space_after = Pt(12)

    # 3. Cuestionarios por Dependencia
    h3 = doc.add_heading("3. Fichas de Recolección de Datos por Dependencia Institucional", level=1)
    for run in h3.runs:
        run.font.color.rgb = NAVY
        run.font.size = Pt(14)

    dependencias = [
        {
            "nombre": "3.1. Admisiones, Mercadeo y Registro de Aspirantes",
            "lider": "Dirección de Mercadeo y Admisiones",
            "items": [
                ("Costos de Inscripción y Matrícula", "Tarifa oficial para programas técnicos, tecnológicos y profesionales periodo 2026-1 y 2026-2."),
                ("Requisitos de Ingreso", "Documentos exactos requeridos para aspirantes bachilleres (Diploma, ICFES, EPS, documento identidad)."),
                ("Convenios Especiales", "Condiciones vigentes de homologación SENA, convenios con colegios y descuentos por pronto pago o cajas de compensación."),
                ("Fechas de Cierre", "Fechas límites de inscripción ordinaria y extraordinaria para cada periodo.")
            ]
        },
        {
            "nombre": "3.2. Registro y Control Académico",
            "lider": "Coordinación de Registro y Control",
            "items": [
                ("Certificados Académicos", "Procedimiento exacto, costo pecuniario y tiempo de respuesta para: Certificado de Notas, Certificado de Estudio, Certificado de Buena Conducta y Contenidos Programáticos."),
                ("Proceso de Grados", "Requisitos documentales, paz y salvos requeridos (Biblioteca, Cartera, Bienestar), fechas de ceremonias solemnes y de ventanilla."),
                ("Novedades Académicas", "Condiciones y plazos para: Cancelación de semestre, cancelación extemporánea de asignaturas, adición de créditos y reintegros."),
                ("Derechos Pecuniarios", "Tabla oficial de tarifas para derechos de grado, duplicado de carnet, validaciones y exámenes supletorios.")
            ]
        },
        {
            "nombre": "3.3. Cartera, Financiación y Tesorería",
            "lider": "Jefatura Financiera y Cartera",
            "items": [
                ("Medios y Canales de Pago", "Enlace oficial de pasarela PSE, cuentas bancarias autorizadas (Bancolombia, Davivienda, etc.) y código de convenio."),
                ("Opciones de Financiación", "Alianzas vigentes (ICETEX, Coopcentral, Financiar, Sufi, etc.) y requisitos para acceder al crédito institucional directo."),
                ("Políticas de Paz y Salvo", "Tiempo de liberación de pagos realizados por PSE y trámite para expedición de paz y salvo financiero para matrícula o grado."),
                ("Devoluciones y Saldos a Favor", "Normativa institucional respecto al retiro de estudiantes y porcentaje de devolución según fechas calendario.")
            ]
        },
        {
            "nombre": "3.4. Bienestar Institucional y Pastoral",
            "lider": "Coordinación de Bienestar Universitario",
            "items": [
                ("Atención Psicológica y Salud", "Horarios, canal de agendamiento y gratuidad de consultas de orientación psicológica para estudiantes."),
                ("Becas y Subsidios", "Requisitos para acceder a becas de excelencia académica, convenios deportivos y apoyos socioeconómicos."),
                ("Talleres y Grupos Representativos", "Oferta deportiva (fútbol, voleibol, tenis de mesa), cultural (teatro, danzas, música) y voluntariado."),
                ("Rutas de Atención y Emergencias", "Protocolo ante situaciones de acoso, violencia de género o vulnerabilidad estudiantil.")
            ]
        },
        {
            "nombre": "3.5. Facultades y Coordinaciones de Programa",
            "lider": "Decanaturas (Ingeniería, Ciencias Económicas, Diseño Digital)",
            "items": [
                ("Modalidades de Grado", "Reglamento específico por facultad: Proyecto de software/investigación, Seminario/Diplomado de profundización, o Pasantía institucional. Porcentajes de avance requeridos."),
                ("Prácticas Profesionales", "Requisito de créditos cursados (mínimo 70%), modalidades de contrato de aprendizaje SENA o convenio de pasantía, y póliza ARL."),
                ("Requisito de Segundo Idioma (Inglés)", "Nivel requerido según marco común europeo (A2, B1 o B2) para cada ciclo (Técnico, Tecnológico, Profesional) y centros de idiomas avalados."),
                ("Mallas Curriculares y Créditos", "Resoluciones vigentes del Ministerio de Educación Nacional (MEN) con el registro calificado de cada programa.")
            ]
        },
        {
            "nombre": "3.6. Tecnologías de la Información y Campus Virtual",
            "lider": "Dirección de TI / Campus Virtual",
            "items": [
                ("Credenciales y Cuentas", "Procedimiento de entrega y restablecimiento de contraseña para el correo institucional (@teinco.edu.co) y plataforma Q10 / Moodle."),
                ("Soporte Aula Virtual", "Canales de soporte para fallas técnicas en evaluaciones virtuales o acceso a cursos."),
                ("Salas de Cómputo y Software", "Normas de uso de laboratorios mecatrónicos, salas Mac, impresoras 3D y licencias académicas otorgadas.")
            ]
        }
    ]

    for dep in dependencias:
        h_dep = doc.add_heading(dep["nombre"], level=2)
        h_dep.paragraph_format.space_before = Pt(12)
        h_dep.paragraph_format.space_after = Pt(4)
        for run in h_dep.runs:
            run.font.color.rgb = NAVY
            run.font.size = Pt(11.5)
            
        p_lid = doc.add_paragraph()
        r_lid_lbl = p_lid.add_run("Dependencia Responsable: ")
        r_lid_lbl.font.bold = True
        r_lid_lbl.font.size = Pt(9.5)
        r_lid_val = p_lid.add_run(dep["lider"])
        r_lid_val.font.size = Pt(9.5)
        p_lid.paragraph_format.space_after = Pt(4)
        
        # Table of requirements
        tbl = doc.add_table(rows=1, cols=3)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr_cells = tbl.rows[0].cells
        hdr_cells[0].text = "Tema / Aspecto"
        hdr_cells[1].text = "Información Oficial Requerida"
        hdr_cells[2].text = "Formato o Soporte Solicitado"
        
        widths = [Inches(1.8), Inches(3.2), Inches(1.5)]
        for i, hc in enumerate(hdr_cells):
            hc.width = widths[i]
            set_cell_background(hc, HEADER_BG)
            set_cell_margins(hc, 80, 80, 100, 100)
            p = hc.paragraphs[0]
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(255, 255, 255)
                
        for tema, req in dep["items"]:
            row_cells = tbl.add_row().cells
            row_cells[0].width = widths[0]
            row_cells[1].width = widths[1]
            row_cells[2].width = widths[2]
            
            p0 = row_cells[0].paragraphs[0]
            r0 = p0.add_run(tema)
            r0.font.bold = True
            r0.font.size = Pt(8.5)
            r0.font.color.rgb = SLATE
            
            p1 = row_cells[1].paragraphs[0]
            r1 = p1.add_run(req)
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = SLATE
            
            p2 = row_cells[2].paragraphs[0]
            r2 = p2.add_run("PDF Oficial / Circular / Texto firmado")
            r2.font.italic = True
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = SLATE
            
            for c in row_cells:
                set_cell_background(c, GRAY_BG)
                set_cell_margins(c, 50, 50, 80, 80)
                
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4. Procedimiento de Ingesta en AsistIA
    h4 = doc.add_heading("4. Pasos para Alimentar la Base de Conocimiento en AsistIA", level=1)
    for run in h4.runs:
        run.font.color.rgb = NAVY
        run.font.size = Pt(14)
        
    p4 = doc.add_paragraph(
        "Una vez el funcionario responsable recopile las circulares o diligencie los datos oficiales, "
        "el procedimiento de actualización en el sistema se realiza de la siguiente manera:\n"
        "1. Iniciar sesión en el Panel Gerencial (ruta http://localhost:8000/ o http://localhost:3000/) con un usuario administrativo.\n"
        "2. Ir a la pestaña 'Base de Conocimiento y PDFs'.\n"
        "3. Opción Automática (Archivos PDF): En el recuadro 'Ingesta Automática de Documentos', seleccionar la dependencia institucional en el desplegable, adjuntar el archivo PDF oficial y presionar 'Indexar Documento en RAG'. El sistema procesa el documento, divide el contenido en fragmentos semánticos y lo indexa de inmediato.\n"
        "4. Opción Manual (Nuevo Trámite): Hacer clic en el botón azul '+ Nuevo Trámite Manual', asignar el título, la dependencia, el correo de contacto institucional y redactar el paso a paso detallado.\n"
        "5. Validación en Chat: Probar una pregunta en la vista de 'Atención Estudiantil' para certificar que AsistIA responde con los nuevos datos actualizados."
    )
    p4.paragraph_format.line_spacing = 1.15
    p4.paragraph_format.space_after = Pt(14)

    # Signatures
    h5 = doc.add_heading("5. Formalización y Entrega de Información", level=1)
    for run in h5.runs:
        run.font.color.rgb = NAVY
        run.font.size = Pt(14)
        
    p5 = doc.add_paragraph(
        "Para constancia del proceso de transferencia y formalización de información institucional, firman:"
    )
    p5.paragraph_format.space_after = Pt(20)
    
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = sig_table.rows[0].cells[0]
    c1 = sig_table.rows[0].cells[1]
    c2 = sig_table.rows[1].cells[0]
    c3 = sig_table.rows[1].cells[1]
    
    c0.width = Inches(3.2)
    c1.width = Inches(3.2)
    c2.width = Inches(3.2)
    c3.width = Inches(3.2)
    
    p_s1 = c0.paragraphs[0]
    p_s1.add_run("_________________________________________\nLíder de Dependencia / Coordinación\nCargo:\nFecha de Entrega:")
    
    p_s2 = c1.paragraphs[0]
    p_s2.add_run("_________________________________________\nRectoría / Vicerrectoría Académica\nVisto Bueno Institucional TEINCO\nFecha de Aprobación:")
    
    doc_path = r"C:\Users\Anderson\Downloads\AsistIA\Guia_Recoleccion_Informacion_Institucional_TEINCO.docx"
    doc.save(doc_path)
    print(f"Document saved successfully at: {doc_path}")

if __name__ == "__main__":
    create_document()
