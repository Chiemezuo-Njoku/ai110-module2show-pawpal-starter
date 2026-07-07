"""PawPal+ — pet care scheduling assistant.

Core implementation: Task and Pet hold data, Owner manages the pets, and
Scheduler is the "brain" that aggregates and organizes tasks across all pets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """A single recurring care task for a pet."""

    description: str
    duration_minutes: int
    frequency: str  # e.g. "daily", "weekly"
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_completed = True


@dataclass
class Pet:
    """A pet and its associated care tasks."""

    pet_id: str
    name: str
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
