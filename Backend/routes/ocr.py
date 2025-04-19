from schemas import OCRResponse
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
import easyocr
from PIL import Image
import io
import os
import tempfile
import fitz
import docx2txt
from pathlib import Path
import numpy as np
import time

ocr_router = APIRouter(prefix="/ocr", tags=["OCR"])

router = APIRouter(tags=["OCR"], prefix="/ocr")

supported_image_formats = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
supported_document_formats = {".pdf", ".docx", ".doc", ".txt"}

_reader = None

def get_ocr_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['ru', 'en'], gpu=False)
    return _reader

async def process_image(image_data: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_data))
        img_array = np.array(image)
        reader = get_ocr_reader()
        
        result = reader.readtext(img_array)
        
        text = " ".join([item[1] for item in result])
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки изображения: {str(e)}")

async def process_pdf(pdf_data: bytes) -> str:
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(pdf_data)
            temp_file_path = temp_file.name
        
        text = ""
        doc = fitz.open(temp_file_path)
        
        try:
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                
                if not page_text.strip():
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    page_text = await process_image(img_data)
                
                text += f"\n--- Страница {page_num + 1} ---\n" + page_text
        finally:
            doc.close()
            
        time.sleep(0.5)
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                os.unlink(temp_file_path)
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(1)
                else:
                    pass
        
        return text
    except Exception as e:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Ошибка обработки PDF: {str(e)}")

async def process_docx(docx_data: bytes) -> str:
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
            temp_file.write(docx_data)
            temp_file_path = temp_file.name
        
        text = docx2txt.process(temp_file_path)
        
        time.sleep(0.5)
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                os.unlink(temp_file_path)
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(1)
                else:
                    pass
        
        return text
    except Exception as e:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Ошибка обработки DOCX: {str(e)}")

async def process_txt(txt_data: bytes) -> str:
    try:
        return txt_data.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return txt_data.decode('cp1251')
        except UnicodeDecodeError:
            for encoding in ['latin-1', 'ISO-8859-5', 'KOI8-R']:
                try:
                    return txt_data.decode(encoding)
                except UnicodeDecodeError:
                    continue
            raise HTTPException(status_code=500, detail="Не удалось определить кодировку текстового файла")

@router.post("/extract-text", response_model=OCRResponse)
async def extract_text(file: UploadFile = File(...)):
    """
    Я ЧОКОПАЙ Я ЧОКОПАЙ
    """
    file_extension = Path(file.filename).suffix.lower() if file.filename else ""
    
    if not file_extension:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Не удалось определить тип файла"}
        )
    
    file_content = await file.read()
    
    try:
        if file_extension in supported_image_formats:
            text = await process_image(file_content)
            file_type = "image"
        elif file_extension == ".pdf":
            text = await process_pdf(file_content)
            file_type = "pdf"
        elif file_extension in {".docx", ".doc"}:
            text = await process_docx(file_content)
            file_type = "document"
        elif file_extension == ".txt":
            text = await process_txt(file_content)
            file_type = "text"
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False, 
                    "message": f"Неподдерживаемый формат файла: {file_extension}",
                    "file_type": "unknown",
                    "text": ""
                }
            )
        
        if not text.strip():
            return OCRResponse(
                text="", 
                success=False,
                file_type=file_type,
                message="Текст не обнаружен или файл пуст"
            )
        
        return OCRResponse(text=text, success=True, file_type=file_type)
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False, 
                "message": e.detail,
                "file_type": file_extension[1:],
                "text": ""
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False, 
                "message": f"Произошла ошибка при обработке файла: {str(e)}",
                "file_type": file_extension[1:],
                "text": ""
            }
        )