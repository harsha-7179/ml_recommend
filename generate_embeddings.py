import os

# Create folder if missing
if not os.path.exists("embeddings"):
    os.makedirs("embeddings")

import pandas as pd
from sentence_transformers import SentenceTransformer

# Load CSV
df = pd.read_csv("data/students.csv")

# Combine fields (improved structured format)
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

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Generate embeddings with progress logs
embeddings = []
for i, t in enumerate(df["text"]):
    if i % 500 == 0:
        print(f"Encoding {i}/{len(df)}...")
    embeddings.append(model.encode(t).tolist())

df["embedding"] = embeddings

# Save PKL
df.to_pickle("embeddings/student_embeddings.pkl")

print("✅ Local embeddings generated successfully!")
