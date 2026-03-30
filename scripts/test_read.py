# 讀取 PDF 前 3 頁文字並寫入 test_output.txt
import sys

try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf 未安裝，嘗試安裝中...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    from pypdf import PdfReader

pdf_path = r"c:\Users\chloe.chang\Documents\claude\職安\職安手冊\指南附件A.pdf"
output_path = r"c:\Users\chloe.chang\Documents\claude\職安\test_output.txt"

reader = PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"PDF 總頁數: {total_pages}")

texts = []
for i in range(min(3, total_pages)):
    page = reader.pages[i]
    text = page.extract_text()
    texts.append(f"=== 第 {i+1} 頁 ===\n{text}\n")
    print(f"已讀取第 {i+1} 頁")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(texts))

print(f"已寫入 {output_path}")
