"""Embed questions.json into app_template.html -> index.html (fully offline, single file)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
qs = json.load(open(os.path.join(ROOT, "questions.json"), encoding="utf-8"))
data = json.dumps(qs, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
tpl = open(os.path.join(HERE, "app_template.html"), encoding="utf-8").read()
assert "/*__QUESTIONS__*/[]" in tpl
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(tpl.replace("/*__QUESTIONS__*/[]", data))
print(f"index.html written with {len(qs)} questions")
