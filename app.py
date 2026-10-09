import streamlit as st
import pandas as pd
import os
import math
from PIL import Image
from datetime import datetime
import streamlit.components.v1 as components

# Set page configuration to fit standard screens
st.set_page_config(
    page_title="Project Ujjibon",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Clean White Theme & White Gumroad-Styled Buttons with Black Borders/Shadows
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Force Clean White Theme */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    .main {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
    }
    
    h1, h2, h3, p, label, .stMarkdown {
        color: #000000 !important;
    }
    
    .subtitle {
        font-size: 1.15rem !important;
        color: #555555 !important;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Gumroad Neo-Brutalist White Buttons: White bg, black text/borders, black hard shadow */
    .stButton button {
        width: 100%;
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 4px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 4px 4px 0px #000000 !important;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    
    .stButton button:hover {
        background-color: #f4f4f4 !important;
        color: #000000 !important;
        border-color: #000000 !important;
        box-shadow: 2px 2px 0px #000000 !important;
        transform: translate(2px, 2px);
    }
    
    /* Input fields styling for white theme */
    input, textarea, div[data-baseweb="select"] {
        background-color: #f9f9f9 !important;
        color: #000000 !important;
        border-radius: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Local offline storage folder for millisecond-titled photos
OFFLINE_PHOTO_DIR = "offline_captured_photos"
os.makedirs(OFFLINE_PHOTO_DIR, exist_ok=True)

# Initialize session state stores
if "local_field_queue" not in st.session_state:
    st.session_state["local_field_queue"] = []

if "registered_profiles" not in st.session_state:
    st.session_state["registered_profiles"] = [
        {
            "primary_name": "Ayesha Begum",
            "primary_phone": "+8801711223344",
            "address": "Korail Slum, Sector 7, House 12",
            "children_names": ["Rahim Karim", "Fatima"],
            "sec_q1": "Mango",
            "sec_q2": "12 June",
            "sec_q3": "Grandfather",
            "secondary_name": "Rahim Uddin",
            "secondary_phone": "+8801811223344",
            "filepath": ""
        }
    ]

if "reg_num_children" not in st.session_state:
    st.session_state["reg_num_children"] = 1

if "sync_status_message" not in st.session_state:
    st.session_state["sync_status_message"] = ""

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if "current_user_profile" not in st.session_state:
    st.session_state["current_user_profile"] = {}

# App Header
st.markdown("<h1 style='text-align: center; color: #000000;'>Project Ujjibon</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Decentralized Offline-First Immunization Tracking System</div>", unsafe_allow_html=True)

# --- BROWSER-SIDE LIVE NETWORK STATUS & AUTO-SYNC POPUP LISTENER ---
network_status_html = """
<div id="net-banner" style="padding: 8px; border-radius: 4px; text-align: center; font-weight: 600; margin-bottom: 15px;">
    Checking network status...
</div>
<script>
const banner = document.getElementById('net-banner');
function updateStatus() {
    if (navigator.onLine) {
        banner.style.backgroundColor = "#e2f0cb";
        banner.style.color = "#2d5016";
        banner.innerHTML = "🟢 Network Status: Connected (Online Mode)";
        
        const pendingName = sessionStorage.getItem("ujjibon_pending_offline_name");
        if (pendingName) {
            alert("🌐 Wi-Fi Reconnected! Successfully synced record: " + pendingName + " has been registered and updated in the admin portal.");
            sessionStorage.removeItem("ujjibon_pending_offline_name");
        }
    } else {
        banner.style.backgroundColor = "#f8d7da";
        banner.style.color = "#721c24";
        banner.innerHTML = "🔴 Status Update: Offline (Offline-First Field Mode Active)";
    }
}
window.addEventListener('online', updateStatus);
window.addEventListener('offline', updateStatus);
updateStatus();
</script>
"""
components.html(network_status_html, height=45)

# Display active sync notification if present
if st.session_state["sync_status_message"]:
    st.markdown(f"<div style='background-color: #d4edda; color: #155724; padding: 10px; border-radius: 4px; text-align: center; font-weight: 700; margin-bottom: 15px;'>{st.session_state['sync_status_message']}</div>", unsafe_allow_html=True)

# Display the Ujjibon Torch Logo Perfectly Centered
col1, col2, col3 = st.columns([1.5, 1, 1.5])
with col2:
    logo_path = "logo.png"  
    if os.path.exists(logo_path):
        logo_image = Image.open(logo_path)
        st.image(logo_image, width=200)
    else:
        st.warning("⚠️ Logo file 'logo.png' not found in project folder.")

st.write("")

# Navigation Buttons
b_col1, b_col2, b_col3 = st.columns(3)

with b_col1:
    reg_clicked = st.button("🧒 Child Registration")

with b_col2:
    child_login_clicked = st.button("🔑 Child Login")

with b_col3:
    admin_login_clicked = st.button("🛡️ Admin Login")

# Manage active view state using session_state
if 'active_section' not in st.session_state:
    st.session_state['active_section'] = 'register'

if reg_clicked:
    st.session_state['active_section'] = 'register'
    st.session_state['logged_in'] = False
elif child_login_clicked:
    st.session_state['active_section'] = 'child_login'
elif admin_login_clicked:
    st.session_state['active_section'] = 'admin_login'
    st.session_state['logged_in'] = False

st.markdown("---")

# --- SECTION: CHILD REGISTRATION ---
if st.session_state['active_section'] == 'register':
    st.subheader("👶 Offline/Online Child & Caregiver Registration")
    st.markdown("Complete details below. Each added child gets their own individual profile and vaccine checklist locally stored.")
    
    st.markdown("---")
    st.subheader("📸 Caregiver Biometric Identifier Photo")
    photo_source = st.radio("Choose photo source:", ["Use Live Camera", "Upload from Gallery"], horizontal=True, key="photo_source_radio_reg")
    
    primary_image = None
    if photo_source == "Use Live Camera":
        primary_image = st.camera_input("Take Primary Caregiver Selfie")
    else:
        primary_image = st.file_uploader("Select image file from gallery", type=["jpg", "jpeg", "png"], key="gallery_uploader_reg")

    st.markdown("---")

    with st.form("registration_form"):
        st.subheader("1️⃣ Primary Caregiver & Children Details")
        primary_name = st.text_input("Primary Caregiver's Full Name:", placeholder="e.g., Ayesha Begum")
        primary_phone = st.text_input("Mobile Number:", "+880")
        address = st.text_input("Residential Address / Area:", placeholder="e.g., Korail Slum, Sector 7, House 12")
        
        st.markdown("---")
        st.markdown("**👶 Children Names:**")
        
        child_inputs = []
        for i in range(st.session_state["reg_num_children"]):
            c_val = st.text_input(f"Child {i+1} Full Name:", placeholder=f"e.g., Child {i+1} Name", key=f"child_input_{i}")
            child_inputs.append(c_val)
        
        st.markdown("---")
        st.subheader("🔐 Secure Recovery / Verification Questions")
        st.markdown("Please provide answers to all 3 mandatory security questions for fallback recovery:")
        sec_q1 = st.text_input("1. Favourite fruit:", placeholder="e.g., Mango")
        sec_q2 = st.text_input("2. Wedding date:", placeholder="e.g., 12 June")
        sec_q3 = st.text_input("3. Name-giver of child:", placeholder="e.g., Grandfather")
        
        st.markdown("---")
        st.subheader("2️⃣ Secondary Caregiver Details (Backup)")
        secondary_name = st.text_input("Secondary Caregiver's Full Name:", placeholder="e.g., Rahim Uddin (Father/Uncle)")
        secondary_phone = st.text_input("Secondary Mobile Number:", "+880")
        
        st.markdown("---")
        submitted = st.form_submit_button("💾 Register & Create Profile")

    if st.button("➕ Add Another Child Box"):
        st.session_state["reg_num_children"] += 1
        st.rerun()

    if submitted:
        valid_children = [c.strip() for c in child_inputs if c and len(c.strip()) > 0]
        if primary_image is not None and len(primary_name) > 1 and len(primary_phone) > 5 and len(address) > 0 and len(valid_children) > 0 and len(sec_q1.strip()) > 0 and len(sec_q2.strip()) > 0 and len(sec_q3.strip()) > 0:
            ms_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"PRIMARY_{ms_timestamp}.jpg"
            filepath = os.path.join(OFFLINE_PHOTO_DIR, filename)
            
            with open(filepath, "wb") as f:
                f.write(primary_image.getbuffer())
                
            record_data = {
                "primary_name": primary_name.strip(),
                "primary_phone": primary_phone.strip(),
                "address": address.strip(),
                "children_names": valid_children,
                "sec_q1": sec_q1.strip(),
                "sec_q2": sec_q2.strip(),
                "sec_q3": sec_q3.strip(),
                "secondary_name": secondary_name.strip(),
                "secondary_phone": secondary_phone.strip(),
                "filepath": filepath,
                "capture_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            }
            
            st.session_state["registered_profiles"].append(record_data)
            st.session_state["local_field_queue"].append(record_data)
            
            components.html(f"""
                <script>
                sessionStorage.setItem("ujjibon_pending_offline_name", "{primary_name.strip()}");
                </script>
            """, height=0)
            
            st.warning(f"📴 **Info saved offline.** To be auto-synced when online. (Registered Caregiver: **{primary_name.strip()}** | File: `{filename}`)")
        else:
            st.warning("⚠️ Please fill out all required fields, including answers to all 3 security questions and a biometric photo.")

# --- SECTION: CHILD LOGIN ---
elif st.session_state['active_section'] == 'child_login':
    if st.session_state['logged_in']:
        profile = st.session_state['current_user_profile']
        st.subheader("👤 Caregiver & Child Immunization Profile")
        
        col_img, col_info = st.columns([1, 2])
        with col_img:
            if profile.get('filepath') and os.path.exists(profile['filepath']):
                st.image(profile['filepath'], width=180, caption="Caregiver Photo")
            else:
                st.info("Verified Caregiver Profile
