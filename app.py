from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app. Add your pets below and PawPal+ keeps track
of them for the rest of your session.
"""
)

# --- Persistent session state ------------------------------------------------
# Streamlit re-runs this whole script top-to-bottom on every interaction, so any
# plain local variable would be rebuilt from scratch each time. st.session_state
# is the "vault": a dict-like store that survives across re-runs. We keep our one
# Owner object in it, so every pet added earlier is still there on the next run.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner: Owner = st.session_state.owner

# --- Add-a-pet form ----------------------------------------------------------
st.subheader("Add a pet")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    submitted = st.form_submit_button("Add pet")

    if submitted:
        if pet_name.strip():
            pet_id = f"p{len(owner.pets) + 1}"
            owner.add_pet(Pet(pet_id=pet_id, name=pet_name.strip(), species=species))
            # Rerun so the tables below re-render from the freshly updated owner.
            # st.toast survives the rerun (a plain st.success would be wiped out).
            st.toast(f"Added {pet_name.strip()} ({species}).")
            st.rerun()
        else:
            st.warning("Please enter a pet name.")

# --- Display current pets ----------------------------------------------------
st.subheader("Your pets")

if owner.pets:
    st.table(
        [
            {"ID": pet.pet_id, "Name": pet.name, "Species": pet.species, "Tasks": len(pet.tasks)}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

# --- Add-a-task form ---------------------------------------------------------
# Tasks belong to a pet, so this form only appears once at least one pet exists.
st.subheader("Add a task")

if owner.pets:
    # Offer unambiguous string labels and map each back to the live Pet in
    # session state. Passing Pet objects straight to selectbox can hand back a
    # stale copy on submit, so the task would attach to the wrong pet.
    pet_by_label = {f"{pet.name} ({pet.pet_id})": pet for pet in owner.pets}
    with st.form("add_task_form", clear_on_submit=True):
        selected_label = st.selectbox("Pet", options=list(pet_by_label.keys()))
        description = st.text_input("Task", value="")
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.number_input("Minutes", min_value=1, max_value=240, value=20)
        with col2:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])
        with col3:
            due = st.time_input("Due time", value=time(8, 0))
        task_submitted = st.form_submit_button("Add task")

        if task_submitted:
            if description.strip():
                pet_by_label[selected_label].add_task(
                    Task(
                        description=description.strip(),
                        duration_minutes=int(duration),
                        frequency=frequency,
                        due_time=due.strftime("%H:%M"),
                    )
                )
                st.toast(f"Added '{description.strip()}' for {selected_label}.")
                st.rerun()
            else:
                st.warning("Please enter a task description.")
else:
    st.info("Add a pet first, then you can give it tasks.")

# --- Today's schedule --------------------------------------------------------
# The Scheduler reads live data from the owner, so it always reflects the tasks
# added above. We show everything ordered by due time and flag any conflicts.
st.subheader("Schedule")

scheduler = Scheduler(owner)
scheduled = scheduler.sort_by_time()

if scheduled:
    st.table(
        [
            {
                "Due": task.due_time,
                "Task": task.description,
                "Minutes": task.duration_minutes,
                "Frequency": task.frequency,
                "Done": "✅" if task.is_completed else "",
            }
            for task in scheduled
        ]
    )
    for warning in scheduler.detect_conflicts():
        st.warning(warning)
else:
    st.info("No tasks yet. Add one above.")
