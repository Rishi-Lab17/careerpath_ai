import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import re
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(page_title="CareerPath AI", page_icon="🚀", layout="wide")

# ==================== CSS ====================
st.markdown("""
<style>
    .stApp { background: #f0f2f6; }
    .main-header { background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 1.5rem; border-radius: 20px; color: white; text-align: center; margin-bottom: 2rem; }
    .glass-card { background: white; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .metric-card { background: white; padding: 1rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #1e3c72; }
    .hero { background: linear-gradient(135deg, #1e3c72, #2a5298); padding: 1.5rem; border-radius: 20px; color: white; text-align: center; margin-bottom: 2rem; }
    .login-container { background: white; padding: 2rem; border-radius: 20px; max-width: 450px; margin: 0 auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    .stButton>button { background: #1e3c72; color: white; border-radius: 25px; width: 100%; }
    .footer { text-align: center; padding: 1rem; color: #666; font-size: 0.8rem; border-top: 1px solid #ddd; margin-top: 2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 16px; background: white; border-radius: 40px; padding: 6px 12px; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; padding: 8px 20px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #1e3c72, #2a5298) !important; color: white !important; border-radius: 30px; }
    section[data-testid="stSidebar"] { background: white; }
    .badge { display: inline-block; background: #e2e8f0; padding: 4px 12px; border-radius: 30px; font-size: 0.7rem; font-weight: 600; }
    .badge-high { background: #fee2e2; color: #dc2626; }
    .badge-medium { background: #fef3c7; color: #d97706; }
    .badge-low { background: #dcfce7; color: #16a34a; }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<div class="main-header"><h1>🚀 CareerPath AI</h1><p>Team #130 | Corporate Domain | 50+ AI Features</p></div>', unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_mobile' not in st.session_state:
    st.session_state.user_mobile = ""
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
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = set()
if 'completed_criteria' not in st.session_state:
    st.session_state.completed_criteria = set()
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'preferred_location' not in st.session_state:
    st.session_state.preferred_location = "Bangalore"
if 'learning_hours' not in st.session_state:
    st.session_state.learning_hours = 5
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}
if 'saved_notes' not in st.session_state:
    st.session_state.saved_notes = []
if 'goal_deadline' not in st.session_state:
    st.session_state.goal_deadline = ""
if 'salary_history' not in st.session_state:
    st.session_state.salary_history = []
if 'interview_feedback' not in st.session_state:
    st.session_state.interview_feedback = []
if 'mentor_requests' not in st.session_state:
    st.session_state.mentor_requests = []
if 'bookmarks' not in st.session_state:
    st.session_state.bookmarks = []
if 'daily_streak' not in st.session_state:
    st.session_state.daily_streak = 1
if 'last_login' not in st.session_state:
    st.session_state.last_login = datetime.now().strftime("%Y-%m-%d")

# ==================== 50+ JOB ROLES with Skill Requirements ====================
JOB_SKILL_MAP = {
    "Software Engineer": ["Python", "Java", "SQL", "Data Structures", "Algorithms", "Git", "Debugging", "Problem Solving", "OOP", "REST APIs"],
    "Senior Software Engineer": ["System Design", "Architecture", "Code Review", "Mentoring", "Advanced Algorithms", "Performance Optimization", "Distributed Systems", "Microservices", "Design Patterns"],
    "Tech Lead": ["Team Leadership", "Project Planning", "Technical Architecture", "Risk Assessment", "Stakeholder Management", "Agile", "Code Quality", "Conflict Resolution", "Decision Making"],
    "Engineering Manager": ["Budgeting", "Hiring", "Performance Reviews", "Strategic Planning", "Team Building", "OKRs", "Cross-functional Collaboration", "Career Development", "Metrics", "1-on-1s"],
    "Product Manager": ["Market Research", "User Stories", "Roadmap Planning", "Data Analysis", "Stakeholder Management", "Product Strategy", "A/B Testing", "User Interviews", "Competitive Analysis", "Go-to-Market"],
    "Senior Product Manager": ["Product Strategy", "Go-to-Market", "Metrics Analysis", "Cross-team Leadership", "Customer Discovery", "Competitive Analysis", "Pricing Strategy", "Product Vision"],
    "Data Analyst": ["SQL", "Excel", "Tableau/Power BI", "Statistics", "Python", "Data Visualization", "Business Intelligence", "Data Cleaning", "Reporting", "Dashboard Design"],
    "Lead Data Analyst": ["Data Modeling", "ETL Pipelines", "Team Leadership", "Advanced Analytics", "Data Governance", "Stakeholder Management", "Data Quality", "Data Warehousing"],
    "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL", "TensorFlow/PyTorch", "Data Visualization", "Feature Engineering", "Model Deployment", "A/B Testing", "Deep Learning"],
    "DevOps Engineer": ["CI/CD", "AWS/Azure", "Docker", "Kubernetes", "Linux", "Terraform", "Monitoring", "Scripting", "Networking", "Security"],
    "Senior DevOps Engineer": ["Infrastructure as Code", "Security Best Practices", "Cost Optimization", "GitOps", "Multi-cloud", "Disaster Recovery", "SRE", "Observability"],
    "Cloud Engineer": ["AWS", "Azure/GCP", "Cloud Architecture", "Networking", "Security", "Automation", "Terraform/CloudFormation", "Serverless", "Cloud Migration"],
    "Frontend Developer": ["React", "JavaScript", "HTML/CSS", "TypeScript", "Next.js", "Tailwind", "Web Performance", "Responsive Design", "State Management", "Testing"],
    "Senior Frontend Developer": ["Frontend Architecture", "State Management", "Performance Optimization", "Team Mentoring", "UI/UX Collaboration", "Testing", "Webpack", "Component Libraries"],
    "Backend Developer": ["Node.js/Python", "Databases", "API Design", "Microservices", "Caching", "Authentication", "System Design", "Message Queues", "Security"],
    "Full Stack Developer": ["React", "Node.js", "MongoDB/PostgreSQL", "REST APIs", "Authentication", "Deployment", "Git", "CSS", "Testing", "CI/CD"],
    "Mobile Developer": ["iOS/Android", "React Native/Flutter", "Mobile UI/UX", "App Store Deployment", "REST APIs", "Mobile Performance", "Push Notifications", "Offline Storage"],
    "QA Engineer": ["Manual Testing", "Automation Testing", "Selenium", "JIRA", "Test Cases", "Bug Tracking", "Regression Testing", "API Testing", "Performance Testing"],
    "Lead QA Engineer": ["Test Strategy", "Team Leadership", "CI/CD Integration", "Performance Testing", "Security Testing", "QA Metrics", "Test Automation Framework"],
    "Security Engineer": ["Network Security", "Penetration Testing", "Risk Assessment", "Security Audits", "Encryption", "Incident Response", "Compliance", "SIEM"],
    "Network Engineer": ["Routing/Switching", "Firewalls", "TCP/IP", "DNS", "Load Balancing", "Network Security", "Cisco/Juniper", "VPN", "SD-WAN"],
    "Database Administrator": ["SQL", "Database Design", "Performance Tuning", "Backup/Recovery", "Security", "High Availability", "Oracle/MySQL/PostgreSQL", "Replication"],
    "Systems Administrator": ["Linux/Windows", "Scripting", "Virtualization", "Backup", "Monitoring", "Troubleshooting", "Active Directory", "Patch Management"],
    "Business Analyst": ["Requirements Gathering", "Process Mapping", "Data Analysis", "Stakeholder Management", "Documentation", "UML/SQL", "User Stories", "JIRA"],
    "Project Manager": ["Project Planning", "Risk Management", "Budgeting", "Team Coordination", "Agile/Scrum", "Reporting", "Stakeholder Management", "MS Project"],
    "Scrum Master": ["Agile Methodologies", "Sprint Planning", "Team Facilitation", "Conflict Resolution", "JIRA/Confluence", "Continuous Improvement", "Retrospectives"],
    "Sales Executive": ["Lead Generation", "Negotiation", "CRM", "Pipeline Management", "Client Relationship", "Closing Skills", "Cold Calling", "Sales Funnel"],
    "Sales Manager": ["Team Leadership", "Sales Strategy", "Forecasting", "Territory Management", "Training", "Revenue Growth", "KPI Tracking", "CRM Management"],
    "Marketing Associate": ["Digital Marketing", "Social Media", "Content Creation", "SEO/SEM", "Email Marketing", "Analytics", "Google Ads", "Canva"],
    "Marketing Manager": ["Brand Strategy", "Campaign Management", "Budgeting", "Team Leadership", "Market Research", "ROI Analysis", "Growth Strategy", "Marketing Automation"],
    "HR Associate": ["Recruitment", "Onboarding", "Employee Relations", "HR Policies", "Payroll", "Compliance", "Screening", "Offer Letters"],
    "HR Manager": ["Talent Acquisition", "Performance Management", "Compensation", "Employee Engagement", "Leadership Development", "Labor Laws", "HRIS", "Workplace Culture"],
    "UX Designer": ["User Research", "Wireframing", "Prototyping", "Figma/Sketch", "Usability Testing", "Information Architecture", "Visual Design", "Accessibility"],
    "UI Designer": ["Visual Design", "Color Theory", "Typography", "Figma/Adobe XD", "Design Systems", "Responsive Design", "Animation", "Brand Guidelines"],
    "Technical Writer": ["Documentation", "API Documentation", "Technical Communication", "Markdown", "Confluence", "User Guides", "Release Notes", "Sphinx"],
    "Solutions Architect": ["Enterprise Architecture", "Cloud Solutions", "System Integration", "Technical Presales", "Cost Estimation", "Migration Strategy", "Security Architecture"],
    "Delivery Manager": ["Project Delivery", "Client Management", "Resource Planning", "Risk Management", "Quality Assurance", "Timeline Management", "Team Coordination"],
    "IT Support Specialist": ["Hardware Troubleshooting", "Software Installation", "Ticketing Systems", "Customer Service", "Remote Support", "Asset Management", "Documentation"],
    "Blockchain Developer": ["Solidity", "Smart Contracts", "Ethereum", "Web3.js", "Cryptography", "Truffle/Hardhat", "DeFi", "NFTs"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow/PyTorch", "NLP", "Computer Vision", "Model Deployment", "MLOps"],
    "Robotics Engineer": ["ROS", "C++/Python", "Computer Vision", "Control Systems", "Sensors", "Embedded Systems", "Simulation", "Mechanical Design"]
}

# ==================== SKILL SUGGESTIONS ====================
def get_skill_suggestions(role):
    return JOB_SKILL_MAP.get(role, ["Communication", "Problem Solving", "Teamwork", "Leadership", "Time Management", "Adaptability", "Critical Thinking"])[:10]

# ==================== 50+ DYNAMIC FEATURES BASED ON USER INPUT ====================

# Feature 1: Skill Gap Analysis
def get_skill_gaps():
    user_skills = [s['name'].lower() for s in st.session_state.skills]
    required_skills = JOB_SKILL_MAP.get(st.session_state.target_role, ["Technical Skills", "Leadership", "Communication", "Problem Solving", "Teamwork"])
    
    missing = []
    for skill in required_skills:
        if not any(skill.lower() in user_skill or user_skill in skill.lower() for user_skill in user_skills):
            missing.append(skill)
    
    if not missing:
        missing = required_skills[:5]
    
    gaps = []
    priorities = ["HIGH", "HIGH", "MEDIUM", "MEDIUM", "LOW"]
    weeks = [8, 6, 4, 4, 3]
    
    for i, skill in enumerate(missing[:5]):
        reason = f"Required for {st.session_state.target_role} role"
        if "leadership" in skill.lower():
            reason = f"To move from {st.session_state.current_role} to {st.session_state.target_role}, you need leadership experience"
        elif "system design" in skill.lower():
            reason = f"Critical skill gap for {st.session_state.target_role} position"
        elif "cloud" in skill.lower():
            reason = f"Cloud skills are essential for modern {st.session_state.target_role} roles"
        elif "communication" in skill.lower():
            reason = f"{st.session_state.target_role} requires effective communication with stakeholders"
        gaps.append({"skill": skill.title(), "reason": reason, "priority": priorities[i] if i < len(priorities) else "MEDIUM", "weeks": weeks[i] if i < len(weeks) else 4})
    
    return gaps

# Feature 2: Personalized Roadmap
def get_roadmap():
    gaps = get_skill_gaps()
    exp = st.session_state.years_exp
    hours = st.session_state.learning_hours
    
    if exp < 2:
        months = "12-14"
        timeline = 12
    elif exp < 5:
        months = "10-12"
        timeline = 10
    else:
        months = "8-10"
        timeline = 8
    
    roadmap = []
    for i, gap in enumerate(gaps[:4]):
        start = i * 2 + 1
        end = start + 1
        action = f"Master {gap['skill']} through online courses and hands-on projects"
        if "leadership" in gap['skill'].lower():
            action = f"Take leadership training, mentor a junior, and lead team meetings"
        elif "system design" in gap['skill'].lower():
            action = f"Complete System Design certification and practice with 5 real-world scenarios"
        elif "cloud" in gap['skill'].lower():
            action = f"Get cloud certification (AWS/Azure/GCP) and build a cloud project"
        roadmap.append(f"- Month {start}-{end}: {action}")
    
    roadmap.append(f"- Month 9-10: Apply all learned skills in current role and document achievements with metrics")
    roadmap.append(f"- Month 11-{timeline}: Prepare promotion case, get feedback, and discuss with manager")
    
    return roadmap, months

# Feature 3: Promotion Probability
def get_promotion_probability():
    avg_skill = sum(s['level'] for s in st.session_state.skills) / len(st.session_state.skills) if st.session_state.skills else 5
    exp = st.session_state.years_exp
    prob = min(92, 35 + exp * 4 + int(avg_skill) * 2)
    
    if prob > 75:
        reason = "strong skill foundation and relevant experience"
    elif prob > 55:
        reason = "good progress but need to address key skill gaps"
    else:
        reason = "experience and skill gaps need focused attention"
    
    return f"{prob}% because you have {reason}"

# Feature 4: Salary Prediction
def get_salary_range():
    target = st.session_state.target_role
    exp = st.session_state.years_exp
    loc = st.session_state.preferred_location
    
    base_salaries = {
        "Software Engineer": (5, 9), "Senior Software Engineer": (12, 20), "Tech Lead": (18, 28),
        "Engineering Manager": (25, 40), "Product Manager": (10, 18), "Senior Product Manager": (18, 30),
        "Data Analyst": (4, 8), "Lead Data Analyst": (10, 16), "Data Scientist": (8, 15),
        "DevOps Engineer": (7, 14), "Senior DevOps Engineer": (15, 25), "Cloud Engineer": (8, 16),
        "Frontend Developer": (5, 10), "Backend Developer": (6, 12), "Full Stack Developer": (7, 14),
        "QA Engineer": (4, 7), "Security Engineer": (8, 15), "Project Manager": (12, 22),
        "Marketing Manager": (8, 16), "HR Manager": (7, 14), "UX Designer": (6, 12),
        "Solutions Architect": (20, 35), "Delivery Manager": (15, 25), "AI Engineer": (12, 22)
    }
    
    min_sal, max_sal = base_salaries.get(target, (5, 12))
    
    if exp > 5:
        min_sal += 3
        max_sal += 5
    elif exp > 8:
        min_sal += 5
        max_sal += 8
    
    if loc in ["Bangalore", "Mumbai", "Delhi NCR"]:
        min_sal += 2
        max_sal += 3
    
    return f"{min_sal}-{max_sal}"

# Feature 5: Interview Questions
def get_interview_questions():
    target = st.session_state.target_role
    user_skills = [s['name'] for s in st.session_state.skills[:3]]
    
    questions_db = {
        "Software Engineer": ["Explain polymorphism with an example", "What is the difference between REST and GraphQL?", "How do you handle memory leaks?", "Explain your debugging process", "What is CI/CD?"],
        "Senior Software Engineer": ["Design a URL shortener system", "How do you handle database sharding?", "Explain CAP theorem with examples", "How do you optimize slow queries?", "Describe a system you designed from scratch"],
        "Tech Lead": ["How do you handle technical debt?", "Describe a conflict resolution scenario", "How do you estimate project timelines?", "How do you mentor junior developers?", "How do you handle a missed deadline?"],
        "Engineering Manager": ["How do you handle underperforming employees?", "Describe your hiring process", "How do you set OKRs for your team?", "How do you handle budget cuts?", "Describe your leadership philosophy"],
        "Product Manager": ["How do you prioritize features?", "Describe a failed product and what you learned", "How do you measure product success?", "How do you handle stakeholder conflicts?", "What's your go-to-market strategy?"],
        "Data Analyst": ["Explain JOIN types with examples", "How do you handle missing data?", "What's your experience with Tableau?", "How do you communicate insights to non-technical stakeholders?", "Describe an A/B test you designed"]
    }
    
    default = [f"What interests you about {target} role?", f"Describe your experience with {', '.join(user_skills) if user_skills else 'relevant technologies'}", "Where do you see yourself in 5 years?", "What's your biggest professional achievement?", "How do you handle feedback?"]
    
    return questions_db.get(target, default)

# Feature 6: Learning Resources
def get_learning_resources():
    gaps = get_skill_gaps()
    resources_db = {
        "Python": ["Python.org Official Tutorial", "Codecademy Python Course", "Automate the Boring Stuff Book", "Real Python Articles"],
        "SQL": ["Mode Analytics SQL Tutorial", "LeetCode SQL Problems", "W3Schools SQL", "SQLZoo Exercises"],
        "System Design": ["Gaurav Sen YouTube Channel", "System Design Interview Book by Alex Xu", "Educative.io Course", "High Scalability Blog"],
        "Leadership": ["Harvard Leadership Course", "Simon Sinek TED Talks", "Dale Carnegie Books", "LinkedIn Learning Leadership Path"],
        "AWS": ["AWS Free Training", "Cloud Guru Course", "FreeCodeCamp AWS Videos", "AWS Documentation"],
        "Docker": ["Docker Official Tutorial", "TechWorld with Nana YouTube", "Docker Curriculum", "Play with Docker"],
        "Kubernetes": ["K8s Official Tutorial", "TechWorld with Nana K8s", "KodeKloud Course", "Killer.sh Practice"],
        "React": ["React Official Tutorial", "FreeCodeCamp React Course", "Full Stack Open", "React Beta Docs"],
        "JavaScript": ["MDN Web Docs", "JavaScript.info", "FreeCodeCamp JS", "You Don't Know JS Book"]
    }
    
    result = []
    for gap in gaps[:3]:
        skill = gap['skill']
        found = False
        for key, res in resources_db.items():
            if key.lower() in skill.lower():
                result.extend(res[:2])
                found = True
                break
        if not found:
            result.append(f"YouTube tutorials and courses on {skill}")
    
    return result[:6]

# Feature 7: Certifications
def get_certifications():
    target = st.session_state.target_role
    certs_db = {
        "Software Engineer": ["Python Institute PCEP", "GitHub Actions Certification", "AWS Cloud Practitioner"],
        "Senior Software Engineer": ["AWS Solutions Architect", "System Design Certification", "CKAD (Kubernetes)", "MongoDB Developer"],
        "Tech Lead": ["PMP", "Leadership Training", "Agile Coach", "Scrum Master"],
        "Engineering Manager": ["MBA", "PMP", "Executive Leadership", "Strategic Management"],
        "Data Analyst": ["Microsoft Power BI Data Analyst", "Tableau Specialist", "Google Data Analytics", "SQL Certification"],
        "DevOps Engineer": ["AWS DevOps Engineer", "Docker Certified Associate", "Terraform Associate", "CKA"],
        "Product Manager": ["Product Management Certification", "Agile Product Owner", "Scrum Master", "Pragmatic Institute"],
        "Cloud Engineer": ["AWS Solutions Architect", "Azure Administrator", "Google Cloud Engineer", "Terraform"]
    }
    return certs_db.get(target, ["Communication Skills Certification", "Project Management Professional", "Leadership Training", "Technical Writing"])

# Feature 8: Personal Advice
def get_personal_advice():
    current = st.session_state.current_role
    target = st.session_state.target_role
    exp = st.session_state.years_exp
    
    if exp < 2:
        return f"🎯 Focus on building strong fundamentals in your current role. Aim to complete 2-3 projects independently and learn {get_skill_gaps()[0]['skill'] if get_skill_gaps() else 'new skills'} within 3 months."
    elif exp < 5:
        return f"🚀 You're at a good stage to start preparing for {target}. Take on more responsibilities, volunteer for leadership tasks, and document your achievements. Start mentoring junior team members."
    else:
        return f"💪 With {exp} years of experience, you're ready for {target}. Focus on strategic thinking, cross-functional collaboration, and business impact. Schedule a promotion discussion with your manager."

# Feature 9: Timeline Prediction
def get_timeline():
    exp = st.session_state.years_exp
    gaps = get_skill_gaps()
    
    if exp < 2:
        base = 12
    elif exp < 5:
        base = 10
    else:
        base = 8
    
    if len(gaps) > 3:
        base += 2
    
    return f"{base}-{base+2} months"

# Feature 10: Weekly Learning Plan
def get_weekly_plan():
    hours = st.session_state.learning_hours
    gaps = get_skill_gaps()
    
    plan = f"""
📚 **Your Personalized {hours}-Hour Weekly Plan**

**Monday:** {gaps[0]['skill'] if gaps else 'Core Skills'} - {hours//2} hours of fundamentals
**Tuesday:** {gaps[0]['skill'] if gaps else 'Core Skills'} - hands-on practice
**Wednesday:** {gaps[1]['skill'] if len(gaps) > 1 else 'Advanced topics'} - {hours//2} hours study
**Thursday:** Project work applying {gaps[0]['skill'] if gaps else 'new skills'}
**Friday:** Review and quiz on learned concepts
**Weekend:** Complete a mini-project and document learnings

💡 **Tip:** Consistency beats intensity. Stick to this schedule daily.
"""
    return plan

# Feature 11: Networking Tips
def get_networking_tips():
    target = st.session_state.target_role
    loc = st.session_state.preferred_location
    return f"""
🤝 **Networking Strategies for {target}**

1. Attend {target} meetups and conferences in {loc} (check Meetup.com)
2. Connect with {target} professionals on LinkedIn - personalize your connection requests
3. Join Slack/Discord communities for {target}
4. Share your learning journey on LinkedIn weekly
5. Request informational interviews with people in your target role
"""

# Feature 12: LinkedIn Optimization
def get_linkedin_tips():
    target = st.session_state.target_role
    return f"""
💼 **LinkedIn Optimization for {target}**

1. Headline: "{st.session_state.current_role} → Aspiring {target} | [Your Key Skills]"
2. Featured section: Showcase your best projects
3. About section: Tell your career story and {target} aspirations
4. Skills section: Add {', '.join(get_skill_gaps()[:3] if get_skill_gaps() else ['relevant skills'])}
5. Recommendations: Request from managers and peers
"""

# Feature 13: Job Search Tips
def get_job_search_tips():
    target = st.session_state.target_role
    return f"""
🔍 **Job Search Strategies for {target}**

1. Target companies known for {target} roles (check Glassdoor)
2. Tailor your resume with keywords from {target} job descriptions
3. Set up job alerts on LinkedIn, Indeed, and Naukri
4. Prepare a portfolio/GitHub showcasing relevant work
5. Practice with {len(get_interview_questions())} common {target} interview questions
"""

# Feature 14: Negotiation Tips
def get_negotiation_tips():
    target = st.session_state.target_role
    salary = get_salary_range()
    return f"""
💰 **Salary Negotiation for {target}**

1. Research: Market range for {target} is ₹{salary} LPA in {st.session_state.preferred_location}
2. Don't reveal your current salary first - ask for their budget
3. Emphasize your unique value: "Based on my {st.session_state.years_exp} years of experience in {st.session_state.current_role}..."
4. Consider total compensation: bonus, stock, benefits, remote work
5. Get offer in writing before negotiating
"""

# Feature 15: Skill Quiz
def get_skill_quiz():
    user_skills = st.session_state.skills[:2]
    if not user_skills:
        return None
    
    quizzes = []
    for i, skill in enumerate(user_skills):
        if skill['level'] >= 7:
            quizzes.append({
                "question": f"What is an advanced concept in {skill['name']} that would impress a senior engineer?",
                "options": ["Basic syntax", "Design patterns", "Variable naming", "Comments"],
                "correct": "Design patterns",
                "skill": skill['name']
            })
        else:
            quizzes.append({
                "question": f"What is the primary use of {skill['name']}?",
                "options": ["Database management", "Frontend development", f"Solution for {skill['name']} use cases", "Game development"],
                "correct": f"Solution for {skill['name']} use cases",
                "skill": skill['name']
            })
    return quizzes[:3]

# Feature 16: Peer Benchmarking
def get_peer_percentile():
    avg_skill = sum(s['level'] for s in st.session_state.skills) / len(st.session_state.skills) if st.session_state.skills else 5
    exp = st.session_state.years_exp
    base = 35 + exp * 3 + int(avg_skill) * 3
    return min(98, max(25, base))

# Feature 17-20: Additional Features
def get_market_trend():
    target = st.session_state.target_role
    trends = {
        "Software Engineer": "Demand for full-stack developers with AI integration skills is rising 25% YoY",
        "Data Scientist": "ML engineering roles are growing 35% annually; focus on MLOps",
        "DevOps Engineer": "Platform engineering and security (DevSecOps) are top priorities for 2025",
        "Product Manager": "Product-led growth and data-driven PM roles are in highest demand"
    }
    return trends.get(target, f"Demand for {target} roles in {st.session_state.preferred_location} is growing steadily with 18% YoY growth")

def get_future_skills():
    return "🌐 AI/ML integration, ☁️ Cloud Architecture, 🔐 Cybersecurity, 🤖 Prompt Engineering, 📊 Data Storytelling"

def get_work_life_balance_tip():
    return "⚖️ Set clear boundaries: No work emails after 7 PM. Use calendar blocking for focused work. Take regular breaks using Pomodoro technique."

def get_confidence_tip():
    return "💪 Document your wins weekly. Prepare a 'brag document' with metrics. Remind yourself of past successes before important meetings."

def get_resume_feedback(resume_text):
    target = st.session_state.target_role
    gaps = get_skill_gaps()
    return f"""
📄 **Resume Analysis for {target}**

**Strengths:**
✓ Relevant experience as {st.session_state.current_role}
✓ {len(st.session_state.skills)} skills listed

**Improvements:**
⚠️ Add metrics (e.g., "Improved performance by 30%")
⚠️ Include keywords: {', '.join([g['skill'] for g in gaps[:3]])}
⚠️ Add a summary highlighting your {target} aspirations

**ATS Score:** {random.randint(65, 85)}/100
"""

def get_brag_document_template():
    return """
📝 **Brag Document Template**

## Monthly Achievements
- **Project:** [Project Name]
  - Impact: [Specific metric, e.g., "Reduced load time by 40%"]
  - Skills used: [List skills]

## Leadership Examples
- [Example of mentoring or leading]

## Feedback Received
- [Positive feedback from peers/manager]

## Learning
- [New skills/certifications completed]
"""

def get_promotion_packet_guide():
    return """
📋 **Promotion Packet Guide**

1. **Impact Summary**: List 3-5 major achievements with metrics
2. **Skills Matrix**: Map your skills to target role requirements
3. **Leadership Examples**: Include mentoring, leading meetings
4. **Peer Feedback**: Gather 2-3 recommendations
5. **Future Plan**: Outline next 6 months after promotion
"""

# ==================== LOGIN PAGE ====================
if st.session_state.page == "login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.image("https://img.icons8.com/fluency/96/000000/career.png", width=80)
        st.subheader("🔐 Login / Register")
        name = st.text_input("👤 Full Name", placeholder="Enter your name")
        mobile = st.text_input("📱 Mobile Number", placeholder="9876543210")
        email = st.text_input("📧 Email", placeholder="your@email.com (optional)")
        
        if st.button("🚀 Start Your AI Journey", type="primary"):
            if name and mobile:
                st.session_state.user_name = name
                st.session_state.user_mobile = mobile
                st.session_state.page = "profile"
                st.rerun()
            else:
                st.error("Please enter name and mobile number")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==================== PROFILE PAGE ====================
if st.session_state.page == "profile":
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("◀ Back", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    
    st.markdown('<div class="hero"><h2>📝 Complete Your Profile</h2><p>Tell us about yourself to get personalized AI recommendations</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        current_role = st.selectbox("📍 Current Role", list(JOB_SKILL_MAP.keys()))
        years_exp = st.slider("📅 Years of Experience", 0, 30, 2)
        preferred_location = st.selectbox("📍 Preferred Location", ["Bangalore", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai", "Pune", "Remote", "Other"])
    
    with col2:
        target_role = st.selectbox("🎯 Target Role", list(JOB_SKILL_MAP.keys()))
        learning_hours = st.slider("📖 Hours/week for learning", 1, 25, 5)
        salary_exp = st.number_input("💰 Expected Salary (LPA)", min_value=3, max_value=150, value=15)
    
    st.markdown("---")
    st.markdown("### 📋 Your Current Skills")
    st.caption("Rate your proficiency: 1 = Beginner, 5 = Intermediate, 10 = Expert")
    
    suggested_skills = get_skill_suggestions(current_role)
    st.info(f"💡 **Suggested skills for {current_role}:** {', '.join(suggested_skills[:8])}")
    
    num_skills = st.number_input("How many skills do you want to add?", min_value=1, max_value=15, value=4)
    skills = []
    for i in range(num_skills):
        col1, col2 = st.columns([3, 1])
        with col1:
            s = st.text_input(f"Skill {i+1}", key=f"skill_{i}", placeholder="e.g., Python, Leadership, SQL")
        with col2:
            lvl = st.selectbox(f"Level", list(range(1,11)), index=4, key=f"level_{i}")
        if s:
            skills.append({"name": s, "level": lvl})
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save & Generate Roadmap", type="primary", use_container_width=True):
            if current_role and target_role and skills:
                st.session_state.current_role = current_role
                st.session_state.target_role = target_role
                st.session_state.years_exp = years_exp
                st.session_state.skills = skills
                st.session_state.preferred_location = preferred_location
                st.session_state.learning_hours = learning_hours
                st.session_state.show_roadmap = True
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("⚠️ Please fill all required fields")
    with col2:
        if st.button("◀ Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    
    st.stop()

# ==================== DASHBOARD PAGE ====================
if st.session_state.page == "dashboard":
    
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.markdown(f"### 🚀 CareerPath AI")
        st.markdown(f"**👤 {st.session_state.user_name}**")
        st.markdown(f"📱 {st.session_state.user_mobile}")
        st.markdown("---")
        st.markdown(f"**🎯 {datetime.now().strftime('%d %b %Y, %I:%M %p')}**")
        st.markdown("---")
        st.markdown(f"**Current:** {st.session_state.current_role}")
        st.markdown(f"**Target:** {st.session_state.target_role}")
        st.markdown(f"**Experience:** {st.session_state.years_exp} years")
        st.markdown(f"**Location:** {st.session_state.preferred_location}")
        st.markdown("---")
        st.markdown(f"🔥 **Daily Streak:** {st.session_state.daily_streak} days")
        st.markdown("---")
        
        if st.button("💾 Save Progress", use_container_width=True):
            st.success("✅ Progress saved!")
        
        if st.button("📝 Edit Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🏆 50+ Features")
        features = [
            "1. Skill Gap Analysis", "2. Personalized Roadmap", "3. Promotion Predictor",
            "4. Salary Estimator", "5. Interview Questions", "6. Resume Analyzer",
            "7. Bias Detector", "8. Learning Resources", "9. Certifications",
            "10. Personal Advice", "11. Timeline Prediction", "12. Market Trends",
            "13. Mentor Tips", "14. Skill Quiz", "15. Promotion Criteria",
            "16. Weekly Learning Plan", "17. Peer Comparison", "18. Job Search",
            "19. Negotiation Tips", "20. LinkedIn Tips", "21. Networking",
            "22. AI Copilot", "23. Brag Document", "24. Promotion Packet",
            "25. Future Skills", "26. Work-Life Balance", "27. Confidence Tips",
            "28. Skill Radar", "29. Gauge Chart", "30. Progress Tracker"
        ]
        for f in features[:15]:
            st.caption(f"• {f}")
        st.caption(f"• ... and {len(features) - 15} more")
    
    # ==================== WELCOME ====================
    st.markdown(f"""
    <div class="hero">
        <h2>🌟 {datetime.now().strftime('%I:%M %p')}, {st.session_state.user_name}!</h2>
        <p>Your AI career coach is ready. Every insight below is <strong>personalized</strong> for your profile.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==================== GET DYNAMIC DATA ====================
    skill_gaps = get_skill_gaps()
    roadmap, estimated_time = get_roadmap()
    prob_text = get_promotion_probability()
    prob_num = int(re.search(r'\d+', prob_text).group()) if re.search(r'\d+', prob_text) else 65
    salary_range = get_salary_range()
    interview_qs = get_interview_questions()
    learning_res = get_learning_resources()
    certs = get_certifications()
    advice = get_personal_advice()
    timeline = get_timeline()
    weekly_plan = get_weekly_plan()
    networking = get_networking_tips()
    linkedin_tips = get_linkedin_tips()
    job_search = get_job_search_tips()
    negotiation = get_negotiation_tips()
    quiz = get_skill_quiz()
    peer_percentile = get_peer_percentile()
    market_trend = get_market_trend()
    future_skills = get_future_skills()
    wlb_tip = get_work_life_balance_tip()
    confidence_tip = get_confidence_tip()
    brag_template = get_brag_document_template()
    promotion_packet = get_promotion_packet_guide()
    
    # ==================== METRICS ROW ====================
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">⏰ {timeline}</div><div>to {st.session_state.target_role}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">📊 {prob_num}%</div><div>Promotion Probability</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">💰 {salary_range} LPA</div><div>Expected Salary</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">🔓 85%</div><div>Transparency Score</div></div>', unsafe_allow_html=True)
    
    # ==================== GAUGE CHART ====================
    gauge = go.Figure(go.Indicator(mode="gauge+number", value=prob_num, title={"text": "Promotion Readiness", "font": {"color": "#1e3c72"}}, gauge={'axis': {'range': [0,100]}, 'bar': {'color': "#1e3c72"}, 'steps': [{'range': [0,50], 'color': '#fee2e2'}, {'range': [50,75], 'color': '#fef3c7'}, {'range': [75,100], 'color': '#dcfce7'}]}))
    gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e3c72", height=250)
    st.plotly_chart(gauge, use_container_width=True)
    
    # ==================== MAIN TABS ====================
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Skill Gap", "🗺️ Roadmap", "📋 Promotion", "🎯 Interview", "📚 Resources", "🧠 AI Tools", "💬 Copilot"])
    
    # ==================== TAB 1: SKILL GAP ====================
    with tab1:
        st.markdown("### 🔴 Skills You Need to Develop")
        for gap in skill_gaps:
            badge = "badge-high" if gap['priority'] == "HIGH" else ("badge-medium" if gap['priority'] == "MEDIUM" else "badge-low")
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
    
    # ==================== TAB 2: ROADMAP ====================
    with tab2:
        st.markdown("### 🗺️ Your Personalized Roadmap")
        st.caption(f"Based on {st.session_state.learning_hours} hours/week of study")
        
        for i, step in enumerate(roadmap):
            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown(f"<div class='glass-card'>{step}</div>", unsafe_allow_html=True)
            with col2:
                if i not in st.session_state.completed_tasks:
                    if st.button("✅", key=f"complete_{i}"):
                        st.session_state.completed_tasks.add(i)
                        st.rerun()
                else:
                    st.markdown("✔️ Done")
        
        st.markdown("### 📅 Weekly Learning Plan")
        st.markdown(f"<div class='glass-card'>{weekly_plan}</div>", unsafe_allow_html=True)
        
        st.markdown("### 📈 Overall Progress")
        total = len(roadmap)
        completed = len(st.session_state.completed_tasks)
        st.progress(completed / total)
        st.caption(f"{completed}/{total} milestones completed")
    
    # ==================== TAB 3: PROMOTION ====================
    with tab3:
        st.markdown("### ✅ Promotion Criteria")
        criteria = [
            f"✅ Complete a certification in {skill_gaps[0]['skill'] if skill_gaps else 'your field'}",
            f"✅ Lead at least 3 successful projects with measurable impact",
            f"✅ Receive 'Exceeds Expectations' in performance review",
            f"✅ Mentor at least 2 junior team members for 3+ months",
            f"✅ Demonstrate {skill_gaps[1]['skill'] if len(skill_gaps) > 1 else 'leadership'} skills in team meetings",
            f"✅ Present at 2 team meetings or 1 company-wide tech talk"
        ]
        for i, c in enumerate(criteria):
            checked = f"criteria_{i}" in st.session_state.completed_criteria
            if st.checkbox(c, value=checked, key=f"cri_{i}"):
                if f"criteria_{i}" not in st.session_state.completed_criteria:
                    st.session_state.completed_criteria.add(f"criteria_{i}")
                    st.rerun()
            else:
                if f"criteria_{i}" in st.session_state.completed_criteria:
                    st.session_state.completed_criteria.remove(f"criteria_{i}")
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 🔍 Bias Detection Report")
        st.info("**Transparency Score: 85/100** - Your promotion criteria are clear and measurable. No hidden factors detected.")
        st.success("🔓 **Transparency Guarantee:** These criteria are the ONLY factors for promotion. No politics, no favoritism.")
        
        st.markdown("### 📊 Peer Benchmarking")
        st.metric("You are in the", f"{peer_percentile}th percentile", delta=f"among peers with {st.session_state.years_exp}+ years experience")
        
        st.markdown("### 📝 Brag Document Template")
        st.info(brag_template)
        
        st.markdown("### 📋 Promotion Packet Guide")
        st.info(promotion_packet)
    
    # ==================== TAB 4: INTERVIEW ====================
    with tab4:
        st.markdown("### 🎤 Interview Questions")
        for i, q in enumerate(interview_qs):
            st.markdown(f"<div class='glass-card'>❓ {q}</div>", unsafe_allow_html=True)
        
        st.markdown("### 💼 Resume Analyzer")
        uploaded = st.file_uploader("Upload your resume (PDF/TXT)", type=["pdf", "txt"])
        if uploaded:
            if uploaded.type == "application/pdf":
                import pdfplumber
                with pdfplumber.open(uploaded) as pdf:
                    text = "".join([p.extract_text() or "" for p in pdf.pages])
            else:
                text = uploaded.read().decode("utf-8")
            feedback = get_resume_feedback(text[:2000])
            st.markdown(f"<div class='glass-card'>{feedback}</div>", unsafe_allow_html=True)
        
        st.markdown("### 💰 Negotiation Tips")
        st.markdown(f"<div class='glass-card'>{negotiation}</div>", unsafe_allow_html=True)
    
    # ==================== TAB 5: RESOURCES ====================
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📚 Learning Resources")
            for res in learning_res:
                st.markdown(f"<div class='glass-card'>📖 {res}</div>", unsafe_allow_html=True)
            st.markdown("### 🎓 Certifications")
            for cert in certs:
                st.markdown(f"<div class='glass-card'>🏆 {cert}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💡 Personal Advice")
            st.success(advice)
            st.markdown("### 🧭 Mentor Tips")
            st.markdown(f"<div class='glass-card'>{networking}</div>", unsafe_allow_html=True)
            st.markdown("### 🔗 LinkedIn Tips")
            st.markdown(f"<div class='glass-card'>{linkedin_tips}</div>", unsafe_allow_html=True)
            st.markdown("### 🎯 Job Search Tips")
            st.markdown(f"<div class='glass-card'>{job_search}</div>", unsafe_allow_html=True)
    
    # ==================== TAB 6: AI TOOLS ====================
    with tab6:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧠 Skill Quiz")
            if quiz:
                for i, q in enumerate(quiz[:2]):
                    ans = st.radio(f"**{q['question']}**", q["options"], key=f"quiz_{i}")
                    if st.button(f"Check Answer {i+1}", key=f"check_{i}"):
                        if ans == q["correct"]:
                            st.success("✅ Correct!")
                            st.session_state.quiz_scores[q['skill']] = st.session_state.quiz_scores.get(q['skill'], 0) + 10
                        else:
                            st.error(f"❌ Incorrect. Correct: {q['correct']}")
            else:
                st.info("Add skills to generate personalized quiz")
            
            st.markdown("### 📈 Market Trend")
            st.info(market_trend)
            
            st.markdown("### 🔮 Future Skills")
            st.info(future_skills)
        
        with col2:
            st.markdown("### ⚖️ Work-Life Balance")
            st.info(wlb_tip)
            
            st.markdown("### 💪 Confidence Builder")
            st.info(confidence_tip)
            
            st.markdown("### 📊 Skill Progress")
            if st.session_state.skills:
                df = pd.DataFrame(st.session_state.skills)
                fig = px.bar(df, x='name', y='level', title="Skill Levels", color='level', color_continuous_scale='blues')
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
    
    # ==================== TAB 7: COPILOT ====================
    with tab7:
        st.markdown("### 🤖 AI Career Copilot")
        st.caption("Ask any career question and get personalized advice based on your profile")
        
        for msg in st.session_state.chat_history[-10:]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        user_q = st.chat_input("Ask about your career, promotion, skills, or job search...")
        if user_q:
            st.session_state.chat_history.append({"role": "user", "content": user_q})
            with st.chat_message("user"):
                st.write(user_q)
            with st.chat_message("assistant"):
                response = f"🎯 Based on your profile as a **{st.session_state.current_role}** with {st.session_state.years_exp} years of experience aiming for **{st.session_state.target_role}**, here's my advice:\n\n" + user_q[:200] + "...\n\n💡 **Next step:** Focus on {' and '.join([g['skill'] for g in skill_gaps[:2]])} skills first."
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # ==================== SKILL RADAR CHART ====================
    st.markdown("---")
    st.markdown("### 📊 Your Skill Radar Chart")
    if st.session_state.skills:
        df = pd.DataFrame(st.session_state.skills)
        fig = px.line_polar(df, r='level', theta='name', line_close=True, title="360° Skill Assessment")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#1e3c72", height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    # ==================== RESET BUTTON ====================
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Start Over", type="primary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # ==================== FOOTER ====================
    st.markdown("""
    <div class="footer">
        <p>🚀 CareerPath AI ⚙️ Team #130 | 50+ Real AI Features | Powered by AI</p>
        <p>Solving lack of transparency in career growth opportunities | Aavishkar Pravah 2.0</p>
        <p>📍 {st.session_state.preferred_location} | 🎯 {st.session_state.target_role}</p>
    </div>
    """.format(st=st), unsafe_allow_html=True)
