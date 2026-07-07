"""Unit tests for pawpal_system core classes."""

from pawpal_system import Owner, Pet, Scheduler, Task


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


def _build_scheduler():
    owner = Owner("Alex")
    rex = Pet("p1", "Rex")
    rex.add_task(Task("Morning walk", 30, "daily", due_time="08:00"))
    mia = Pet("p2", "Mia")
    mia.add_task(Task("Feed", 10, "daily", due_time="08:00"))
    mia.add_task(Task("Play", 20, "once", due_time="17:00", is_completed=True))
    owner.add_pet(rex)
    owner.add_pet(mia)
    return Scheduler(owner), rex, mia


def test_sort_by_time():
    scheduler, _, _ = _build_scheduler()
    times = [task.due_time for task in scheduler.sort_by_time()]
    assert times == ["08:00", "08:00", "17:00"]


def test_filter_by_completion():
    scheduler, _, _ = _build_scheduler()
    assert [t.description for t in scheduler.filter_by_completion(True)] == ["Play"]
    assert len(scheduler.filter_by_completion(False)) == 2


def test_filter_by_pet_is_case_insensitive():
    scheduler, _, _ = _build_scheduler()
    assert [t.description for t in scheduler.filter_by_pet("rex")] == ["Morning walk"]


def test_detect_conflicts_flags_overlap():
    scheduler, _, _ = _build_scheduler()
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_mark_complete_regenerates_daily_task():
    scheduler, rex, _ = _build_scheduler()
    walk = rex.tasks[0]

    next_task = scheduler.mark_task_complete(walk)

    assert walk.is_completed is True
    assert next_task is not None
    assert next_task.is_completed is False
    assert next_task.due_time == "08:00"
    assert len(rex.tasks) == 2  # original + regenerated


def test_mark_complete_once_task_does_not_recur():
    scheduler, _, mia = _build_scheduler()
    play = mia.tasks[1]  # "once", already complete

    assert scheduler.mark_task_complete(play) is None
    assert len(mia.tasks) == 2  # unchanged
