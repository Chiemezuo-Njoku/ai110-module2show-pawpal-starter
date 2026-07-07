"""Unit tests for pawpal_system core classes and Scheduler features."""

from pawpal_system import Owner, Pet, Scheduler, Task


# --- Helpers -----------------------------------------------------------------


def make_scheduler(*pets: Pet) -> Scheduler:
    """Wrap the given pets in an owner and return a Scheduler over them."""
    owner = Owner("Alex")
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner)


# --- Task basics (original coverage) -----------------------------------------


def test_task_completion():
    task = Task("Morning walk", 30, "daily")
    assert task.is_completed is False

    task.mark_complete()
    assert task.is_completed is True


def test_task_addition():
    pet = Pet("p1", "Rex")
    assert pet.tasks == []

    pet.add_task(Task("Refill water", 5, "daily"))
    assert len(pet.tasks) == 1


# --- Sorting -----------------------------------------------------------------


def test_scheduler_sorting_chronological():
    """Tasks added out of order come back earliest-first by due_time."""
    pet = Pet("p1", "Rex")
    pet.add_task(Task("Evening walk", 30, "daily", due_time="18:00"))
    pet.add_task(Task("Breakfast", 10, "daily", due_time="07:30"))
    pet.add_task(Task("Lunch", 10, "daily", due_time="12:00"))
    scheduler = make_scheduler(pet)

    ordered = [task.due_time for task in scheduler.sort_by_time()]

    # sort_by_time relies on "HH:MM" strings comparing in clock order. Pulling
    # out just the due_time strings makes the expected order obvious.
    assert ordered == ["07:30", "12:00", "18:00"]


def test_scheduler_sorting_crosses_noon_boundary():
    """Zero-padded 24-hour strings sort correctly across AM/PM.

    This is the assumption sort_by_time depends on: "09:00" < "14:30" as plain
    strings. It would break if a time were written un-padded (e.g. "9:00"),
    so this test pins the format contract.
    """
    pet = Pet("p1", "Rex")
    pet.add_task(Task("Afternoon", 15, "daily", due_time="14:30"))
    pet.add_task(Task("Morning", 15, "daily", due_time="09:00"))
    scheduler = make_scheduler(pet)

    ordered = [task.description for task in scheduler.sort_by_time()]

    assert ordered == ["Morning", "Afternoon"]


def test_scheduler_sorting_empty_is_safe():
    """No tasks means an empty list, not an error."""
    scheduler = make_scheduler(Pet("p1", "Rex"))
    assert scheduler.sort_by_time() == []


def test_scheduler_sorting_keeps_tied_times():
    """Two tasks at the same time both survive the sort (no dropped ties)."""
    pet = Pet("p1", "Rex")
    pet.add_task(Task("Walk", 30, "daily", due_time="08:00"))
    pet.add_task(Task("Feed", 10, "daily", due_time="08:00"))
    scheduler = make_scheduler(pet)

    ordered = scheduler.sort_by_time()

    assert len(ordered) == 2
    assert all(task.due_time == "08:00" for task in ordered)


# --- Recurrence --------------------------------------------------------------


def test_daily_task_recurs_next_day():
    """Completing a daily task marks it done and appends a fresh copy."""
    pet = Pet("p1", "Rex")
    walk = Task("Morning walk", 30, "daily", due_time="08:00")
    pet.add_task(walk)
    scheduler = make_scheduler(pet)

    next_task = scheduler.mark_task_complete(walk)

    # The original is now complete...
    assert walk.is_completed is True
    # ...and a brand-new occurrence was generated and attached to the pet.
    assert next_task is not None
    assert len(pet.tasks) == 2
    assert pet.tasks[1] is next_task


def test_daily_recurrence_is_a_distinct_fresh_task():
    """The regenerated task is a new, incomplete object, not the old reference.

    We only track "HH:MM" (no date), so a +1 day timedelta leaves the clock
    time unchanged -- that's expected. The meaningful assertions are that the
    new task is a *different* object, is not yet complete, and copies the
    description/duration/frequency of the original.
    """
    pet = Pet("p1", "Rex")
    walk = Task("Morning walk", 30, "daily", due_time="08:00")
    pet.add_task(walk)
    scheduler = make_scheduler(pet)

    next_task = scheduler.mark_task_complete(walk)

    assert next_task is not walk  # a fresh instance, not the same object
    assert next_task.is_completed is False
    assert next_task.description == "Morning walk"
    assert next_task.duration_minutes == 30
    assert next_task.frequency == "daily"
    assert next_task.due_time == "08:00"  # time-of-day unchanged (no date tracked)


