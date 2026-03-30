def process_skills(skill_string):
    return set([skill.strip().lower() for skill in skill_string.split(",")])


def get_skill_gap(user_skills, job_skills):
    user_set = process_skills(user_skills)
    job_set = process_skills(job_skills)

    missing_skills = job_set - user_set

    return list(missing_skills)


def analyze_gap_for_top_jobs(user_skills, recommended_jobs):
    results = []

    for _, row in recommended_jobs.iterrows():
        job_title = row['job_title']
        job_skills = row['skills']

        gap = get_skill_gap(user_skills, job_skills)

        results.append({
            "job_title": job_title,
            "missing_skills": gap
        })

    return results