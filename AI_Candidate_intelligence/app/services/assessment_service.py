ROLE_QUESTIONS = {
    "AI Engineer": [
        {
            "question": "What is supervised learning?",
            "answer": "Supervised learning is a machine learning approach where a model learns from labeled training data."
        },
        {
            "question": "What is overfitting in machine learning?",
            "answer": "Overfitting occurs when a model learns the training data too closely and performs poorly on unseen data."
        },
        {
            "question": "What is the difference between AI and Generative AI?",
            "answer": "AI performs tasks that require intelligence, while Generative AI creates new content such as text, images, code, or audio."
        }
    ],

    "Machine Learning Engineer": [
        {
            "question": "What is a machine learning model?",
            "answer": "A machine learning model is an algorithm trained on data to make predictions or decisions."
        },
        {
            "question": "What is a training dataset?",
            "answer": "A training dataset is the data used to teach a machine learning model."
        },
        {
            "question": "What is model evaluation?",
            "answer": "Model evaluation measures how well a trained model performs using appropriate metrics and test data."
        }
    ],

    "Python Backend Developer": [
        {
            "question": "What is FastAPI?",
            "answer": "FastAPI is a modern Python web framework used to build APIs."
        },
        {
            "question": "What is REST API?",
            "answer": "A REST API is an application programming interface that follows REST principles for communication over HTTP."
        },
        {
            "question": "What is SQL?",
            "answer": "SQL is a language used to store, retrieve, and manipulate data in relational databases."
        }
    ],

    "Data Scientist": [
        {
            "question": "What is data preprocessing?",
            "answer": "Data preprocessing involves cleaning and transforming raw data before analysis or machine learning."
        },
        {
            "question": "What is exploratory data analysis?",
            "answer": "Exploratory data analysis is the process of understanding datasets using statistics and visualizations."
        },
        {
            "question": "What is regression?",
            "answer": "Regression is a supervised learning technique used to predict continuous numerical values."
        }
    ],

    "Full Stack Developer": [
        {
            "question": "What is HTML?",
            "answer": "HTML is the standard markup language used to structure web pages."
        },
        {
            "question": "What is CSS?",
            "answer": "CSS is used to style and design web pages."
        },
        {
            "question": "What is JavaScript?",
            "answer": "JavaScript is a programming language commonly used to add interactive behavior to web applications."
        }
    ]
}


def generate_assessment(role: str):

    questions = ROLE_QUESTIONS.get(role)

    if not questions:
        return []

    return [
        {
            "question_number": index + 1,
            "question": item["question"]
        }
        for index, item in enumerate(questions)
    ]


def evaluate_answers(role: str, answers: list):

    questions = ROLE_QUESTIONS.get(role, [])

    results = []

    total_score = 0

    for index, answer in enumerate(answers):

        if index >= len(questions):
            break

        correct_answer = questions[index]["answer"]

        user_answer = answer.get("answer", "").lower()

        keywords = [
            word.lower()
            for word in correct_answer.split()
            if len(word) > 4
        ]

        matched = sum(
            1
            for keyword in keywords
            if keyword in user_answer
        )

        if keywords:
            score = round(
                min((matched / len(keywords)) * 100, 100)
            )
        else:
            score = 0

        total_score += score

        results.append({
            "question": questions[index]["question"],
            "answer": answer.get("answer", ""),
            "score": score
        })

    if results:
        readiness_score = round(
            total_score / len(results)
        )
    else:
        readiness_score = 0

    if readiness_score >= 80:
        level = "Ready"
    elif readiness_score >= 60:
        level = "Nearly Ready"
    else:
        level = "Needs Improvement"

    return {
        "readiness_score": readiness_score,
        "readiness_level": level,
        "results": results
    }