def test_weekly_task_recurs():
    """Weekly frequency also regenerates (uses a 7-day timedelta)."""
    pet = Pet("p1", "Rex")
    bath = Task("Bath", 20, "weekly", due_time="10:00")
    pet.add_task(bath)
    scheduler = make_scheduler(pet)

    next_task = scheduler.mark_task_complete(bath)

    assert next_task is not None
    assert next_task.frequency == "weekly"
    assert len(pet.tasks) == 2


def test_once_task_does_not_recur():
    """A non-recurring task completes but spawns nothing."""
    pet = Pet("p1", "Rex")
    vet = Task("Vet visit", 60, "once", due_time="14:00")
    pet.add_task(vet)
    scheduler = make_scheduler(pet)

    result = scheduler.mark_task_complete(vet)

    assert result is None
    assert vet.is_completed is True
    assert len(pet.tasks) == 1  # no duplicate created


# --- Conflict detection ------------------------------------------------------


def test_conflict_detected_for_same_time():
    """Two tasks (across different pets) at the same time raise one warning."""
    rex = Pet("p1", "Rex")
    rex.add_task(Task("Walk", 30, "daily", due_time="08:00"))
    mia = Pet("p2", "Mia")
    mia.add_task(Task("Feed", 10, "daily", due_time="08:00"))
    scheduler = make_scheduler(rex, mia)

    warnings = scheduler.detect_conflicts()

    # One overlapping slot -> exactly one warning, and it names the time.
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflict_returns_empty_list():
    """Distinct times produce no warnings and never raise."""
    pet = Pet("p1", "Rex")
    pet.add_task(Task("Walk", 30, "daily", due_time="08:00"))
    pet.add_task(Task("Dinner", 10, "daily", due_time="18:00"))
    scheduler = make_scheduler(pet)

    assert scheduler.detect_conflicts() == []


def test_completed_tasks_do_not_conflict():
    """Only incomplete tasks can conflict -- a done task frees its slot."""
    pet = Pet("p1", "Rex")
    pet.add_task(Task("Walk", 30, "daily", due_time="08:00", is_completed=True))
    pet.add_task(Task("Feed", 10, "daily", due_time="08:00"))
    scheduler = make_scheduler(pet)

    # Only one *incomplete* task sits at 08:00, so there is no overlap.
    assert scheduler.detect_conflicts() == []


def test_three_tasks_one_slot_is_single_warning():
    """Three tasks sharing a slot yield one grouped warning, not one per pair."""
    pet = Pet("p1", "Rex")
    pet.add_task(Task("Walk", 30, "daily", due_time="08:00"))
    pet.add_task(Task("Feed", 10, "daily", due_time="08:00"))
    pet.add_task(Task("Meds", 5, "daily", due_time="08:00"))
    scheduler = make_scheduler(pet)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


# --- Filtering ---------------------------------------------------------------


def test_filter_by_completion():
    pet = Pet("p1", "Rex")
    pet.add_task(Task("Walk", 30, "daily", due_time="08:00"))
    pet.add_task(Task("Vet", 60, "once", due_time="14:00", is_completed=True))
    scheduler = make_scheduler(pet)

    assert [t.description for t in scheduler.filter_by_completion(True)] == ["Vet"]
    assert [t.description for t in scheduler.filter_by_completion(False)] == ["Walk"]


def test_filter_by_pet_is_case_insensitive():
    rex = Pet("p1", "Rex")
    rex.add_task(Task("Walk", 30, "daily", due_time="08:00"))
    mia = Pet("p2", "Mia")
    mia.add_task(Task("Feed", 10, "daily", due_time="08:00"))
    scheduler = make_scheduler(rex, mia)

    assert [t.description for t in scheduler.filter_by_pet("rex")] == ["Walk"]
    assert [t.description for t in scheduler.filter_by_pet("MIA")] == ["Feed"]
