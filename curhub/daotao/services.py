from django.db import transaction
from .models import (
    ChuongTrinhDaoTao, MucTieuDaoTao, 
    ChuanDauRa, ChiTietHocPhanTrongCTDT,
    HocPhan
)
import pandas as pd
import docx
import json
import langextract as lx

def import_program_from_docx(file_path: str) -> dict:
    """
    Import training program from a .docx file using LangExtract.
    Returns a dict matching import_program_schema.
    """
    doc = docx.Document(file_path)
    # Flatten all tables into text
    text_blocks = []
    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            text_blocks.append("\\t".join(cells))
        text_blocks.append("")
    full_text = "\\n".join(text_blocks)
    # Load the JSON schema
    schema_path = "curhub/daotao/schemas/import_program_schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    # Prompt construction
    prompt = (
        "Extract a JSON object matching the following JSON schema:\\n"
        f"{json.dumps(schema)}\\n\\n"
        "From this text:\\n"
        f"{full_text}"
    )
    # Run extraction
    result = lx.extract(
        text_or_documents=full_text,
        prompt_description=prompt,
        examples=[],
        model_id="gemini-2.5-flash",
        fence_output=True
    )
    return result

# Business logic functions will be defined here
def clone_chuong_trinh_dao_tao(original_ctdt_pk: int) -> ChuongTrinhDaoTao:
    """
    Tạo một phiên bản mới (clone) từ một CTĐT đã có.
    """
    pass

def process_uploaded_courses_file(file, ctdt) -> (int, int, list):
    """
    Xử lý file upload học phần và thêm vào CTĐT.
    Trả về: (success_count, error_count, errors_list)
    """
    pass
