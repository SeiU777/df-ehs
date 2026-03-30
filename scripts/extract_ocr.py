"""使用 pdfplumber 嘗試提取 PDF 文字，若失敗則用 OCR"""
import sys
import subprocess
import os

# 安裝必要套件
for pkg in ["pdfplumber"]:
    try:
        __import__(pkg)
    except ImportError:
        print(f"正在安裝 {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

import pdfplumber

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "職安手冊")
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "職安手冊_text")
os.makedirs(output_dir, exist_ok=True)

pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    txt_name = pdf_file.replace(".pdf", ".txt")
    txt_path = os.path.join(output_dir, txt_name)

    print(f"\n處理: {pdf_file}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"  頁數: {total_pages}")

            all_text = []
            for i, page in enumerate(pdf.pages):
                # 提取文字
                text = page.extract_text()
                if text and text.strip():
                    all_text.append(f"\n=== 第 {i+1} 頁 ===\n{text}")
                else:
                    # 嘗試提取表格
                    tables = page.extract_tables()
                    if tables:
                        table_text = []
                        for t_idx, table in enumerate(tables):
                            for row in table:
                                row_text = " | ".join([str(cell) if cell else "" for cell in row])
                                table_text.append(row_text)
                        all_text.append(f"\n=== 第 {i+1} 頁 (表格) ===\n" + "\n".join(table_text))
                    else:
                        all_text.append(f"\n=== 第 {i+1} 頁 (無法提取文字，可能為圖片) ===")

            final_text = "\n".join(all_text)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(final_text)

            # 統計有效頁數
            text_pages = sum(1 for t in all_text if "無法提取文字" not in t)
            print(f"  有文字頁數: {text_pages}/{total_pages}")
            print(f"  已儲存: {txt_name} ({len(final_text)} 字元)")

    except Exception as e:
        print(f"  錯誤: {e}")

print("\n=== 全部完成！===")
print(f"文字檔已儲存至: {output_dir}")
