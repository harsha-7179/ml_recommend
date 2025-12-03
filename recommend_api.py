import os
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
SIMILARITY_THRESHOLD = 0.05   # still here for weak cutoff

# Load embeddings
if not os.path.exists("embeddings/student_embeddings.pkl"):
    print("Warning: student_embeddings.pkl not found. Run embeddings generator first!")

try:
    data = pd.read_pickle("embeddings/student_embeddings.pkl")
except FileNotFoundError:
    print("ERROR: Could not load embeddings!")
    data = pd.DataFrame({
        "id": [9999],
        "embedding": [np.zeros(10)],
        "name": ["Dummy Student"]
    })

# Flask setup
app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.route("/")
def home():
    return app.send_static_file("index.html")


# --------------------------------------------------------
# 🔥 REALISTIC COSINE + SIGMOID SCALING
# --------------------------------------------------------
@app.route("/recommend", methods=["GET"])
def recommend():
    student_id = request.args.get("student_id")

    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    try:
        student_id = int(student_id)
    except:
        return jsonify({"error": "student_id must be an integer"}), 400

    # Find target student
    target_row = data[data["id"] == student_id]
    if target_row.empty:
        return jsonify({"error": f"Student ID {student_id} not found"}), 404

    # --- Embeddings ---
    idx = target_row.index[0]
    target_emb = np.array(data.loc[idx, "embedding"]).reshape(1, -1)
    all_embs = np.vstack(data["embedding"].values)

    # --- Raw cosine similarity ---
    sims = cosine_similarity(target_emb, all_embs)[0]

    # --------------------------------------------------------
    # 🌟 NON-LINEAR SIGMOID SCALING (REALISTIC)
    # --------------------------------------------------------
    raw = sims

    # Shift and stretch cosine values (center around 0.25)
    x = (raw - 0.25) * 8.0

    # Apply sigmoid transform (smooth curve 0–1)
    sigmoid = 1 / (1 + np.exp(-x))

    # Add tiny jitter so scores aren’t identical
    sims = sigmoid + (np.random.rand(len(sigmoid)) * 0.02 - 0.01)

    # Clip to [0, 1]
    sims = np.clip(sims, 0.0, 1.0)

    # Save similarity values
    data["similarity"] = sims

    # Sort and remove self
    sorted_df = data.sort_values("similarity", ascending=False)
    sorted_df = sorted_df[sorted_df["id"] != student_id]

    # Apply threshold
    strong_matches = sorted_df[sorted_df["similarity"] >= SIMILARITY_THRESHOLD]

    # Fallback to top 5
    top_matches = strong_matches.head(5) if len(strong_matches) > 0 else sorted_df.head(5)

    # Drop embeddings for JSON
    if "embedding" in top_matches.columns:
        top_matches = top_matches.drop(columns=["embedding"])

    return jsonify(top_matches.to_dict(orient="records"))


# --------------------------------------------------------
# Run server
# --------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
