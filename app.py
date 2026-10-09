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

if "presentation_offline_mode" not in st.session_state:
    st.session_state["presentation_offline_mode"] = False

# App Header
st.markdown("<h1 style='text-align: center; color: #000000;'>Project Ujjibon</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Decentralized Offline-First Immunization Tracking System</div>", unsafe_allow_html=True)

# --- PRESENTATION DEMO MODE TOGGLE BAR ---
col_mode1, col_mode2, col_mode3 = st.columns([1, 2, 1])
with col_mode2:
    mode_toggle = st.radio(
        "🎛️ Presentation Demo Mode (Simulate Field Network):",
        ["🌐 Online Mode", "📴 Simulate Offline Field Mode"],
        horizontal=True,
        index=1 if st.session_state["presentation_offline_mode"] else 0
    )
    if "Offline" in mode_toggle:
        st.session_state["presentation_offline_mode"] = True
    else:
        st.session_state["presentation_offline_mode"] = False

# Display Live Status Banner based on Demo Mode toggle
if not st.session_state["presentation_offline_mode"]:
    st.markdown("<div style='background-color: #e2f0cb; color: #2d5016; padding: 8px; border-radius: 4px; text-align: center; font-weight: 600; margin-bottom: 15px;'>🟢 Network Status: Connected (Online Mode)</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='background-color: #f8d7da; color: #721c24; padding: 8px; border-radius: 4px; text-align: center; font-weight: 600; margin-bottom: 15px;'>🔴 Status Update: Offline (Offline-First Field Mode Active)</div>", unsafe_allow_html=True)

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
            
            if st.session_state["presentation_offline_mode"]:
                st.session_state["local_field_queue"].append(record_data)
                st.warning(f"📴 **Info saved offline.** To be auto-synced when online. (Registered Caregiver: **{primary_name.strip()}** | File: `{filename}`)")
            else:
                st.success(f"🌐 Profile successfully registered and synced online! Caregiver: **{primary_name.strip()}**")
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
                st.info("Verified Caregiver Profile")
        with col_info:
            st.markdown(f"**Primary Caregiver:** {profile.get('primary_name')}")
            st.markdown(f"**Mobile Number:** {profile.get('primary_phone')}")
            st.markdown(f"**Address:** {profile.get('address')}")
            st.markdown(f"**Secondary Contact:** {profile.get('secondary_name', 'N/A')} ({profile.get('secondary_phone', 'N/A')})")
            
        st.markdown("---")
        st.subheader("💉 Vaccination Checklists by Child")
        
        children_list = profile.get('children_names', ['Child 1'])
        
        for idx, child in enumerate(children_list, 1):
            st.markdown(f"### 👶 Child {idx}: {child}")
            
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                st.checkbox(f"BCG (At Birth) - {child}", value=True, key=f"bcg_{idx}_{child}")
                st.checkbox(f"Pentavalent 1 (6 Wks) - {child}", value=True, key=f"penta1_{idx}_{child}")
                st.checkbox(f"Pentavalent 2 (10 Wks) - {child}", value=False, key=f"penta2_{idx}_{child}")
                st.checkbox(f"Pentavalent 3 (14 Wks) - {child}", value=False, key=f"penta3_{idx}_{child}")
                st.checkbox(f"PCV 1 (6 Wks) - {child}", value=True, key=f"pcv1_{idx}_{child}")
            with col_v2:
                st.checkbox(f"PCV 2 (10 Wks) - {child}", value=False, key=f"pcv2_{idx}_{child}")
                st.checkbox(f"PCV 3 (14 Wks) - {child}", value=False, key=f"pcv3_{idx}_{child}")
                st.checkbox(f"OPV & IPV Doses - {child}", value=False, key=f"opv_{idx}_{child}")
                st.checkbox(f"MR Dose 1 (9 Months) - {child}", value=False, key=f"mr1_{idx}_{child}")
                st.checkbox(f"MR Dose 2 (15 Months) - {child}", value=False, key=f"mr2_{idx}_{child}")
            
            st.markdown("---")
            
        if st.button("💾 Save All Vaccine Status Updates"):
            if st.session_state["presentation_offline_mode"]:
                st.warning("📴 Saved locally in offline-first mode! Updates queued for future network sync.")
            else:
                st.success("🌐 Vaccine records updated and synced online successfully!")
                
        st.write("")
        if st.button("🚪 Log Out / Back to Login"):
            st.session_state['logged_in'] = False
            st.session_state['current_user_profile'] = {}
            st.rerun()

    else:
        st.subheader("🔑 Child / Guardian Portal Login")
        st.markdown("Provide your verification photo and optional fallback lookup details.")
        
        st.markdown("---")
        st.subheader("📸 Biometric / Face Verification Photo (Mandatory)")
        login_photo_source = st.radio("Choose photo source:", ["Use Live Camera", "Upload from Gallery"], horizontal=True, key="photo_source_radio_login")
        
        login_image = None
        if login_photo_source == "Use Live Camera":
            login_image = st.camera_input("Take Verification Selfie")
        else:
            login_image = st.file_uploader("Select image file from gallery", type=["jpg", "jpeg", "png"], key="gallery_uploader_login")

        st.markdown("---")

        with st.form("login_form"):
            st.subheader("1️⃣ Lookup & Fallback Verification Details")
            login_primary_name = st.text_input("Primary Caregiver's Full Name (Optional):", placeholder="e.g., Ayesha Begum")
            login_primary_phone = st.text_input("Mobile Number (Optional):", "+880")
            
            st.markdown("---")
            login_submitted = st.form_submit_button("🔍 Verify and Open Profile")

        if login_submitted:
            if login_image is not None:
                ms_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = f"LOGIN_{ms_timestamp}.jpg"
                filepath = os.path.join(OFFLINE_PHOTO_DIR, filename)
                
                with open(filepath, "wb") as f:
                    f.write(login_image.getbuffer())
                
                matched_profile = None
                if login_primary_phone:
                    for p in st.session_state["registered_profiles"]:
                        if login_primary_phone.strip() in p.get("primary_phone", ""):
                            matched_profile = p
                            break
                
                if not matched_profile and len(st.session_state["registered_profiles"]) > 0:
                    matched_profile = st.session_state["registered_profiles"][-1]
                
                st.session_state['current_user_profile'] = {
                    "primary_name": matched_profile.get("primary_name", login_primary_name.strip() if login_primary_name else "Ayesha Begum"),
                    "primary_phone": matched_profile.get("primary_phone", login_primary_phone.strip() if login_primary_phone else "+8801700000000"),
                    "address": matched_profile.get("address", "Korail Slum, Dhaka"),
                    "secondary_name": matched_profile.get("secondary_name", "Rahim Uddin"),
                    "secondary_phone": matched_profile.get("secondary_phone", "+8801800000000"),
                    "children_names": matched_profile.get("children_names", ["Rahim Karim", "Fatima"]),
                    "filepath": matched_profile.get("filepath", filepath)
                }
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.warning("⚠️ Biometric verification photo is mandatory for login. Please capture or upload a photo.")

