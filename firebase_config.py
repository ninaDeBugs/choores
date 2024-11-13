import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase config (using secrets)
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

# Function to load family data
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
        chores_docs = list(chores_ref.stream()) # Fetch all the documents in the collection
        if not chores_docs:
            return [] 

        chores = [doc.to_dict() for doc in chores_docs]
        return chores

    except Exception as e:
        st.error(f"Error loading chores: {e}")

@st.cache_data(ttl=60)  # Cache load_chores() for 1min
def get_chores_from_cache():
    return load_chores()

# update or create chore
def save_chore(chore):
    try:
        fam_id = st.session_state.get('family_id')
        chores_collection_name = f"{fam_id}_chores"
        chore_name = chore['name']  # Chore name is the document ID
        chore_ref = db.collection(chores_collection_name).document(chore_name)
        st.session_state.success_message = f"{chore} .... .... attempting to save to firestore"
        chore_ref.set(chore)  # Attempt to save the chore
        st.session_state.success_message = "saved chore"
        
        st.cache_data.clear()  # Clear cache to ensure fresh data next time
        st.session_state.success_message = "Chore saved successfully and cache cleared."
    except Exception as e:
        print(f"Error updating chore: {e}")
        st.error(f"Error saving chore: {e}")

if "success_message" in st.session_state:
        st.success(st.session_state["success_message"])
        del st.session_state["success_message"]

# delete chore
def delete_chore(chore_name):
    fam_id = st.session_state.get('family_id')
    try:
        chores_collection_name = f"{fam_id}_chores"
        chore_ref = db.collection(chores_collection_name).document(chore_name)
        chore_ref.delete()
        st.cache_data.clear()
    except Exception as e:
        print(f"Error deleting chore: {e}")
