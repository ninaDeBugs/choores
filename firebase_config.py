import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Set up firebase (using streamlit secrets)
firebase_credentials = {
    "type": st.secrets["firebase"]["type"],
    "project_id": st.secrets["firebase"]["project_id"],
    "private_key_id": st.secrets["firebase"]["private_key_id"],
    "private_key": st.secrets["firebase"]["private_key"],
    "client_email": st.secrets["firebase"]["client_email"],
    "client_id": st.secrets["firebase"]["client_id"],
    "auth_uri": st.secrets["firebase"]["auth_uri"],
    "token_uri": st.secrets["firebase"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
}

# Initialize Firebase app iff it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
db = firestore.client()


def load_family_data():
    try:
        families_ref = db.collection("families")
        families = [doc.to_dict() for doc in families_ref.stream()]
        return families
    except Exception as e:
        st.error(f"Error loading family data: {e}")
        print(f"Error loading family data: {e}")


# Function to load chores for a specific family
def load_chores():
    fam_id = st.session_state.get('family_id')
    chores_collection_name = f"{fam_id}_chores"
    chores_ref = db.collection(chores_collection_name)

    try:
        chores_docs = list(chores_ref.stream()) # Fetch all documents in the collection
        if not chores_docs:
            return [] 

        chores = [doc.to_dict() for doc in chores_docs] # as list of dicts
        return chores

    except Exception as e:
        st.error(f"Error loading chores: {e}")

# Cache load_chores() for 1min
@st.cache_data(ttl=60)  
def get_chores_from_cache():
    return load_chores()


# update or create chore in db
def save_chore(chore):
    try:
        fam_id = st.session_state.get('family_id')
        chores_collection_name = f"{fam_id}_chores"
        chore_name = chore['name']  # document ID = chore name
        chore_ref = db.collection(chores_collection_name).document(chore_name)
        chore_ref.set(chore) 
        
        st.cache_data.clear()  # Clear cache to ensure fresh data
    except Exception as e:
        st.error(f"Error saving chore: {e}")

# delete chore from db
def delete_chore(chore_name):
    fam_id = st.session_state.get('family_id')
    try:
        chores_collection_name = f"{fam_id}_chores"
        chore_ref = db.collection(chores_collection_name).document(chore_name)
        chore_ref.delete()
        st.cache_data.clear() # Clear cache to ensure fresh data
    except Exception as e:
        st.error(f"Error deleting chore: {e}")
