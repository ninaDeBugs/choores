import streamlit as st
import pandas as pd
import json
from datetime import datetime
from login import load_chores, save_chores
from home import design
from history import mark_as_done, calc_next

def all_chores_page():
    # -------- st.session_state.page = "all_chores"
    design()

    st.divider()
    st.markdown("<h4 style='text-align: center;'>All Chores</h4>", unsafe_allow_html=True)

    if "chores" not in st.session_state:
        st.session_state["chores"] = load_chores()
    chores = st.session_state["chores"].get('chores', [])
    
    if chores:
        for chore in chores:
            if st.button(chore['name']):
                st.session_state.selected_chore = chore['name']
                st.session_state.page = "chore_detail"
                st.rerun()

    else: # if no chores
        st.markdown("<h5 style='text-align: center;'> <span style='color:#C3391C'> No chores found </span></h5>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>(Create a new chore in the sidebar)</p>", unsafe_allow_html=True)


def chore_detail_page():
    # -------- st.session_state.page = "chore_detail_page"
    member_name = st.session_state.get('member_id').lower().capitalize()
    today = datetime.now().strftime("%b %d")

    design()
    st.divider()
    selected_chore_name = st.session_state.get('selected_chore')

    if "chores" not in st.session_state:
        st.session_state["chores"] = load_chores()
    chores = st.session_state["chores"].get('chores', [])
    selected_chore = next((chore for chore in chores if chore['name'] == selected_chore_name), None)
    st.markdown(f"<h4 style='text-align: center;'>{selected_chore['name']}</h4>", unsafe_allow_html=True)
    
    # mark as done for logged-in member
    if st.button("MARK AS DONE"):
        mark_as_done(selected_chore['name'], member_name, today)
        st.success(f"**'{selected_chore['name']}'** marked as done for **{member_name}** on **{today}**")

    # calculate next
    if not selected_chore['next']:
        selected_chore['next'] = calc_next(selected_chore)
        save_chores({"chores": chores})
        chores = st.session_state["chores"].get('chores', [])

    st.markdown(f"<h6>Next : <span style='color:#6293e3'>{selected_chore['next']}</span></h6>", unsafe_allow_html=True)
    st.markdown("</br>", unsafe_allow_html=True)

    # history
    st.markdown(f"<h6>History: </h6>", unsafe_allow_html=True)
    if selected_chore['history']:
        df = pd.DataFrame(selected_chore['history'])
        st.write(df.style.hide(axis="index").hide(axis="columns").to_html(), unsafe_allow_html=True)
    else:
        st.write("No history available.")
    st.caption("Only the last cycle is shown")
