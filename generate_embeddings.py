import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure embeddings folder exists
os.makedirs("embeddings", exist_ok=True)

# Load CSV
try:
    df = pd.read_csv("data/students.csv")
except FileNotFoundError:
    print("FATAL ERROR: students.csv not found in the 'data' folder.")
    exit()


# ---- Combine fields into a single text string ----
def combine_fields(row):
    return (
        f"Skills: {row['skills']}. "
        f"Project Title: {row['project_title']}. "
        f"Project Description: {row['project_description']}. "
        f"Passing Year: {row['passing_year']}. "
        f"Student Profile Summary: A motivated student skilled in {row['skills']} "
        f"who built a project titled {row['project_title']}."
    )

df["text"] = df.apply(combine_fields, axis=1)


# ---- TF-IDF Vectorizer ----
print("Starting TF-IDF transformation...")

vectorizer = TfidfVectorizer(max_features=2000)
tfidf_matrix = vectorizer.fit_transform(df["text"])

df["embedding"] = list(tfidf_matrix.toarray())


# ---- CRITICAL: Save ALL required fields ----
final_df = df[[
    "id",
    "name",
    "skills",
    "project_title",
    "project_description",
    "passing_year",
    "embedding"
]]

final_df.to_pickle("embeddings/student_embeddings.pkl")

print("✅ Embeddings generated & ALL fields saved successfully!")
