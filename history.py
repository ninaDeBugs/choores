import streamlit as st
from datetime import datetime
from firebase_config import load_chores, get_chores_from_cache, save_chore, load_family_data

def mark_as_done(chore, member_name, todays_date):
    # Ensure 'history' field is initialized as a list if it doesn't exist
    if 'history' not in chore or not isinstance(chore['history'], list):
        chore['history'] = []  # Initialize if not present or incorrect type

    # calculate history and next
    chore['history'].append([member_name, todays_date]) 
    chore['next'] = calc_next(chore)
    st.success(f"Updated chore data before saving: {chore}")
    save_chore(chore)

    st.session_state["success_message"] = f"**'{chore['name']}'** marked as done by **{member_name}** on **{todays_date}**"
    return chore

def calc_next(chore):
    # get default member order from Firestore
    family_id = int(st.session_state.get('family_id'))
    families_json = load_family_data()  # Fetch family data from Firestore
    family_info = next((f for f in families_json if f["ID"] == family_id), None)
    
    if not family_info:
        st.error("Family data not found.")
        print("Family data not found.")
        return None
    
    dft_order = family_info['members']  # Default member order

    # calculate the next member based on the chore history
    history = chore.get('history', [])
    if not history:
        ans = dft_order[0]
    else:
        # Count how many times each member has done the chore
        member_counter = {m: 0 for m in dft_order}
        for entry in history:
            member = entry[0]  # first element in each history entry is the member name
            member_counter[member] += 1

        member_counter_set = set(member_counter.values())

        if len(member_counter_set) == 1:
            # reset the counter if everyone's caught up
            chore['history'] = []
            ans = dft_order[0]
        else:
            # next is whoever has the lowest count & to break ties, whoever is next in default order
            leastnum = min(member_counter.values())
            ans = next(m for m in dft_order if member_counter[m] == leastnum)

    return ans
