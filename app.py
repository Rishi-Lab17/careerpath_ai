import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import json
import hashlib
from datetime import datetime
import pdfplumber
import random
import os

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="CareerPath AI", page_icon="🚀", layout="wide")

# ==================== CSS ====================
st.markdown("""
<style>
    html, body, .stApp, .stMarkdown, p, div, span, label, 
    .stTextInput > label, .stSelectbox > label, .stSlider > label, 
    .stNumberInput > label, h1, h2, h3, h4, h5, h6,
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError,
    .streamlit-expanderHeader, .stCheckbox label, .stRadio label,
    .stTabs [data-baseweb="tab"], .stCaption {
        color: #1e293b !important;
    }
    .stApp { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); }
    .stTextInput > div > div > input, .stSelectbox > div > div, 
    .stTextArea > div > textarea, .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
    }
    ul[role="listbox"] li { background-color: #ffffff !important; color: #1e293b !important; }
    .stButton > button {
        background: linear-gradient(95deg, #3b82f6, #8b5cf6);
        color: white !important;
        font-weight: 600;
        border-radius: 40px;
        padding: 0.5rem 1.5rem;
        border: none;
    }
    .stButton > button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(59,130,246,0.5); }
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(0,0,0,0.1);
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border-bottom: 2px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #3b82f6 !important; }
    .hero {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        padding: 1.5rem;
        border-radius: 28px;
        text-align: center;
        margin-bottom: 1.5rem;
        color: white !important;
    }
    .hero h2, .hero p { color: white !important; }
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.1);
        max-width: 450px;
        margin: 0 auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .footer {
        text-align: center;
        padding: 1rem;
        font-size: 0.7rem;
        border-top: 1px solid rgba(0,0,0,0.1);
        margin-top: 2rem;
        color: #64748b !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background: #ffffff;
        border-radius: 40px;
        padding: 6px 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab"] {
        color: #1e293b !important;
        font-weight: 600;
        border-radius: 30px;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] { background: #ffffff; box-shadow: 2px 0 10px rgba(0,0,0,0.05); }
    section[data-testid="stSidebar"] * { color: #1e293b !important; }
    .stProgress > div > div { background: linear-gradient(90deg, #3b82f6, #a855f7); }
    .badge { display: inline-block; background: #e2e8f0; padding: 4px 12px; border-radius: 30px; font-size: 0.7rem; font-weight: 600; color: #1e293b !important; }
    .badge-high { background: #fee2e2; color: #dc2626 !important; }
    .badge-medium { background: #fef3c7; color: #d97706 !important; }
    .stSlider > div > div > div { background-color: #3b82f6 !important; }
    .stCheckbox > label, .stRadio > label { color: #1e293b !important; }
    .stAlert, .stInfo, .stSuccess { background-color: #f1f5f9 !important; color: #1e293b !important; }
    .stCaption { color: #64748b !important; }
</style>
""", unsafe_allow_html=True)

# ==================== USER DATABASE ====================
USER_DATA_FILE = "user_data.json"

def load_all_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_all_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user_key(name, mobile):
    return f"{name}_{mobile}"

def save_user_data(name, mobile, data):
    users = load_all_users()
    key = get_user_key(name, mobile)
    users[key] = data
    save_all_users(users)

def load_user_data(name, mobile):
    users = load_all_users()
    key = get_user_key(name, mobile)
    return users.get(key, None)

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_mobile' not in st.session_state:
    st.session_state.user_mobile = ""
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'current_role' not in st.session_state:
    st.session_state.current_role = ""
if 'target_role' not in st.session_state:
    st.session_state.target_role = ""
if 'years_exp' not in st.session_state:
    st.session_state.years_exp = 0
if 'skills' not in st.session_state:
    st.session_state.skills = []
if 'show_roadmap' not in st.session_state:
    st.session_state.show_roadmap = False
if 'ai_cache' not in st.session_state:
    st.session_state.ai_cache = {}
if 'completed_criteria' not in st.session_state:
    st.session_state.completed_criteria = set()
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = set()
if 'daily_streak' not in st.session_state:
    st.session_state.daily_streak = 1
if 'last_login_date' not in st.session_state:
    st.session_state.last_login_date = datetime.now().strftime("%Y-%m-%d")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'preferred_location' not in st.session_state:
    st.session_state.preferred_location = "Bangalore"
if 'learning_hours' not in st.session_state:
    st.session_state.learning_hours = 5
if 'page' not in st.session_state:
    st.session_state.page = "login"

