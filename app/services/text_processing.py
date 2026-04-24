from pathlib import Path

from fastapi import HTTPException


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise HTTPException(status_code=500, detail="pypdf is required to parse PDF files") from exc

        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)

    if suffix in {".docx", ".doc"}:
        try:
            import docx
        except ImportError as exc:
            raise HTTPException(status_code=500, detail="python-docx is required to parse DOCX files") from exc

        document = docx.Document(str(path))
        return "\n".join(p.text for p in document.paragraphs)

    raise HTTPException(status_code=400, detail=f"Unsupported file format: {suffix}")
