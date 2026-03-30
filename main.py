import pandas as pd
from src.similarity import get_top_matches
from src.gap_analysis import analyze_gap_for_top_jobs
from src.learning_recommender import generate_learning_recommendations

# Load data
jobs = pd.read_csv("data/processed/cleaned_jobs.csv")

# User input
user_skills = "python sql"

# Step 1: Recommend jobs
recommended_jobs = get_top_matches(user_skills, jobs)

# Step 2: Find skill gaps
gap_results = analyze_gap_for_top_jobs(user_skills, recommended_jobs)

# Step 3: Generate learning path
learning_results = generate_learning_recommendations(gap_results)

# OUTPUT

print("\n🎯 Recommended Jobs:\n")
print(recommended_jobs[['job_title', 'match_score']])

print("\n📉 Skill Gaps:\n")
for item in gap_results:
    print(f"{item['job_title']} → Missing Skills: {item['missing_skills']}")

print("\n📚 Learning Path:\n")
for item in learning_results:
    print(f"\n{item['job_title']}:")
    for step, skill in enumerate(item['learning_path'], start=1):
        print(f"  Step {step}: Learn {skill}")