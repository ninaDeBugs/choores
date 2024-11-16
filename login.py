import streamlit as st
from firebase_config import load_family_data

def login_page():
    st.markdown("<h1 style='text-align: center;'>Choores</h1>", unsafe_allow_html=True)

    # Initialize session state if not present
    if 'family_id' not in st.session_state:
        st.session_state['family_id'] = ""
    if 'member_id' not in st.session_state:
        st.session_state['member_id'] = ""

    family_id = st.text_input("Family ID", placeholder="Enter Family ID", value=st.session_state['family_id'], key="family_id_input")
    member_id = st.text_input("Member ID", placeholder="Enter Your Name", value=st.session_state['member_id'], key="member_id_input")
  
    if st.button("Log In", key="log_in"):
        families_json = load_family_data() 
        
        # Check if the family ID exists
        try:
            family_id = int(family_id)
        except ValueError:
            st.error("Please enter a valid numeric Family ID.")
            return

        family_info = next((f for f in families_json if f["ID"] == family_id), None)
        if family_info is None:
            st.error("The Family ID does not exist.")
            return

        # Check if the member ID exists in the family members
        if member_id.rstrip().lower() not in [member.rstrip().lower() for member in family_info["members"]]:
            st.warning("You are not a member of this family.")
            return

        # If both checks pass, update session state and log in
        st.session_state['family_id'] = family_id
        st.session_state['member_id'] = member_id.capitalize()
        st.session_state.page = "home" 
        st.rerun()  # Refresh to show home page

    if st.button("Create Choores Family Account"):
        st.info("This feature is not available yet :)")

    if st.button("Add member to existing Choores Family"):
        st.info("This feature is not available yet :)")
