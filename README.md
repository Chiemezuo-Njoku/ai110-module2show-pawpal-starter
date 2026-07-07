# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Features

PawPal+ turns a flat list of pet-care tasks into an organized, self-maintaining daily plan:

- **⏱️ Sort by time** — every task carries a `due_time` (`"HH:MM"`), and `Scheduler.sort_by_time()` returns the full day in chronological order using a `sorted()` lambda key over zero-padded time strings.
- **⚠️ Conflict warnings** — `Scheduler.detect_conflicts()` groups incomplete tasks by time slot and flags when two tasks (across *any* pets) are booked at the same moment, returning non-crashing warning messages that the UI shows via `st.warning`.
- **🔁 Daily / weekly recurrence** — completing a recurring task with `Scheduler.mark_task_complete()` automatically generates its next occurrence using `datetime` + `timedelta`, so the schedule refills itself instead of emptying out.
- **🔎 Filtering** — narrow the task list by completion status (`filter_by_completion`) or by pet name, case-insensitive (`filter_by_pet`).
- **📊 Duration planning** — `organize_by_duration()` orders quick wins first and `total_remaining_minutes()` totals the outstanding workload.
- **🖥️ Streamlit UI** — add pets and tasks, mark tasks complete, and view a live, sorted schedule with inline conflict banners.
- **✅ Tested** — 16 pytest cases cover sorting, recurrence, conflict detection, and filtering.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:
Today's Schedule for Alex
================================
  [ ] Refill water           5 min  (daily)
  [ ] Clean litter box      15 min  (daily)
  [ ] Morning walk          30 min  (daily)
--------------------------------
Total time remaining: 50 min

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

The scheduling logic in `pawpal_system.py` is covered by a pytest suite in
`tests/test_pawpal.py`. Run it from the project root:

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

### What the tests cover

| Area | Scenarios verified |
|------|--------------------|
| **Sorting** (`sort_by_time`) | Tasks return in chronological order; correct across the noon boundary (zero-padded `"HH:MM"`); empty schedule is safe; tied times are preserved. |
| **Recurrence** (`mark_task_complete`) | Completing a `daily`/`weekly` task generates a fresh, incomplete next occurrence via `timedelta`; the new task is a distinct object; `once` tasks do **not** recur. |
| **Conflict detection** (`detect_conflicts`) | Tasks sharing a `due_time` are flagged; distinct times raise no warning; completed tasks free their slot; three tasks in one slot yield a single grouped warning. |
| **Filtering** | By completion status and by pet name (case-insensitive). |

### Sample test output

Paste the output of a successful `python -m pytest` run here:

```
<!-- paste `python -m pytest` output here, e.g.: -->
tests\test_pawpal.py ................                                    [100%]

============================= 16 passed in 0.05s ==============================
```

### Confidence Level

Rate your confidence in the current test coverage (1–5 stars):

**Confidence:** ⭐️⭐️⭐️⭐️⭐️ <!-- replace with your rating, e.g. ⭐️⭐️⭐️ (3/5) -->

> _Why this rating:_ <!-- one line: what gives you confidence, or what's still untested -->


## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `organize_by_duration()` | `sort_by_time` orders every task by its `due_time` ("HH:MM") via a `sorted()` lambda key; zero-padded strings compare chronologically. |
| Filtering | `Scheduler.filter_by_completion(bool)`, `filter_by_pet(name)` | Filter by done/not-done, or by pet name (case-insensitive). |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups incomplete tasks by `due_time`; returns a warning string per overlapping slot. Never raises — an empty list means no conflicts. |
| Recurring tasks | `Scheduler.mark_task_complete(task)` | Marks the task done; for `daily`/`weekly` frequency, uses `datetime` + `timedelta` to generate the next occurrence and attaches it to the owning pet. |

## 📸 Demo Walkthrough

A typical session, from empty app to a live schedule:

1. **Launch the app** — `streamlit run app.py` and open the local URL.
2. **Add a pet** — under **Add a pet**, enter a name (e.g. "Rex") and species, then submit. The pet appears in the **Your pets** table.
3. **Schedule a task** — under **Add a task**, pick the pet, describe the task (e.g. "Morning walk"), set the duration, frequency (`daily`/`weekly`/`once`), and a due time, then submit.
4. **View the schedule** — the **Schedule** table lists every task sorted by due time. Add a second task at the *same* time (e.g. feed another pet at 08:00) and a **conflict warning** banner appears.
5. **Complete a task** — under **Mark a task done**, select a task and click **Mark complete**. A success message confirms it, and because the task is `daily`, its next occurrence is generated automatically and shown in the schedule.

### Terminal demo (no browser)

Prefer the terminal? `python main.py` runs the same logic and prints a schedule. Paste a sample run here:

```
<!-- paste `python main.py` output here -->
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
