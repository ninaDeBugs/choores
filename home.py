import streamlit as st
from firebase_config import get_chores_from_cache, save_chore, delete_chore, load_family_data 

def design():
    family_id = st.session_state.get('family_id')
    member_id = st.session_state.get('member_id')

    st.markdown("<h1 style='text-align: center;'>Choores</h1>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='display: flex; justify-content: space-between;'>
            <div><p><em>Hi {member_id}</em></p></div>
            <div style='text-align: center;'><p> Family ID: {family_id} </p></div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    chores = get_chores_from_cache()

    # All chores button
    if st.sidebar.button("All Chores", key="all_chores"):
        st.session_state.page = "all_chores"
        st.rerun()

    # # Create chore
    # with st.sidebar.expander("Create Chore"):
    #     new_chore_name = st.text_input("Chore Name").lower().strip()
    #     if st.button("Add Chore"):
    #         if new_chore_name:
    #             if new_chore_name not in [chore['name'].lower() for chore in chores]:
    #                 new_chore = {"name": new_chore_name.capitalize(), "history": [], "next": ""}
    #                 chores.append(new_chore) # update local chores variable
    #                 save_chore(new_chore)  # Save to db
    #                 st.session_state["success_message"] = f"Added Chore: **'{new_chore_name}'**"
    #                 st.session_state.page = "all_chores"
    #                 st.rerun()
    #             else:
    #                 st.error("Chore already exists")
    #         else:
    #             st.warning("Please enter a Chore name")

    # Create chore
    with st.sidebar.expander("Create Chore"):
        family_id = int(st.session_state.get('family_id'))
        families_json = load_family_data()
        family_info = next((f for f in families_json if f["ID"] == family_id), None)
        dft_members = family_info['members']  # Default member order

        new_chore_name = st.text_input("Chore Name").capitalize().strip()
        selected_members = st.multiselect("Add members doing this Chore", options=dft_members)
        
        if st.button("Add Chore"):
            if selected_members:
                if new_chore_name:
                    if new_chore_name.lower() not in [chore['name'].lower() for chore in chores]:
                        new_chore = {
                            "name": new_chore_name,
                            "members": selected_members,
                            "history": [],
                            "next": ""
                        }
                        chores.append(new_chore)  # Update local chores variable
                        save_chore(new_chore)  # Save to db
                        
                        st.session_state["success_message"] = f"Added Chore: **'{new_chore_name}'**"
                        st.session_state.page = "all_chores"
                        st.rerun()
                    else:
                        st.error("Chore already exists")
                else:
                    st.warning("Please enter a Chore name")
            else:
                st.error("No members selected for this chore.")

    # Delete chore
    with st.sidebar.expander("Delete Chore"):
        to_remove = st.text_input("Which chore would you like to delete?").capitalize().strip()
        matching_chore = next((chore for chore in chores if chore['name'].lower() == to_remove.lower()), None)
        
        if st.button("DELETE", key="delete_button"):
            if matching_chore:
                delete_chore(matching_chore['name'])

                chores = [chore for chore in chores if chore['name'].lower() != to_remove.lower()] # update local chores variable
                st.session_state["success_message"] = f"Chore **'{to_remove}'** has been deleted."
                st.session_state.page = "all_chores"
                st.rerun()
            else:
                st.error("Chore not found.")

    # Show success message if any
    if "success_message" in st.session_state:
        st.success(st.session_state.pop("success_message"))

    # Search
    search_query = st.sidebar.text_input("Search chores").strip()
    filtered_chores = []
    if search_query:
        filtered_chores = [chore for chore in chores if search_query.lower() in chore["name"].lower()]
        if not filtered_chores:
            st.sidebar.warning("No such Chore")

    for chore in filtered_chores:
        if st.sidebar.button(chore["name"], key=f"chore_{chore['name'].lower()}"):
            st.session_state.selected_chore = chore['name']
            st.session_state.page = "chore_detail"
            st.rerun()

def home_page():
    # -------- st.session_state.page = "home"
    design()