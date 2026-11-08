"""Build questions.json from the section files, balance answer positions, and validate.

Usage: python bank/build.py            (writes questions.json + prints report)
       python bank/build.py --check    (report only, no write)
"""
import json, os, random, re, sys, runpy
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SOURCES = {
    "WOP": "LectureNotes - Winning on Purpose.pdf",
    "SA5": "Reading - 5 Ways to Become More Self-Aware.pdf",
    "UNA": "Reading - Working with People Who Aren't Self-Aware.pdf",
    "ETH": "LectureNotes - Ethics.pdf",
    "TTD": "Reading - How to Tackle Your Toughest Decisions.pdf",
    "COM": "LectureNotes - Effective Communication.pdf",
    "ECT": "Reading - 8 Communication Techniques Engineering Leaders Need to Succeed.pdf",
    "HPT": "Reading - High-Performing Teams Start with a Culture of Shared Values.pdf",
    "ORG": "LectureNotes - Organizational Awareness.pdf",
    "CUL": "Reading - The Leader's Guide to Corporate Culture.pdf",
    "CCM": "LectureNotes - Crisis and Conflict Management and Negotiation.pdf",
    "CAT": "Reading - Conflict Analysis Tools.pdf",
}
SECTIONS = [
    ("s1_winning_on_purpose.py", 1, "Winning on Purpose"),
    ("s2_ethics.py", 2, "Ethics"),
    ("s3_communication.py", 3, "Effective Communication"),
    ("s4_organizational_awareness.py", 4, "Organizational Awareness"),
    ("s5_conflict_negotiation.py", 5, "Crisis and Conflict Management and Negotiation"),
]
TARGET = {1: 100, 2: 100, 3: 100, 4: 100, 5: 100}
BANNED = re.compile(r"\b(all|none) of the above\b|\bboth [a-d] and [a-d]\b", re.I)


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def load():
    raw = []
    for fn, num, name in SECTIONS:
        qs = runpy.run_path(os.path.join(HERE, fn))["QS"]
        for t in qs:
            raw.append((num, name) + tuple(t))
    return raw


def build(raw):
    rng = random.Random(404)
    # Balanced target positions: cycle 0..3, shuffled, so each position gets ~25%.
    n = len(raw)
    positions = [i % 4 for i in range(n)]
    rng.shuffle(positions)
    out, counters = [], Counter()
    for (num, name, key, page, q, correct, wrongs, expl), pos in zip(raw, positions):
        wrongs = list(wrongs)
        rng.shuffle(wrongs)
        opts = wrongs[:]
        opts.insert(pos, correct)
        counters[num] += 1
        out.append({
            "id": f"S{num}-{counters[num]:03d}",
            "section": name,
            "source": f"{SOURCES[key]}, p. {page}",
            "question": q,
            "options": opts,
            "answer_index": pos,
            "explanation": expl,
        })
    return out


def validate(qs, raw):
    errs, warns = [], []
    if len(qs) != 500:
        errs.append(f"Total is {len(qs)}, expected 500")
    by_sec = Counter(q["section"] for q in qs)
    for fn, num, name in SECTIONS:
        if by_sec[name] != TARGET[num]:
            errs.append(f"Section '{name}' has {by_sec[name]}, expected {TARGET[num]}")
    ids = Counter(q["id"] for q in qs)
    errs += [f"Duplicate id {i}" for i, c in ids.items() if c > 1]
    seen = {}
    for q in qs:
        o = q["options"]
        if len(o) != 4:
            errs.append(f"{q['id']}: {len(o)} options")
        if not isinstance(q["answer_index"], int) or not 0 <= q["answer_index"] <= 3:
            errs.append(f"{q['id']}: bad answer_index")
        if len({norm(x) for x in o}) != len(o):
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
    # near-duplicates: same correct answer AND high token overlap of question
    toks = [(q["id"], set(norm(q["question"]).split()), norm(q["options"][q["answer_index"]])) for q in qs]
    for i in range(len(toks)):
        for j in range(i + 1, len(toks)):
            a, b = toks[i], toks[j]
            if a[2] == b[2]:
                jac = len(a[1] & b[1]) / max(1, len(a[1] | b[1]))
                if jac > 0.6:
                    warns.append(f"Possible near-duplicate: {a[0]} / {b[0]} (jaccard {jac:.2f})")
    return errs, warns


def report(qs, raw):
    print("== Counts per section (lecture / reading) ==")
    for fn, num, name in SECTIONS:
        sec = [r for r in raw if r[0] == num]
        lec = sum(1 for r in sec if SOURCES[r[2]].startswith("LectureNotes"))
        print(f"  {name:<50} total={len(sec):>3}  lecture={lec:>3}  reading={len(sec)-lec:>3}")
        for key in sorted({r[2] for r in sec}):
            print(f"      {key}: {sum(1 for r in sec if r[2]==key)}")
    pos = Counter(q["answer_index"] for q in qs)
    print("== Answer position distribution ==", {"ABCD"[k]: pos[k] for k in range(4)})
    longest = sum(1 for q in qs if len(q["options"][q["answer_index"]]) == max(len(o) for o in q["options"]))
    print(f"== Correct option is the (tied) longest in {longest}/{len(qs)} questions ({100*longest/len(qs):.0f}%) ==")


if __name__ == "__main__":
    raw = load()
    qs = build(raw)
    report(qs, raw)
    errs, warns = validate(qs, raw)
    for w in warns:
        print("WARN:", w)
    for e in errs:
        print("ERROR:", e)
    print(f"== {len(errs)} errors, {len(warns)} warnings ==")
    if "--check" not in sys.argv:
        with open(os.path.join(ROOT, "questions.json"), "w", encoding="utf-8") as f:
            json.dump(qs, f, ensure_ascii=False, indent=1)
        print("wrote questions.json")
    sys.exit(1 if errs else 0)
