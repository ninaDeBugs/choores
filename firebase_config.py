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

# Initialize Firebase app (only if it hasn't been initialized yet)
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

# Function to load chores for a specific family (with collection creation if needed)
def load_chores():
    fam_id = st.session_state.get('family_id')
    chores_collection_name = f"{fam_id}_chores"
    chores_ref = db.collection(chores_collection_name)

    try:
        # Fetch all the documents in the collection
        chores_docs = list(chores_ref.stream())

        if not chores_docs:
            return []  # Return an empty list if no chores are found

        # Return the list of chores directly
        chores = [doc.to_dict() for doc in chores_docs]
        return chores

    except Exception as e:
        st.error(f"Error loading chores: {e}")
        # return []  # Return an empty list if an error occurs


@st.cache_data(ttl=60)  # Cache for 1min
def get_chores_from_cache():
    return load_chores()


# Function to save chores for a specific family
def save_chores(chores):
    fam_id = st.session_state.get('family_id')
    chores_collection_name = f"{fam_id}_chores"
    chores_ref = db.collection(chores_collection_name)

    try:
        for chore in chores:
            chore_name = chore["name"]
            chore_ref = chores_ref.document(chore_name)
            chore_ref.set(chore)

        st.cache_data.clear()  # Clear cache to ensure data freshness
    except Exception as e:
        st.error(f"Error saving chores: {e}")
        print(f"Error saving chores: {e}")

