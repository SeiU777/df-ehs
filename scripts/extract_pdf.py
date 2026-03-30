"""提取職安手冊 PDF 文字內容"""
import sys
import os

try:
    from pypdf import PdfReader
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf", "-q"])
    from pypdf import PdfReader

pdf_dir = os.path.join(os.path.dirname(__file__), "職安手冊")
output_dir = os.path.join(os.path.dirname(__file__), "職安手冊_text")
os.makedirs(output_dir, exist_ok=True)

pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    txt_name = pdf_file.replace(".pdf", ".txt")
    txt_path = os.path.join(output_dir, txt_name)

    print(f"處理: {pdf_file}")
    try:
        reader = PdfReader(pdf_path)
        print(f"  頁數: {len(reader.pages)}")

        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- 第 {i+1} 頁 ---\n{page_text}"

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  已儲存: {txt_name}")
    except Exception as e:
        print(f"  錯誤: {e}")

print("\n完成！")
