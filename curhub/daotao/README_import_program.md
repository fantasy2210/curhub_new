# Import Training Program Module

This document explains the **import_training_program** functionality, so that any AI tool can use it to fully extract and ingest curriculum data into our system.

## Overview

- **Service function**: `import_program_from_docx(file_path: str) -> dict`  
  - Reads a `.docx` file containing one or more tables of training-program data.
  - Flattens each table row into tab-separated text lines.
  - Builds a prompt combining:
    1. The JSON Schema (`schemas/import_program_schema.json`).
    2. The extracted table text.
  - Calls **LangExtract** (`lx.extract`) with zero examples to parse and return a JSON object matching the schema.
  - Returns a Python `dict` representing the program and its courses.

- **Management command**: `import_training_program <docx_file>`  
  - Entry point for command-line or AI invocation.
  - Calls the service function and prints the resulting JSON to standard output.
  - Exit on any exception with an error message.

## JSON Schema

Located at: `schemas/import_program_schema.json`

```json
{
  "$schema": "...draft-07/schema#",
  "title": "TrainingProgramImport",
  "type": "object",
  "properties": { … },
  "required": ["program_code","program_name","academic_year","semester","courses"]
}
```

- Defines keys: `program_code`, `program_name`, `academic_year`, `semester`
- `courses`: array of objects with:
  - `course_code`, `course_name`, `credits`
  - Optional fields: `prerequisites`, `theory_hours`, `practice_hours`, `self_study_hours`, `evaluation`, `description`.

## Usage Example

```bash
# From project root
python manage.py import_training_program path/to/program.docx
```

Output:

```json
{
  "program_code": "CTDL2025",
  "program_name": "Công nghệ thông tin",
  "academic_year": "2025-2026",
  "semester": 1,
  "courses": [
    {
      "course_code": "IT101",
      "course_name": "Lập trình cơ bản",
      "credits": 3,
      …
    }
  ]
}
```

## Integration with AI

1. **Instruction**: Provide the DOCX file path.
2. **Command**: Invoke `import_training_program`.
3. **Capture**: Read JSON output for downstream ingestion.
4. **Validation**: Ensure JSON structure matches the schema before database insert.

This README enables any AI agent to understand and call the import process end-to-end.
## Integration with PDF Sources

If the program specification is provided as a PDF, follow these steps:

1. Convert the PDF to a DOCX or extract its tables as plain text:
   - Use a tool like `pdf2docx` or other PDF-to-DOCX converters to preserve table structure.
   - Alternatively, extract PDF tables into TSV or CSV format for easier ingestion.

2. Verify the extracted DOCX or text to ensure the tables represent rows and columns correctly.

3. Invoke the import command on the converted DOCX:
```bash
python manage.py import_training_program path/to/program.docx
```

4. For AI-driven workflows, you can feed raw PDF text directly into the service:
```python
from daotao.services import import_program_from_docx

# After converting PDF to DOCX or plain text
program_data = import_program_from_docx("path/to/converted_program.docx")
print(program_data)
```

5. Capturing the output JSON enables downstream ingestion:
   - The JSON strictly adheres to the schema in `schemas/import_program_schema.json`.
   - AI agents must include the schema and the extracted text in the prompt to `lx.extract` for accurate parsing:
   ```
   Extract a JSON object matching import_program_schema.json from this text:
   {pdf_or_docx_text}
   ```

This ensures any AI component understands how to convert PDF-based curricula into the structured format required by our system.
## Example: Doctor of Medicine Program (PDF Input)

If you receive a PDF describing the Tra Vinh MD curriculum, such as:

```
Tôi xin giới thiệu những thông tin chi tiết về chương trình đào tạo Bác sĩ Y khoa của Trường Đại học Trà Vinh. Đây là một tài liệu toàn diện, được ban hành vào năm 2024, mô tả chi tiết về cấu trúc và nội dung chương trình học.
I. Thông tin tổng quan
Tên chương trình: Bác sĩ Y khoa (Doctor of Medicine).
Trường: Khoa Y Dược, Trường Đại học Trà Vinh.
Mã ngành: 7720101.
Trình độ đào tạo: Đại học.
Hình thức đào tạo: Chính quy.
... (v.v.)
```

1. Convert the PDF to DOCX (preserving tables) or extract tables to TSV.
2. Save the result as `tra_vinh_md.docx`.
3. Run the import command:
   ```bash
   python manage.py import_training_program tra_vinh_md.docx
   ```
4. The service will:
   - Flatten all table rows into text blocks.
   - Include the JSON schema (`schemas/import_program_schema.json`) in the prompt.
   - Call LangExtract (`lx.extract`) to parse:
     - Program metadata (name, code, institution, year, credits, degree).
     - Objectives and outcomes.
     - Curriculum blocks and semester plans.
     - Detailed course information (prerequisites, content, hours).
   - Return a JSON object strictly matching the schema.

Use this JSON output for downstream ingestion or AI-driven workflows.