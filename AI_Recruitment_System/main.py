import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Loading the datasets
candidates = pd.read_csv("data/candidates.csv")
companies = pd.read_csv("data/companies.csv")
interviews = pd.read_csv("data/interview_score.csv")


candidate_data = pd.merge(
    candidates,
    interviews,
    on="CandidateID"
)

print("\n=== AI Recruitment System ===\n")

for _, company in companies.iterrows():

    company_name = company["CompanyName"]
    required_skill = company["RequiredSkill"]

    candidate_data["combined"] = (
        candidate_data["Skills"] + " " + required_skill
    )

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(candidate_data["combined"])

    similarity = cosine_similarity(vectors)

    candidate_data["FinalScore"] = (
        candidate_data["OverallRating"] * 10
    )

    best_candidate = candidate_data.sort_values(
        by="FinalScore",
        ascending=False
    ).iloc[0]

    print(f"Company : {company_name}")
    print(f"Best Candidate :  {best_candidate['Name']}")
    print(f"Skill :  {best_candidate['Skills']}")
    print(f"Interview Rating :{best_candidate['OverallRating']}")
    print("-"  * 40)