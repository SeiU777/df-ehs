"""使用 PyMuPDF + OCR 提取掃描型 PDF 的文字內容"""
import sys
import subprocess
import os

# 安裝必要套件
packages = ["pymupdf"]
for pkg in packages:
    try:
        __import__(pkg.replace("-", ""))
    except ImportError:
        print(f"正在安裝 {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

import fitz  # pymupdf

pdf_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "職安手冊")
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "職安手冊_text")
os.makedirs(output_dir, exist_ok=True)

pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])

total_extracted = 0

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_dir, pdf_file)
    txt_name = pdf_file.replace(".pdf", ".txt")
    txt_path = os.path.join(output_dir, txt_name)

    print(f"\n處理: {pdf_file}")
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"  頁數: {total_pages}")

        all_text = []
        text_pages = 0
        for i in range(total_pages):
            page = doc[i]
            # 嘗試多種方式提取文字
            text = page.get_text("text")
            if not text or not text.strip():
                text = page.get_text("blocks")
                if text:
                    text = "\n".join([block[4] for block in text if block[6] == 0])

            if text and text.strip():
                all_text.append(f"\n=== 第 {i+1} 頁 ===\n{text.strip()}")
                text_pages += 1
            else:
                all_text.append(f"\n=== 第 {i+1} 頁 (圖片頁) ===")

        doc.close()

        final_text = "\n".join(all_text)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        print(f"  有文字頁數: {text_pages}/{total_pages}")
        print(f"  已儲存: {txt_name} ({len(final_text)} 字元)")
        total_extracted += text_pages

    except Exception as e:
        print(f"  錯誤: {e}")

print(f"\n=== 全部完成！===")
print(f"總共提取到文字的頁數: {total_extracted}")
print(f"文字檔已儲存至: {output_dir}")

if total_extracted == 0:
    print("\n*** 所有頁面都是掃描圖片，需要 OCR ***")
    print("正在嘗試安裝 easyocr 進行 OCR（這可能需要幾分鐘）...")

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "easyocr", "-q"])
        import easyocr

        reader = easyocr.Reader(['ch_tra', 'en'], gpu=False)
        print("OCR 引擎已就緒，開始辨識...")

        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            txt_name = pdf_file.replace(".pdf", ".txt")
            txt_path = os.path.join(output_dir, txt_name)

            print(f"\nOCR 處理: {pdf_file}")
            doc = fitz.open(pdf_path)
            all_text = []

            for i in range(len(doc)):
                page = doc[i]
                # 將頁面轉換為圖片
                pix = page.get_pixmap(dpi=200)
                img_path = os.path.join(output_dir, f"temp_page_{i}.png")
                pix.save(img_path)

                # OCR 辨識
                results = reader.readtext(img_path, detail=0)
                text = "\n".join(results)

                if text.strip():
                    all_text.append(f"\n=== 第 {i+1} 頁 ===\n{text}")
                    print(f"  第 {i+1} 頁: {len(text)} 字元")
                else:
                    all_text.append(f"\n=== 第 {i+1} 頁 (無法辨識) ===")
                    print(f"  第 {i+1} 頁: 無法辨識")

                # 刪除暫存圖片
                os.remove(img_path)

            doc.close()

            final_text = "\n".join(all_text)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(final_text)
            print(f"  已儲存: {txt_name} ({len(final_text)} 字元)")

        print("\n=== OCR 全部完成！===")

    except Exception as e:
        print(f"\nOCR 失敗: {e}")
        print("建議手動安裝: pip install easyocr")
        print("然後重新執行此腳本")
