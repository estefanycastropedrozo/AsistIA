"""
Base de Conocimiento Curada e Institucional de TEINCO
Corporación Tecnológica Industrial Colombiana
Almacena la información oficial de trámites, calendarios, reglamentos y contactos.
"""

TEINCO_DIVISIONS_CONTACT = {
    "Registro y Control": {
        "division_name": "Registro y Control Académico",
        "email": "coordinacionregistroycontrol@teinco.edu.co",
        "phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office": "Sede Principal: Calle 57 No. 9-28 | Sede Caracas: Av. Caracas No. 57-41, Bogotá D.C.",
        "schedule": "Lun a Vie: 7:00 a.m. a 10:00 p.m. | Sáb: 7:00 a.m. a 4:00 p.m. (Sede Principal) y 7:00 a.m. a 1:00 p.m. (Sede Caracas) | Dom: Cerrado"
    },
    "Admisiones y Mercadeo": {
        "division_name": "Admisiones y Mercadeo",
        "email": "admisiones@teinco.edu.co",
        "phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office": "Sede Principal TEINCO - Calle 57 No. 9-28, Piso 1, Bogotá D.C.",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 4:00 p.m."
    },
    "Bienestar Institucional": {
        "division_name": "Bienestar Institucional y Pastoral",
        "email": "bienestar@teinco.edu.co",
        "phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office": "Sede Principal TEINCO - Calle 57 No. 9-28, Piso 3, Bogotá D.C.",
        "schedule": "Lunes a Viernes: 8:00 a.m. a 6:00 p.m."
    },
    "Cartera y Financiación": {
        "division_name": "Cartera, Facturación y Tesorería",
        "email": "cartera@teinco.edu.co",
        "phone": "+57 601 7433200 Ext. 104 - 105 | WhatsApp: 301 333 7956",
        "office": "Sede Principal TEINCO - Calle 57 No. 9-28, Mezanine, Bogotá D.C.",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 8:00 p.m. | Sábados: 8:00 a.m. a 1:00 p.m."
    },
    "Coordinación Académica": {
        "division_name": "Coordinación Académica y Programa de Software",
        "email": "coordinacion.software@teinco.edu.co",
        "phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office": "Sede Principal TEINCO - Calle 57 No. 9-28, Piso 2, Bloque B, Bogotá D.C.",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 2:00 p.m."
    },
    "Soporte y Sistemas": {
        "division_name": "Dirección de Tecnologías de la Información y Campus Virtual",
        "email": "soporte.sistemas@teinco.edu.co",
        "phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office": "Sede Principal TEINCO - Calle 57 No. 9-28, Piso 4, Bogotá D.C.",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Soporte virtual 24/7"
    }
}

