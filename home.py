import streamlit as st
import json

# Cache this function to avoid reloading data unnecessarily
@st.cache_data
def load_chores():
    with open('data.json', 'r') as file:
        return json.load(file)

@st.cache_data
def load_family_data():
    with open('families.json', 'r') as file:
        return json.load(file)

def save_chores(chores):
    # Avoid caching here since this function writes data
    with open('data.json', 'w') as file:
        json.dump(chores, file, indent=4)

def design():
    st.markdown("<h1 style='text-align: center;'>Choores</h1>", unsafe_allow_html=True)

    family_id = st.session_state.get('family_id')
    member_id = st.session_state.get('member_id')

    st.markdown(
        f"""
        <div style='display: flex; justify-content: space-between;'>
            <div><p><em>Hi {member_id.lower().capitalize()}</em></p></div>
            <div style='text-align: center;'><p> Family ID: {family_id} </p></div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # all chores
    if st.sidebar.button("All Chores", key="all_chores"):
        st.session_state.page = "all_chores"
        st.rerun()

    if "chores" not in st.session_state:
        st.session_state["chores"] = load_chores()
    chores = st.session_state["chores"].get('chores', [])

    # create chore
    with st.sidebar.popover("Create Chore"):
        new_chore_name = st.text_input("Chore Name").lower().strip()
        if st.button("Add Chore"):
            if new_chore_name:
                if new_chore_name not in [chore['name'].lower() for chore in chores]:
                    new_chore = {"name": new_chore_name.capitalize(), "history": [], "next": ""}
                    chores.append(new_chore)
                    save_chores({"chores": chores})  # Save the updated chores
                    st.session_state["chores"] = {"chores": chores}
                    st.success(f"Added chore: '{new_chore_name}'")
                    st.rerun()
                else:
                    st.warning("Chore already exists")
            else:
                st.warning("Please enter a chore name.")

    # delete chore
    with st.sidebar.popover("Delete Chore"):
        to_remove = st.text_input("Which chore would you like to delete?").lower().strip()
        if st.button("DELETE", key="delete_button"):
            if to_remove in [chore['name'].lower() for chore in chores]:
                chores = [chore for chore in chores if chore['name'].lower() != to_remove]
                save_chores({"chores": chores})
                st.session_state["chores"] = {"chores": chores}
                st.success(f"Chore '{to_remove.capitalize()}' has been deleted.")
                st.session_state.page = "all_chores"
                st.rerun()
            else:
                st.error("Chore not found")

    # Search input in the sidebar
    search_query = st.sidebar.text_input("Search chores")
    if "chores" not in st.session_state:
        st.session_state["chores"] = load_chores()
    chores = st.session_state["chores"].get('chores', [])
    filtered_chores = []

    # Filter chores based on search query
    if search_query:
        filtered_chores = [chore for chore in chores if search_query.lower() in chore["name"].lower()]
        if not filtered_chores:
            st.sidebar.warning("No such chore :/")

    # Display filtered chores
    for chore in filtered_chores:
        if st.sidebar.button(chore["name"], key=f"chore_{chore['name']}"):
            st.session_state.selected_chore = chore['name']
            st.session_state.page = "chore_detail"
            st.rerun()

def home_page():
    # -------- st.session_state.page = "home"
    design()

