import sys
import os

# Fix module path issue
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

import streamlit as st
import pandas as pd

from src.similarity import get_top_matches
from src.gap_analysis import analyze_gap_for_top_jobs, get_skill_gap
from src.learning_recommender import generate_learning_recommendations, generate_learning_path
from src.skill_extractor import extract_text_from_pdf, extract_skills

# Load datasets
jobs = pd.read_csv("data/processed/cleaned_jobs.csv")
skills_df = pd.read_csv("data/processed/cleaned_skills.csv")
skills_list = skills_df['skill'].tolist()

# UI
st.title("🚀 CareerPath AI")
st.subheader("Smart Career Recommendation System")

# Inputs
user_skills = st.text_input("Enter your skills (comma separated):")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

selected_job = st.selectbox(
    "🎯 Select a target job role (optional):",
    ["None"] + jobs['job_title'].unique().tolist()
)

# Button
if st.button("Analyze"):

    final_skills = user_skills

    # 🔹 Resume upload
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        extracted_skills = extract_skills(text, skills_list)

        if extracted_skills:
            st.success(f"🧠 Extracted Skills: {extracted_skills}")
            final_skills = ", ".join(extracted_skills)
        else:
            st.warning("No skills detected in resume.")

    # 🔹 Validate skills
    if final_skills and len(final_skills.strip()) > 2:

        # =========================
        # 🎯 TARGET JOB ANALYSIS
        # =========================
        if selected_job != "None":

            st.header("🎯 Target Job Analysis")

            job_row = jobs[jobs['job_title'] == selected_job].iloc[0]
            job_skills = job_row['skills']

            st.write(f"### 📌 Required Skills for {selected_job}")
            st.write(", ".join([s.strip() for s in job_skills.split(",")]))

            gap = get_skill_gap(final_skills, job_skills)

            if len(gap) == 0:
                st.success("✅ You are fully ready for this role!")
            else:
                st.warning(f"📉 Missing Skills: {', '.join(gap)}")

                learning_path = generate_learning_path(gap)

                st.write("📚 Learning Path:")
                for i, skill in enumerate(learning_path, 1):
                    st.write(f"Step {i}: Learn {skill}")

        # =========================
        # 🎯 GENERAL RECOMMENDATION
        # =========================
        recommended_jobs = get_top_matches(final_skills, jobs)
        gap_results = analyze_gap_for_top_jobs(final_skills, recommended_jobs)
        learning_results = generate_learning_recommendations(gap_results)

        # 🎯 Best role
        st.header("🏆 Best Fit Role")
        best_job = recommended_jobs.iloc[0]
        st.success(f"{best_job['job_title']} ({round(best_job['match_score']*100,2)}% match)")

        # 🎯 Recommended Roles
        st.header("🎯 Recommended Roles")
        recommended_jobs['match_score'] = (recommended_jobs['match_score'] * 100).round(2)

        st.dataframe(
            recommended_jobs[['job_title', 'match_score']].rename(
                columns={'match_score': 'Match %'}
            )
        )

        # 📉 Skill Gaps
        st.header("📉 Skill Gaps")

        for item in gap_results:
            if item['job_title'] == selected_job:
                continue

            if len(item['missing_skills']) == 0:
                st.success(f"✅ {item['job_title']} → You are job-ready!")
            else:
                st.warning(f"{item['job_title']} → Missing: {', '.join(item['missing_skills'])}")

        # 📚 Learning Path
        st.header("📚 Learning Path")

        for item in learning_results:
            if item['job_title'] == selected_job:
                continue

            st.write(f"### 🎯 {item['job_title']}")

            if len(item['learning_path']) == 0:
                st.success("✅ No learning required — you are ready!")
            else:
                for i, skill in enumerate(item['learning_path'], 1):
                    st.write(f"Step {i}: Learn {skill}")

        # 🧠 Final Advice
        st.header("🧠 Final Career Advice")

        if len(gap_results[0]['missing_skills']) == 0:
            st.success("You are job-ready! Start applying 🚀")
        else:
            st.info("You are close to your goal. Focus on missing skills to improve your chances.")

    else:
        st.error("Please enter valid skills or upload a resume!")