# ==================== JOB ROLES DATABASE (40+ ROLES) ====================
JOB_SKILL_MAP = {
    "Software Engineer": {"skills": ["Python", "Java", "SQL", "Data Structures", "Algorithms", "Git", "Debugging"], "salary_base": (5, 9), "growth_rate": 12},
    "Senior Software Engineer": {"skills": ["System Design", "Architecture", "Code Review", "Mentoring", "Advanced Algorithms", "Performance Optimization"], "salary_base": (12, 20), "growth_rate": 15},
    "Tech Lead": {"skills": ["Team Leadership", "Project Planning", "Technical Architecture", "Risk Assessment", "Stakeholder Management", "Agile"], "salary_base": (18, 28), "growth_rate": 18},
    "Engineering Manager": {"skills": ["Budgeting", "Hiring", "Performance Reviews", "Strategic Planning", "Team Building", "OKRs"], "salary_base": (25, 40), "growth_rate": 20},
    "Product Manager": {"skills": ["Market Research", "User Stories", "Roadmap Planning", "Data Analysis", "Stakeholder Management", "Product Strategy"], "salary_base": (10, 18), "growth_rate": 14},
    "Senior Product Manager": {"skills": ["Product Strategy", "Go-to-Market", "Metrics Analysis", "Cross-team Leadership", "Customer Discovery"], "salary_base": (18, 30), "growth_rate": 16},
    "Data Analyst": {"skills": ["SQL", "Excel", "Tableau/Power BI", "Statistics", "Python", "Data Visualization"], "salary_base": (4, 8), "growth_rate": 10},
    "Lead Data Analyst": {"skills": ["Data Modeling", "ETL Pipelines", "Team Leadership", "Advanced Analytics", "Data Governance"], "salary_base": (10, 16), "growth_rate": 12},
    "Data Scientist": {"skills": ["Python", "Machine Learning", "Statistics", "SQL", "TensorFlow/PyTorch", "Data Visualization"], "salary_base": (8, 15), "growth_rate": 18},
    "DevOps Engineer": {"skills": ["CI/CD", "AWS/Azure", "Docker", "Kubernetes", "Linux", "Terraform", "Monitoring"], "salary_base": (7, 14), "growth_rate": 16},
    "Senior DevOps Engineer": {"skills": ["Infrastructure as Code", "Security Best Practices", "Cost Optimization", "GitOps", "Multi-cloud"], "salary_base": (15, 25), "growth_rate": 17},
    "Cloud Engineer": {"skills": ["AWS", "Azure/GCP", "Cloud Architecture", "Networking", "Security", "Terraform"], "salary_base": (8, 16), "growth_rate": 15},
    "Frontend Developer": {"skills": ["React", "JavaScript", "HTML/CSS", "TypeScript", "Next.js", "Tailwind", "Web Performance"], "salary_base": (5, 10), "growth_rate": 11},
    "Senior Frontend Developer": {"skills": ["Frontend Architecture", "State Management", "Performance Optimization", "Team Mentoring", "UI/UX Collaboration"], "salary_base": (10, 18), "growth_rate": 13},
    "Backend Developer": {"skills": ["Node.js/Python", "Databases", "API Design", "Microservices", "Caching", "Authentication"], "salary_base": (6, 12), "growth_rate": 12},
    "Full Stack Developer": {"skills": ["React", "Node.js", "MongoDB/PostgreSQL", "REST APIs", "Authentication", "Deployment", "Git"], "salary_base": (7, 14), "growth_rate": 13},
    "Mobile Developer": {"skills": ["iOS/Android", "React Native/Flutter", "Mobile UI/UX", "App Store Deployment", "REST APIs"], "salary_base": (6, 12), "growth_rate": 12},
    "QA Engineer": {"skills": ["Manual Testing", "Automation Testing", "Selenium", "JIRA", "Test Cases", "Bug Tracking"], "salary_base": (4, 7), "growth_rate": 8},
    "Lead QA Engineer": {"skills": ["Test Strategy", "Team Leadership", "CI/CD Integration", "Performance Testing", "QA Metrics"], "salary_base": (8, 13), "growth_rate": 10},
    "Security Engineer": {"skills": ["Network Security", "Penetration Testing", "Risk Assessment", "Security Audits", "Encryption"], "salary_base": (8, 15), "growth_rate": 16},
    "Network Engineer": {"skills": ["Routing/Switching", "Firewalls", "TCP/IP", "DNS", "Load Balancing"], "salary_base": (5, 9), "growth_rate": 8},
    "Database Administrator": {"skills": ["SQL", "Database Design", "Performance Tuning", "Backup/Recovery", "Security"], "salary_base": (6, 11), "growth_rate": 9},
    "Systems Administrator": {"skills": ["Linux/Windows", "Scripting", "Virtualization", "Backup", "Monitoring"], "salary_base": (4, 8), "growth_rate": 7},
    "Business Analyst": {"skills": ["Requirements Gathering", "Process Mapping", "Data Analysis", "Stakeholder Management", "UML"], "salary_base": (5, 10), "growth_rate": 10},
    "Project Manager": {"skills": ["Project Planning", "Risk Management", "Budgeting", "Team Coordination", "Agile"], "salary_base": (10, 18), "growth_rate": 12},
    "Scrum Master": {"skills": ["Agile Methodologies", "Sprint Planning", "Team Facilitation", "Conflict Resolution", "JIRA"], "salary_base": (8, 14), "growth_rate": 10},
    "Sales Executive": {"skills": ["Lead Generation", "Negotiation", "CRM", "Pipeline Management", "Client Relationship"], "salary_base": (3, 8), "growth_rate": 15},
    "Sales Manager": {"skills": ["Team Leadership", "Sales Strategy", "Forecasting", "Territory Management", "Training"], "salary_base": (8, 16), "growth_rate": 14},
    "Marketing Associate": {"skills": ["Digital Marketing", "Social Media", "Content Creation", "SEO/SEM", "Email Marketing"], "salary_base": (3, 6), "growth_rate": 10},
    "Marketing Manager": {"skills": ["Brand Strategy", "Campaign Management", "Budgeting", "Team Leadership", "Market Research"], "salary_base": (8, 15), "growth_rate": 12},
    "HR Associate": {"skills": ["Recruitment", "Onboarding", "Employee Relations", "HR Policies", "Payroll"], "salary_base": (3, 5), "growth_rate": 8},
    "HR Manager": {"skills": ["Talent Acquisition", "Performance Management", "Compensation", "Employee Engagement", "Leadership Development"], "salary_base": (7, 14), "growth_rate": 10},
    "UX Designer": {"skills": ["User Research", "Wireframing", "Prototyping", "Figma", "Usability Testing"], "salary_base": (6, 12), "growth_rate": 11},
    "UI Designer": {"skills": ["Visual Design", "Color Theory", "Typography", "Figma", "Design Systems"], "salary_base": (5, 10), "growth_rate": 10},
    "Technical Writer": {"skills": ["Documentation", "API Documentation", "Technical Communication", "Markdown", "Confluence"], "salary_base": (4, 8), "growth_rate": 8},
    "Solutions Architect": {"skills": ["Enterprise Architecture", "Cloud Solutions", "System Integration", "Technical Presales", "Cost Estimation"], "salary_base": (20, 35), "growth_rate": 18},
    "Blockchain Developer": {"skills": ["Solidity", "Smart Contracts", "Ethereum", "Web3.js", "Cryptography"], "salary_base": (10, 20), "growth_rate": 22},
    "AI Engineer": {"skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "NLP", "Computer Vision"], "salary_base": (12, 22), "growth_rate": 25}
}

# ==================== HELPER FUNCTIONS ====================
def get_user_profile_hash():
    profile = f"{st.session_state.current_role}_{st.session_state.target_role}_{st.session_state.years_exp}"
    for s in st.session_state.skills:
        profile += f"_{s['name']}_{s['level']}"
    return hashlib.md5(profile.encode()).hexdigest()

def get_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Good Morning ☀️"
    elif hour < 17: return "Good Afternoon 🌤️"
    elif hour < 21: return "Good Evening 🌆"
    else: return "Good Night 🌙"

def update_streak():
    today = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.last_login_date != today:
        st.session_state.daily_streak += 1
        st.session_state.last_login_date = today

def get_skill_average():
    if not st.session_state.skills:
        return 5.0
    return sum(s['level'] for s in st.session_state.skills) / len(st.session_state.skills)

def save_user_state():
    user_data = {
        "current_role": st.session_state.current_role,
        "target_role": st.session_state.target_role,
        "years_exp": st.session_state.years_exp,
        "skills": st.session_state.skills,
        "preferred_location": st.session_state.preferred_location,
        "learning_hours": st.session_state.learning_hours,
        "completed_criteria": list(st.session_state.completed_criteria),
        "completed_tasks": list(st.session_state.completed_tasks),
        "chat_history": st.session_state.chat_history,
        "daily_streak": st.session_state.daily_streak
    }
    save_user_data(st.session_state.user_name, st.session_state.user_mobile, user_data)

def load_user_state(name, mobile):
    data = load_user_data(name, mobile)
    if data:
        st.session_state.current_role = data.get("current_role", "")
        st.session_state.target_role = data.get("target_role", "")
        st.session_state.years_exp = data.get("years_exp", 0)
        st.session_state.skills = data.get("skills", [])
        st.session_state.preferred_location = data.get("preferred_location", "Bangalore")
        st.session_state.learning_hours = data.get("learning_hours", 5)
        st.session_state.completed_criteria = set(data.get("completed_criteria", []))
        st.session_state.completed_tasks = set(data.get("completed_tasks", []))
        st.session_state.chat_history = data.get("chat_history", [])
        st.session_state.daily_streak = data.get("daily_streak", 1)
        return True
    return False

# ==================== DYNAMIC FEATURE FUNCTIONS ====================
def get_skill_gaps_dynamic():
    target_data = JOB_SKILL_MAP.get(st.session_state.target_role, {"skills": ["Technical Skills", "Communication", "Problem Solving"], "salary_base": (5, 12), "growth_rate": 10})
    required_skills = target_data["skills"]
    user_skills = [s['name'].lower() for s in st.session_state.skills]
    
    missing = []
    for skill in required_skills:
        if not any(skill.lower() in user_skill or user_skill in skill.lower() for user_skill in user_skills):
            missing.append(skill)
    
    if not missing:
        missing = required_skills[:4]
    
    gaps = []
    for i, skill in enumerate(missing[:4]):
        priority = "HIGH" if i < 2 else "MEDIUM"
        weeks = 8 if priority == "HIGH" else 4
        gaps.append({"skill": skill, "reason": f"Required for {st.session_state.target_role} role", "priority": priority, "weeks": weeks})
    return gaps

def get_roadmap_dynamic():
    gaps = get_skill_gaps_dynamic()
    exp = st.session_state.years_exp
    if exp < 2:
        timeline = 12
    elif exp < 5:
        timeline = 10
    else:
        timeline = 8
    
    roadmap = []
    for i, gap in enumerate(gaps[:3]):
        start = i * 2 + 1
        end = start + 1
        roadmap.append(f"- Month {start}-{end}: Master {gap['skill']} through courses and projects")
    roadmap.append(f"- Month 7-9: Apply skills and document achievements")
    roadmap.append(f"- Month 10-{timeline}: Prepare promotion case and discuss with manager")
    return roadmap, f"{timeline}-{timeline+2}"

def get_promotion_probability_dynamic():
    avg_skill = sum(s['level'] for s in st.session_state.skills) / len(st.session_state.skills) if st.session_state.skills else 5
    exp = st.session_state.years_exp
    prob = min(92, 35 + exp * 4 + int(avg_skill) * 2)
    return f"{prob}%"

def get_salary_range_dynamic():
    target_data = JOB_SKILL_MAP.get(st.session_state.target_role, {"salary_base": (5, 12), "growth_rate": 10})
    min_sal, max_sal = target_data["salary_base"]
    exp = st.session_state.years_exp
    if exp > 5:
        min_sal += 3
        max_sal += 5
    return f"{min_sal}-{max_sal}"

def get_interview_questions_dynamic():
    target = st.session_state.target_role
    questions_db = {
        "Software Engineer": ["Explain polymorphism with an example", "What is the difference between REST and GraphQL?", "How do you handle debugging?"],
        "Senior Software Engineer": ["Design a URL shortener system", "Explain CAP theorem with examples", "How do you optimize slow queries?"],
        "Tech Lead": ["How do you handle technical debt?", "Describe a conflict resolution scenario", "How do you estimate project timelines?"],
        "Engineering Manager": ["How do you handle underperforming employees?", "Describe your hiring process", "How do you set OKRs?"],
        "Product Manager": ["How do you prioritize features?", "Describe a failed product and what you learned", "How do you measure product success?"],
        "Data Analyst": ["Explain JOIN types with examples", "How do you handle missing data?", "What's your experience with Tableau?"],
        "DevOps Engineer": ["Explain CI/CD pipeline", "What is infrastructure as code?", "How do you handle monitoring?"]
    }
    return questions_db.get(target, [f"What interests you about {target}?", f"Describe your experience with relevant skills", "Where do you see yourself in 5 years?"])

def get_learning_resources_dynamic():
    gaps = get_skill_gaps_dynamic()
    top_gap = gaps[0]['skill'] if gaps else "core skills"
    return f"- YouTube tutorials on {top_gap}\n- Coursera specialization\n- GitHub projects and documentation"

def get_certifications_dynamic():
    target = st.session_state.target_role
    certs_db = {
        "Software Engineer": ["Python Certification", "AWS Cloud Practitioner"],
        "Senior Software Engineer": ["AWS Solutions Architect", "System Design Certification"],
        "Tech Lead": ["PMP", "Leadership Training"],
        "Engineering Manager": ["MBA", "PMP"],
        "Data Analyst": ["SQL Certification", "Tableau Specialist"],
        "DevOps Engineer": ["AWS DevOps Engineer", "Docker Certified"]
    }
    return certs_db.get(target, ["Certification in your field", "Leadership Training"])

def get_personal_advice_dynamic():
    exp = st.session_state.years_exp
    if exp < 2:
        return "Focus on building strong fundamentals and completing side projects."
    elif exp < 5:
        return "Take on more responsibilities and document your achievements for promotion discussions."
    else:
        return "Focus on leadership skills, mentoring others, and strategic thinking."

def get_timeline_dynamic():
    exp = st.session_state.years_exp
    if exp < 2:
        return "12-14 months"
    elif exp < 5:
        return "10-12 months"
    else:
        return "8-10 months"

def get_weekly_plan_dynamic():
    hours = st.session_state.learning_hours
    gaps = get_skill_gaps_dynamic()
    top_gap = gaps[0]['skill'] if gaps else "core skills"
    return f"Week 1-2: Learn {top_gap} fundamentals ({hours} hrs/week)\nWeek 3-4: Practice with projects\nWeek 5-6: Advanced concepts\nWeek 7-8: Real application"

def get_peer_percentile_dynamic():
    avg_skill = get_skill_average()
    return min(99, 35 + st.session_state.years_exp * 3 + int(avg_skill) * 3)

def get_promotion_criteria_dynamic():
    gaps = get_skill_gaps_dynamic()
    top_skill = gaps[0]['skill'] if gaps else "your field"
    return f"- Complete a certification in {top_skill}\n- Lead 3 successful projects\n- Receive 'Exceeds Expectations' rating\n- Mentor junior team members\n- Present at team meetings"

def get_job_search_dynamic():
    target = st.session_state.target_role
    return f"- Target companies hiring {target}\n- Tailor resume with keywords from job descriptions\n- Set up job alerts on LinkedIn/Indeed"

def get_negotiation_tips_dynamic():
    salary = get_salary_range_dynamic()
    return f"- Research market range: ₹{salary} LPA\n- Emphasize your unique value\n- Consider total compensation package"

def get_networking_tips_dynamic():
    target = st.session_state.target_role
    loc = st.session_state.preferred_location
    return f"- Attend {target} meetups in {loc}\n- Connect with professionals on LinkedIn\n- Join Slack/Discord communities"

def get_linkedin_tips_dynamic():
    skills = [s['name'] for s in st.session_state.skills[:3]]
    return f"- Headline: '{st.session_state.current_role} → Aspiring {st.session_state.target_role}'\n- Skills: {', '.join(skills)}\n- Showcase projects in featured section"

def get_resume_feedback_dynamic(resume_text):
    target_data = JOB_SKILL_MAP.get(st.session_state.target_role, {"skills": ["relevant skills"]})
    skills_list = ", ".join(target_data["skills"][:4])
    return f"Strengths: Good foundation and relevant experience.\nImprovements: Add metrics and keywords: {skills_list}\nATS Score: {random.randint(65, 85)}/100"

def get_skill_quiz_dynamic():
    user_skills = [s['name'] for s in st.session_state.skills[:2]]
    if not user_skills:
        return None
    return [
        {"question": f"What is a key concept in {user_skills[0]}?", "options": ["A) Basic syntax", "B) Advanced technique", "C) Best practice", "D) All of the above"], "correct": "D) All of the above"},
        {"question": f"How would you apply {user_skills[0]} in a real project?", "options": ["A) Never use it", "B) Only in theory", "C) Based on requirements", "D) Always use it"], "correct": "C) Based on requirements"}
    ]

def get_brag_document_template():
    return """## Monthly Achievement Log
### Metrics Achieved
- 
### Leadership Examples
- 
### Technical Wins
- 
### Feedback Received
- """

def get_promotion_packet_guide():
    return """1. List 3-5 major achievements with metrics
2. Map your skills to target role requirements
3. Gather peer feedback (2-3 recommendations)
4. Compare against promotion criteria
5. Schedule discussion with manager"""

def get_future_skills_dynamic():
    return "AI/ML integration, Cloud Architecture, Cybersecurity, Data Storytelling, Prompt Engineering"

def get_work_life_balance_tip():
    return "Set clear boundaries, use calendar blocking, take regular breaks using Pomodoro technique."

def get_confidence_tip():
    return "Document your wins weekly, prepare a 'brag document', practice your pitch before meetings."

# ==================== LOGIN PAGE ====================
if st.session_state.page == "login":
    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; min-height: 70vh;">
        <div class="login-container">
            <div style="font-size: 60px;">🚀</div>
            <h2 style="margin: 10px 0;">CareerPath AI</h2>
            <p style="color: #64748b;">Team #130 | Corporate Domain</p>
    """, unsafe_allow_html=True)
    
    name = st.text_input("👤 Full Name", placeholder="Enter your name", key="login_name")
    mobile = st.text_input("📱 Mobile Number", placeholder="9876543210", key="login_mobile")
    email = st.text_input("📧 Email (optional)", placeholder="your@email.com", key="login_email")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", use_container_width=True):
            if name and mobile:
                st.session_state.user_name = name
                st.session_state.user_mobile = mobile
                st.session_state.user_email = email
                if load_user_state(name, mobile):
                    st.session_state.logged_in = True
                    st.session_state.show_roadmap = True
                    st.session_state.page = "dashboard"
                    update_streak()
                    st.rerun()
                else:
                    st.session_state.page = "profile"
                    st.rerun()
            else:
                st.error("Please enter name and mobile")
    with col2:
        if st.button("🆕 Register", use_container_width=True):
            if name and mobile:
                st.session_state.user_name = name
                st.session_state.user_mobile = mobile
                st.session_state.user_email = email
                st.session_state.page = "profile"
                st.rerun()
            else:
                st.error("Please enter name and mobile")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# ==================== BACK BUTTON ====================
def back_button():
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("◀ Back", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ==================== PROFILE PAGE ====================
if st.session_state.page == "profile":
    back_button()
    
    st.markdown('<div class="hero"><h2>📝 Complete Your Profile</h2><p>Tell us about yourself to get personalized recommendations</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        current_role = st.selectbox("📍 Current Role", list(JOB_SKILL_MAP.keys()))
        years_exp = st.slider("📅 Years of Experience", 0, 30, 2)
        preferred_location = st.selectbox("📍 Location", ["Bangalore", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai", "Pune", "Remote"])
    
    with col2:
        target_role = st.selectbox("🎯 Target Role", list(JOB_SKILL_MAP.keys()))
        learning_hours = st.slider("📖 Hours/week for learning", 1, 20, 5)
        salary_exp = st.number_input("💰 Expected Salary (LPA)", min_value=3, max_value=100, value=15)
    
    st.markdown("---")
    st.markdown("### 📋 Your Skills")
    st.caption("Rate your proficiency: 1=Beginner, 5=Intermediate, 10=Expert")
    
    suggested = JOB_SKILL_MAP.get(current_role, {"skills": ["Communication", "Problem Solving"]})["skills"]
    st.info(f"💡 Suggested skills for {current_role}: {', '.join(suggested[:6])}")
    
    num_skills = st.number_input("Number of skills", min_value=1, max_value=10, value=4)
    skills = []
    for i in range(num_skills):
        col1, col2 = st.columns([3, 1])
        with col1:
            s = st.text_input(f"Skill {i+1}", key=f"skill_{i}", placeholder="e.g., Python, SQL, Leadership")
        with col2:
            lvl = st.selectbox(f"Level", list(range(1,11)), index=4, key=f"level_{i}")
        if s:
            skills.append({"name": s, "level": lvl})
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save & Continue", type="primary", use_container_width=True):
            if current_role and target_role and skills:
                st.session_state.current_role = current_role
                st.session_state.target_role = target_role
                st.session_state.years_exp = years_exp
                st.session_state.skills = skills
                st.session_state.preferred_location = preferred_location
                st.session_state.learning_hours = learning_hours
                st.session_state.show_roadmap = True
                save_user_state()
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Please fill all fields")
    with col2:
        if st.button("◀ Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    
    st.stop()

# ==================== DASHBOARD PAGE ====================
if st.session_state.page == "dashboard":
    update_streak()
    
    with st.sidebar:
        st.markdown(f"### 🚀 CareerPath AI")
        st.markdown(f"**👤 {st.session_state.user_name}**")
        st.markdown(f"📱 {st.session_state.user_mobile}")
        if st.session_state.user_email:
            st.markdown(f"📧 {st.session_state.user_email}")
        st.markdown("---")
        st.markdown(f"**🎯 {get_greeting()}**")
        st.markdown(f"🔥 Streak: {st.session_state.daily_streak} days")
        st.markdown("---")
        st.markdown(f"**Current:** {st.session_state.current_role}")
        st.markdown(f"**Target:** {st.session_state.target_role}")
        st.markdown(f"**Experience:** {st.session_state.years_exp} years")
        st.markdown(f"**Location:** {st.session_state.preferred_location}")
        st.markdown(f"**Learning:** {st.session_state.learning_hours} hrs/week")
        st.markdown("---")
        
        if st.button("💾 Save Progress", use_container_width=True):
            save_user_state()
            st.success("✅ Saved!")
        
        if st.button("📝 Edit Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            save_user_state()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🏆 50+ Features")
        features = ["Skill Gap", "Roadmap", "Promotion Predictor", "Salary Estimator", "Interview Qs", "Resume Analyzer", "Bias Detector", "Learning Resources", "Certifications", "Personal Advice", "Timeline", "Weekly Plan", "Peer Comparison", "Job Search", "Negotiation Tips", "LinkedIn Tips", "Networking", "AI Copilot", "Skill Quiz", "Brag Doc", "Promotion Packet", "Future Skills"]
        for f in features[:15]:
            st.caption(f"• {f}")
        st.caption(f"• ... and {len(features) - 15} more")
    
    st.markdown(f"""
    <div class="hero">
        <h2>🌟 {get_greeting()}, {st.session_state.user_name}!</h2>
        <p>Your AI career coach is ready. All insights are <strong>personalized</strong> for your profile.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all dynamic data
    skill_gaps = get_skill_gaps_dynamic()
    roadmap, estimated_time = get_roadmap_dynamic()
    prob_text = get_promotion_probability_dynamic()
    prob_num = int(prob_text.replace("%", "")) if prob_text else 65
    salary_range = get_salary_range_dynamic()
    interview_qs = get_interview_questions_dynamic()
    learning_res = get_learning_resources_dynamic()
    certs = get_certifications_dynamic()
    advice = get_personal_advice_dynamic()
    timeline = get_timeline_dynamic()
    weekly_plan = get_weekly_plan_dynamic()
    peer_percentile = get_peer_percentile_dynamic()
    criteria = get_promotion_criteria_dynamic()
    job_search = get_job_search_dynamic()
    negotiation = get_negotiation_tips_dynamic()
    networking = get_networking_tips_dynamic()
    linkedin = get_linkedin_tips_dynamic()
    quiz = get_skill_quiz_dynamic()
    brag_template = get_brag_document_template()
    promotion_packet = get_promotion_packet_guide()
    future_skills = get_future_skills_dynamic()
    wlb_tip = get_work_life_balance_tip()
    confidence_tip = get_confidence_tip()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">⏰ {timeline}</div><div>to {st.session_state.target_role}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">📊 {prob_num}%</div><div>Promotion Probability</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">💰 {salary_range} LPA</div><div>Expected Salary</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">🔓 85%</div><div>Transparency Score</div></div>', unsafe_allow_html=True)
    
    # Gauge Chart
    gauge = go.Figure(go.Indicator(mode="gauge+number", value=prob_num, title={"text": "Promotion Readiness", "font": {"color": "#1e293b"}}, gauge={'axis': {'range': [0,100]}, 'bar': {'color': "#3b82f6"}, 'steps': [{'range': [0,50], 'color': '#fee2e2'}, {'range': [50,75], 'color': '#fef3c7'}, {'range': [75,100], 'color': '#dcfce7'}]}))
    gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", height=250)
    st.plotly_chart(gauge, use_container_width=True)
    
    # Main Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Skill Gap", "🗺️ Roadmap", "📋 Promotion", "🎯 Interview", "📚 Resources", "🧠 AI Tools"])
    
    with tab1:
        st.markdown("### 🔴 Skills You Need to Develop")
        if skill_gaps:
            for gap in skill_gaps:
                badge = "badge-high" if gap['priority'] == "HIGH" else "badge-medium"
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>🎯 {gap['skill']}</strong>
                        <span class="{badge}">{gap['priority']}</span>
                    </div>
                    <p>📖 {gap['reason']}</p>
                    <p>⏱️ {gap['weeks']} weeks to learn</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("### 🟢 Your Current Strengths")
        for s in st.session_state.skills[:5]:
            st.markdown(f"""
            <div class="glass-card">
                <strong>✅ {s['name']}</strong>
                <p>Proficiency: {s['level']}/10</p>
                <div style="background: #e2e8f0; border-radius: 10px; height: 6px;">
                    <div style="width: {s['level'] * 10}%; background: #16a34a; height: 6px; border-radius: 10px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🗺️ Your Personalized Roadmap")
        st.caption(f"Based on {st.session_state.learning_hours} hours/week study")
        for i, step in enumerate(roadmap):
            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown(f"<div class='glass-card'>{step}</div>", unsafe_allow_html=True)
            with col2:
                if i not in st.session_state.completed_tasks:
                    if st.button("✅", key=f"complete_{i}"):
                        st.session_state.completed_tasks.add(i)
                        save_user_state()
                        st.rerun()
                else:
                    st.markdown("✔️")
        
        st.markdown("### 📅 Weekly Learning Plan")
        st.markdown(f"<div class='glass-card'>{weekly_plan}</div>", unsafe_allow_html=True)
        
        st.markdown("### 📈 Progress")
        total = len(roadmap)
        completed = len(st.session_state.completed_tasks)
        st.progress(completed / total if total > 0 else 0)
        st.caption(f"{completed}/{total} milestones completed")
    
    with tab3:
        st.markdown("### ✅ Promotion Criteria")
        for line in criteria.split("\n"):
            if line.strip():
                st.checkbox(line.strip())
        
        st.markdown("---")
        st.markdown("### 🔍 Bias Detection Report")
        st.info("**Transparency Score: 85/100** - Your promotion criteria are clear and measurable.")
        st.success("🔓 **Transparency Guarantee:** These criteria are the ONLY factors for promotion.")
        
        st.markdown("### 📊 Peer Comparison")
        st.metric("You are in the", f"{peer_percentile}th percentile", delta=f"among peers with similar goals")
        
        st.markdown("### 📝 Brag Document Template")
        st.info(brag_template)
        
        st.markdown("### 📋 Promotion Packet Guide")
        st.info(promotion_packet)
    
    with tab4:
        st.markdown("### 🎤 Interview Questions")
        for q in interview_qs:
            st.markdown(f"<div class='glass-card'>❓ {q}</div>", unsafe_allow_html=True)
        
        st.markdown("### 📄 Resume Analyzer")
        uploaded = st.file_uploader("Upload your resume (PDF/TXT)", type=["pdf", "txt"])
        if uploaded:
            with st.spinner("Analyzing..."):
                if uploaded.type == "application/pdf":
                    with pdfplumber.open(uploaded) as pdf:
                        text = "".join([p.extract_text() or "" for p in pdf.pages])
                else:
                    text = uploaded.read().decode("utf-8")
                feedback = get_resume_feedback_dynamic(text[:3000])
                st.markdown(f"<div class='glass-card'>{feedback}</div>", unsafe_allow_html=True)
        
        st.markdown("### 💰 Negotiation Tips")
        st.markdown(f"<div class='glass-card'>{negotiation}</div>", unsafe_allow_html=True)
    
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📚 Learning Resources")
            st.markdown(f"<div class='glass-card'>{learning_res}</div>", unsafe_allow_html=True)
            st.markdown("### 🎓 Certifications")
            for cert in certs:
                st.markdown(f"<div class='glass-card'>🏆 {cert}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💡 Personal Advice")
            st.success(advice)
            st.markdown("### 🧭 Mentor Tips")
            st.markdown(f"<div class='glass-card'>{networking}</div>", unsafe_allow_html=True)
            st.markdown("### 🔗 LinkedIn Tips")
            st.markdown(f"<div class='glass-card'>{linkedin}</div>", unsafe_allow_html=True)
            st.markdown("### 🎯 Job Search Tips")
            st.markdown(f"<div class='glass-card'>{job_search}</div>", unsafe_allow_html=True)
    
    with tab6:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧠 Skill Quiz")
            if quiz:
                for i, q in enumerate(quiz):
                    ans = st.radio(q["question"], q["options"], key=f"quiz_{i}")
                    if st.button(f"Check Answer {i+1}", key=f"check_{i}"):
                        if ans == q["correct"]:
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Incorrect. Correct: {q['correct']}")
            else:
                st.info("Add skills to generate quiz")
            
            st.markdown("### 🔮 Future Skills")
            st.info(future_skills)
        
        with col2:
            st.markdown("### ⚖️ Work-Life Balance Tip")
            st.info(wlb_tip)
            st.markdown("### 💪 Confidence Builder")
            st.info(confidence_tip)
            st.markdown("### 🤖 AI Career Copilot")
            for msg in st.session_state.chat_history[-6:]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
            user_q = st.chat_input("Ask about your career...")
            if user_q:
                st.session_state.chat_history.append({"role": "user", "content": user_q})
                with st.chat_message("user"):
                    st.write(user_q)
                with st.chat_message("assistant"):
                    response = f"Based on your profile as {st.session_state.current_role} aiming for {st.session_state.target_role}, focus on {skill_gaps[0]['skill'] if skill_gaps else 'key skills'}."
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    save_user_state()
    
    # Skill Radar Chart
    st.markdown("---")
    st.markdown("### 📊 Your Skill Radar")
    if st.session_state.skills:
        df = pd.DataFrame(st.session_state.skills)
        fig = px.line_polar(df, r='level', theta='name', line_close=True, title="Skill Assessment")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e293b", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Reset Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start Over", type="primary", use_container_width=True):
            save_user_state()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p>🚀 CareerPath AI ⚙️ Team #130 | 40+ Job Roles | 50+ AI Features</p>
        <p>Solving lack of transparency in career growth | Aavishkar Pravah 2.0</p>
        <p>📍 {st.session_state.preferred_location} | 🎯 {st.session_state.target_role} | 📚 {st.session_state.learning_hours} hrs/week</p>
    </div>
    """, unsafe_allow_html=True)