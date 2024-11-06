import streamlit as st
import json
import os

@st.cache_data
def load_chores():
    fam_id = st.session_state.get('family_id')
    filename = f'{fam_id}_data.json'
    
    # If the file doesn't exist, create w/ initial content
    if not os.path.exists(filename):
        save_chores( {"chores": []} )

    with open(filename, 'r') as file:
        return json.load(file)

def save_chores(chores):
    fam_id = st.session_state.get('family_id')
    filename = f'{fam_id}_data.json'
    with open(filename, 'w') as file:
        json.dump(chores, file, indent=4)

    # update session state
    st.session_state["chores"] = chores

@st.cache_data
def load_family_data():
    with open('families.json', 'r') as file:
        return json.load(file)

def login_page():
    # -------- st.session_state.page = "login"
    st.markdown("<h1 style='text-align: center;'>Choores</h1>", unsafe_allow_html=True)

    # Initialize session state if not present
    if 'family_id' not in st.session_state:
        st.session_state['family_id'] = ""
    if 'member_id' not in st.session_state:
        st.session_state['member_id'] = ""

    family_id = st.text_input("Family ID", placeholder="Enter Family ID", value=st.session_state['family_id'], key="family_id_input")
    member_id = st.text_input("Member ID", placeholder="Enter Your Name", value=st.session_state['member_id'], key="member_id_input")
  
    if st.button("Log In", key="log_in"):
        if "families" not in st.session_state:
            st.session_state["families"] = load_family_data()
        families_json = st.session_state["families"]

        try:
            family_id = int(family_id)
        except ValueError:
            st.error("Please enter a valid numeric Family ID.")
            return

        # Check if the family ID exists
        family_info = next((f for f in families_json["families"] if f["ID"] == family_id), None)
        if family_info is None:
            st.warning("The Family ID does not exist.")
            return

        # Check if the member ID exists in the family members
        if member_id.rstrip().lower() not in [member.rstrip().lower() for member in family_info["members"]]:
            st.warning("You are not a member of this family.")
            return

        # # Explicitly clear and reload session data for chores
        # if "chores" in st.session_state:
        #     st.session_state.pop("chores")
        
        # Confirm clear and reload fresh data from file
        st.session_state["chores"] = load_chores()

        # If both checks pass, update session state and log in
        st.session_state['family_id'] = family_id
        st.session_state['member_id'] = member_id
        st.session_state.page = "home" 
        st.rerun() # Refresh to show home page

    if st.button("Create Choores Family Account"):
        st.info("This feature is not available yet :)")

    if st.button("Add member to existing Choores Family"):
        st.info("This feature is not available yet :)")
