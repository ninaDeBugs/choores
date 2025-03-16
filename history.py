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
    default_order = chore.get('members', [])
    
    # 0. New chores, next is first in default order
    if not history and not next:
        return default_order[0]
    
    # 1. Members in history, in order from latest participant
    history_order = []
    seen = set()
    for entry in reversed(history):
        if entry['member'] not in seen:
            history_order.append(entry['member'])
            seen.add(entry['member'])
    
    # 2. Count how many times each member has done the chore
    member_count = {member: 0 for member in default_order}
    for entry in history:
        member_count[entry['member']] += 1
    
    # 3. Find the members with lowest count
    min_count = min(member_count.values())
    least_participative_members = [member for member, count in member_count.items() if count == min_count]
    
    # 4. If everyone has done it the same number of times, return the person who did it longest time ago
    if len(least_participative_members) == len(default_order):
        chore['history'] = []
        return history_order[-1] 
    
    # 5. If everyone hasn't done it the same number of times
        # 5a. Return someone who hasn't done it at all
    for member in least_participative_members:
        if member not in history_order:
            least_participative_members.remove(member)
            return member

        #5b. Return the person who's done it but did it the longest time ago
    for member in reversed(history_order): 
        if member in least_participative_members:
            return member
