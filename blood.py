
import streamlit as st
import uuid
from collections import Counter

st.set_page_config(
    page_title="LifeLink - Blood Donation",
    page_icon="🩸",
    layout="wide"
)

# ---------------- DATA ----------------

DISTRICTS = [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural",
    "Bengaluru Urban", "Bidar", "Chamarajanagar",
    "Chikkaballapur", "Chikkamagaluru", "Chitradurga",
    "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag",
    "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar",
    "Koppal", "Mandya", "Mysuru", "Raichur", "Ramanagara",
    "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada",
    "Vijayapura", "Yadgir", "Vijayanagara"
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "AB-": ["A-", "B-", "AB-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"]
}

for key in ["donors", "requests", "rides", "notifications"]:
    if key not in st.session_state:
        st.session_state[key] = []

if "logged_donor" not in st.session_state:
    st.session_state.logged_donor = None

if "navigation" not in st.session_state:
    st.session_state.navigation = "Home"


# ---------------- NAVIGATION CALLBACK ----------------

def open_register():
    st.session_state.navigation = "Register Donor"


# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: #eef5fb;
    color: #142d50;
}

.block-container {
    max-width: 1350px;
    padding-top: 1rem;
}

h1, h2, h3, h4, p, label {
    color: #142d50;
}

