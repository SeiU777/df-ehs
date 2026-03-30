"""備份 Claude Code 對話檔案"""
import os
import shutil

# 來源
src = os.path.expanduser(
    r"~\.claude\projects\c--Users-chloe-chang-Documents-claude---\f8c91037-d214-4021-8f25-af3d644a63a0.jsonl"
)

# 備份目錄
archive_dir = os.path.expanduser(r"~\.claude\conversation-archives\職安")
os.makedirs(archive_dir, exist_ok=True)

# 備份檔名
dst = os.path.join(archive_dir, "2026-03-13_職災分析報告與HTML生成_f8c91037.jsonl")

# 複製
shutil.copy2(src, dst)

# 回報
size_mb = os.path.getsize(dst) / (1024 * 1024)
print(f"✅ 對話已備份")
print(f"")
print(f"📄 備份位置：{dst}")
print(f"📊 檔案大小：{size_mb:.2f} MB")
print(f"🆔 Session ID：f8c91037-d214-4021-8f25-af3d644a63a0")
print(f"")
print(f"原始對話仍在原位，可正常使用 --resume 繼續。")
