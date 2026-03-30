def generate_learning_path(missing_skills):
    """
    Takes missing skills list and returns ordered learning steps
    """

    learning_priority = {
        "statistics": 1,
        "excel": 1,
        "sql": 1,

        "python": 2,
        "power bi": 2,
        "machine learning": 2,

        "deep learning": 3,
        "nlp": 3,
        "computer vision": 3,
        "tensorflow": 3,
        "pytorch": 3,

        "spark": 3,
        "hadoop": 3,
        "mlops": 4
    }

    # Assign priority
    sorted_skills = sorted(
        missing_skills,
        key=lambda x: learning_priority.get(x.lower(), 5)
    )

    return sorted_skills


def generate_learning_recommendations(gap_results):
    final_output = []

    for item in gap_results:
        job_title = item['job_title']
        missing_skills = item['missing_skills']

        learning_path = generate_learning_path(missing_skills)

        final_output.append({
            "job_title": job_title,
            "learning_path": learning_path
        })

    return final_output