# Mentorship Bootcamp

Welcome. This repo is where you'll push everything you build during the 12-week backend roadmap. Read this whole file before your first commit.

## How this repo works

Each of you has your **own folder** under `students/`. That's your space — keep it organized, and don't touch anyone else's.

Inside your folder, you create a new folder for **each week**: `week-01`, `week-02`, `week-03`, and so on. Each week folder has its own code, and reflection.

```
rushd-n/
├── README.md                  ← you are here
├── students/
│   ├── your-name/
│   │   ├── README.md          ← introduction about yourself
│   │   ├── week-01/
│   │   │   ├── reflection.md  ← what was hard, what clicked, questions
│   │   │   └── src/           ← your actual code
│   │   ├── week-02/
│   │   └── ...
│   └── other-students/        ← DO NOT TOUCH
```

## The rules (read these carefully)

### 1. Your folder is your folder

You only write code inside `students/<your-name>/`. Do not edit, rename, move, or delete files in any other student's folder. Do not edit shared files (this README, root configs) without asking first.

If your PR changes a file with someone else's name on it, it will be rejected.

### 2. One folder per week

At the start of each week, create a new folder: `students/<your-name>/week-NN/` where `NN` is zero-padded (`week-01`, not `week-1`). Inside it, you need at minimum:

- `reflection.md` — three honest answers: what was hard, what clicked, what's still fuzzy.
- `src/` — your code for the week's exercises and deliverable.

If a week's folder is missing reflection, **the week isn't done**, regardless of how good the code is.

### 3. `reflection.md` is required every week

This isn't busywork. Writing what you learned forces you to notice what you actually learned (vs. what you copied). Three sections:

```markdown
# Week N reflection

## What was hard
...

## What clicked
...

## What's still fuzzy
...
```

Keep it short — 5–10 sentences total is fine. Be honest. "Everything was easy" is almost never true and tells me you're not paying attention. "I still don't get async" is useful — I can help with that.

### 4. Never merge to `main` without review

You never push directly to `main`. Ever. Workflow:

1. Create a branch named `<your-name>/week-NN-topic` (example: `muhammad/week-03-pydantic`).
2. Commit and push to that branch as you work — multiple times per week, not all at once on Sunday night.
3. When the week's deliverable is done, open a Pull Request to `main`.
4. **Tag @mohammedbabelly20 in the PR description and request my review.**
5. Wait for review. I'll leave comments. Address them in new commits on the same branch (don't force-push).
6. Once I approve, you merge. Not before.

If you merge to `main` without my approval, I will revert it and we will have a conversation.

### 5. Commit messages

Bad commits make your code unreviewable and your git history useless. Rules:

- **Imperative mood:** "add login endpoint", not "added" or "adds".
- **Under 50 characters** for the subject line.
- **Specific.** "fix", "update", "wip", "changes", "asdf" — all rejected. Tell me *what* changed.
- If the change needs context, add a blank line and a short paragraph explaining *why*.

Good examples:

```
add CSV reader with type hints
fix off-by-one in pagination offset
refactor todo storage to use Pydantic models
```

Bad examples:

```
fix
updates
wip changes to file
asdf
final fixes (please work this time)
```

## Getting started

1. Make sure your GitHub account is added as a collaborator on this repo.
2. Clone the repo: `git clone <repo-url>`
3. Create your folder: `mkdir -p students/<your-name>` (use lowercase, no spaces — `ahmed`, not `Ahmed Khalid`).
4. Add a `students/<your-name>/README.md` with a short intro about yourself and your goals.
5. Open a PR titled "Add <your-name> to students" and tag me.
6. Once merged, you're ready for week 1.

## Questions?

Ask in our group chat. If it's a code question, push your code first so I can see it — "I have a bug" with no code is impossible to help with.

Good luck. Push often, ask early, and don't fake the reflections.

— Mohammed (@mohammedbabelly20)