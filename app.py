import streamlit as st
from login import login_page
from home import home_page
from chores import all_chores_page, chore_detail_page

def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "selected_chore" not in st.session_state:
        st.session_state.selected_chore = ""

    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "all_chores":
        all_chores_page()
    elif st.session_state.page == "chore_detail":
        chore_detail_page()
    

if __name__ == "__main__":
    main()


# SESSION STATE VARIABLES

# family_id
# member_id
# page
# selected_chore
