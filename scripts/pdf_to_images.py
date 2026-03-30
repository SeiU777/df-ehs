"""將 PDF 頁面轉換為圖片，供 Claude 直接閱讀"""
import sys
import subprocess
import os

try:
    import fitz
except ImportError:
    print("正在安裝 pymupdf...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymupdf", "-q"])
    import fitz

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "職安手冊")
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "職安手冊_images")
os.makedirs(output_dir, exist_ok=True)

pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    base_name = pdf_file.replace(".pdf", "")

    print(f"\n處理: {pdf_file}")
    doc = fitz.open(pdf_path)
    print(f"  頁數: {len(doc)}")

    for i in range(len(doc)):
        page = doc[i]
        # 轉換為圖片 (150 DPI，平衡品質與檔案大小)
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(output_dir, f"{base_name}_p{i+1:02d}.png")
        pix.save(img_path)
        print(f"  第 {i+1} 頁 -> {os.path.basename(img_path)}")

    doc.close()

print(f"\n=== 全部完成！===")
print(f"圖片已儲存至: {output_dir}")
