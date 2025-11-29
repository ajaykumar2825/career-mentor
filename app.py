import streamlit as st

st.set_page_config(page_title="Career Mentor", layout="wide")

st.title("🎓 Career Mentor App")
st.write("Helping students and early-career professionals plan their next steps.")

# -------------------------------
# Profile form
# -------------------------------
st.header("Your Profile")
with st.form("profile_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    education = st.selectbox("Education Level", ["Undergraduate", "Graduate", "Early Career"])
    degree = st.text_input("Degree")
    year = st.number_input("Year of Study", min_value=1, max_value=6, step=1)
    skills = st.text_area("List your skills (comma separated)")
    interests = st.text_area("Career interests (comma separated)")
    time_per_week = st.slider("Hours you can spend per week", 2, 40, 10)
    submitted = st.form_submit_button("Save Profile")

# -------------------------------
# Recommendation Engine
# -------------------------------
def recommend_next_steps(skills, interests):
    skills = [s.strip().lower() for s in skills]
    interests = [i.strip().lower() for i in interests]
    recos = []

    if "python" in skills and "data science" in interests:
        recos.append({
            "title": "Build a churn prediction app",
            "how": [
                "Clean Telco dataset, encode categorical features, split train/test",
                "Train Logistic Regression and XGBoost, compare metrics",
                "Generate SHAP plots for explainability",
                "Deploy with Streamlit and add file upload"
            ],
            "resources": [
                "https://www.kaggle.com/datasets/blastchar/telco-customer-churn",
                "https://docs.streamlit.io",
                "https://shap.readthedocs.io"
            ],
            "validation": "Deployed app URL + README with screenshots"
        })

    if "html" in skills and "frontend developer" in interests:
        recos.append({
            "title": "Create a responsive landing page",
            "how": [
                "Use semantic HTML with landmarks and headings",
                "Apply CSS Grid/Flexbox for layout",
                "Ensure accessibility: alt text, contrast, keyboard navigation"
            ],
            "resources": [
                "https://developer.mozilla.org/en-US/docs/Web/HTML",
                "https://web.dev/accessibility/"
            ],
            "validation": "Lighthouse accessibility score ≥ 90"
        })

    return recos

# -------------------------------
# Roadmap Generator
# -------------------------------
def build_roadmap(recos, weeks=6, hours_per_week=10):
    roadmap = []
    remaining_hours = weeks * hours_per_week
    for r in recos:
        estimated = len(r["how"]) * 2  # assume ~2 hours per step
        if estimated <= remaining_hours:
            roadmap.append({
                "title": r["title"],
                "steps": r["how"],
                "resources": r["resources"],
                "validation": r["validation"],
                "estimated_hours": estimated
            })
            remaining_hours -= estimated

    # Group into 2-week sprints
    sprints, sprint, sprint_hours = [], [], 0
    for task in roadmap:
        if sprint_hours + task["estimated_hours"] > hours_per_week * 2:
            sprints.append({"goals": [t["title"] for t in sprint], "tasks": sprint})
            sprint, sprint_hours = [], 0
        sprint.append(task)
        sprint_hours += task["estimated_hours"]
    if sprint:
        sprints.append({"goals": [t["title"] for t in sprint], "tasks": sprint})

    return sprints

# -------------------------------
# GitHub & LinkedIn Feedback
# -------------------------------
st.header("🔍 Profile Feedback")

with st.form("feedback_form"):
    gh_repos = st.number_input("GitHub repo count", 0, 50, 3)
    has_profile_readme = st.checkbox("Has GitHub profile README?")
    top_repos_readme = st.number_input("Top repos with README", 0, 10, 2)
    recent_commit_days = st.number_input("Days since last commit", 0, 365, 60)

    headline_len = st.number_input("LinkedIn headline length (characters)", 0, 220, 30)
    about_len = st.number_input("LinkedIn About length (words)", 0, 2000, 150)
    featured_count = st.number_input("Featured links count", 0, 10, 1)
    quant_bullets = st.number_input("Quantified bullets in experience/projects", 0, 20, 2)

    fb_submit = st.form_submit_button("Get Feedback")

if fb_submit:
    st.subheader("GitHub Feedback")
    if gh_repos < 5:
        st.warning("Add at least 5 public repos with clear READMEs.")
    else:
        st.success("Repo count looks good!")
    if not has_profile_readme:
        st.warning("Create a profile README in a repo named your-username.")
    if top_repos_readme < 3:
        st.warning("Add detailed READMEs with screenshots and badges to your top repos.")
    if recent_commit_days > 30:
        st.warning("Push at least one commit in the last 30 days.")

    st.subheader("LinkedIn Feedback")
    if headline_len < 20:
        st.warning("Expand your headline: role | skills | artifacts.")
    if not (300 <= about_len <= 600):
        st.warning("Write an About section between 300–600 words.")
    if featured_count < 3:
        st.warning("Add at least 3 featured links (apps, repos, certificates).")
    if quant_bullets < 5:
        st.warning("Use numbers in your experience/projects (e.g., AUC 0.86, 200 users).")

# -------------------------------
# Job Matching
# -------------------------------
st.header("💼 Job Matches")

jobs = [
    {"title": "Data Analyst Intern", "company": "ABC Corp", "location": "Hyderabad",
     "role": "data scientist", "required_skills": ["python", "sql", "statistics"], "url": "https://example.com"},
    {"title": "Frontend Developer", "company": "XYZ Ltd", "location": "Bangalore",
     "role": "frontend developer", "required_skills": ["html", "css", "javascript"], "url": "https://example.com"}
]

# -------------------------------
# Main App Logic
# -------------------------------
if submitted:
    st.success(f"Profile saved for {name} ({email})")

    skills_list = [s.strip().lower() for s in skills.split(",") if s.strip()]
    interests_list = [i.strip().lower() for i in interests.split(",") if i.strip()]

    st.write("Skills:", ", ".join(skills_list))
    st.write("Interests:", ", ".join(interests_list))

    # Recommendations
    st.subheader("🎯 Recommended Next Steps")
    recos = recommend_next_steps(skills_list, interests_list)
    if recos:
        for r in recos:
            with st.expander(r["title"]):
                st.markdown("**How to do it:**")
                for step in r["how"]:
                    st.markdown(f"- {step}")
                st.markdown("**Resources:**")
                for link in r["resources"]:
                    st.markdown(f"- [{link}]({link})")
                st.markdown(f"**Validation:** {r['validation']}")
    else:
        st.warning("No matching recommendations found. Try adding more skills or interests.")

    # Roadmap
    if recos:
        st.subheader("📅 Roadmap")
        sprints = build_roadmap(recos, weeks=6, hours_per_week=time_per_week)
        if sprints:
            for i, sprint in enumerate(sprints, start=1):
                with st.expander(f"Sprint {i}: {', '.join(sprint['goals'])}"):
                    for task in sprint["tasks"]:
                        st.markdown(f"**Task:** {task['title']}")
                        st.markdown(f"- Estimated hours: {task['estimated_hours']}")
                        st.markdown("**Steps:**")
                        for step in task["steps"]:
                            st.markdown(f"  - {step}")
                        st.markdown("**Resources:**")
                        for link in task["resources"]:
                            st.markdown(f"  - [{link}]({link})")
                        st.markdown(f"**Validation:** {task['validation']}")
        else:
            st.info("No roadmap generated yet.")

    # Job Matching
    st.subheader("Top Job Recommendations")
    stu_skills = set(skills_list)
    for job in jobs:
        overlap = stu_skills & set(job["required_skills"])
        if overlap:
            st.markdown(f"**{job['title']} at {job['company']} ({job['location']})**")
            st.markdown(f"- Required Skills: {', '.join(job['required_skills'])}")
            st.markdown(f"- [Apply Here]({job['url']})")    