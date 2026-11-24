"""score.py — score the client model's answer against the SAME rules Vault 2 used.

Run:  .venv\\Scripts\\python.exe score.py answers.txt
answers.txt = the model's final block, copied verbatim from the chat, four lines like:
    Q1: 1, 7, 19, 24
Markdown the chat may add (**bold**, `code`, bullets) is ignored, and so are chapter labels and stray
punctuation: "Q2: 2, 5, 13, 21." and "Q3: Ch 4, ch-5, chapter 7, 14" both read as four numbers.
A line counts only if, after its label, it holds nothing but chapter numbers. If a question appears
more than once, the LAST such line counts (the prompt asks for the four lines at the very end).
Only the first four numbers count, and they must be four different chapters.
The rules are copied from Vault 2's spine_search.py (sealed 18 Oct); they are not changed for Vault 3.
Vault 2's column is the take's result: run 20261101_171405, SPINE_PARTIAL 1/4.

Live Edition (2 Nov 2026), snag V3-S01: the final-rehearsal build read "Q2: 2, 5, 13, 21." (a full stop)
or "Q3: Ch 4, 5, 7, 14" as MISSING, so a held thread would have printed NOT HELD on camera.
The rules and the output format are unchanged.
"""
import re, sys
sys.stdout.reconfigure(errors="replace")
RULES = {  # identical to Vault 2 (sealed 18 Oct)
    "Q1": ({1, 7, 19, 24}, 3, "the watcher"),
    "Q2": ({2, 5, 13, 21}, 2, "the lie"),
    "Q3": ({4, 5, 7},      2, "the cost"),
    "Q4": ({22, 23, 24},   2, "the door"),
}
V2 = {"Q1": "HELD", "Q2": "NOT HELD", "Q3": "NOT HELD", "Q4": "NOT HELD"}   # Vault 2 take, local only

text = re.sub(r"[*`>#_\-–—]", " ", open(sys.argv[1], encoding="utf-8-sig").read())

def answer(q: str) -> list[int]:
    """The chapters on the last line labelled q (e.g. 'Q1:', 'Q1.', 'Q1 )') that holds only numbers."""
    found = []
    for line in text.splitlines():
        m = re.match(rf"^\s*{q}(?!\d)\s*[:.)]?\s*(.*)$", line, re.IGNORECASE)
        if not m:
            continue
        rest = re.sub(r"(?i)\b(?:chapters?|chs?)\b\.?", " ", m.group(1))   # 'Ch 4', 'chapter 7'
        if re.search(r"\d", rest) and re.fullmatch(r"[\d\s,.;/]*", rest):
            found = [int(x) for x in re.findall(r"\d+", rest)][:4]
    return found

held = 0
print(f"{'':4} {'thread':<12} {'answer (top 4)':<18} {'predicted':<16} {'rule':<6} {'V3':<10} V2 (local)")
for q, (expected, need, label) in RULES.items():
    got = answer(q)
    hit = len([c for c in got if c in expected])
    ok = len(got) == 4 and len(set(got)) == 4 and hit >= need   # four different chapters, as Vault 2 ranked them
    held += ok
    print(f"{q:4} {label:<12} {', '.join(map(str, got)) or 'MISSING':<18} "
          f"{', '.join(map(str, sorted(expected))):<16} >={need:<4} "
          f"{'HELD' if ok else 'NOT HELD':<10} {V2[q]}")
print(f"\n{'V3_SPINE_OK' if held == 4 else 'V3_SPINE_PARTIAL'}  {held}/4 held   (Vault 2, local only: 1/4)")
