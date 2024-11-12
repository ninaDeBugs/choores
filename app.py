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
# family_id - stored to track the family context
# member_id - stored to track the member who is logged in
# page - tracks which page is being shown (login, home, all_chores, chore_detail)
# selected_chore - stores the name of the selected chore for details