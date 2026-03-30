from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(user_skills, job_skills_list):

    user_skills = " ".join([s.strip() for s in user_skills.split(",")])

    job_skills_list = [
        " ".join([s.strip() for s in skills.split(",")])
        for skills in job_skills_list
    ]

    all_skills = [user_skills] + job_skills_list

    vectorizer = CountVectorizer().fit_transform(all_skills)
    vectors = vectorizer.toarray()

    similarity_matrix = cosine_similarity(vectors)
    similarity_scores = similarity_matrix[0][1:]

    return similarity_scores


def get_top_matches(user_skills, jobs_df, top_n=3):
    job_skills_list = jobs_df['skills'].tolist()

    scores = calculate_similarity(user_skills, job_skills_list)

    jobs_df['match_score'] = scores

    top_jobs = jobs_df.sort_values(by='match_score', ascending=False)

    return top_jobs.head(top_n)