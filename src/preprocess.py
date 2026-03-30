import pandas as pd
import os

def load_data(jobs_path, skills_path):
    jobs = pd.read_csv(jobs_path)
    skills = pd.read_csv(skills_path)
    return jobs, skills


def clean_jobs_data(jobs_df):
    jobs_df = jobs_df.dropna()
    jobs_df.columns = jobs_df.columns.str.lower()

    if 'job_title' in jobs_df.columns:
        jobs_df['job_title'] = jobs_df['job_title'].str.lower()

    if 'skills' in jobs_df.columns:
        jobs_df['skills'] = jobs_df['skills'].str.lower()

    return jobs_df


def clean_skills_data(skills_df):
    skills_df = skills_df.dropna()
    skills_df.columns = skills_df.columns.str.lower()

    if 'skill' in skills_df.columns:
        skills_df['skill'] = skills_df['skill'].str.lower()

    return skills_df


def save_processed_data(jobs_df, skills_df):
    os.makedirs('data/processed', exist_ok=True)

    jobs_df.to_csv('data/processed/cleaned_jobs.csv', index=False)
    skills_df.to_csv('data/processed/cleaned_skills.csv', index=False)


if __name__ == "__main__":
    jobs_path = "data/raw/jobs.csv"
    skills_path = "data/raw/skills.csv"

    print("Loading data...")

    jobs, skills = load_data(jobs_path, skills_path)

    print("Cleaning data...")

    jobs_clean = clean_jobs_data(jobs)
    skills_clean = clean_skills_data(skills)

    print("Saving processed data...")

    save_processed_data(jobs_clean, skills_clean)

    print("✅ Data preprocessing completed successfully!")
    print("Jobs shape:", jobs_clean.shape)
    print("Skills shape:", skills_clean.shape)