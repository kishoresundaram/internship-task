from fastapi import FastAPI
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from llm import generate_reason

app = FastAPI()


# -------------------------
# Load Dataset
# -------------------------

candidate_df = pd.read_csv("data/candidates.csv")
company_df = pd.read_csv("data/companies.csv")
interview_df = pd.read_csv("data/interview_score.csv")


# Merge candidate details with interview score

merged_df = pd.merge(
    candidate_df,
    interview_df,
    on="CandidateID"
)


# Home API


@app.get("/")
def home():
    return {"message": "AI Recruitment System"}


# Candidate API


@app.get("/candidates")
def fetch_candidates():
    return merged_df.to_dict(orient="records")


# Company Api

@app.get("/companies")
def fetch_companies():
    return company_df.to_dict(orient="records")



# Best CandIdate

@app.get("/best-candidate")
def get_best_candidate():

    temp_df = merged_df.copy()

    temp_df["FinalScore"] = (
        temp_df["OverallRating"] * 0.6
        + temp_df["Coding"] * 0.4
    )

    best = temp_df.sort_values(
        by="FinalScore",
        ascending=False
    ).iloc[0]

    return {

        "Candidate": best["Name"],
        "Skills": best["Skills"],
        "FinalScore": round(best["FinalScore"],2)

    }



#  recommendation API

@app.get("/recommend/{company_name}")
def recommend_candidate(company_name: str):

    company = company_df[
        company_df["Company"].str.lower()
        == company_name.lower()
    ]

    if company.empty:
        return {"message":"Company not found"}

    company = company.iloc[0]

    rankings = []

    required_skills = company["RequiredSkills"]


    for _, candidate in merged_df.iterrows():

        if candidate["Experience"] < company["MinExperience"]:
            continue


        skills = [
            required_skills,
            candidate["Skills"]
        ]

        vectorizer = CountVectorizer()

        vectors = vectorizer.fit_transform(skills)

        similarity = cosine_similarity(
            vectors[0],
            vectors[1]
        )[0][0]


        skill_score = similarity * 70

        interview_score = candidate["OverallRating"] * 3

        final_score = skill_score + interview_score


        rankings.append({

            "Candidate": candidate["Name"],
            "SkillMatch": round(similarity*100,2),
            "FinalScore": round(final_score,2)

        })


    rankings.sort(
        key=lambda x:x["FinalScore"],
        reverse=True
    )


    return{

        "Company":company["Company"],
        "Role":company["Role"],
        "TopCandidate":rankings[:3]

    }


# -------------------------
# AI Reason API
# -------------------------

@app.get("/ai-reason/{company_name}")
def ai_reason(company_name:str):

    company = company_df[
        company_df["Company"].str.lower()
        == company_name.lower()
    ]

    if company.empty:
        return {"message":"Company not found"}

    company = company.iloc[0]


    eligible_candidates = merged_df[
        merged_df["Experience"] >= company["MinExperience"]
    ]


    if eligible_candidates.empty:
        return {"message":"No suitable candidates found"}


    best = eligible_candidates.sort_values(

        by="OverallRating",
        ascending=False

    ).iloc[0]


    reason = generate_reason(best,company)


    return{

        "Company":company["Company"],
        "Role":company["Role"],
        "RecommendedCandidate":best["Name"],
        "Reason":reason

    }