import streamlit as st
import json
from home import load_family_data, load_chores

def login_page():
    # -------- st.session_state.page = "login"
    st.markdown("<h1 style='text-align: center;'>Choores</h1>", unsafe_allow_html=True)

    # Initialize session state if not present
    if 'family_id' not in st.session_state:
        st.session_state['family_id'] = ""
    if 'member_id' not in st.session_state:
        st.session_state['member_id'] = ""

    # Use unique keys for each text input
    family_id = st.text_input("Family ID", placeholder="Enter Family ID", value=st.session_state['family_id'], key="family_id_input")
    member_id = st.text_input("Member ID", placeholder="Enter Your Name", value=st.session_state['member_id'], key="member_id_input")
  
    if st.button("Log In", key="log_in"):
        # Load family data only once per session
        if "families_json" not in st.session_state:
            st.session_state["families_json"] = load_family_data()
        families_json = st.session_state["families_json"]

        # Convert family_id to integer if IDs in JSON are integers
        try:
            family_id_int = int(family_id)
        except ValueError:
            st.warning("Please enter a valid numeric Family ID.")
            return

        # Check if the family ID exists
        family_info = next((f for f in families_json["families"] if f["ID"] == family_id_int), None)

        if family_info is None:
            st.warning("The Family ID does not exist.")
            return

        # Check if the member ID exists in the family members
        if member_id.rstrip().lower() not in [member.rstrip().lower() for member in family_info["members"]]:
            st.warning("You are not a member of this family.")
            return

        # Explicitly clear and reload session data for chores
        if "chores" in st.session_state:
            st.session_state.pop("chores")  # Remove the existing data
        
        # Confirm clear and reload fresh data from file
        st.session_state["chores"] = load_chores()
        st.success("Session chores data reloaded successfully.")  # Add this to confirm reloading

        # If both checks pass, update session state and log in
        st.session_state['family_id'] = family_id
        st.session_state['member_id'] = member_id
        st.session_state.page = "home" # Refresh to show home page
        st.rerun()

    if st.button("Create Choores Family Account"):
        st.info("This feature is not available yet :)")

    if st.button("Add member to existing Choores Family"):
        st.info("This feature is not available yet :)")
