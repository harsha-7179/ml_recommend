import csv
from faker import Faker
import random

fake = Faker()

skills_pool = [
    "Python", "Java", "C++", "HTML", "CSS", "JavaScript", 
    "React", "Node.js", "SQL", "Machine Learning", 
    "Deep Learning", "Data Science", "Django", "Flask",
    "AWS", "GCP", "Docker", "Kubernetes", "TensorFlow"
]

projects_pool = [
    "Chatbot using NLP",
    "E-commerce Website",
    "Machine Learning Model for Prediction",
    "Portfolio Website",
    "AI Resume Analyzer",
    "Face Recognition System",
    "Stock Price Predictor",
    "Student Management System",
    "Weather Forecasting App",
    "Sentiment Analysis"
]

descriptions = [
    "This project uses advanced ML techniques.",
    "A web development project using modern frameworks.",
    "This system automates data processing.",
    "A complete end-to-end application.",
    "AI-powered solution for real-world problems."
]

with open("data/students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "skills", "project_title", "project_description", "passing_year"])

    for i in range(1, 10001):
        name = fake.name()
        skills = ", ".join(random.sample(skills_pool, random.randint(3, 6)))
        title = random.choice(projects_pool)
        desc = random.choice(descriptions)
        year = random.randint(2020, 2025)

        writer.writerow([i, name, skills, title, desc, year])

print("🔥 10000 Fake student records generated in data/students.csv")
