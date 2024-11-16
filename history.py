import streamlit as st
from datetime import datetime
from firebase_config import save_chore, load_family_data

def mark_as_done(chore, member_name, todays_date):
    # Append history & next
    chore['history'].append({'member': member_name, 'date': todays_date})
    chore['next'] = calc_next(chore)
    save_chore(chore)

    st.session_state["success_message"] = f"**'{chore['name']}'** marked as done by **{member_name}** on **{todays_date}**"
    return chore


def calc_next(chore):
    history = chore.get('history', [])
    dft_order = chore.get('members')
    
    if not history: # then first member in default order is up next
        ans = dft_order[0]
    else:
        # Count how many times each member has done the chore
        member_counter = {m: 0 for m in dft_order}
        for entry in history:
            member = entry['member'] 
            member_counter[member] += 1

        member_counter_set = set(member_counter.values())
        if len(member_counter_set) == 1:
            # Reset the history if everyone's count is the same
            chore['history'] = []
            ans = dft_order[0]
        else:
            # Find the member with the lowest count; break ties using default order
            leastnum = min(member_counter.values())
            ans = next(m for m in dft_order if member_counter[m] == leastnum)

    return ans
