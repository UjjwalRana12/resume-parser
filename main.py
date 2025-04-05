# main.py

import json
from agents.resume_parser import parse_resume_file
from utils.similiarity import compare_with_resume

# List of dummy existing documents/resumes/job descriptions to compare with
existing_docs = [
    "Experienced software engineer skilled in Python, Django, and REST APIs.",
    "Full-stack web developer with expertise in React and Node.js.",
    "Data scientist with experience in machine learning and deep learning projects."
]

if __name__ == "__main__":
    try:
        resume_path = "C9742.pdf"
        parsed_resume = parse_resume_file(resume_path)

        # Save parsed result
        with open("parsed_resume.json", "w") as f:
            json.dump(parsed_resume, f, indent=2)

        print("🔍 Comparing with other documents...\n")
        results = compare_with_resume(parsed_resume, existing_docs)

        for i, match in enumerate(results, 1):
            print(f"{i}. Document: {match['document']}")
            print(f"   Similarity Score: {match['similarity_score']:.2f}\n")

    except Exception as e:
        print(f"❌ Error: {e}")
