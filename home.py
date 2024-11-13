import streamlit as st
from firebase_config import load_chores, save_chores, get_chores_from_cache  # Import Firestore functions

def design():
    family_id = st.session_state.get('family_id')
    member_id = st.session_state.get('member_id')

    st.markdown("<h1 style='text-align: center;'>Choores</h1>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='display: flex; justify-content: space-between;'>
            <div><p><em>Hi {member_id.lower().capitalize()}</em></p></div>
            <div style='text-align: center;'><p> Family ID: {family_id} </p></div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Fetch chores from Firestore
    chores = get_chores_from_cache()

    # Sidebar buttons
    if st.sidebar.button("All Chores", key="all_chores"):
        st.session_state.page = "all_chores"
        st.rerun()

    # Create chore
    with st.sidebar.popover("Create Chore"):
        new_chore_name = st.text_input("Chore Name").lower().strip()
        if st.button("Add Chore"):
            if new_chore_name:
                if new_chore_name not in [chore['name'].lower() for chore in chores]:
                    new_chore = {"name": new_chore_name.capitalize(), "history": [], "next": ""}
                    chores.append(new_chore)
                    save_chores(chores)  # Save the updated chores
                    st.session_state["success_message"] = f"Added Chore: '{new_chore_name}'"
                    st.session_state.page = "all_chores"
                    st.rerun()
                else:
                    st.error("Chore already exists")
            else:
                st.warning("Please enter a Chore name")

    # Delete chore
    with st.sidebar.popover("Delete Chore"):
        to_remove = st.text_input("Which chore would you like to delete?").lower().strip()
        if st.button("DELETE", key="delete_button"):
            if to_remove in [chore['name'].lower() for chore in chores]:
                chores = [chore for chore in chores if chore['name'].lower() != to_remove]
                save_chores(chores)
                st.session_state["success_message"] = f"Chore '{to_remove.capitalize()}' has been deleted"
                st.session_state.page = "all_chores"
                st.rerun()
            else:
                st.error("Chore not found")

    # Show success message if any
    if "success_message" in st.session_state:
        st.success(st.session_state["success_message"])
        del st.session_state["success_message"]

    # Search
    search_query = st.sidebar.text_input("Search chores")
    filtered_chores = []
    if search_query:
        filtered_chores = [chore for chore in chores if search_query.lower() in chore["name"].lower()]
        if not filtered_chores:
            st.sidebar.warning("No such Chore")

    # Display filtered chores
    for chore in filtered_chores:
        if st.sidebar.button(chore["name"], key=f"chore_{chore['name']}"):
            st.session_state.selected_chore = chore['name']
            st.session_state.page = "chore_detail"
            st.rerun()

def home_page():
    # -------- st.session_state.page = "home"
    design()
