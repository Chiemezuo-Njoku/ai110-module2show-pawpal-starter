"""Unit tests for pawpal_system core classes."""

from pawpal_system import Pet, Task


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
