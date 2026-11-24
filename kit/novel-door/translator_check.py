"""translator_check.py — Gate 1: is this new venv the SAME translator as the Vault 2 run?

Run:  .venv\\Scripts\\python.exe translator_check.py
Re-embeds Vault 2's four questions with this venv's sentence-transformers and compares them with
the vectors vector-snake wrote on the day: Vault 2's run 20261101_171405, exported by gate.sql to
novel-ssot\\spine\\questions.parquet. If they drift, a question asked through the server would be measured
with a different ruler than the book. Ends with SAME_TRANSLATOR or TRANSLATOR_DRIFT.
"""
import os, sys
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq

os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
BOOK = Path(os.environ.get("NOVEL_SSOT", r"C:\Dev\novel-ssot"))
import sentence_transformers, torch
from sentence_transformers import SentenceTransformer

rows = pq.read_table(BOOK / "spine" / "questions.parquet").to_pylist()
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
print(f"VENV       sentence-transformers {sentence_transformers.__version__} · torch {torch.__version__}")
worst = 1.0
for r in rows:
    new = model.encode([r["text"]], normalize_embeddings=True)[0]
    old = np.asarray(r["vector"], dtype=np.float32)
    cos = float(np.dot(new, old) / (np.linalg.norm(new) * np.linalg.norm(old)))
    worst = min(worst, cos)
    print(f"{r['qid'].upper():<4} cosine {cos:.6f}  {r['text'][:60]}")
if worst >= 0.9999:
    print(f"SAME_TRANSLATOR  min cosine {worst:.6f} >= 0.9999")
else:
    sys.exit(f"TRANSLATOR_DRIFT  min cosine {worst:.6f} < 0.9999")
