"""PawPal+ — pet care scheduling assistant.

Core implementation: Task and Pet hold data, Owner manages the pets, and
Scheduler is the "brain" that aggregates and organizes tasks across all pets.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta
from typing import List


@dataclass
class Task:
    """A single recurring care task for a pet."""

    description: str
    duration_minutes: int
    frequency: str  # e.g. "daily", "weekly", "once"
    due_time: str = "00:00"  # 24-hour "HH:MM"
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_completed = True


@dataclass
class Pet:
    """A pet and its associated care tasks."""

    pet_id: str
    name: str
    species: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)


class Owner:
    """Manages the collection of pets belonging to a single owner."""

    def __init__(self, name: str) -> None:
        """Create an owner with the given name and no pets yet."""
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flat list of every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The 'brain': aggregates tasks from an Owner and organizes them.

    The Scheduler holds a reference to an Owner (dependency injection) so it
    always reads live data rather than a stale copy.
    """

    def __init__(self, owner: Owner) -> None:
        """Bind the scheduler to the owner whose tasks it will organize."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Delegate to the owner to collect tasks from every pet."""
        return self.owner.get_all_tasks()

    def get_incomplete_tasks(self) -> List[Task]:
        """Return only the tasks that still need to be done."""
        return [task for task in self.get_all_tasks() if not task.is_completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return only the tasks already finished."""
        return [task for task in self.get_all_tasks() if task.is_completed]

    def organize_by_duration(self) -> List[Task]:
        """Order incomplete tasks shortest-first (quick wins first)."""
        return sorted(self.get_incomplete_tasks(), key=lambda t: t.duration_minutes)

    def total_remaining_minutes(self) -> int:
        """Sum the duration of all incomplete tasks."""
        return sum(task.duration_minutes for task in self.get_incomplete_tasks())

    # --- Sorting & filtering -------------------------------------------------

    def sort_by_time(self) -> List[Task]:
        """Return all tasks ordered by ``due_time`` (earliest first).

        Because ``due_time`` is a zero-padded 24-hour "HH:MM" string, plain
        string comparison already sorts chronologically ("08:30" < "14:05"),
        so the lambda key can hand the string straight to ``sorted``.
        """
        return sorted(self.get_all_tasks(), key=lambda t: t.due_time)

    def filter_by_completion(self, is_completed: bool) -> List[Task]:
        """Return tasks whose completion status matches ``is_completed``."""
        return [task for task in self.get_all_tasks() if task.is_completed == is_completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return the tasks belonging to the pet with ``pet_name`` (case-insensitive)."""
        target = pet_name.strip().lower()
        return [
            task
            for pet in self.owner.pets
            if pet.name.lower() == target
            for task in pet.tasks
        ]

    # --- Recurring tasks -----------------------------------------------------

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete ``task`` and, if it recurs, schedule its next occurrence.

        Returns the newly generated Task for a "daily"/"weekly" task, or
        ``None`` for a one-off task with nothing to reschedule.
        """
        task.mark_complete()

        frequency = task.frequency.strip().lower()
        deltas = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        if frequency not in deltas:
            return None

        # Anchor the "HH:MM" string to an arbitrary date so we can do real
        # date arithmetic, advance it, then read the time back out.
        next_dt = datetime.strptime(task.due_time, "%H:%M") + deltas[frequency]
        next_task = replace(
            task,
            due_time=next_dt.strftime("%H:%M"),
            is_completed=False,
        )

        # Attach the fresh occurrence to whichever pet owned the original.
        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.add_task(next_task)
                break
        return next_task

    # --- Conflict detection --------------------------------------------------

    def detect_conflicts(self) -> List[str]:
        """Return a warning per group of incomplete tasks sharing a ``due_time``.

        Never raises: an empty list means the schedule is clear.
        """
        by_time: dict[str, List[Task]] = {}
        for task in self.get_incomplete_tasks():
            by_time.setdefault(task.due_time, []).append(task)

        warnings: List[str] = []
        for due_time, tasks in sorted(by_time.items()):
            if len(tasks) > 1:
                descriptions = ", ".join(t.description for t in tasks)
                warnings.append(
                    f"[!] Conflict at {due_time}: {len(tasks)} tasks overlap ({descriptions})."
                )
        return warnings
