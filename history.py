import streamlit as st
import json
from datetime import datetime
from home import load_chores, save_chores, load_family_data

def mark_as_done(chore_name, member_name, todays_date):
    if "chores" not in st.session_state:
        st.session_state["chores"] = load_chores()
    chores = st.session_state["chores"].get('chores', [])

    # calculate history & next
    for chore in chores:
        if chore['name'] == chore_name:
            previous_history = chore.get('history', [])
            previous_next = chore.get('next')
            chore['history'].append([member_name, todays_date]) 
            chore['next'] = calc_next(chore)

    # update
    save_chores({"chores": chores})
    st.session_state["chores"] = {"chores": chores}

@st.cache_data
def calc_next(chore):
    history = chore.get('history', [])

    # get default order    
    family_id = int(st.session_state.get('family_id'))
    if "families_json" not in st.session_state:
        st.session_state["families_json"] = load_family_data()
    families_json = st.session_state["families_json"]
    family_info = next((f for f in families_json["families"] if f["ID"] == family_id), None)
    dft_order = family_info['members']

    # update next accordingly
    if history:
        member_counters = {m: 0 for m in dft_order}
        for entry in history:
            member = entry[0]  # first element in each history entry is the member name
            if member in member_counters:
                member_counters[member] += 1

        # logic to reset the counter if everyone's caught up
        values_set = set(member_counters.values())
        if len(values_set) == 1:
            chore['history'] = []
            ans = dft_order[0]
        else: 
            # next is whoever has lowest num & to break ties, whoever is next in default order
            leastnum = min(member_counters.values())
            ans = next(m for m in dft_order if member_counters[m] == leastnum)
    else:
        ans = dft_order[0]

    return ans
