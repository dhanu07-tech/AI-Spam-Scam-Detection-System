import re
import streamlit as st
import sqlite3
import os
import joblib
import base64
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from reportlab.platypus import SimpleDocTemplate,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from streamlit_option_menu import option_menu


# page configuration
st.set_page_config(
    page_title="AI Spam And Scam Detection System",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@media (max-width: 768px) {

    .main .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    div.stButton > button {
        width: 100%;
    }

    h1 {
        font-size: 28px !important;
    }

    p {
        font-size: 16px;
    }
}

</style>
""", unsafe_allow_html=True)

      

st.markdown("""
<style>

.stTextArea textarea {
    color: black !important;
    background-color: white !important;
    -webkit-text-fill-color: black !important;
}

.stTextInput input {
    color: black !important;
    background-color: white !important;
    -webkit-text-fill-color: black !important;
}

</style>
""", unsafe_allow_html=True)
        

# load model only once
@st.cache_resource
def load_resource():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_resource()
    


def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_bg(bg):
    st.markdown(
        f"""
        <style>
        .stApp{{
            background:
            linear-gradient(rgba(5,10,25,.75), rgba(5,10,25,.75)),
            url("data:image/jpg;base64,{bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


bg = get_base64("images1/fraud.jpg")
logo = get_base64("images2/logo1.png")

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    email TEXT,
    password TEXT
)
""")


# create users table
conn.commit()

#cursor.execute("SELECT * FROM users")
#users = cursor.fetchall()
#st.write("Database Users:",users)


def signup(username,email,password):
    try:
        cursor.execute(
            "INSERT INTO users (username,email,password) VALUES (?,?,?)",
            (username,email,password)
        )
        conn.commit()
        return True
    except:
        return False

def login(username,password):
    cursor.execute(
        "SELECT*FROM users WHERE username=? AND password=?",
        (username,password)
    )
    return cursor.fetchone()



st.markdown(f"""
<style>

.stApp{{
background:
linear-gradient(rgba(5,10,25,.75),rgba(5,10,25,.75)),
url("data:image/jpg;base64,{bg}");
background-size:cover;
background-position:center;
background-attachment:fixed;
}}

[data-testid="stSidebar"]{{
    background:linear-gradient(180deg,#071739,#0A4EA6);
}}

[data-testid="stSidebar"] *{{
    color:white !important;
}}

.left-box{{
padding-top:60px;
color:white;
}}

.left-box h1{{
font-size:52px;
font-weight:bold;
color:white;
}}

.left-box h2{{
font-size:36px;
color:#2EC5FF;
}}

.left-box p{{
font-size:18px;
color:#EAEAEA;
}}

.login-box{{
background:rgba(15,23,42,.92);
width:450;
min-height:500;
padding:35;
border-radius:20px;
backdrop-filter:blur(10px);
border:1px solid rgba(46,197,255,.3);
box-shadow:0 8px 30px rgba(0,0,0,.35);
}}


.login-box h2{{
color:white;
text-align:center;
}}

.login-box p{{
color:#DDEEFF;
text-align:center;
}}

.stTextInput input{{
background:white;
color:black;
border-radius:10px;
}}

.stButton>button{{
width:100%;
height:48px;
background:#1976D2;
color:white; !important;
border:none;
border-radius:10px;
font-weight:bold;
box-shadow:0 4px 12px rgba(0,0,0,.3);
}}

.stButton>button:hover{{
background:#1565C0;
}}

[data-testid="stMetric"]{{
background:#0F172A;
border:1px solid #29B6F6;
border-radius:12px;
padding:15px;
}}

[data-testid="stFileUploader"]{{
background:#0F172A;
border:1px solid #29B6F6;
border-radius:12px;
padding:10px;
}}

html, body, [class*="css"] {{
    color:white
}}


h1,h2,h3,h4,h5,h6 {{
    color:white !important;
}}


p,label,span,div {{
    color:white !important;
}}


[data-testid="stMarkdownContainer"] {{
    color:white !important;
}}


.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stRadio label,
.stCheckbox label {{
    color:white !important;
}}


[data-testid="stMetricValue"],
[data-testid="stMetricLabel"] {{
    color:white !important;
}}


[data-testid="stAlert"] {{
    color:white !important;
}}

</style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style="
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    padding:8px;
    background:rgba(0,0,0,.45);
    text-align:center;
    color:#C0C0C0;
    font-size:13px;
    backdrop-filter:blur(5px);
    ">
    © 2026 AI Spam & Scam Detection System | All Rights Reserved
    </div>
    """, unsafe_allow_html=True)

# check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
# show login page if user is not logged in
if not st.session_state.logged_in:

    left, right = st.columns([1,1.5])
    
    # left side - project information
    with left:
        

        st.markdown("""
        <h1 style="color:white;font-size:58px;font-weight:bold;">
        🛡 AI Spam & Scam Detection System
        </h1>

        <h2 style="color:#00D4FF;font-size:32px;">
        Stay Safe. Detect Scams Instantly.
        </h2>

        <p style="color:white;font-size:20px;line-height:1.8;">
        AI-powered protection against phishing, spam, fake links, and online scams.
        Sign in to start secure and real-time threat analysis.
        </p>
        """, unsafe_allow_html=True)
        
       
    # right side - login form
    with right:
        

        st.markdown("""
            <div class="login-box">
            <h2>🔐 Welcome</h2>
            <p>Login to Continue</p>
            </div>
            """, unsafe_allow_html=True)

            

        choice = st.radio(
            "Select",
           ["Login","Sign Up"],
            horizontal=True
        )


        if choice == "Login":

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("🚀Login"):

                if login(username, password):

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

                else:

                    st.error("❌ Invalid Username or Password")

        elif choice == "Sign Up":

            new_user = st.text_input("New Username")
            new_email = st.text_input("Email")
            new_pass = st.text_input("New Password", type="password")

            if st.button("Create Account"):

                if signup(new_user , new_email, new_pass):

                    st.success("Account Created Successfully")

                else:

                    st.error("Username already exists")
            
    st.stop()

# sidebar navigation    
with st.sidebar:

    st.success(f"👤 {st.session_state.username}")

    st.image("images2/logo2.png", width=70)

    st.markdown("## AI Spam & Scam")
    st.caption("Smart • Secure • Reliable")
    
    # initialize default selected page
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = 0
        
    # navigation menu 
    page = option_menu(
        menu_title="Navigation",
        options=[
            "🏠 Home",
            "🔍 Smart Scanner",
            "📊 Analysis Result",
            "📜 Prediction History",
            "📄 Report Download",
            "ℹ️ About"
        ],
        icons=[
            "house",
            "envelope",
            "bar-chart",
            "clock-history",
            "file-earmark-pdf",
            "info-circle"
        ],
        manual_select=st.session_state.selected_page,
        default_index=0
    )

    st.markdown("---")

    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    # sidebar branding
    st.image(
        "images2/logo1.png",
        width=230
    )

    st.markdown(
        "<h3 style='text-align:center;color:#29B6F6;'>AI Spam & Scam Detection</h3>",
        unsafe_allow_html=True
    )
    
    # sidebar system status
    st.success("🟢 System Status")
    st.caption("All Systems Operational")

    st.markdown("---")

    
    # logout button
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
   

# initialize prediction history 
if "history"not in st.session_state:
    st.session_state.history = []


# home page
if page == "🏠 Home":
    
    
    st.markdown("""
    <style>

        .main{
        background:rgba(10,25,50,0.75);
        padding:30px;
        border-radius:20px;
        border:1px solid rgba(41,182,246,.35);
        box-shadow:0 8px 25px rgba(0,180,255,.20);
    }
       

    .big{
        font-size:52px;
        font-weight:800;
        color:white;
        line-height:1.15;
        margin-bottom:15px;
    }

    .blue{
        color:#25C5FF;
    }

    .sub{
        font-size:24px;
        color:#EAF6FF;
        font-weight:600;
        margin-bottom:12px;
    }

    .desc{
        color:#F5F5F5;
        font-size:20px;
        line-height:1.7;
        margin-bottom:25px;
    }

    .scan-btn{
    background:linear-gradient(90deg,#00d4ff,#4f6cff);
    padding:15px;
    text-align:center;
    border-radius:12px;
    font-size:22px;
    font-weight:bold;
    color:white;
    margin-top:25px;
    }

    </style>    
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .nav-guide {
        background: rgba(0, 0, 0, 0.75);
        color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #444;
        margin-bottom: 20px;
    }
    .nav-guide h3 {
        color: white;
    }
    .nav-guide ul {
        color: white;
        margin-bottom: 0;
    }
    </style>

    <div class="nav-guide">
    <h3>📌 Navigation Guide</h3>

    <p>👈 open the <b>☰ Menu</b> to access:</p>

    <ul>
    <li>🔍 Smart Scanner</li>
    <li>📊 Analysis Result</li>
    <li>📜 Prediction History</li>
    <li>📄 Report Download</li>
    <li>ℹ️ About</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

        
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    #  home page  welcome banner
    st.markdown("""
    <div class="big">
    Welcome to<br>
    AI Spam & Scam<br>
    <span class="blue">Detection System</span>
    </div>
    """, unsafe_allow_html=True)
    
    # home page subtitle
    st.markdown("""
    <div class="sub">
    Smart • Secure • Reliable
    </div>
    """, unsafe_allow_html=True)
    
    # home page description
    st.markdown("""
    <div class="desc">
    Detect spam, phishing, scams and malicious
    content with the power of Artificial Intelligence.
    </div>
    """, unsafe_allow_html=True)

    
    # start scanning button
    if st.button("🔍 Start Scanning Now →", use_container_width=True):
        st.info("👉 Open the Smart Scanner page from the left navigation.")

    st.markdown("</div>", unsafe_allow_html=True)

    

    c1, c2, c3, c4 = st.columns(4)

    # statistics data
    total_scans = 1243
    safe_messages = 983
    scam_detected = 271
    total_reports = 1275

    # dashboard metric cards
    def card(title, value, icon,idx):

        
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#0d1b3a,#102a56);
            border:1px solid #00c8ff;
            border-radius:15px;
            padding:18px;
            text-align:center;
            box-shadow:0 0 12px rgba(0,200,255,.35);
        ">
            <div style="font-size:32px;">{icon}</div>
            <div style="color:#00d4ff;font-size:18px;font-weight:bold;">
                {title}
            </div>
            <div style="color:white;font-size:34px;font-weight:bold;">
                {value}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # interactive trend chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            y=[3,4,5,4,6,7,6,8],
            mode="lines",
            fill="tozeroy"
        ))

        fig.update_layout(
            height=110,
            margin=dict(l=0,r=0,t=0,b=0),
            xaxis=dict(showgrid=False,visible=False),
            yaxis=dict(showgrid=False,visible=False),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key=f"chart_{idx}"
        )


    with c1:
        card("Total Scans", total_scans, "📊",1)

    with c2:
        card("Safe Messages", safe_messages, "✅",2)

    with c3:
        card("Scam Detected", scam_detected, "⚠️",3)

    with c4:
        card("Total Reports", total_reports, "📄",4)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # feature showcase section
    st.markdown("""
    <h2 style='text-align:center;color:#00d4ff;'>
    🚀 Powerful Features
    </h2>
    <p style='text-align:center;color:white;'>
    Advanced AI Security Features for Complete Protection
    </p>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    
    # AI security status panel
    with f1:
        st.markdown("""
        <div style="
        background:#0d1b3a;
        border:1px solid #00c8ff;
        border-radius:15px;
        padding:20px;
        text-align:center;
        height:240px;
        box-shadow:0px 0px 15px rgba(0,200,255,.4);">

        <h1>🛡️</h1>

        <h3 style="color:#00d4ff;">
        AI Spam Detection
        </h3>

        <p style="color:white;">
        Detect spam emails, phishing messages,
        and malicious content instantly using AI.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div style="
        background:#0d1b3a;
        border:1px solid #00c8ff;
        border-radius:15px;
        padding:20px;
        text-align:center;
        height:240px;
        box-shadow:0px 0px 15px rgba(0,200,255,.4);">

        <h1>⚡</h1>

        <h3 style="color:#00d4ff;">
        Real-Time Analysis
        </h3>

        <p style="color:white;">
        Analyze Emails, URLs,
        QR Codes and UPI IDs
        in real time.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div style="
        background:#0d1b3a;
        border:1px solid #00c8ff;
        border-radius:15px;
        padding:20px;
        text-align:center;
        height:240px;
        box-shadow:0px 0px 15px rgba(0,200,255,.4);">

        <h1>📄</h1>

        <h3 style="color:#00d4ff;">
        Smart Reports
        </h3>

        <p style="color:white;">
        Download detailed PDF reports
        with prediction history
        and security recommendations.
        </p>

        </div>
        """, unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
    background:linear-gradient(90deg,#0d1b3a,#102b55);
    padding:20px;
    border-radius:15px;
    border:1px solid #00d4ff;
    box-shadow:0px 0px 15px rgba(0,200,255,.4);
    ">

    <h2 style="color:#00d4ff;">
    🛡 AI Security Status
    </h2>

    <p style="color:white;font-size:18px;">
    ✔ AI Engine : Active <br>
    ✔ Spam Detection : Online <br>
    ✔ URL Scanner : Running <br>
    ✔ QR Scanner : Ready <br>
    ✔ UPI Scanner : Ready <br>
    ✔ Report Generator : Active
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;
    color:#A9C8FF;
    font-size:15px;
    padding-bottom:15px;">

    © 2026 AI Spam & Scam Detection System | All Rights Reserved

    </div>
    """, unsafe_allow_html=True)
    

    # security images gallery
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("images1/02_secure.jpg")

    with col2:
        st.image("images1/04_secure.jpg")

    with col3:
        st.image("images1/05_privacy.jpg")

    with col4:
        st.image("images1/fraud.jpg")

    st.divider()
    
    # protection status metrics 
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric("📧 Email", "Protected")

    with col2:
        st.metric("🎣 Phishing", "Active")

    with col3:
        st.metric("🌐 URL Check", "Enabled")

    with col4:
        st.metric("📄 Reports", "Ready")

    st.divider()
     
    # security modules overview
    st.subheader("🛡 Security Modules")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.info("📧 Spam Detection")

    with c2:
        st.info("🎣 Phishing Detection")

    with c3:
        st.info("🌐 URL Reputation")

    with c4:
        st.info("📷 QR Scam Detection")

    c5,c6,c7,c8 = st.columns(4)

    with c5:
        st.info("💳 Fake UPI")

    with c6:
        st.info("📱 WhatsApp")

    with c7:
        st.info("📞 Phone Risk")

    with c8:
        st.info("📩 SMS Detection")

    st.divider()
    
    # project overview dashboard 
    st.subheader("📊 Project Overview")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("🤖 AI Model", "Naive Bayes")

    with col2:
        st.metric("🛡 Modules", "8")

    with col3:
        st.metric("📜 History", "Enabled")

    st.divider()
    
    # online and offline protection summary
    left,right = st.columns(2)

    with left:

        st.success("""
    ### 🌐 Online Protection

    ✔ Email

    ✔ WhatsApp

    ✔ SMS

    ✔ Website Links

    ✔ QR Codes

    ✔ UPI
    """)

    with right:

        st.success("""
    ### 🏢 Offline Protection

    ✔ Printed QR

    ✔ Payment QR

    ✔ Phone Number

    ✔ Printed Notices
    """)

    st.divider()
    
    # cyber security tips
    st.warning("""
    ### 🔒 Security Tips

    • Never share OTP.

    • Verify unknown links.

    • Check sender identity.

    • Avoid fake UPI requests.

    • Scan suspicious QR codes.
    """)

    st.divider()

    # navigate to smart scanner 
    if st.button("🚀 Start Scanning"):

         st.session_state.selected_page=1
         st.rerun()


# smart scanner page         
elif page == "🔍 Smart Scanner":


    emails = [
        # spam
        "win a free lottery now",
        "claim your cash prize",
        "congratulations you won reward",
        "click here to claim your gift",
        "limited time offer",
        "urgent update your bank account",
        "verify your account immediately",
        "you have won iphone",
        "earn money from home",
        "exclusive bonus available",
        "your account has been suspended",
        "confirm your otp now",
        "claim your refund today",
        "upi payment failed click here",
        "work from home and earn daily",

        # Not Spam
        "meeting tomorrow at 10 AM",
        "please send the project report",
        "happy birthday",
        "lets have lunch",
        "project submission completed",
        "how are you",
        "see you tomorrow",
        "call me when free",
        "thank you for your help",
        "family dinner tonight",
        "team meeting has been rescheduled",
        "invoice attached for your reference",
        "class starts at 9 AM tomorrow",
        "please review the document",
        "your order has been delivered"
    ]

    labels = [
        # Spam
        "spam","spam","spam","spam","spam",
        "spam","spam","spam","spam","spam",
        "spam","spam","spam","spam","spam",

        # Not Spam
        "not spam","not spam","not spam","not spam","not spam",
        "not spam","not spam","not spam","not spam","not spam",
        "not spam","not spam","not spam","not spam","not spam"
    ]
    
    # check database size
    print("emails:",len(emails))
    print("labels:",len(labels))
    
    # print all emails with their serial numbers
    for i,mail in enumerate(emails,1):
        print(i,mail)
        
    
    # spam detection model
    joblib.dump(model, "model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    
    # spam keywords database 
    spam_words = [
        "free", "win", "winner", "lottery", "offer", "prize",
        "urgent", "gift", "limited", "cash prize", "reward",
        "click", "click here", "bonus", "claim",
        "verify", "verification", "confirm",
        "bank", "account", "otp", "password", "login",
        "loan", "credit card", "debit card",
        "upi", "payment", "refund", "transaction",
        "bitcoin", "crypto", "investment", "earn money",
        "work from home", "job offer",
        "iphone", "airpods", "amazon gift card",
        "congratulations", "selected", "exclusive",
        "act now", "limited time", "update",
        "suspended", "security alert", "kyc",
        "ipl match win money", "currency"
    ]
    
    # File uploader CSS
    st.markdown("""
    <style>
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span{
        color: black !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
     
    # upload email or message
    uploaded_file = st.file_uploader(
        "📂  upload email or message",
        type=["txt","eml","csv"]
    )

    
    # email input section
    if uploaded_file is not None:
        email = uploaded_file.read().decode("utf-8",errors="ignore")
        st.success("✅file uploaded successfully")

        st.subheader("📄  file information")

        st.write(f"**file name:**{uploaded_file.name}")
        st.write(f"**file type:**{uploaded_file.type}")
        st.write(f"**file size:**{uploaded_file.size}bytes")
        
        st.text_area("file content",email,height=200)

    else:
        email = st.text_area("📧 enter email text")

        
    # start email analysis
    if st.button("🔍check email"):


        if email.strip() == "":
           st.warning("enter enter an email.")
           st.stop()

        else:

            text = email.lower()

            found = []

            score = 0

            for word in spam_words:

                if word in text:

                    found.append(word)

                    score += 1
   
            # spam score analysis
            st.write("### spam score")
            st.progress(min(score/10,1.0))
            st.write(f"{score}/10")
     
            st.write("###risk level")

            if score >= 5:
                st.error("⚠️high risk")
            elif score >= 3:
                st.warning("⚠medium risk")
            else:
                st.success("⌛low risk")

            st.write("### spam keywords found")

            if found:
                for w in found:
                    st.write("✅",w)
            else:
                st.write("no spam keywords found.")

            st.write("### REASON")
            
            # machine learning prediction
            test = vectorizer.transform([email])

            prediction = model.predict(test)[0]

            probability = model.predict_proba(test)[0]

            confidence = max(probability)

            spam_index = list(model.classes_).index("spam")
            spam_probability = probability[spam_index]

            if prediction == "spam":
                st.error("🚨 ML Prediction : SPAM")
            else:
                st.success("✅ ML Prediction : NOT SPAM")

            st.write(f"Confidence : {confidence*100:.2f}%")

            st.progress(float(spam_probability))

            st.write(f"Spam Probability : {spam_probability*100:.2f}%")
            
            # suspicious link detection
            st.subheader("🔗  Suspicious Link Detection")

            suspicious = False
            reasons = []

            urls = re.findall(r'https?://\S+|www\.\S+',email)


            if urls:
                st.write("links found:")
                for url in urls:
                    st.write("•",url)

                    if url.startswith("http://"):
                        suspicious = True
                        reasons.append("uses HTTP instead of HTTPS")

                    if "bit.ly" in url or "tinyurl.com" in url or "t.co" in url:
                        suspicious = True
                        reasons.append("shortened URL detected")

                    if ".xyz" in url or ".top" in url or ".click" in url:
                        suspicious = True
                        reasons.append("suspicious domain detected")

            else:
                st.write("no links found.")

            if suspicious:
                st.error(" suspicious link detected")
                for reason in reasons:
                    st.write("•",reason)
            else:
                st.success(" ✅ no suspicious links found")


            final_prediction = prediction

            if score >= 3:
                final_prediction = "spam"

            if suspicious:
                final_prediction = "spam"

            st.header("📋 Final Decision")

            if final_prediction == "spam":
                st.error("🚨 FINAL RESULT : SPAM")
            else:
                st.success("✅ FINAL RESULT : NOT SPAM")


            st.session_state.email = email
            st.session_state.urls = urls
            st.session_state.found = found


            st.success("Email Checked Successfully ✅")
            
                        
            # url reputation check
            st.header(" 🌐 Url Reputation Check")

            bad_domains = [
                ".xyz",
                ".top",
                ".click",
                ".zip",
                ".work",
                ".gq",
                ".tk",
                ".cf",
                ".ml",
                ".ga",
                ".buzz",
                ".monster",
                ".live",
                ".cam"
            ]

            shorteners = [
                "bit.ly",
                "tinyurl.com",
                "t.co",
                "is.gd",
                "cutt.ly",
                "goo.gl",
                "rb.gy",
                "rebrand.ly",
                "ow.ly",
                "shorturl.at",
                "buff.ly"
            ]

            
            url_score = 0
            url_reasons = []

            if urls:

                for url in urls:

                    if url.startswith("http://"):
                        url_score += 2
                        url_reasons.append("uses http instead of https")

                    if any(short in url for short in shorteners):
                        url_score += 2
                        url_reasons.append("shortened url")

                    if any(domain in url for domain in bad_domains):
                        url_score += 2
                        url_reasons.append("suspicious domain extension")

                    if re.search(r"https?://\d+\.\d+\.\d+\.\d+",url):
                        url_score += 3
                        url_reasons.append("uses ip address instead of domain")

                    if len(url) > 80:
                        url_score += 1
                        url_reasons.append("very long url")

                    st.write("### url reputation score")
                    st.progress(min(url_score /10,1.0))
                    st.write(f"{url_score}/10")

                    if url_score >= 5:
                        st.error("🚨 bad url reputation")
                    elif url_score >= 3:
                        st.warning("⚠️ suspicious url")
                    else:
                        st.success("✅good url reputation")

                    if url_reasons:
                        st.write("### reasons")
                        for reason in set(url_reasons):
                            st.write("•",reason)
                    else:
                        st.info("no url found to check.")
                        
            
            # message scam detection check
            st.header("📂 Message Based Scam Detector")

            message_keywords = [
                "urgent", "act now", "claim here", "click here",
                "work from home", "winner", "gift", "lottery",
                "reward", "limited offer", "claim reward",
                "verify", "verification", "update",
                "account", "bank", "otp", "payment",
                "job offer", "investment", "refund",
                "upi", "transaction", "password",
                "login", "security alert", "kyc",
                "confirm", "cash prize", "free"
            ]

           
            message_found = []

            for word in message_keywords:
                if word in text:
                   message_found.append(word)

            message_score = len(message_found)

            st.write("### message scam score")
            st.progress(min(message_score/10,1.0))
            st.write(f"{message_score}/10")

            if message_score >= 4:
                st.error("⚠️ high message scam risk")
            elif message_score >= 2:
                st.warning("🛡medium message scam risk")
            else:
                st.success("✅low message scam risk")

            if message_found:
                st.write("### message scam indicators")
                for word in message_found:
                    st.write("🎯 ",word)

            else:
                st.write("no message scam indicators detected.")


            if("scan" in text and "receive money" in text) or \
              ("scan message" in text and "reward" in text) or \
              ("scan message" in text and "cashback" in text):
                 st.error(" ⚠️ possible message scam")

                                        
            # whatsapp scam detection
            st.header("⚧️ Whatsapp Scam Detection")

            whatsapp_keywords = [
                "otp",
                "upi",
                "qr code",
                "scan",
                "payment",
                "pay",
                "send money",
                "reward",
                "gift",
                "lottery",
                "winner",
                "job offer",
                "work from home",
                "investment",
                "crypto",
                "bitcoin",
                "urgent",
                "click here",
                "new number",
                "hi dad",
                "hi mom",
                "loan",
                "limited offer",
                "receive money",
                "collect request",
                "claim reward",
                "cashback",
                "bank",
                "cash prize",
                "hii customer"
            ]
                    
                   
            whatsapp_found = []

            for word in whatsapp_keywords:
                if word in text:
                   whatsapp_found.append(word)

            whatsapp_score = len(whatsapp_found)

            st.write("### whatsapp scam sore")
            st.progress(min(whatsapp_score /10,1.0))
            st.write(f"{whatsapp_score}/10")

            if whatsapp_score >= 4:
                      st.error("⚠️ high whatsapp scam risk")
            elif whatsapp_score >= 2:
                        st.warning("❇️ medium whatsapp scam risk")
            else:
                        st.success("✅ low whatsapp scam risk")

            if whatsapp_found:
                st.write("### detected whatsapp scam keywords")
                for word in whatsapp_found:
                    st.write("🎯",word)

            else:
                st.write("no whatsapp scam keywords detected.")

            

            # phishing detection check
            st.header("🎣 Phishing Detection")

            phishing_keywords = [
                "verify",
                "verification",
                "account",
                "bank",
                "password",
                "login",
                "otp",
                "kyc",
                "credit card",
                "debit card",
                "upi",
                "payment",
                "refund",
                "transaction",
                "security",
                "update",
                "wallet"
                "security alert",
                "update",
                "wallet",
                "confirm",
                "authenticate",
                "identity",
                "click here",
                "reset password",
                "unlock account",
                "expired",
                "suspended",
                "blocked",
                "urgent",
                "immediately",
                "limited time"
            ]
        
        
                    
            phishing_found = []

            for word in phishing_keywords:
                if word in text:
                   phishing_found.append(word)

            phishing_score = len(phishing_found)

            st.write("### Phishing Score")
            st.progress(min(phishing_score / 10, 1.0))
            st.write(f"{phishing_score}/10")

            if phishing_score >= 4:
                st.error("🎣 High Phishing Risk")
            elif phishing_score >= 2:
                st.warning("⚠️ Medium Phishing Risk")
            else:
                st.success("✅ Low Phishing Risk")

            if phishing_found:
                st.write("### Phishing Keywords")
                for word in phishing_found:
                    st.write("🔴", word)
            else:
                st.write("No phishing keywords found.")

                
            # qr scam detection check
            st.header("📷 QR Code Scam Detection")

            qr_keywords = [
                "qr",
                "qr code",
                "scan qr",
                "scan code",
                "scan now",
                "scan this code",
                "scan to pay",
                "scan to receive",
                "scan to claim",
                "scan and pay",

                "payment request",
                "collect request",
                "upi collect",
                "upi",
                "upi id",

                "receive money",
                "send money",
                "payment pending",
                "payment failed",

                "cashback",
                "reward",
                "gift",
                "lottery",
                "claim prize",
                "claim reward",
                "refund",

                "verify payment",
                "confirm payment",
                "bank",
                "wallet"
            ]

            
            qr_found = []

            for word in qr_keywords:
                if word in text:
                   qr_found.append(word)

            keyword_count = len(qr_found)

            if keyword_count >= 3:
                qr_score = 3
            elif keyword_count == 2:
                qr_score = 2
            elif keyword_count == 1:
                qr_score = 1
            else:
                qr_score = 0

                
            st.write("### QR Scam Score")
            st.progress(qr_score / 3)
            st.write(f"{qr_score}/3")

            if qr_score >= 3:
                st.error("🚨 High QR Scam Risk")
            elif qr_score >= 2:
                st.warning("⚠️ Medium QR Scam Risk")
            elif qr_score == 1:
                st.info("🟡 Low QR Scam Risk")
            else:
                st.success("✅ No QR Scam Risk")

            if qr_found:
                st.write("### QR Scam Indicators")
                for word in qr_found:
                    st.write("📌", word)
            else:
                st.write("No QR scam indicators detected.")

                
            if (
               ("scan" in text and "receive money" in text) or
               ("scan qr" in text and "reward" in text) or
               ("scan qr" in text and "cashback" in text) or
               ("scan code" in text and "payment" in text) or
               ("scan to receive" in text)
           ):
               st.error("⚠️ Possible QR Payment Scam Detected")


            # fake upi payment check
            st.header("💳 Fake UPI Payment Request Detection")

            upi_keywords = [
                "upi",
                "upi id",
                "paytm",
                "phonepe",
                "google pay",
                "gpay",
                "bhim",
                "fampay",
                "amazon pay",

                "scan and pay",
                "scan qr",
                "qr code",
                "collect request",
                "payment request",
                "approve payment",
                "receive money",
                "send money",

                "payment pending",
                "payment failed",
                "refund",
                "cashback",
                "reward",
                "bank transfer",
                "wallet",
                "merchant",
                "verify payment",
                "confirm payment",
                "claim reward"
            ]

           
            
                   
            upi_found = []

            for word in upi_keywords:
                if word in text:
                   upi_found.append(word)

            upi_score = len(upi_found)

            st.write("### upi scam score")
            st.progress(min(upi_score/10,1.0))
            st.write(f"{upi_score}/10")

            if upi_score >= 4:
                 st.error(" ⚠️ high fake upi payment risk")
            elif upi_score >= 2:
                 st.warning("💡 medium fake upi payment risk")
            else:
                 st.success("✅low fake upi payment risk")

            if upi_found:
                st.write("### detected upi scam indicators")
                for word in upi_found:
                    st.write("💳 ", word)
            else:
                st.write("no suspicious upi payment requesr detected.")

            st.header("📞  Phone Number Pattern Check")

            phone_numbers = re.findall(r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",text)

            phone_score = 0
            phone_reasons = []

            if phone_numbers:

                st.write("### phone numbers found")

                for number in phone_numbers:
                    st.write("📱 ",number)

                    if len(set(number[-10:])) <= 2:
                        phone_score += 2
                        phone_reasons.append(f"{number} - too many reapeated number")

                    if re.search(r"(\d)\1{4,}",number):
                        phone_score += 2
                        phone_reasons.append(f"{number} - reapeated digits reapeated")

                    if number.startswith("+"):
                        phone_score += 1
                        phone_reasons.append(f"{number} - international number")
                                                 
            else:
                  st.write("no phone numbers detected.")

            st.write("### phone number risk score")
            st.progress(min(phone_score/10,1.0))
            st.write(f"{phone_score}/10")

            if phone_score >= 4:
                st.error("🚨 high phone number risk")
            elif phone_score >= 2:
                st.warning("⚠️medium phone number risk")
            else:
                st.success("✅low phone number risk")

            if phone_reasons:
                st.write("### reasons")
                for reason in phone_reasons:
                    st.write("•",reason)

            # sms scam detection check
            st.header("📩 SMS Scam Detection")

            sms_keywords = [
                "otp",
                "bank",
                "account",
                "kyc",
                "update",
                "verify",
                "click",
                "link",
                "winner",
                "lottery",
                "cash prize",
                "reward",
                "urgent",
                "blocked",
                "suspended",
                "dear customer",
                "loan",
                "credit",
                "debit",
                "refund",
                "upi",
                "payment",
                "expire",
                "delivery",
                "courier"
                "tracking",
                "work from home",
                "job offer",
                "investment",
                "crypto",
                "confirm",
                "limited offer"
            ]
              
            sms_found = []

            for word in sms_keywords:
                if word in text:
                   sms_found.append(word)

            sms_score = len(sms_found)

            st.write("### sms scam score")
            st.progress(min(sms_score/10,1.0))
            st.write(f"{sms_score}/10")

            if sms_score >= 4:
                st.error("🚨 high sms scam risk")
            elif sms_score >= 2:
                st.warning(" ⚠️ medium sms scam risk")
            else:
                st.success(" ✅ low sms scam risk")

            if sms_found:
                st.write("### sms scam keywords")
                for word in sms_found:
                    st.write("📱 ", word)
            else:
                st.write("no sms scam keywords detected.")


            # calculate risk percentage 
            risk_percentage = spam_probability * 100
            
            # display risk percentage 
            st.write("### 📊 Risk Percentage")

            st.progress(risk_percentage / 100)

            st.write(f"**{risk_percentage:.2f}%**")
            
            # store analysis results in session
            st.session_state.prediction = prediction
            st.session_state.confidence = confidence
            st.session_state.risk_percentage = risk_percentage
            st.session_state.score = score
            st.session_state.suspicious = suspicious
            st.session_state.url_score = url_score
            st.session_state.phishing_score = phishing_score
            st.session_state.qr_score = qr_score
            st.session_state.upi_score = upi_score
            st.session_state.whatsapp_score = whatsapp_score
            st.session_state.phone_score = phone_score
            st.session_state.sms_score = sms_score
            st.session_state.message_score = message_score 
            

            st.session_state.analysis_done = True
            
            # save scam history
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
            
               
            st.session_state.history.append({
                "Date & Time": current_time,
                "Email": email[:50],
                "Result": prediction,
                "Risk Score": f"{risk_percentage:.1f}%"
            })

            # show analysis summary
            if st.session_state.get("analysis_done", False):

                st.success(f"Prediction: {st.session_state.prediction}")

                st.metric(
                    "Risk Score",
                    f"{st.session_state.risk_percentage:.1f}%"
                )

                st.metric(
                    "Confidence",
                    f"{st.session_state.confidence * 100:.2f}%"
                )

                if st.button("📊 View Full Analysis"):

                    st.session_state.selected_page = 2
                    st.rerun()

# analysis result page
elif page == "📊 Analysis Result":
    
    # check if analysis data is available  
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False

    if not st.session_state.analysis_done:
        st.warning("⚠ No analysis available.")
        st.info("Please scan an email from Smart Scanner.")
        st.stop()

    prediction = st.session_state.prediction
    confidence = st.session_state.confidence
    risk_percentage = st.session_state.risk_percentage

    score = st.session_state.score
    suspicious = st.session_state.get("suspicious",False)
    url_score = st.session_state.url_score
    phishing_score = st.session_state.phishing_score
    qr_score = st.session_state.qr_score
    upi_score = st.session_state.upi_score
    whatsapp_score = st.session_state.whatsapp_score
    phone_score = st.session_state.phone_score
    sms_score = st.session_state.sms_score
    message_score = st.session_state.message_score

    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#0B1F3A,#1565C0);
    padding:30px;
    border-radius:18px;
    border:1px solid #42A5F5;
    text-align:center;
    margin-bottom:20px;
    ">

    <h1 style="color:white;">
    📊 AI Fraud Analysis Result
    </h1>

    <h3 style="color:#E3F2FD;">
    Complete AI Powered Security Analysis
    </h3>

    <p style="color:white;">
    Spam Detection • Phishing • URL Reputation • QR Scam • Fake UPI • SMS Fraud
    </p>

    </div>
    """, unsafe_allow_html=True)
    


    # retrieve stored analysis results         
    st.title("📊 AI Fraud Analysis Result")

    st.success("✅ Analysis Completed Successfully")

    st.divider()

    # display analysis header 
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🎯 Prediction", prediction)

    with col2:
        st.metric("📊 Risk Score", f"{risk_percentage:.1f}%")

    with col3:
        st.metric("🤖 Confidence", f"{confidence*100:.2f}%")

    st.divider()
    
    # display detection scores
    st.subheader("🛡 Detection Scores")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📧 Spam Score",f" {score}/10")
        st.metric("🌐 URL Reputation",f" {url_score}/10")
        st.metric("🎣 Phishing",f"{phishing_score}/10")
        st.metric("📷 QR Scam",f"{qr_score}/10")

    with col2:
        st.metric("💳 Fake UPI",f" {upi_score}/10")
        st.metric("📱 WhatsApp",f"{whatsapp_score}/10")
        st.metric("📞 Phone Risk",f" {phone_score}/10")
        st.metric("📩 SMS Scam",f"{sms_score}/10")

    st.divider()

    if risk_percentage >= 75:
        st.error("🚨 High Risk Scam Detected")

    elif risk_percentage >= 40:
        st.warning("⚠️ Suspicious Message")

    else:
        st.success("✅ Safe Message")

    st.divider()
    
    # display security recommendations
    st.info("""

        🔒 Security Recommendations

        ✔ Don't click unknown links

        ✔ Never share OTP

        ✔ Verify sender identity

        ✔ Verify UPI payment requests

        ✔ Report suspicious messages
    """)

        
    # show risk status    
    st.header("📊 Scam Risk Dashboard")

    overall_score = (
        score+
        qr_score+
        upi_score+
        phone_score+
        url_score+
        message_score+
        phishing_score+
        whatsapp_score+
        sms_score
    )
        

    risk_percentage = min((overall_score/90)*100,100)
    
    # calculate overall scam risk 
    st.subheader("overall scam risk")

    st.progress(risk_percentage / 100)

    st.write(f" risk score : {risk_percentage:.1f}%")

    if risk_percentage >= 75:
        st.error("🚨 high risk")
    elif risk_percentage >= 40:
        st.warning("⚠️low risk")
    else:
        st.success("✅low risk")
        
    # display overall security dashboard 
    st.header("📊 Professional Security Dashboard")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("🌐 spam score",f"{score}/10")

    with col2:
        st.metric("🎣 phishing", f"{phishing_score}/10")

    with col3:
        st.metric("📱 whatsapp",f"{whatsapp_score}/10")

    col4,col5,col6 = st.columns(3)

    with col4:
        st.metric("📷 qr scam",f"{qr_score}/10")

    with col5:
        st.metric("💳  upi scam",f"{upi_score}/10")

    with col6:
        st.metric("📞 phone risk", f"{phone_score}/10")

    col7,col8,col9 = st.columns(3)

    with col7:
        st.metric("📩 sms scam",f"{sms_score}/10")

    with col8:
        st.metric("🌍 url reputation",f"{url_score}/10")

    with col9:
        st.metric("📄 message scam",f"{message_score}/10")

    st.divider()

    col10,col11 = st.columns(2)
    
    # display machine learning results 
    with col10:
        st.metric("🤖 ml prediction",prediction.upper())


    with col11:
        st.metric("🎯 ml confidence",f"{confidence*100:.2f}%")

        
    # show overall security status 
    st.subheader("🛡 overall security status")

    if risk_percentage >= 75:
        st.error(f"🚨 high risk ({ risk_percentage:.1f}%)")

    elif risk_percentage >= 40:
        st.warning(f"⚠️ medium risk ({risk_percentage:.1f}%)")

    else:
        st.success(f"✅ low risk ({risk_percentage:.1f}%)")
        


    # detection summary 
    st.subheader("Detection Summary")

    st.write(f"🌐 rule based spam score :{score}")
    st.write(f"🤖 ml prediction:{prediction}")
    st.write(f"🤖 ml confidence:{confidence*100:.2f}")
    st.write(f"🔗 suspicious link: {'Yes' if suspicious else 'No'}")
    st.write(f"🎣 url reputation score: {url_score}/10")
    st.write(f"📄 message based scam score: {message_score}/10")
    st.write(f"🎯 phishing score: {phishing_score}/10")
    st.write(f"⚠️ qr scam score: {qr_score}/10")
    st.write(f"📱 whatsapp score: {whatsapp_score}/10")
    st.write(f"💬 fake upi scam score: {upi_score}/10")
    st.write(f"📞 phone number risk score: {phone_score}/10")
    st.write(f"📜 sms scam score: {sms_score}/10")

    if suspicious:
        st.write("🔗 suspicious link : yes")
    else:
        st.write("🔗suspicious link : no")
        
   
    # weekly scan activity chart
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    scans = [35, 48, 60, 55, 72, 90, 80]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=days,
            y=scans,
            mode="lines+markers",
            line=dict(width=4),
            marker=dict(size=8),
            name="Scans"
        )
    )

    fig.update_layout(
        title="📈 Weekly Scan Activity",
        xaxis_title="Day",
        yaxis_title="Number of Scans",
        height=400,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="weekly_scan_chart"
    )
    

    # security recommendation chart
    if risk_percentage >= 75:
        labels = ["High Risk", "Review Needed", "Safe"]
        values = [70, 20, 10]

    elif risk_percentage >= 40:
        labels = ["Review Needed", "Safe", "High Risk"]
        values = [50, 35, 15]

    else:
        labels = ["Safe", "Review Needed", "High Risk"]
        values = [80, 15, 5] 


    fig = px.pie(
        names=labels,
        values=values,
        title="🛡security recommendation",
        hole=0.45
    )

    fig.update_layout(
        height=350,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="security_pie_chart"
    )
    
    # create risk analysis data 
    data = {
        "Category": [
            "Spam",
            "Phishing",
            "URL",
            "QR",
            "UPI",
            "Phone",
            "SMS"
        ],
        "Score": [
            score,
            phishing_score,
            url_score,
            qr_score,
            upi_score,
            phone_score,
            sms_score
        ]
    }

    df = pd.DataFrame(data)
    
    # detection statistics
    average_score = df["Score"].mean()
    highest_score = df["Score"].max()
    highest_category = df.loc[df["Score"].idxmax(),"Category"]

    st.header("📊 Detection Summary")

    st.write(f"📈 average risk score: {average_score:.2f}/10")
    st.write(f"⚠️ highest risk: {highest_category}")
    st.write(f"🔥 highest score: {highest_score}/10")

    st.subheader("📋 Score Statistics")

    st.write(f"maximum Score: {df['Score'].max()}")
    st.write(f"minimum Score: {df['Score'].min()}")
    st.write(f"average Score: {df['Score'].mean():.2f}")
    st.write(f"total Score: {df['Score'].sum()}")

    # email statistics 
    st.header("📈 Email Statistics")

    email = st.session_state.get("email", "")
    urls = st.session_state.get("urls", [])
    found = st.session_state.get("found", [])


    total_words = len(email.split())
    total_characters = len(email)
    total_links=len(urls)
    total_spam_keywords = len(found)
    
    # display security metrics 
    col1,col2 = st.columns(2)

    with col1:
        st.metric("📝 total words",total_words)
        st.metric("🔗 links found", total_links)

    with col2:
        st.metric(" 🔤 characters",total_characters)
        st.metric(" 🚩spam keywords", total_spam_keywords)

    st.divider()

    col3,col4,col5 = st.columns(3)

    with col3:
        st.metric("📱  whatsapp", whatsapp_score)

    with col4:
        st.metric("🎣 phishing", phishing_score)

    with col5:
        st.metric("📩 sms scam",sms_score)

    col6,col7,col8= st.columns(3)

    with col6:
        st.metric(" 💳 upi scam", upi_score)

    with col7:
        st.metric("📷 qr scam",qr_score)

    with col8:
        st.metric("🌐 url risk", url_score)


    # final scam decision
    st.header("🛡 Final Decision")

    if (
        prediction == "spam"
        or score >= 3
        or qr_score >= 3
        or upi_score >= 3
        or phone_score >= 3
        or url_score >= 3
        or message_score >= 3
        or phishing_score >= 3
        or whatsapp_score >= 3
        or sms_score >= 3
        or suspicious
    ):
            
            
        st.error("⚠️ high risk - possible scam")
    else:
        st.success("✅ safe message")
        
    # save scan history
    st.session_state.history.append({
        "message":email[:40]+"...",
        "ml prediction":prediction,
        "spam score":score,
        "phishing":phishing_score,
        "qr":qr_score,
        "upi":upi_score,
        "phone":phone_score,
        "sms":sms_score,
        "risk%":f"{risk_percentage:.1f}%"
    })

    # generate pdf report 
    os.makedirs("report", exist_ok=True)

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate("report/scam_report.pdf")

    story = []
    
    
    story.append(Paragraph("<b>AI spam and scam detection report</b>",styles["Title"]))

    # add message summary to pdf 
    story.append(Paragraph("<b>📧 Message Summary</b>", styles["Heading2"]))
    story.append(Paragraph(f"ML Prediction : {prediction}", styles["BodyText"]))
    story.append(Paragraph(f"Confidence : {confidence*100:.2f}%", styles["BodyText"]))
    story.append(Paragraph(f"Overall Risk : {risk_percentage:.1f}%", styles["BodyText"]))

    # add detection scores to pdf 
    story.append(Paragraph("<b>🛡 Detection Scores</b>", styles["Heading2"]))
    story.append(Paragraph(f"Rule-Based Spam : {score}/10", styles["BodyText"]))
    story.append(Paragraph(f"URL Reputation : {url_score}/10", styles["BodyText"]))
    story.append(Paragraph(f"Message Scam : {message_score}/10", styles["BodyText"]))
    story.append(Paragraph(f"Phishing : {phishing_score}/10", styles["BodyText"]))
    story.append(Paragraph(f"QR Scam : {qr_score}/10", styles["BodyText"]))
    story.append(Paragraph(f"WhatsApp Scam : {whatsapp_score}/10", styles["BodyText"]))
    story.append(Paragraph(f"Fake UPI : {upi_score}/10", styles["BodyText"]))
    story.append(Paragraph(f"Phone Risk : {phone_score}/10", styles["BodyText"]))
    story.append(Paragraph(f"SMS Scam : {sms_score}/10", styles["BodyText"]))

    # add final decision to pdf 
    story.append(Paragraph("<b>🛡 Final Decision</b>", styles["Heading2"]))
    story.append(Paragraph("Possible Scam Detected", styles["BodyText"]))

    # add security recommendations
    story.append(Paragraph("<b>🔒 Security Recommendations</b>", styles["Heading2"]))
    story.append(Paragraph("• Do not click unknown links", styles["BodyText"]))
    story.append(Paragraph("• Never share OTP", styles["BodyText"]))
    story.append(Paragraph("• Verify sender identity", styles["BodyText"]))
    story.append(Paragraph("• Verify UPI payment requests", styles["BodyText"]))
    story.append(Paragraph("• Report suspicious messages", styles["BodyText"]))

    # build and download pdf report 
    pdf.build(story)

    with open("report/scam_report.pdf","rb") as pdf_file:

        st.download_button(
            "📄 download pdf report",
            pdf_file,
            file_name="scam_report.pdf",
            mime="application/pdf"
        )

    # display security recommendations
    st.header("🛡  Security Recommendations")

    if risk_percentage >= 75:
        st.error("""

        

    ⚠️ do not click links

    ⚠️ do not share otp

    ⚠️ do not scam unknown qr codes

    ⚠️verify with the official websites or bank

    ⚠️ report the message as spam
    """)
                

    elif risk_percentage >= 40:
        st.warning("""



    ⚠️ be careful

    ✔️ verify sender

    ✔️check official website

    ✔️ don't share personal details
    """)


    else:
        st.success("""
    ✅ messsage appears relatively safe.

    still verify important finincial requests before acting.
    """)
        

    # display detected keywords
    if found:
        st.info("Detected keywords: " + ", ".join(found))
    else:
        st.info("No suspicious keywords detected.")

            
# prediction history page 
elif page == "📜 Prediction History":

    # custom css styling 
    st.markdown("""
    <style>


    div[data-baseweb="popover"]{
        background:#0B1220 !important;
    }

    ul{
        background:#0B1220 !important;
    }

    li{
        background:#0B1220 !important;
        color:white !important;
    }

    li:hover{
        background:#1E293B !important;
    }

    div[role="option"]{
        background:#0B1220 !important;
        color:white !important;
    }

    a{

        color:white !important;
    }

    a:visited{
        color:white !important;
    }

    a:hover{
        color:#29B6F6 !important;
    }

    </style>
    """, unsafe_allow_html=True)
    
    
    st.markdown("""
        <style>

        /* DataFrame Container */
        [data-testid="stDataFrame"]{
            background-color:#0B1220 !important;
            border:2px solid #29B6F6 !important;
            border-radius:12px !important;
        }

        /* Inner Grid */
        [data-testid="stDataFrame"] div{
            background-color:#0B1220 !important;
            color:white !important;
        }

        /* Header */
        [data-testid="stDataFrame"] th{
            background-color:#111827 !important;
            color:white !important;
        }

        /* Cells */
        [data-testid="stDataFrame"] td{
            background-color:#0B1220 !important;
            color:white !important;
        }

        /* Scroll Area */
        [data-testid="stDataFrame"].glideDataEditor{
            background:#0B1220 !important;
            color:white !important;
        }

        /* Grid Cells */
        [data-testid="stDataFrame"] .glideDataEditor div{
            color:white !important;
            background:#0B1220 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>

        /* Text Input */
        .stTextInput input{
            background:#0B1220 !important;
            color:white !important;
            border:2px solid #29B6F6 !important;
        }

        /* Placeholder */
        .stTextInput input::placeholder{
            color:#B0B0B0 !important;
        }

        /* Selectbox */
        .stSelectbox div[data-baseweb="select"] > div{
            background:#0B1220 !important;
            color:white !important;
            border:2px solid #29B6F6 !important;
        }

        /* Dropdown options */
        div[role="listbox"]{
            background:#0B1220 !important;
        }

        div[role="option"]{
            background:#0B1220 !important;
            color:white !important;
        }

        div[role="option"]:hover{
            background:#1E293B !important;
        }

        </style>
        """, unsafe_allow_html=True)

    # prediction history header 
    st.markdown("""
    <h1 style='color:#00D4FF;'>📄 Prediction History</h1>
    <p style='color:white;font-size:18px;'>
    View all your past email scans and predictions
    </p>
    """, unsafe_allow_html=True)
    

    # dashboard statistics 
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📧 Total Scans", "1243")

    with c2:
        st.metric("✅ Safe Messages", "983")

    with c3:
        st.metric("⚠️ Scam Detected", "271")

    with c4:
        st.metric("📄 Reports Generated", "1273")

    st.markdown("---")
    
    
    # search and filter options 
    col1, col2, col3, col4 = st.columns([3,2,2,1])

    with col1:
        search = st.text_input(
            "🔍 Search by Email or Keyword",
            placeholder="Enter email or keyword..."
        )

    with col2:
        date_filter = st.selectbox(
            "📅 Select Date Range",
            ["Today", "Last 7 Days", "Last 30 Days", "All"]
        )

    with col3:
        result_filter = st.selectbox(
            "⚙️ Filter by Result",
            ["All", "Safe", "Spam", "Scam"]
        )

    with col4:
        st.write("")
        st.write("")
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()



    st.markdown("---")
    

    # sample prediction hsitory data
    data = pd.DataFrame({
        "#":[1,2,3,4,5,6,7,8],
        "Email / Message":[
            "vishnu.sahni2024@gmail.com",
            "secure@yourbank.com",
            "lottery.win.big@prizes.com",
            "info@amazon.in",
            "update-br@shorts-friends.com",
            "paytm.service@paytm.com",
            "free.income.guarantee@money.com",
            "meeting.schedule@company.com"
        ],
        "Result":[
            "Scam",
            "Safe",
            "Scam",
            "Safe",
            "Scam",
            "Safe",
            "Scam",
            "Safe"
        ],
        "Risk Score":[
            82.45,
            18.35,
            91.30,
            12.35,
            76.10,
            6.82,
            88.36,
            15.40
        ],
        "Scan Date & Time":[
            "23 May 2025, 10:30 AM",
            "23 May 2025, 09:45 AM",
            "23 May 2025, 08:15 AM",
            "22 May 2025, 06:40 PM",
            "22 May 2025, 05:22 PM",
            "22 May 2025, 01:10 PM",
            "22 May 2025, 10:02 AM",
            "22 May 2025, 09:05 AM"
        ]
    })

     
    # display prediction history table
    for i,row in data.iterrows():

        c1,c2,c3,c4,c5,c6 = st.columns([0.5,3,1.5,2,2,2])

        with c1:
            st.write(row["#"])

        with c2:
            st.write(row["Email / Message"])

        with c3:
            if row["Result"]=="Safe":
                st.success("✅ Safe")
            else:
                st.error("⚠ Scam")

        with c4:
            risk = float(str(row["Risk Score"]).replace("%",""))

            st.progress(risk/100)
            st.caption(f"{risk:.2f}%")
           

        with c5:
            st.write(row["Scan Date & Time"])

        with c6:

            b1,b2,b3 = st.columns(3)

            with b1:
                st.button("👁",key=f"view{i}")

            with b2:
                st.button("📄",key=f"pdf{i}")

            with b3:
                st.button("🗑",key=f"delete{i}")

        st.divider()


    st.markdown("---")

   

    st.info(
        "💡 Tip: Click on 👁 to view details, 📄 to download the report, and 🗑 to delete the record."
    )


    st.markdown("---")

    st.markdown("""
    <div style="
    text-align:center;
    color:#AFCBFF;
    font-size:15px;
    padding:10px;">
    © 2026 AI Spam & Scam Detection System | All Rights Reserved
    </div>
    """, unsafe_allow_html=True) 

    st.divider()

# report download page   
elif page == "📄 Report Download":
    
    # custom css styling
    st.markdown("""
    <style>

    div[data-baseweb="popover"]{
        background:#0B1220 !important;
    }

    ul{
        background:#0B1220 !important;
    }

    li{
        background:#0B1220 !important;
        color:white !important;
    }

    li:hover{
        background:#1E293B !important;
    }

    div[role="option"]{
        background:#0B1220 !important;
        color:white !important;
    }

    a{
        color:white !important;
    }

    a:visited{
        color:white !important;
    }

    a:hover{
        color:#29B6F6 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    div[data-testid="stDownloadButton"]>button{
        background: #0B1220 !important;
        color: white !important;
        border: 2px solid #29B6F6 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stDownloadButton']>button:hover{
        background: #16213E !important;
        color: white !important;
        border-color: #00E5FF !important;
    }
    </style>
    """, unsafe_allow_html=True)
    

    st.markdown("""
        <style>

        /* Download links */
        a{
            color:white !important;
            text-decoration:none !important;
        }

        a:visited{
            color:white !important;
        }

        a:hover{
            color:#29B6F6 !important;
        }

        </style>
        """, unsafe_allow_html=True) 
        

    st.markdown("""
        <style>

        [data-testid="stDataFrame"]{
            background:#0B1220 !important;
            border:2px solid #29B6F6 !important;
            border-radius:12px !important;
        }

        .glideDataEditor{
            background:#0B1220 !important;
            color:white !important;
        }

        .glideDataEditor *{
            background:#0B1220 !important;
            color:white !important;
        }

        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <style>

        /* Text Input */
        .stTextInput input{
            background:#0B1220 !important;
            color:white !important;
            border:2px solid #29B6F6 !important;
        }

        /* Placeholder */
        .stTextInput input::placeholder{
            color:#B0B0B0 !important;
        }

        /* Selectbox */
        .stSelectbox div[data-baseweb="select"] > div{
            background:#0B1220 !important;
            color:white !important;
            border:2px solid #29B6F6 !important;
        }

        /* Dropdown options */
        div[role="listbox"]{
            background:#0B1220 !important;
        }

        div[role="option"]{
            background:#0B1220 !important;
            color:white !important;
        }

        div[role="option"]:hover{
            background:#1E293B !important;
        }

        </style>
        """, unsafe_allow_html=True)

    # report download header
    st.markdown("""
    <h1 style='color:#00D4FF;'>📄 Report Download</h1>
    <p style='color:white;font-size:18px;'>
    Download professional PDF reports of your email analysis.
    </p>
    """, unsafe_allow_html=True)

    # report statistics dashboard 
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📄 Total Reports", "25")

    with c2:
        st.metric("✅ Safe Reports", "13")

    with c3:
        st.metric("⚠ Scam Reports", "10")

    with c4:
        st.metric("⬇ Total Downloads", "18")

    st.markdown("---")


    # generate new pdf report
    st.subheader("📑 Generate New Report")

    col1, col2 = st.columns([3,1])

    with col1:

        with col1:

            if st.session_state.history:
                
                reports = []
                
                for item in st.session_state.history:
                    reports.append(item.get("Email", ""))

                selected_report = st.selectbox(
                    "Select a scan from history",
                    reports
                )
            else:
                st.info("No reports available.")

                

        with col2:
                st.write("")
                st.write("")

                st.markdown("""
                <style>
                div.stButton > button{
                    background:#7B3FF2;
                    color:white;
                    border-radius:10px;
                    font-weight:bold;
                    height:45px;
                }
                </style>
                """, unsafe_allow_html=True)

        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.success("PDF Report Generated Successfully!")

    st.markdown("---")

    st.caption("Download your AI generated fraud analysis report")

    st.divider()
    
    # download generated pdf
    if os.path.exists("report/scam_report.pdf"):

        with open("report/scam_report.pdf", "rb") as pdf:

            st.download_button(
                label="📥 Download PDF Report",
                data=pdf,
                file_name="AI_Fraud_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.success("✅ Report Ready For Download")

    else:

        st.warning("⚠️ No report available. Please scan an email first.")

    st.divider()
    
    # available reports table 
    st.subheader("📂 Available Reports")

    reports = pd.DataFrame({
        "#":[1,2,3,4],
        "Email / Message":[
            "winner.offer2025@gmail.com",
            "secure@yourbank.com",
            "lottery.win.big@prizes.com",
            "info@amazon.in"
        ],
        "Result":[
            "Scam",
            "Safe",
            "Scam",
            "Safe"
        ],
        "Risk Score":[
            82.45,
            18.35,
            91.20,
            12.60
        ],
        "Scan Date & Time":[
            "23 May 2025 10:30 AM",
            "23 May 2025 09:45 AM",
            "22 May 2025 06:15 PM",
            "22 May 2025 05:05 PM"
        ]
    })


    h1,h2,h3,h4,h5,h6 = st.columns([0.5,3,1.5,2,2,2])

    h1.markdown("**#**")
    h2.markdown("**Email / Message**")
    h3.markdown("**Result**")
    h4.markdown("**Risk Score**")
    h5.markdown("**Scan Date & Time**")
    h6.markdown("**Actions**")

    st.divider()

    # display report list 
    for i,row in reports.iterrows():

        c1,c2,c3,c4,c5,c6 = st.columns([0.5,3,1.5,2,2,2])

        c1.write(row["#"])
        c2.write(row["Email / Message"])

        if row["Result"]=="Safe":
            c3.success("✅ Safe")
        else:
            c3.error("⚠ Scam")
           
        c4.progress(row["Risk Score"]/100)
        c4.caption(f"{row['Risk Score']:.2f}%")

        c5.write(row["Scan Date & Time"])

        b1,b2,b3 = c6.columns(3)

        with b1:
            st.button("👁", key=f"preview{i}")

        with b2:
            st.button("⬇", key=f"download{i}")

        with b3:
            st.button("🗑", key=f"delete{i}")

        st.divider()

        st.markdown("---")

    # report summary statistics 
    a1, a2, a3 = st.columns(3)

    with a1:
        st.success("✅ Safe Reports : 13")

    with a2:
        st.error("⚠ Scam Reports : 10")

    with a3:
        st.info("📄 Total Reports : 23")

    # user tips
    st.info("""
    💡 **Tips**

    • Click 👁 Preview to view report details.

    • Click ⬇ Download to save the PDF report.

    • Click 🗑 Delete to remove the report.

    • Reports are generated automatically after every scan.
    """)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # footer 
    st.markdown("""
    <div style="
    text-align:center;
    color:#B5C7E3;
    font-size:14px;
    padding:10px;">

    © 2026 AI Spam & Scam Detection System | All Rights Reserved

    </div>
    """, unsafe_allow_html=True)

# about page
elif page == "ℹ️ About":
    
    # load background image
    bg = get_base64("images1/05_privacy.jpg")

    set_bg(bg)

    # project header 
    col1, col2 = st.columns([1,5])

    with col1:
        st.image("images2/logo2.png", width=90)

    with col2:
        st.markdown("""
        <h2 style='color:#00D4FF;'>AI Spam & Scam Detection System</h2>
        <p style='color:white;'>
        Smart • Secure • Reliable
        </p>
        """, unsafe_allow_html=True)
        
    # advanced features 
    st.subheader("🚀 Advanced Key Features")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.info("""
    🧠 **AI Detection**

    ✔ Machine Learning

    ✔ Spam Detection

    ✔ Scam Detection
    """)

    with c2:
        st.info("""
    🌐 **Real-Time Protection**

    ✔ URL Scanner

    ✔ QR Scanner

    ✔ UPI Detection
    """)

    with c3:
        st.info("""
    📊 **Analytics**

    ✔ Risk Score

    ✔ Prediction History

    ✔ Dashboard
    """)

    with c4:
        st.info("""
    📄 **Reports**

    ✔ PDF Reports

    ✔ Download History

    ✔ Export Data
    """)
        
    # security features 
    st.subheader("🔒 Security Features")

    st.success("✅ Spam Email Detection")
    st.success("✅ Phishing Website Detection")
    st.success("✅ Fake UPI Detection")
    st.success("✅ QR Code Scam Detection")
    st.success("✅ SMS Scam Detection")
    st.success("✅ Suspicious Link Detection")
    
    # technologies used
    st.subheader("⚙️ Technologies Used")

    st.write("""
    - Python
    - Streamlit
    - Scikit-Learn
    - Pandas
    - Plotly
    - HTML
    - CSS
    - Machine Learning
    """)

    st.markdown("---")

    st.divider()
    
    # project statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🛡 Security Modules", "8")

    with col2:
        st.metric("🤖 AI Model", "Naive Bayes")

    with col3:
        st.metric("📄 Reports", "PDF")

    with col4:
        st.metric("📜 History", "Enabled")       


    st.divider()
    
    # project overview
    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#081F4D,#0A4EA6);
    padding:30px;
    border-radius:18px;
    border:1px solid #4FC3F7;
    ">

    <h2 style="color:white;">🛡 Project Overview</h2>

    <p style="color:white;">
    The AI Spam & Scam Detection System is an intelligent cyber security
    application developed using Machine Learning and Rule-Based Detection.
    It helps users identify spam emails, phishing attacks, fake UPI requests,
    QR scams, SMS fraud, WhatsApp scams and malicious website links before
    they become victims of cyber crime.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # poject objectives
    st.subheader("🎯 Project Objectives")

    st.info("""
    ✔ Protect users from online fraud.

    ✔ Detect suspicious messages instantly.

    ✔ Provide AI-based scam prediction.

    ✔ Generate downloadable PDF reports.

    ✔ Improve cyber security awareness.
    """)

    st.divider()
    
    # developer information
    st.subheader("👨‍💻 Developer")

    st.success("""

    Name : Dhanshree Raju Sutar

    Project : AI Spam & Scam Detection System

    Version : 1.0

    Purpose : To build an AI-powered spam and scam detection system that helps users identify fraudulent messages and improve online security 
    """)

    st.divider()
    
    # security statement
    st.subheader("🔒 Security Statement")

    st.warning("""
    This application is developed for educational and cyber security
    awareness purposes. It assists users in identifying potentially
    fraudulent emails and messages using AI and rule-based analysis.
    Users should always verify suspicious communications before taking
    any action.
    """)

    st.divider()

    st.success("🛡 Detect Early • Stay Safe • Prevent Digital Fraud") 
    bg = get_base64("images1/05_privacy.jpg")

    st.divider()
    
    # footer 
    st.markdown("""
    <hr>
    <div style="text-align:center;color:#B0C4DE;">
    © 2026  AI Spam & Scam Detection System | All Rights Reserved
    </div>
    """, unsafe_allow_html=True)


       
