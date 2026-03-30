"""提取 HSG 48 PDF 文字內容並儲存為文字檔"""
import sys
import os

try:
    from pypdf import PdfReader
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf", "-q"])
    from pypdf import PdfReader

pdf_path = r"C:\Users\chloe.chang\Desktop\HSG 48.pdf"
output_path = os.path.join(os.path.dirname(__file__), "HSG48_text.txt")

print(f"讀取: {pdf_path}")
reader = PdfReader(pdf_path)
print(f"總頁數: {len(reader.pages)}")

text = ""
for i, page in enumerate(reader.pages):
    page_text = page.extract_text()
    if page_text:
        text += f"\n=== PAGE {i+1} ===\n{page_text}"
    print(f"  處理第 {i+1}/{len(reader.pages)} 頁")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\n已儲存至: {output_path}")
print(f"總字元數: {len(text)}")
