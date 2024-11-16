import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from firebase_config import get_chores_from_cache, save_chore
from home import design
from history import mark_as_done, calc_next

def all_chores_page():
    # -------- st.session_state.page = "all_chores"
    design()

    st.divider()
    st.markdown("<h4 style='text-align: center;'>All Chores</h4>", unsafe_allow_html=True)

    chores = get_chores_from_cache()
    
    if chores:
        col1, col2 = st.columns(2)

        # Depending on the index, decide which column the button will go into
        for idx, chore in enumerate(chores):
            if idx % 2 == 0:
                with col1:
                    if st.button(chore['name']):
                        st.session_state.selected_chore = chore['name']
                        st.session_state.page = "chore_detail"
                        st.rerun()
            else:
                with col2:
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

    toronto_tz = ZoneInfo("America/Toronto")
    today = datetime.now(toronto_tz).strftime("%b %d")
    # today = datetime.now().strftime("%b %d")
    member_name = st.session_state.get('member_id').lower().capitalize()
    selected_chore_name = st.session_state.get('selected_chore')


    chores = get_chores_from_cache()
    selected_chore = next((chore for chore in chores if chore['name'] == selected_chore_name), None)
    st.markdown(f"<h4 style='text-align: center;'>{selected_chore['name']}</h4>", unsafe_allow_html=True)

    # Mark as done for logged-in member
    if st.button("MARK AS DONE"):
        selected_chore = mark_as_done(selected_chore, member_name, today)
        st.rerun()

    if "success_message" in st.session_state:
        st.success(st.session_state["success_message"])
        del st.session_state["success_message"]

    # Calculate next member to do the chore
    if not selected_chore['next']:
        selected_chore['next'] = calc_next(selected_chore)
        save_chore(selected_chore) 

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