# --- SECTION: ADMIN LOGIN ---
elif st.session_state['active_section'] == 'admin_login':
    if st.session_state.get('admin_logged_in', False):
        st.subheader("🛡️ Health Worker / Admin Dashboard")
        st.markdown("Welcome back! Here is the overview of decentralized immunization nodes, local queues, and AI risk analysis.")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Total Registered Profiles", len(st.session_state["registered_profiles"]))
        with m_col2:
            st.metric("Pending Offline Queue", len(st.session_state["local_field_queue"]))
        with m_col3:
            st.metric("System Mode", "Offline-First Local")
            
        st.markdown("---")
        
        st.title("📊 Orjon: A Probabilistic AI")
        st.markdown("Calculates dropout risk using core factors: **Confirmed visits and High risk queues**.")
        st.markdown("---")

        st.subheader("📋 Generated High-Risk Children Queue")
        st.markdown("Workers physically visit children on this list first to minimize dropout rates, focusing exclusively on **Korail Slum**.")

        risk_data = {
            "Child_Name": ["Rahim Karim", "Mim Akter", "Puja Rani", "Arman Khan", "Rifat Hossain", "Sadia Islam"],
            "Slum_Zone": ["Korail Slum", "Korail Slum", "Korail Slum", "Korail Slum", "Korail Slum", "Korail Slum"],
            "Overdue_Days": [60, 45, 50, 30, 12, 5],
            "Missed_Sessions": [4, 3, 3, 2, 1, 0],
            "Distance_KM": [4.0, 3.5, 3.1, 2.9, 1.2, 0.8],
            "Contact_Failures": [3, 2, 2, 1, 0, 0],
            "Risk_Score": [169.0, 125.5, 125.5, 81.5, 30.8, 6.0],
            "Status": ["🚨 HIGH RISK", "🚨 HIGH RISK", "🚨 HIGH RISK", "🚨 HIGH RISK", "✅ Stable", "✅ Stable"]
        }

        df = pd.DataFrame(risk_data)
        st.dataframe(df, use_container_width=True)

        high_risk_count = (df["Status"] == "🚨 HIGH RISK").sum()
        st.markdown(f"**Total High-Risk Children Flagged for Field Intervention in Korail Slum:** `{high_risk_count}`")

        st.markdown("---")

        st.subheader("💉 Vial Opening Optimizer & eVLMIS Integration")
        st.markdown("Calculates total projected doses and required vials using your exact slide formulas.")

        v_col1, v_col2, v_col3 = st.columns(3)
        with v_col1:
            confirmed_visits = st.number_input("Confirmed Visits:", min_value=0, max_value=500, value=25)
        with v_col2:
            high_risk_queue_input = st.number_input("High-Risk Queue Count:", min_value=0, max_value=100, value=int(high_risk_count))
        with v_col3:
            wastage_factor = st.slider("Wastage Factor (Decimal):", min_value=0.0, max_value=0.5, value=0.10, step=0.05)

        vaccine_option = st.selectbox(
            "Select Vaccine Type & Doses per Vial:",
            ["Pentavalent (10 doses/vial)", "PCV - Pneumococcal (4 doses/vial)", "MR - Measles Rubella (10 doses/vial)", "BCG (20 doses/vial)"]
        )

        if "4 doses" in vaccine_option:
            doses_per_vial = 4
        elif "20 doses" in vaccine_option:
            doses_per_vial = 20
        else:
            doses_per_vial = 10

        total_projected_doses = (confirmed_visits + high_risk_queue_input) * (1 + wastage_factor)
        vials_to_open = math.ceil(total_projected_doses / doses_per_vial)

        res_c1, res_c2 = st.columns(2)
        with res_c1:
            st.metric("Total Projected Doses Required", f"{total_projected_doses:.2f}")
        with res_c2:
            st.metric("Vials to Open", f"{vials_to_open} Vial(s)")

        st.info("💡 **cVLMIS / eVLMS Integration Note:** This calculated usage data feeds directly into our national eVLMS central database, providing accurate tracking of total vaccines consumed.")

        st.markdown("---")
        st.subheader("📁 All Registered Caregivers & Children Database")
        
        for idx, prof in enumerate(st.session_state["registered_profiles"], 1):
            with st.expander(f"Profile {idx}: {prof.get('primary_name')} ({prof.get('primary_phone')})"):
                st.write(f"**Residential Address:** {prof.get('address')}")
                st.write(f"**Backup Contact:** {prof.get('secondary_name')} ({prof.get('secondary_phone')})")
                st.write(f"**Security Answers:** 1. {prof.get('sec_q1')} | 2. {prof.get('sec_q2')} | 3. {prof.get('sec_q3')}")
                
                st.markdown("##### 👶 Children Immunization Status:")
                children_list = prof.get('children_names', [])
                for c_idx, child_name in enumerate(children_list, 1):
                    if "rahim karim" in child_name.lower() or "rahim" in child_name.lower():
                        doses_taken_list = ["BCG (At Birth)", "Pentavalent 1 (6 Wks)", "PCV 1 (6 Wks)"]
                        doses_left_list = ["Pentavalent 2 (10 Wks)", "Pentavalent 3 (14 Wks)", "PCV 2 (10 Wks)", "PCV 3 (14 Wks)", "OPV & IPV Doses", "MR Dose 1 (9 Months)", "MR Dose 2 (15 Months)"]
                    else:
                        doses_taken_list = ["BCG (At Birth)"]
                        doses_left_list = ["Pentavalent 1, 2, 3", "PCV 1, 2, 3", "OPV & IPV Doses", "MR Dose 1 & 2"]

                    st.markdown(f"**{c_idx}. {child_name}**")
                    col_dt, col_dl = st.columns(2)
                    with col_dt:
                        st.markdown(f"✅ **Doses Taken ({len(doses_taken_list)}):**")
                        for d in doses_taken_list:
                            st.markdown(f"- {d}")
                    with col_dl:
                        st.markdown(f"⏳ **Doses Left to Take ({len(doses_left_list)}):**")
                        for d in doses_left_list:
                            st.markdown(f"- {d}")
                    st.markdown("---")
                
        st.write("")
        if st.button("🚪 Admin Log Out"):
            st.session_state['admin_logged_in'] = False
            st.rerun()
            
    else:
        st.subheader("🛡️ Health Worker / Admin Portal")
        st.markdown("Please enter your authorized credentials to access the admin dashboard.")
        
        with st.form("admin_login_form"):
            admin_username = st.text_input("Admin Username", placeholder="Enter username")
            admin_passcode = st.text_input("Secure Passcode", type="password", placeholder="Enter passcode")
            admin_submitted = st.form_submit_button("🔑 Login to Dashboard")
            
        if admin_submitted:
            if admin_username.strip() == "raik" and admin_passcode.strip() == "123456":
                st.session_state['admin_logged_in'] = True
                st.success("🎉 Admin authentication successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or passcode. Please try again (Hint: username is 'raik', passcode is '123456').")
