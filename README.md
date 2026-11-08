# IE404 Midterm Practice

Interactive multiple-choice practice for **IE404 Management for Engineers (METU)** midterm topics.
500 original questions with explanations and source references (lecture notes + weekly readings).

**Open the app:** https://osmantalhayildiz07-hub.github.io/ie404-midterm-practice/

## Sections (100 questions each: ~70 lecture notes, ~30 readings)
1. Winning on Purpose (+ self-awareness readings)
2. Ethics (+ How to Tackle Your Toughest Decisions)
3. Effective Communication (+ 8 Communication Techniques, High-Performing Teams)
4. Organizational Awareness (+ The Leader's Guide to Corporate Culture)
5. Crisis and Conflict Management and Negotiation (+ Conflict Analysis Tools)

## Modes
- **Section practice** â€” random order, instant feedback with explanation and source page.
- **Full exam** â€” 50 / 100 / 500 questions drawn across sections, optional timer, answers at the end.
- **My mistakes** â€” re-practice questions you last answered wrong (progress is stored in your browser only).

Keyboard: `1â€“4` or `Aâ€“D` to answer, `Enter` next, `â†` previous (exam).

## Editing questions
Questions live in `bank/s*.py`. After editing:

```bash
python bank/build.py      # validates and writes questions.json
python bank/make_app.py   # embeds questions into index.html
```

Questions are study aids written from the course materials; course PDFs are not included in this repository.