SEED_KNOWLEDGE_ARTICLES = [
    # --- ADMISIONES ---
    {
        "division": "Admisiones y Mercadeo",
        "category": "Inscripciones y Requisitos",
        "title": "Requisitos de Inscripción para Estudiantes Nuevos en TEINCO",
        "content": (
            "Para inscribirte a los programas tecnológicos y profesionales de TEINCO requieres: "
            "1) Formulario de inscripción diligenciado en la página oficial. "
            "2) Fotocopia legible del documento de identidad (C.C. o T.I.). "
            "3) Fotocopia del diploma de bachiller o acta de grado original. "
            "4) Resultado de las pruebas de Estado Saber 11 (ICFES). "
            "5) Certificado de afiliación a EPS o SISBÉN vigente. "
            "6) 1 fotografía tamaño 3x4 fondo blanco reciente. "
            "Una vez cargados los documentos, admisiones te agendará la entrevista vocacional."
        ),
        "keywords": "inscripcion, requisitos, matricularse, nuevo ingreso, icfes, bachiller, saber 11, documentos",
        "contact_email": "admisiones@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m."
    },
    {
        "division": "Admisiones y Mercadeo",
        "category": "Oferta Académica",
        "title": "Programas Académicos y Carreras por Ciclos Propedéuticos en TEINCO",
        "content": (
            "La oferta académica de TEINCO está organizada en 3 Facultades mediante ciclos propedéuticos que te permiten titularte como Técnico Profesional, Tecnólogo y Profesional/Ingeniero: "
            "1) Facultad de Ingeniería y Tecnologías: Ingeniería de Sistemas (Técnica en Programación de Computadores, Tecnología en Desarrollo de Software, Ingeniería de Sistemas) e Ingeniería Mecatrónica (Técnica en Mantenimiento Mecatrónico, Tecnología en Automatización Industrial, Ingeniería Mecatrónica). "
            "2) Facultad de Ciencias Económicas y Administrativas: Administración de Empresas (Técnica en Procesos Administrativos, Tecnología en Gestión Empresarial, Administración de Empresas) y Contaduría Pública (Técnica en Procesos Contables, Tecnología en Gestión Contable y Tributaria, Contaduría Pública). "
            "3) Facultad de Diseño y Comunicación Digital: Profesional en Diseño Digital Publicitario (Técnica en Producción Gráfica, Tecnología en Proyectos Publicitarios, Diseño Digital) y Profesional en Marketing y Negocios Digitales (Técnica en Estrategias Comerciales, Tecnología en Gestión de Mercadeo, Marketing y Negocios Digitales)."
        ),
        "keywords": "carreras, programas, ingenieria de sistemas, mecatronica, administracion de empresas, contaduria publica, diseno digital publicitario, marketing y negocios digitales, facultades, ciclos propedeuticos, que carreras hay",
        "contact_email": "admisiones@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 4:00 p.m."
    },
    {
        "division": "Admisiones y Mercadeo",
        "category": "Oferta Académica",
        "title": "Facultad de Ingeniería y Tecnologías TEINCO",
        "content": (
            "La Facultad de Ingeniería y Tecnologías de TEINCO ofrece programas por ciclos propedéuticos: "
            "1) Ingeniería de Sistemas: Ciclo Técnico en Programación de Computadores, Ciclo Tecnológico en Desarrollo de Software y Sistemas de Información, y Ciclo Profesional en Ingeniería de Sistemas. "
            "2) Ingeniería Mecatrónica: Ciclo Técnico en Mantenimiento de Sistemas Mecatrónicos, Ciclo Tecnológico en Automatización de Procesos Industriales, y Ciclo Profesional en Ingeniería Mecatrónica. "
            "Dispone de laboratorios de robótica, electrónica y salas de cómputo especializadas."
        ),
        "keywords": "ingenieria, ingenieria de sistemas, mecatronica, automatizacion, programacion, computadores, tecnologia en software",
        "contact_email": "admisiones@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m."
    },
    {
        "division": "Admisiones y Mercadeo",
        "category": "Oferta Académica",
        "title": "Facultad de Ciencias Económicas y Administrativas TEINCO",
        "content": (
            "La Facultad de Ciencias Económicas y Administrativas de TEINCO forma líderes empresariales y financieros: "
            "1) Administración de Empresas: Ciclo Técnico en Procesos Administrativos, Ciclo Tecnológico en Gestión Empresarial, y Ciclo Profesional en Administración de Empresas. "
            "2) Contaduría Pública: Ciclo Técnico en Procesos Contables y Financieros, Ciclo Tecnológico en Gestión Contable y Tributaria, y Ciclo Profesional en Contaduría Pública. "
            "Enfoque en alta gerencia, finanzas corporativas, emprendimiento y estándares internacionales NIIF."
        ),
        "keywords": "administracion, empresas, contaduria, contable, tributaria, finanzas, economia, gestion empresarial",
        "contact_email": "admisiones@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m."
    },
    {
        "division": "Admisiones y Mercadeo",
        "category": "Oferta Académica",
        "title": "Facultad de Diseño y Comunicación Digital TEINCO",
        "content": (
            "La Facultad de Diseño y Comunicación Digital lidera la creatividad publicitaria y el comercio electrónico: "
            "1) Profesional en Diseño Digital Publicitario: Ciclo Técnico en Producción Gráfica Digital, Ciclo Tecnológico en Gestión de Proyectos Digitales Publicitarios, y Ciclo Profesional en Diseño Digital Publicitario. "
            "2) Profesional en Marketing y Negocios Digitales: Ciclo Técnico en Ejecución de Estrategias Comerciales, Ciclo Tecnológico en Gestión de Mercadeo Digital, y Ciclo Profesional en Marketing y Negocios Digitales. "
            "Abarca branding, animación, redes sociales, e-commerce, pauta y analítica de audiencias."
        ),
        "keywords": "diseno, diseno digital, publicidad, marketing, mercadeo digital, negocios digitales, diseno publicitario, produccion grafica",
        "contact_email": "admisiones@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m."
    },
    {
        "division": "Admisiones y Mercadeo",
        "category": "Homologaciones",
        "title": "Transferencias Externas y Homologación de Asignaturas",
        "content": (
            "Si vienes de otra universidad o del SENA, puedes solicitar homologación de materias. "
            "Debes radicar en admisiones: 1) Certificado oficial de calificaciones de la institución de procedencia. "
            "2) Contenidos programáticos (sílabos) debidamente sellados. "
            "3) Certificado de buena conducta. "
            "El comité curricular evaluará las materias cursadas con nota mínima de 3.5 y afinidad de contenido del 80%."
        ),
        "keywords": "homologacion, homologar, sena, transferencia, cambio de universidad, convalidar materias",
        "contact_email": "admisiones@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m."
    },

    # --- REGISTRO Y CONTROL ACADÉMICO ---
    {
        "division": "Registro y Control",
        "category": "Certificados y Constancias",
        "title": "Expedición de Certificados de Estudio y Calificaciones",
        "content": (
            "Para solicitar un certificado de notas, constancia de estudio, terminación de materias o conducta: "
            "1) Descarga la orden de pago o solicítala a Cartera y cancela los derechos mediante PSE o en bancos. "
            "2) Envía el soporte de pago al correo coordinacionregistroycontrol@teinco.edu.co indicando: Nombre completo, número de documento, programa académico y tipo de certificado. "
            "El tiempo oficial de expedición es de 3 a 5 días hábiles con firma digital reglamentaria o retiro presencial en ventanilla."
        ),
        "keywords": "certificado, notas, constancia de estudio, certificado de conducta, contenidos programmaticos, expedicion",
        "contact_email": "coordinacionregistroycontrol@teinco.edu.co",
        "contact_phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office_location": "Sede Principal Calle 57 No. 9-28 / Sede Caracas Av. Caracas No. 57-41",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 4:00 p.m."
    },
    {
        "division": "Registro y Control",
        "category": "Matrícula y Horarios",
        "title": "Proceso de Matrícula Académica y Asignación de Horarios",
        "content": (
            "La matrícula consta de dos fases obligatorias: "
            "1) Matrícula Financiera: Pago del valor del semestre en fechas ordinarias o extraordinarias. "
            "2) Matrícula Académica: Inscripción de asignaturas en el portal Q10. "
            "Los estudiantes pueden realizar adición o retiro de asignaturas durante las dos primeras semanas de clases del calendario académico oficial."
        ),
        "keywords": "matricula academica, inscribir materias, horarios, semestres, carga academica, q10",
        "contact_email": "coordinacionregistroycontrol@teinco.edu.co",
        "contact_phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office_location": "Sede Principal Calle 57 No. 9-28 / Sede Caracas Av. Caracas No. 57-41",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 4:00 p.m."
    },
    {
        "division": "Registro y Control",
        "category": "Grados y Titulación",
        "title": "Requisitos para Grado y Ceremonia de Titulación en TEINCO",
        "content": (
            "Para postularse a grado en TEINCO debes: "
            "1) Aprobar el 100% de los créditos de la malla curricular. "
            "2) Aprobar la opción de grado elegida (Proyecto de Software, Monografía, Seminario). "
            "3) Certificar el nivel de inglés exigido institucionalmente. "
            "4) Presentar la prueba de Estado Saber TyT / Saber Pro. "
            "5) Obtener el Paz y Salvo general (Biblioteca, Cartera, Coordinación, Bienestar). "
            "6) Cancelar los derechos de grado dentro de las fechas fijadas por Secretaría General."
        ),
        "keywords": "grado, ceremonia de grado, paz y salvo, saber pro, saber tyt, derechos de grado, titulacion",
        "contact_email": "coordinacionregistroycontrol@teinco.edu.co",
        "contact_phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office_location": "Sede Principal Calle 57 No. 9-28 / Sede Caracas Av. Caracas No. 57-41",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 4:00 p.m."
    },

    # --- BIENESTAR INSTITUCIONAL ---
    {
        "division": "Bienestar Institucional",
        "category": "Salud y Psicología",
        "title": "Acompañamiento Psicológico, Orientación y Salud Integral",
        "content": (
            "Bienestar ofrece atención gratuita y confidencial: "
            "• Orientación y consulta psicológica para manejo de estrés, ansiedad y orientación vocacional. "
            "• Primeros auxilios y enfermería institucional en la sede principal. "
            "• Programa de acompañamiento y permanencia estudiantil (PAE) para estudiantes en condición de prueba académica. "
            "Para agendar tu cita, escribe a bienestar@teinco.edu.co o acércate al piso 3."
        ),
        "keywords": "psicologia, cita psicologica, salud, enfermeria, estres, orientacion emocional, permanencia",
        "contact_email": "bienestar@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28, Piso 3",
        "schedule": "Lunes a Viernes: 8:00 a.m. a 6:00 p.m."
    },
    {
        "division": "Bienestar Institucional",
        "category": "Cultura y Deportes",
        "title": "Actividades Culturales y Selecciones Deportivas TEINCO",
        "content": (
            "Bienestar promueve la formación integral extracurricular: "
            "• Deportes: Fútbol de Salón (Masculino y Femenino), Voleibol, Baloncesto, Tenis de Mesa y Ajedrez. "
            "• Cultura: Danza moderna y folclórica, Ensamble Musical, Teatro y Fotografía. "
            "La participación en selecciones institucionales otorga puntos para beneficios de becas."
        ),
        "keywords": "deportes, futbol, voleibol, musica, danza, teatro, ajedrez, torneos, gimnasio, actividades",
        "contact_email": "bienestar@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28, Piso 3",
        "schedule": "Lunes a Viernes: 8:00 a.m. a 6:00 p.m."
    },
    {
        "division": "Bienestar Institucional",
        "category": "Becas y Auxilios",
        "title": "Becas por Rendimiento Académico y Auxilios Socioeconómicos",
        "content": (
            "TEINCO premia el esfuerzo de sus estudiantes: "
            "1) Beca de Excelencia: Exención de matrícula para el promedio ponderado más alto del programa (mínimo 4.5). "
            "2) Beca Monitoría: Para estudiantes destacados que apoyan laboratorios, salas de software o tutorías académicas. "
            "3) Descuento por Hermanos: 10% de descuento cuando dos familiares directos estudian en TEINCO. "
            "Las convocatorias se abren al cierre de cada semestre lectivo."
        ),
        "keywords": "becas, descuentos, monitorias, convenio familiar, promedio, auxilio economico, gratuidad",
        "contact_email": "bienestar@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28, Piso 3",
        "schedule": "Lunes a Viernes: 8:00 a.m. a 6:00 p.m."
    },

    # --- CARTERA Y FINANCIACIÓN ---
    {
        "division": "Cartera y Financiación",
        "category": "Medios de Pago",
        "title": "Medios de Pago Autorizados y Generación de Recibos",
        "content": (
            "Puedes cancelar matrículas y derechos pecuniarios a través de: "
            "1) Botón PSE en línea desde la página oficial de TEINCO. "
            "2) Consignación bancaria en Bancolombia o Banco Davivienda usando el código de convenio institucional. "
            "3) Caja institucional en la sede principal con tarjeta débito, crédito o efectivo. "
            "Para legalizar pagos en bancos, la referencia se valida en el sistema en 24 horas hábiles."
        ),
        "keywords": "pse, pago matricula, bancos, consignacion, davivienda, bancolombia, recibo de pago, factura",
        "contact_email": "cartera@teinco.edu.co",
        "contact_phone": "+57 601 7433200 Ext. 104 - 105",
        "office_location": "Sede Principal Calle 57 No. 9-28, Mezanine",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 8:00 p.m. | Sábados: 8:00 a.m. a 1:00 p.m."
    },
    {
        "division": "Cartera y Financiación",
        "category": "Financiación y Créditos",
        "title": "Opciones de Financiación, Crédito Directo e ICETEX",
        "content": (
            "TEINCO te ofrece alternativas para financiar tu matrícula: "
            "• Crédito Directo TEINCO: Cuota inicial del 40% y el saldo en cuotas mensuales durante el semestre académico sin trámites bancarios complejos. "
            "• ICETEX: Líneas Tú Eliges (0%, 25%, 100%) y subsidios de sostenimiento. "
            "• Convenios Financieros: Fincomercio, Banco Pichincha, Sufi Bancolombia y Coopecrédito con tasas preferenciales."
        ),
        "keywords": "icetex, cuotas, credito directo, financiacion, cuota inicial, fincomercio, pichincha, pagar a plazos",
        "contact_email": "cartera@teinco.edu.co",
        "contact_phone": "+57 601 7433200 Ext. 104 - 105",
        "office_location": "Sede Principal Calle 57 No. 9-28, Mezanine",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 8:00 p.m. | Sábados: 8:00 a.m. a 1:00 p.m."
    },
    {
        "division": "Cartera y Financiación",
        "category": "Paz y Salvo",
        "title": "Expedición de Paz y Salvo Financiero",
        "content": (
            "El Paz y Salvo Financiero certifica que te encuentras al día en todas tus obligaciones pecuniarias. "
            "Es indispensable para solicitar certificados de estudio, renovar matrícula semestral y para postulación a grados. "
            "Si estás al día con tus pagos, se genera en línea o solicitándolo al correo cartera@teinco.edu.co en 24 a 48 horas hábiles."
        ),
        "keywords": "paz y salvo financiero, deuda, saldo pendiente, estado de cuenta, factura al dia",
        "contact_email": "cartera@teinco.edu.co",
        "contact_phone": "+57 601 7433200 Ext. 104",
        "office_location": "Sede Principal Calle 57 No. 9-28, Mezanine",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 8:00 p.m."
    },

    # --- COORDINACIÓN ACADÉMICA ---
    {
        "division": "Coordinación Académica",
        "category": "Prácticas Profesionales",
        "title": "Reglamento y Requisitos de Prácticas Profesionales en Software",
        "content": (
            "Para iniciar tu Práctica Profesional en la Tecnología en Desarrollo de Software requieres: "
            "1) Haber aprobado como mínimo el 70% del total de créditos del plan de estudios. "
            "2) Estar a paz y salvo académico y financiero. "
            "3) Modalidades autorizadas: Contrato de Aprendizaje SENA, Convenio de Pasantía, o Validación de Experiencia Laboral vigente (mínimo 6 meses en desarrollo de software). "
            "4) Radicar la Carta de Solicitud y ARL de la empresa ante la coordinación académica."
        ),
        "keywords": "practica profesional, pasantia, contrato de aprendizaje, empresa, requisitos practica, 70 por ciento creditos",
        "contact_email": "coordinacion.software@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28, Bloque B, Piso 2",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 2:00 p.m."
    },
    {
        "division": "Coordinación Académica",
        "category": "Opciones de Grado",
        "title": "Opciones de Grado para Tecnología en Desarrollo de Software",
        "content": (
            "En tu último semestre puedes escoger entre: "
            "1) Proyecto de Desarrollo e Implementación de Software (Creación de aplicativos funcionales reales como AsistIA). "
            "2) Seminario / Diplomado de Profundización Tecnológica (aprobado con nota mínima de 3.5). "
            "3) Monografía de Investigación Aplicada o participación en semillero de investigación TEINCO."
        ),
        "keywords": "opciones de grado, proyecto de grado, monografia, seminario de grado, diplomado, desarrollo de software",
        "contact_email": "coordinacion.software@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28, Bloque B, Piso 2",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 2:00 p.m."
    },
    {
        "division": "Coordinación Académica",
        "category": "Evaluaciones y Supletorios",
        "title": "Exámenes Supletorios y Habilitaciones Académicas",
        "content": (
            "Según el Reglamento Estudiantil: "
            "• Supletorio: Procede por inasistencia justificada a parciales o finales (incapacidad médica o fuerza mayor). Se solicita dentro de los 3 días hábiles siguientes al examen ante la coordinación cancelando los derechos respectivos. "
            "• Habilitación: Aplica para asignaturas teóricas reprobadas con calificación definitiva entre 2.0 y 2.9 (escala 0.0 a 5.0). La nota aprobatoria mínima es 3.0."
        ),
        "keywords": "supletorio, habilitacion, examen supletorio, perder materia, incapacidad medica, nota minima",
        "contact_email": "coordinacion.software@teinco.edu.co",
        "contact_phone": "+57 601 7433200",
        "office_location": "Sede Principal Calle 57 No. 9-28, Bloque B, Piso 2",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Sábados: 7:00 a.m. a 2:00 p.m."
    },

    # --- SOPORTE Y SISTEMAS ---
    {
        "division": "Soporte y Sistemas",
        "category": "Plataformas y Accesos",
        "title": "Acceso al Campus Virtual Moodle y Correo Institucional TEINCO",
        "content": (
            "Para ingresar al Campus Virtual y herramientas tecnológicas: "
            "1) Correo Institucional: usuario@teinco.edu.co con servicios de Google Workspace y Microsoft 365 Educación. "
            "2) Campus Virtual Moodle: Acceso a aulas virtuales, foros y entrega de evidencias de aprendizaje. "
            "3) Portal Académico Q10: Consulta de notas definitivas, asistencias y horarios. "
            "En caso de olvido de contraseña o bloqueo, escribe a soporte.sistemas@teinco.edu.co adjuntando tu documento de identidad."
        ),
        "keywords": "clave, contraseña, correo institucional, moodle, campus virtual, q10, aulas virtuales, bloqueo",
        "contact_email": "soporte.sistemas@teinco.edu.co",
        "contact_phone": "+57 601 7433200 | WhatsApp: 301 333 7956",
        "office_location": "Sede Principal Calle 57 No. 9-28, Piso 4",
        "schedule": "Lunes a Viernes: 7:00 a.m. a 10:00 p.m. | Soporte virtual 24/7"
    }
]
