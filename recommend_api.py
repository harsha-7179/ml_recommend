import os
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Auto-generate embeddings if missing
if not os.path.exists("embeddings/student_embeddings.pkl"):
    os.system("python generate_embeddings.py")

# Load data
data = pd.read_pickle("embeddings/student_embeddings.pkl")

# Flask app
app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/recommend", methods=["GET"])
def recommend():
    student_id = request.args.get("student_id")

    if student_id is None:
        return jsonify({"error": "student_id is required"}), 400

    student_id = int(student_id)

    # Find row
    idx = data.index[data["id"] == student_id][0]

    target_emb = np.array(data.loc[idx, "embedding"]).reshape(1, -1)
    all_embs = np.vstack(data["embedding"].values)

    sims = cosine_similarity(target_emb, all_embs)[0]

    data["similarity"] = sims
    sorted_df = data.sort_values("similarity", ascending=False)
    sorted_df = sorted_df[sorted_df["id"] != student_id]

    top = sorted_df.head(10)

    return jsonify(top.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
