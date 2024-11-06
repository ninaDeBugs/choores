import streamlit as st
import json
from datetime import datetime
from login import load_chores, save_chores, load_family_data

def mark_as_done(chore_name, member_name, todays_date):
    if "chores" not in st.session_state:
        st.session_state["chores"] = load_chores()
    chores = st.session_state["chores"].get('chores', [])

    # calculate history & next
    for chore in chores:
        if chore['name'] == chore_name:
            chore['history'].append([member_name, todays_date]) 
            chore['next'] = calc_next(chore)

    # update
    save_chores({"chores": chores})

@st.cache_data
def calc_next(chore):
    # get default member order    
    family_id = int(st.session_state.get('family_id'))
    if "families" not in st.session_state:
        st.session_state["families"] = load_family_data()
    families_json = st.session_state["families"]
    family_info = next((f for f in families_json["families"] if f["ID"] == family_id), None)
    dft_order = family_info['members']

    # update next accordingly
    history = chore.get('history', [])
    if not history:
        ans = dft_order[0]
    else:
        member_counter = {m: 0 for m in dft_order}
        for entry in history:
            member = entry[0]  # first element in each history entry is the member name
            if member in member_counter:
                member_counter[member] += 1

        member_counter_set = set(member_counter.values())

        if len(member_counter_set) == 1:
            # reset the counter if everyone's caught up
            chore['history'] = []
            ans = dft_order[0]
        else: 
            # next is whoever has lowest num & to break ties, whoever is next in default order
            leastnum = min(member_counter.values())
            ans = next(m for m in dft_order if member_counter[m] == leastnum)

    return ans
