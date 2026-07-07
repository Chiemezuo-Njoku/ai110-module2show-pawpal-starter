"""PawPal+ demo — build an owner with pets and tasks, then print the schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # Set up the owner and their pets.
    owner = Owner("Alex")

    rex = Pet("p1", "Rex")
    rex.add_task(Task("Morning walk", 30, "daily", due_time="08:00"))
    rex.add_task(Task("Refill water", 5, "daily", due_time="12:00"))

    whiskers = Pet("p2", "Whiskers")
    whiskers.add_task(Task("Clean litter box", 15, "daily", due_time="08:00"))
    whiskers.add_task(Task("Vet checkup", 60, "weekly", due_time="16:00", is_completed=True))

    owner.add_pet(rex)
    owner.add_pet(whiskers)

    # The scheduler reads live data from the owner.
    scheduler = Scheduler(owner)

    # Print today's schedule: incomplete tasks, shortest first.
    print(f"Today's Schedule for {owner.name}")
    print("=" * 32)

    for task in scheduler.organize_by_duration():
        print(f"  [ ] {task.description:<20} {task.duration_minutes:>3} min  ({task.frequency})")

    print("-" * 32)
    print(f"  Total time remaining: {scheduler.total_remaining_minutes()} min")

    # --- Smarter scheduling features -----------------------------------------

    # 1. Sorting: order every task by its due time ("HH:MM").
    print("\nBy due time")
    print("=" * 32)
    for task in scheduler.sort_by_time():
        print(f"  {task.due_time}  {task.description}")

    # 2. Filtering: narrow tasks by pet name or completion status.
    print("\nRex's tasks")
    print("=" * 32)
    for task in scheduler.filter_by_pet("Rex"):
        print(f"  {task.description} ({task.due_time})")

    print("\nCompleted tasks")
    print("=" * 32)
    for task in scheduler.filter_by_completion(True):
        print(f"  {task.description}")

    # 3. Conflict detection: two tasks share the 08:00 slot.
    print("\nConflicts")
    print("=" * 32)
    for warning in scheduler.detect_conflicts() or ["  None"]:
        print(f"  {warning}")

    # 4. Recurring tasks: completing a daily task regenerates the next one.
    print("\nRecurring")
    print("=" * 32)
    walk = rex.tasks[0]
    next_task = scheduler.mark_task_complete(walk)
    print(f"  Completed '{walk.description}'; next occurrence due at {next_task.due_time}")
    print(f"  Rex now has {len(rex.tasks)} tasks")


if __name__ == "__main__":
    main()