.brand-header {
    background: linear-gradient(110deg,#142d50,#713044);
    padding: 22px 30px;
    border-radius: 15px;
    color: white;
    margin-bottom: 18px;
}

.brand-header h1 {
    color: white !important;
    font-size: 40px;
    margin: 0;
}

.brand-header p {
    color: #ffe4ed !important;
    font-size: 18px;
    margin: 8px 0 0;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: white !important;
    border: 1px solid #cbd9e8;
    border-radius: 9px;
    padding: 8px 12px;
}

div[data-testid="stRadio"] div[role="radiogroup"] label p,
div[data-testid="stRadio"] div[role="radiogroup"] label span {
    color: #142d50 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: #ffe5ed !important;
    border: 2px solid #bd3157 !important;
}

.stButton button {
    background: #a52f50 !important;
    color: white !important;
    border-radius: 9px;
    border: none;
    font-weight: bold;
    padding: 10px 18px;
}

.stButton button p {
    color: white !important;
}

.stButton button:hover {
    background: #78223d !important;
}

.hero-card {
    background: linear-gradient(120deg,#deedf8,#ffffff);
    border: 1px solid #cbddec;
    border-radius: 18px;
    padding: 35px;
    min-height: 375px;
}

.hero-card h1 {
    color: #ad2d50 !important;
    font-size: 43px;
}

.hero-card h3 {
    color: #193653 !important;
}

.hero-card p {
    color: #405b75 !important;
    font-size: 17px;
    line-height: 1.8;
}

.drop-card {
    height: 375px;
    background: linear-gradient(135deg,#e5f1fa,#ffffff);
    border: 1px solid #cbddec;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.feature-card {
    background: white;
    padding: 22px 14px;
    border-radius: 14px;
    text-align: center;
    min-height: 180px;
    border: 1px solid #d7e4ef;
}

.feature-card h3 {
    color: #193653 !important;
    font-size: 18px;
}

.feature-card p {
    color: #405b75 !important;
    font-size: 14px;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #d7e4ef;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- BLOOD DROP LOGO ----------------

DROP_SVG = """
<svg width="48" height="55" viewBox="0 0 100 110"
xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="pinkdrop" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#ff8ab9"/>
<stop offset="50%" stop-color="#ff2875"/>
<stop offset="100%" stop-color="#df004e"/>
</linearGradient>
</defs>
<path d="M50 4 C43 20 10 55 10 76 C10 99 27 108 50 108
C73 108 90 99 90 76 C90 55 57 20 50 4Z"
fill="url(#pinkdrop)"/>
</svg>
"""

st.markdown(f"""
<div class="brand-header">
    <div style="display:flex;align-items:center;gap:16px;">
        {DROP_SVG}
        <h1>LifeLink</h1>
    </div>
    <p>Blood Donation Management System</p>
</div>
""", unsafe_allow_html=True)


# ---------------- NAVIGATION ----------------

PAGES = [
    "Home", "Register Donor", "Donor Login", "Request Blood",
    "Find Donors", "Track Request", "Offer a Ride",
    "Available Rides", "Notifications", "Admin"
]

page = st.radio(
    "Main Navigation",
    PAGES,
    horizontal=True,
    key="navigation",
    label_visibility="collapsed"
)


# ---------------- HOME ----------------

if page == "Home":

    left, right = st.columns([1.05, 1])

    with left:
        st.markdown("""
        <div class="hero-card">
            <h1>LifeLink</h1>
            <br>
            <h3>Connecting Blood Donors, Saving Lives.</h3>
            <br>
            <p>
            Every drop matters. Every life counts.
            Join our blood donation community and help
            patients receive blood when they need it.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "🩸 Donate Blood - Make a Difference",
            on_click=open_register
        )

    with right:
        big_drop = DROP_SVG.replace(
            'width="48" height="55"',
            'width="220" height="260"'
        )

        st.markdown(f"""
        <div class="drop-card">
            {big_drop}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Our Services")

    columns = st.columns(4)

    features = [
        ("👥", "Connect with Donors",
         "Find blood donors and connect with people who can help."),
        ("🩸", "Support Patients",
         "Help patients find the blood groups they need."),
        ("🛡️", "Trusted & Secure",
         "Manage donor and blood request information."),
        ("⏱️", "Emergency Support",
         "Coordinate urgent blood requests and transport.")
    ]

    for col, feature in zip(columns, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <h1>{feature[0]}</h1>
                <h3>{feature[1]}</h3>
                <p>{feature[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## LifeLink Overview")

    a, b, c = st.columns(3)
    a.metric("Registered Donors", len(st.session_state.donors))
    b.metric("Blood Requests", len(st.session_state.requests))
    c.metric("Available Rides", len(st.session_state.rides))


# ---------------- REGISTER DONOR ----------------

elif page == "Register Donor":

    st.title("🩸 Donor Registration")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", 18, 100, 18)
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        phone = st.text_input("Mobile Number")
        email = st.text_input("Email")
        blood = st.selectbox("Blood Group", BLOOD_GROUPS)
        district = st.selectbox("District", DISTRICTS)
        address = st.text_area("Address")
        available = st.checkbox("I am available to donate blood")

        submit = st.form_submit_button("Register Donor")

        if submit:
            if not name.strip() or not phone.strip():
                st.error("Please enter your name and phone number.")
            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Enter a valid 10-digit phone number.")
            elif not available:
                st.warning("Please confirm your availability.")
            else:
                donor_id = "D" + uuid.uuid4().hex[:6].upper()

                st.session_state.donors.append({
                    "id": donor_id,
                    "name": name.strip(),
                    "age": age,
                    "gender": gender,
                    "phone": phone.strip(),
                    "email": email.strip(),
                    "blood": blood,
                    "district": district,
                    "address": address,
                    "available": True
                })

                st.session_state.notifications.append(
                    f"New donor registered: {name}"
                )

                st.success("Registration successful!")
                st.write("Your Donor ID:")
                st.code(donor_id)
                st.info("Save this ID for donor login.")


# ---------------- DONOR LOGIN ----------------

elif page == "Donor Login":

    st.title("🔐 Donor Login")

    donor_id = st.text_input("Enter Donor ID")

    if st.button("Login"):
        donor = next(
            (d for d in st.session_state.donors
             if d["id"].lower() == donor_id.strip().lower()),
            None
        )

        if donor:
            st.session_state.logged_donor = donor
            st.success("Login successful!")
        else:
            st.error("Donor ID not found.")

    if st.session_state.logged_donor:
        d = st.session_state.logged_donor
        st.subheader("Donor Profile")
        st.write("Name:", d["name"])
        st.write("Donor ID:", d["id"])
        st.write("Blood Group:", d["blood"])
        st.write("District:", d["district"])
        st.write("Phone:", d["phone"])

        if st.button("Logout"):
            st.session_state.logged_donor = None
            st.rerun()


# ---------------- REQUEST BLOOD ----------------

elif page == "Request Blood":

    st.title("🏥 Request Blood")

    with st.form("request_form"):
        patient = st.text_input("Patient Name")
        hospital = st.text_input("Hospital Name")
        district = st.selectbox("Hospital District", DISTRICTS)
        blood = st.selectbox("Required Blood Group", BLOOD_GROUPS)
        units = st.number_input("Number of Units", 1, 20, 1)
        contact = st.text_input("Contact Number")
        urgency = st.selectbox(
            "Urgency", ["Normal", "Urgent", "Emergency"]
        )

        submit = st.form_submit_button("Submit Blood Request")

        if submit:
            if not patient.strip() or not hospital.strip() or not contact.strip():
                st.error("Please fill in all required fields.")
            elif not contact.strip().isdigit() or len(contact.strip()) != 10:
                st.error("Enter a valid 10-digit contact number.")
            else:
                request_id = "R" + uuid.uuid4().hex[:6].upper()

                st.session_state.requests.append({
                    "id": request_id,
                    "patient": patient.strip(),
                    "hospital": hospital.strip(),
                    "district": district,
                    "blood": blood,
                    "units": units,
                    "contact": contact.strip(),
                    "urgency": urgency,
                    "status": "Contact Pending"
                })

                matches = [
                    d for d in st.session_state.donors
                    if d["blood"] in COMPATIBLE[blood]
                    and d["available"]
                ]

                st.session_state.notifications.append(
                    f"New blood request: {request_id}"
                )

                st.success("Blood request submitted!")
                st.write("Your Request ID:")
                st.code(request_id)
                st.write("Compatible registered donors:", len(matches))


# ---------------- FIND DONORS ----------------

elif page == "Find Donors":

    st.title("🔍 Find Blood Donors")

    blood = st.selectbox("Required Blood Group", BLOOD_GROUPS)
    district = st.selectbox(
        "District", ["All Karnataka"] + DISTRICTS
    )

    matches = [
        d for d in st.session_state.donors
        if d["blood"] in COMPATIBLE[blood] and d["available"]
    ]

    if district != "All Karnataka":
        matches = [d for d in matches if d["district"] == district]

    st.subheader(f"{len(matches)} compatible donor(s) found")

    if matches:
        for d in matches:
            with st.container(border=True):
                st.subheader(d["name"])
                st.write("Donor ID:", d["id"])
                st.write("Blood Group:", d["blood"])
                st.write("District:", d["district"])
                st.write("Phone:", d["phone"])
    else:
        st.warning("No matching registered donors found.")


# ---------------- TRACK REQUEST ----------------

elif page == "Track Request":

    st.title("📍 Track Blood Request")

    request_id = st.text_input("Enter Request ID")

    if st.button("Track Request"):
        request = next(
            (r for r in st.session_state.requests
             if r["id"].lower() == request_id.strip().lower()),
            None
        )

        if request:
            st.success("Request found!")
            st.write("Request ID:", request["id"])
            st.write("Patient:", request["patient"])
            st.write("Hospital:", request["hospital"])
            st.write("Blood Group:", request["blood"])
            st.write("District:", request["district"])
            st.write("Urgency:", request["urgency"])
            st.write("Status:", request["status"])

            stages = [
                "Contact Pending", "Donor Contacted",
                "Donor Accepted", "Donation Scheduled",
                "Donation Completed"
            ]

            if request["status"] in stages:
                st.progress(
                    (stages.index(request["status"]) + 1) / len(stages)
                )
        else:
            st.error("Request ID not found.")


# ---------------- OFFER A RIDE ----------------

elif page == "Offer a Ride":

    st.title("🚗 Offer a Ride")

    with st.form("ride_form"):
        driver = st.text_input("Driver Name")
        phone = st.text_input("Mobile Number")
        start = st.selectbox("Starting District", DISTRICTS)
        destination = st.selectbox("Destination District", DISTRICTS)
        vehicle = st.selectbox(
            "Vehicle Type", ["Car", "Bike", "Auto", "Other"]
        )

        submit = st.form_submit_button("Submit Ride Offer")

        if submit:
            if not driver.strip() or not phone.strip():
                st.error("Enter driver name and phone number.")
            elif not phone.strip().isdigit() or len(phone.strip()) != 10:
                st.error("Enter a valid 10-digit phone number.")
            else:
                ride_id = "T" + uuid.uuid4().hex[:6].upper()

                st.session_state.rides.append({
                    "id": ride_id,
                    "driver": driver.strip(),
                    "phone": phone.strip(),
                    "start": start,
                    "destination": destination,
                    "vehicle": vehicle
                })

                st.session_state.notifications.append(
                    f"New ride offer: {ride_id}"
                )

                st.success("Ride offer added!")
                st.code(ride_id)


# ---------------- AVAILABLE RIDES ----------------

elif page == "Available Rides":

    st.title("🚘 Available Rides")

    if st.session_state.rides:
        for ride in st.session_state.rides:
            with st.container(border=True):
                st.subheader("Ride " + ride["id"])
                st.write("Driver:", ride["driver"])
                st.write("Phone:", ride["phone"])
                st.write("From:", ride["start"])
                st.write("To:", ride["destination"])
                st.write("Vehicle:", ride["vehicle"])
    else:
        st.info("No rides available currently.")


# ---------------- NOTIFICATIONS ----------------

elif page == "Notifications":

    st.title("🔔 Notifications")

    if st.session_state.notifications:
        for i, message in enumerate(
            reversed(st.session_state.notifications), 1
        ):
            st.info(f"{i}. {message}")
    else:
        st.info("No notifications available.")


# ---------------- ADMIN ----------------

elif page == "Admin":

    st.title("⚙️ Admin Dashboard")

    password = st.text_input("Admin Password", type="password")

    if password == "admin123":

        st.success("Admin access granted!")

        a, b, c = st.columns(3)
        a.metric("Total Donors", len(st.session_state.donors))
        b.metric("Blood Requests", len(st.session_state.requests))
        c.metric("Ride Offers", len(st.session_state.rides))

        st.subheader("📊 Donors by Blood Group")

        blood_counts = Counter(
            d["blood"] for d in st.session_state.donors
        )

        st.bar_chart({
            "Donors": [
                blood_counts.get(group, 0)
                for group in BLOOD_GROUPS
            ]
        })

        st.subheader("📍 Donors by District")

        district_counts = Counter(
            d["district"] for d in st.session_state.donors
        )

        st.bar_chart(dict(district_counts))

        st.subheader("🩸 Blood Requests")

        for r in st.session_state.requests:
            with st.container(border=True):
                st.write("Request ID:", r["id"])
                st.write("Patient:", r["patient"])
                st.write("Blood Group:", r["blood"])
                st.write("Hospital:", r["hospital"])

                options = [
                    "Contact Pending",
                    "Donor Contacted",
                    "Donor Accepted",
                    "Donation Scheduled",
                    "Donation Completed",
                    "Cancelled"
                ]

                new_status = st.selectbox(
                    "Update Status",
                    options,
                    index=options.index(r["status"]),
                    key="status_" + r["id"]
                )

                if st.button("Save Status", key="save_" + r["id"]):
                    r["status"] = new_status
                    st.session_state.notifications.append(
                        f"Request {r['id']} updated: {new_status}"
                    )
                    st.success("Status updated!")
                    st.rerun()

        st.subheader("👥 Registered Donors")

        if st.session_state.donors:
            st.dataframe([
                {
                    "Donor ID": d["id"],
                    "Name": d["name"],
                    "Blood Group": d["blood"],
                    "District": d["district"],
                    "Phone": d["phone"]
                }
                for d in st.session_state.donors
            ], use_container_width=True)
        else:
            st.info("No donors registered.")

    elif password:
        st.error("Incorrect password.")


# ---------------- FOOTER ----------------

st.markdown("---")
st.markdown(
    "<center><b>🩸 LifeLink</b> | Connecting Blood Donors, Saving Lives</center>",
    unsafe_allow_html=True
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>

/* Main website */
.stApp {
    background-color: #eef5fb;
    color: #193653;
}

/* Headings and normal text */
h1, h2, h3, h4, p, label {
    color: #193653;
}

/* Success and information messages */
div[data-testid="stAlert"] {
    color: #ffffff !important;
}

div[data-testid="stAlert"] * {
    color: #ffffff !important;
}

/* Donor ID code box */
div[data-testid="stCode"] {
    background-color: #252525 !important;
    border-radius: 10px;
}

div[data-testid="stCode"] pre,
div[data-testid="stCode"] code {
    color: #ffffff !important;
}

/* Buttons */
.stButton button {
    background-color: #a52f50 !important;
    color: #ffffff !important;
    border-radius: 9px;
    font-weight: bold;
}

.stButton button p {
    color: #ffffff !important;
}

/* Input labels */
.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stTextArea label {
    color: #193653 !important;
    font-weight: 600 !important;
}

/* Navigation letters */
div[data-testid="stRadio"] label p {
    color: #193653 !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# FIX: DONOR ID INPUT TEXT VISIBILITY
st.markdown("""
<style>

/* White background for input boxes */
.stApp div[data-baseweb="input"] > div {
    background-color: #ffffff !important;
    border: 2px solid #9aafc5 !important;
}

/* Dark text while typing */
.stApp input,
.stApp textarea {
    color: #142d50 !important;
    -webkit-text-fill-color: #142d50 !important;
    caret-color: #e52d68 !important;
    background-color: #ffffff !important;
    opacity: 1 !important;
}

/* Donor ID placeholder */
.stApp input::placeholder {
    color: #718096 !important;
    -webkit-text-fill-color: #718096 !important;
    opacity: 1 !important;
}

/* Input labels */
.stApp div[data-testid="stTextInput"] label {
    color: #142d50 !important;
}

</style>
""", unsafe_allow_html=True)
