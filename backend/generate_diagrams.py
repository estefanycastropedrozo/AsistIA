import os
from PIL import Image, ImageDraw, ImageFont

def create_gantt_chart():
    width, height = 1200, 600
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    # Header
    draw.rectangle([(0, 0), (width, 70)], fill="#0F4C81")
    draw.text((30, 22), "DIAGRAMA DE GANTT - PROYECTO ASISTIA TEINCO 2026", fill="#FFFFFF")
    
    # Columns (Months)
    months = ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6", "Mes 7", "Mes 8", "Mes 9", "Mes 10", "Mes 11", "Mes 12"]
    start_x = 350
    col_w = (width - start_x - 30) / 12
    
    for i, m in enumerate(months):
        x = start_x + i * col_w
        draw.line([(x, 80), (x, height - 30)], fill="#E2E8F0", width=1)
        draw.text((x + 8, 85), m, fill="#475569")
        
    tasks = [
        ("1. Levantamiento de Requisitos y Curaduría", 0, 2, "#3B82F6"),
        ("2. Diseño de Arquitectura RAG y Modelos UML", 1.5, 4, "#10B981"),
        ("3. Desarrollo del Núcleo Backend FastAPI & Vector Store", 3.5, 7, "#F59E0B"),
        ("4. Construcción Frontend React SPA & Dashboard", 5, 8.5, "#6366F1"),
        ("5. Ingesta Documental y Módulo de PDFs", 7, 9.5, "#EC4899"),
        ("6. Control de Acceso RBAC y Seguridad Ley 1581", 8, 10, "#8B5CF6"),
        ("7. Pruebas de Carga, Anti-Alucinaciones y Validación", 9, 11, "#14B8A6"),
        ("8. Despliegue Piloto y Documentación Final", 10, 12, "#0F4C81")
    ]
    
    y = 125
    for name, start_m, end_m, color in tasks:
        draw.text((30, y + 4), name, fill="#1E293B")
        bx1 = start_x + start_m * col_w
        bx2 = start_x + end_m * col_w
        draw.rounded_rectangle([(bx1, y), (bx2, y + 26)], radius=5, fill=color)
        y += 50
        
    img.save("diagram_gantt.png")
    print("Gantt chart created: diagram_gantt.png")

def create_uml_model():
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.rectangle([(0, 0), (width, 60)], fill="#0F4C81")
    draw.text((30, 18), "MODELO ENTIDAD-RELACIÓN Y PERSISTENCIA (SQLALCHEMY ORM) - ASISTIA", fill="#FFFFFF")
    
    # Tables definition
    tables = [
        ("conversation_sessions", 50, 100, 320, 220, [
            ("PK id : Integer", True),
            ("session_token : String(64) UNIQUE", True),
            ("user_role : String(32)", False),
            ("created_at : DateTime", False),
            ("last_active : DateTime", False)
        ]),
        ("chat_messages", 430, 100, 360, 290, [
            ("PK id : Integer", True),
            ("FK session_id : Integer", True),
            ("sender : String(16)", False),
            ("content : Text (Sanitizado)", False),
            ("detected_division : String(64)", False),
            ("confidence_score : Float", False),
            ("response_time_ms : Float", False),
            ("created_at : DateTime", False)
        ]),
        ("message_feedbacks", 850, 100, 300, 200, [
            ("PK id : Integer", True),
            ("FK message_id : Integer", True),
            ("is_helpful : Boolean", False),
            ("comment : Text", False),
            ("created_at : DateTime", False)
        ]),
        ("knowledge_articles", 50, 420, 360, 270, [
            ("PK id : Integer", True),
            ("division : String(64)", False),
            ("category : String(64)", False),
            ("title : String(255)", False),
            ("content : Text", False),
            ("keywords : Text", False),
            ("contact_email : String(128)", False),
            ("created_at : DateTime", False)
        ]),
        ("admin_users", 500, 450, 340, 240, [
            ("PK id : Integer", True),
            ("email : String(128) UNIQUE", True),
            ("full_name : String(128)", False),
            ("password_hash : String(255)", False),
            ("role : String(32) [SuperAdmin/Operario]", False),
            ("is_active : Boolean", False)
        ])
    ]
    
    for tname, x, y, w, h, cols in tables:
        # Box header
        draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=6, fill="#FFFFFF", outline="#CBD5E1", width=2)
        draw.rounded_rectangle([(x, y), (x + w, y + 36)], radius=6, fill="#0F4C81")
        draw.text((x + 12, y + 9), tname, fill="#FFFFFF")
        
        cy = y + 46
        for col, is_pk in cols:
            color = "#0F4C81" if is_pk else "#334155"
            draw.text((x + 14, cy), col, fill=color)
            cy += 30
            
    # Connector lines
    # sessions -> messages
    draw.line([(370, 170), (430, 170)], fill="#0F4C81", width=2)
    draw.polygon([(425, 165), (430, 170), (425, 175)], fill="#0F4C81")
    draw.text((380, 150), "1 : N", fill="#64748B")
    
    # messages -> feedbacks
    draw.line([(790, 170), (850, 170)], fill="#0F4C81", width=2)
    draw.polygon([(845, 165), (850, 170), (845, 175)], fill="#0F4C81")
    draw.text((800, 150), "1 : 1", fill="#64748B")
    
    img.save("diagram_uml_model.png")
    print("UML model diagram created: diagram_uml_model.png")

if __name__ == "__main__":
    create_gantt_chart()
    create_uml_model()
