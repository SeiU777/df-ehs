"""搜尋 Excel 中包含「吳柏勝」的所有資料列"""
import pandas as pd

file_path = r'c:\Users\chloe.chang\Documents\claude\職安\參考資料\公司職災資料\職災統計__2023.1-2025.12.xlsx'

# 讀取所有工作表
xls = pd.ExcelFile(file_path)
print('工作表列表:', xls.sheet_names)
print()

for sheet in xls.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet, dtype=str)
    print(f'=== 工作表: {sheet} (共 {len(df)} 列, {len(df.columns)} 欄) ===')
    print(f'欄位: {list(df.columns)}')

    # 在所有欄位中搜尋「吳柏勝」
    mask = df.apply(lambda row: row.astype(str).str.contains('吳柏勝', na=False).any(), axis=1)
    matched = df[mask]

    if len(matched) > 0:
        print(f'找到 {len(matched)} 筆包含「吳柏勝」的資料:')
        for idx, row in matched.iterrows():
            print(f'\n--- 第 {idx} 列 ---')
            for col in df.columns:
                print(f'  {col}: {row[col]}')
    else:
        print('未找到包含「吳柏勝」的資料')
    print()
