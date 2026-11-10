"""Build questions.json from bank/lectures/*.py and bank/readings/*.py, balance answer positions, validate.

Usage: python bank/build.py            (writes questions.json + prints report)
       python bank/build.py --check    (report only, no write)
"""
import json, os, random, re, sys, runpy
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BANNED = re.compile(r"\b(all|none) of the above\b|\bboth [a-d] and [a-d]\b", re.I)
TYPES = ("lecture", "reading")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def load():
    """Return list of (meta, tuple) in display order: by type, then week, then file name."""
    files = []
    for sub in ("lectures", "readings"):
        d = os.path.join(HERE, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"):
                ns = runpy.run_path(os.path.join(d, fn))
                files.append((ns["META"], ns["QS"], f"{sub}/{fn}"))
    files.sort(key=lambda f: (TYPES.index(f[0]["type"]), f[0]["week"], f[2]))
    return files


def build(files):
    rng = random.Random(404)
    raw = [(m, t) for m, qs, _ in files for t in qs]
    positions = [i % 4 for i in range(len(raw))]
    rng.shuffle(positions)
    out = []
    for (m, (qid, page, q, correct, wrongs, expl)), pos in zip(raw, positions):
        opts = list(wrongs)
        rng.shuffle(opts)
        opts.insert(pos, correct)
        out.append({
            "id": qid, "type": m["type"], "week": m["week"], "topic": m["topic"], "doc": m["title"],
            "source": f"{m['file']}, p. {page}", "question": q, "options": opts,
            "answer_index": pos, "explanation": expl,
        })
    return out


def validate(files, qs):
    errs, warns = [], []
    for m, items, path in files:
        for k in ("type", "week", "topic", "title", "file"):
            if k not in m:
                errs.append(f"{path}: META missing '{k}'")
        if m.get("type") not in TYPES:
            errs.append(f"{path}: bad type {m.get('type')}")
        for t in items:
            if len(t) != 6 or len(t[4]) != 3:
                errs.append(f"{path}: malformed tuple {t[0] if t else '?'}")
    errs += [f"Duplicate id {i}" for i, c in Counter(q["id"] for q in qs).items() if c > 1]
    seen = {}
    for q in qs:
        o = q["options"]
        if len(o) != 4:
            errs.append(f"{q['id']}: {len(o)} options")
        if not 0 <= q["answer_index"] <= 3:
            errs.append(f"{q['id']}: bad answer_index")
        if len({norm(x) for x in o}) != 4:
            errs.append(f"{q['id']}: duplicate options")
        if any(not x.strip() for x in o) or not q["question"].strip() or not q["explanation"].strip():
            errs.append(f"{q['id']}: empty field")
        for x in o + [q["question"]]:
            if BANNED.search(x):
                errs.append(f"{q['id']}: banned phrase in '{x[:50]}'")
        k = norm(q["question"])
        if k in seen:
            errs.append(f"Duplicate question: {seen[k]} and {q['id']}")
        seen[k] = q["id"]
    toks = [(q["id"], set(norm(q["question"]).split()), norm(q["options"][q["answer_index"]])) for q in qs]
    for i in range(len(toks)):
        for j in range(i + 1, len(toks)):
            a, b = toks[i], toks[j]
            if a[2] == b[2] and len(a[1] & b[1]) / max(1, len(a[1] | b[1])) > 0.6:
                warns.append(f"Possible near-duplicate: {a[0]} / {b[0]}")
    return errs, warns


def report(files, qs):
    for t in TYPES:
        sub = [q for q in qs if q["type"] == t]
        print(f"== {t.upper()} questions: {len(sub)} ==")
        for m, items, path in files:
            if m["type"] == t:
                print(f"   W{m['week']}  {m['title']:<62} {len(items):>3}")
    print(f"== TOTAL: {len(qs)} ==")
    pos = Counter(q["answer_index"] for q in qs)
    print("== Answer positions ==", {"ABCD"[k]: pos[k] for k in range(4)})
    longest = sum(1 for q in qs if len(q["options"][q["answer_index"]]) == max(map(len, q["options"])))
    print(f"== Correct option is the (tied) longest in {longest}/{len(qs)} ({100*longest/len(qs):.0f}%) ==")


if __name__ == "__main__":
    files = load()
    qs = build(files)
    report(files, qs)
    errs, warns = validate(files, qs)
    for w in warns:
        print("WARN:", w)
    for e in errs:
        print("ERROR:", e)
    print(f"== {len(errs)} errors, {len(warns)} warnings ==")
    if "--check" not in sys.argv and not errs:
        with open(os.path.join(ROOT, "questions.json"), "w", encoding="utf-8") as f:
            json.dump(qs, f, ensure_ascii=False, indent=1)
        print("wrote questions.json")
    sys.exit(1 if errs else 0)
