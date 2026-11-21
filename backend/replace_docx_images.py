import os
import zipfile
import io
from PIL import Image

def update_zip_images(docx_path):
    media_dir = r"C:\Users\Anderson\.gemini\antigravity\brain\fe79d206-c449-400d-b3df-a376a2910183\.user_uploaded"
    
    img_map = {
        "word/media/image5.jpeg": "diagram_gantt.png",
        "word/media/image6.jpeg": "diagram_uml_model.png",
        "word/media/image7.jpeg": os.path.join(media_dir, "media_1793732884639.png"),
        "word/media/image8.jpeg": os.path.join(media_dir, "media_1793733621519.png"),
        "word/media/image9.jpeg": os.path.join(media_dir, "media_1793734747181.png"),
        "word/media/image10.jpeg": os.path.join(media_dir, "media_1793734758927.png"),
        "word/media/image11.jpeg": os.path.join(media_dir, "media_1793735544710.png"),
        "word/media/image12.jpeg": os.path.join(media_dir, "media_1793735574053.png"),
        "word/media/image13.jpeg": os.path.join(media_dir, "media_1793732415950.png"),
        "word/media/image14.jpeg": os.path.join(media_dir, "media_1793732895868.png"),
        "word/media/image15.jpeg": os.path.join(media_dir, "media_1793728158755.png"),
        "word/media/image16.jpeg": os.path.join(media_dir, "media_1793725646743.png"),
        "word/media/image17.jpeg": os.path.join(media_dir, "media_1793725923966.png")
    }
    
    # Pre-convert replacements to JPEG bytes
    replacements = {}
    for target_name, src_file in img_map.items():
        if os.path.exists(src_file):
            im = Image.open(src_file)
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGB")
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=92)
            replacements[target_name] = buf.getvalue()
            print(f"Prepared replacement for {target_name} from {src_file}")
            
    # Re-write zip
    temp_zip = docx_path + ".tmp.zip"
    with zipfile.ZipFile(docx_path, 'r') as zin, zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename in replacements:
                zout.writestr(item, replacements[item.filename])
            else:
                zout.writestr(item, zin.read(item.filename))
                
    os.replace(temp_zip, docx_path)
    print("Zip image replacement complete!")

if __name__ == "__main__":
    update_zip_images("AsistIA_Doc_Final.docx")
