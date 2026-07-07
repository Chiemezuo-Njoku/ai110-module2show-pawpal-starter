"""PawPal+ demo — build an owner with pets and tasks, then print the schedule."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # Set up the owner and their pets.
    owner = Owner("Alex")

    rex = Pet("p1", "Rex")
    rex.add_task(Task("Morning walk", 30, "daily"))
    rex.add_task(Task("Refill water", 5, "daily"))

    whiskers = Pet("p2", "Whiskers")
    whiskers.add_task(Task("Clean litter box", 15, "daily"))
    whiskers.add_task(Task("Vet checkup", 60, "weekly", is_completed=True))

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


if __name__ == "__main__":
    main()
