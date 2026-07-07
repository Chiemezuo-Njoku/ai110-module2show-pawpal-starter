import streamlit as st

from pawpal_system import Owner, Pet, Task

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
            st.success(f"Added {pet_name.strip()} ({species}).")
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
