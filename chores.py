import streamlit as st
import pandas as pd
from datetime import datetime
from firebase_config import load_chores, save_chores, get_chores_from_cache
from home import design
from history import mark_as_done, calc_next

def all_chores_page():
    # -------- st.session_state.page = "all_chores"
    design()

    st.divider()
    st.markdown("<h4 style='text-align: center;'>All Chores</h4>", unsafe_allow_html=True)

    # Fetch chores from Firestore
    chores = get_chores_from_cache()

    if chores and chores["chores"]:
        for chore in chores:
            if st.button(chore['name']):
                st.session_state.selected_chore = chore['name']
                st.session_state.page = "chore_detail"
                st.rerun()

    else:  # if no chores
        st.markdown("<h5 style='text-align: center;'> <span style='color:#C3391C'> No chores found </span></h5>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>(Create a new chore in the sidebar)</p>", unsafe_allow_html=True)


def chore_detail_page():
    # -------- st.session_state.page = "chore_detail_page"
    design()
    st.divider()

    today = datetime.now().strftime("%b %d")
    member_name = st.session_state.get('member_id').lower().capitalize()
    selected_chore_name = st.session_state.get('selected_chore')

    # Fetch chores from Firestore
    chores = get_chores_from_cache()

    # Find the selected chore from the list
    selected_chore = next((chore for chore in chores if chore['name'] == selected_chore_name), None)
    st.markdown(f"<h4 style='text-align: center;'>{selected_chore['name']}</h4>", unsafe_allow_html=True)

    # Mark as done for logged-in member
    if st.button("MARK AS DONE"):
        mark_as_done(selected_chore['name'], member_name, today)
        st.rerun()

    if "success_message" in st.session_state:
        st.success(st.session_state["success_message"])
        del st.session_state["success_message"]

    # Calculate next member to do the chore
    if not selected_chore['next']:
        selected_chore['next'] = calc_next(selected_chore)
        save_chores({"chores": chores})  # Save updated chore data back to Firestore

    st.markdown(f"<h6>Next : <span style='color:#6293e3'>{selected_chore['next']}</span></h6>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)

    # Show history
    st.markdown(f"<h6>History: </h6>", unsafe_allow_html=True)
    if selected_chore['history']:
        df = pd.DataFrame(selected_chore['history'])
        st.write(df.style.hide(axis="index").hide(axis="columns").to_html(), unsafe_allow_html=True)
    else:
        st.write("No history available.")
    
    st.caption("Only the last cycle is shown")

