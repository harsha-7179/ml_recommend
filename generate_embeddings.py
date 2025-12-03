import os
import pandas as pd
# Use TfidfVectorizer from scikit-learn (No PyTorch/Sentence-Transformers needed)
from sklearn.feature_extraction.text import TfidfVectorizer

# Create folder if missing
if not os.path.exists("embeddings"):
    os.makedirs("embeddings")

# Load CSV
df = pd.read_csv("data/students.csv")

# Combine fields (same as before)
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

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=1000)

print("Starting TF-IDF transformation...")

# Fit and transform the text data to get the embeddings
tfidf_matrix = vectorizer.fit_transform(df["text"])

# Convert the sparse matrix to a list of vectors for storage
embeddings = tfidf_matrix.toarray().tolist()

df["embedding"] = embeddings

# Save PKL
df.to_pickle("embeddings/student_embeddings.pkl")

print("✅ Local embeddings generated successfully using TF-IDF!")