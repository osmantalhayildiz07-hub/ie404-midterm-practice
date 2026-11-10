# IE404 Midterm Practice

Interactive multiple-choice practice for **IE404 Management for Engineers (METU)** midterm topics.
584 original questions with explanations and source page references. Questions from the
instructor's **lecture slides** and from the **reading assignments** are kept in separate areas.

**Open the app:** https://osmantalhayildiz07-hub.github.io/ie404-midterm-practice/

## Lecture slides (434 questions)
| Week | Deck | Questions |
|---|---|---|
| 1 | Winning on Purpose | 70 |
| 2 | Ethics | 70 |
| 3 | Effective Communication | 70 |
| 4 | Build and Manage Your Team | 84 |
| 5 | Organizational Awareness | 70 |
| 6 | Crisis and Conflict Management and Negotiation | 70 |

## Reading assignments (150 questions)
| Week | Reading | Questions |
|---|---|---|
| 1 | 5 Ways to Become More Self-Aware | 15 |
| 1 | Working with People Who Aren't Self-Aware | 15 |
| 2 | How to Tackle Your Toughest Decisions | 30 |
| 3 | 8 Communication Techniques Engineering Leaders Need to Succeed | 18 |
| 4 | High-Performing Teams Start with a Culture of Shared Values | 12 |
| 5 | The Leader's Guide to Corporate Culture | 30 |
| 6 | Conflict Analysis Tools | 30 |

## Modes
- **Practice** a single deck or reading, or all slides / all readings — random order, instant feedback with explanation and source page.
- **Full exam** — slides + readings, slides only, or readings only; 50 / 100 / all questions drawn in proportion to each document; optional timer; answers at the end.
- **My mistakes** — re-practice questions you last answered wrong (progress is stored in your browser only).

Keyboard: `1–4` or `A–D` to answer, `Enter` next, `←` previous (exam).

## Editing questions
Each document has its own file: `bank/lectures/*.py` and `bank/readings/*.py`
(a `META` header plus `QS` tuples: `(id, page, question, correct, [3 distractors], explanation)`). After editing:

```bash
python bank/build.py      # validates and writes questions.json
python bank/make_app.py   # embeds questions into index.html
```

Questions are study aids written from the course materials; course PDFs are not included in this repository.
