from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

PDF_DIR = Path("myPDF")
OUTPUT_DIR = Path("assets")

# Render quality
DPI = 300
QUALITY = 90


def clean_name(name: str) -> str:
    # Remove duplicate .pdf extensions if present
    while name.lower().endswith(".pdf"):
        name = name[:-4]
    return name.strip()


def pdf_to_webp(pdf_path: Path):
    folder_name = clean_name(pdf_path.name)
    out_dir = OUTPUT_DIR / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)

    zoom = DPI / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_no, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples,
        )

        img.save(
            out_dir / f"page_{page_no:03}.webp",
            format="WEBP",
            quality=QUALITY,
            method=6,
        )

    doc.close()
    print(f"✓ {pdf_path.name} -> {out_dir}")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    pdfs = sorted(PDF_DIR.glob("*.pdf"))

    if not pdfs:
        print("No PDFs found.")
        return

    for pdf in pdfs:
        pdf_to_webp(pdf)

    print("\nDone!")


if __name__ == "__main__":
    main()