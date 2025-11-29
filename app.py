import streamlit as st

st.set_page_config(page_title="Career Mentor", layout="wide")

st.title("🎓 Career Mentor App")
st.write("Helping students and early-career professionals plan their next steps.")

# Profile form
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

if submitted:
    st.success(f"Profile saved for {name} ({email})")
    st.write("Skills:", skills.split(","))
    st.write("Interests:", interests.split(","))