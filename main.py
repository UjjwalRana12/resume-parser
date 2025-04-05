from agents.resume_parser import parse_resume_file
from utils.similiarity import compare_with_resume
from utils.mailer import send_email

if __name__ == "__main__":
    resume = parse_resume_file("harsh_resume.pdf")

    documents = [
        "Software engineer with 5 years experience in Python, Flask, and AWS.",
        "Data analyst familiar with SQL, Excel, and Power BI.",
        "Front-end developer skilled in React, JavaScript, and CSS."
    ]

    results = compare_with_resume(resume, documents)

    email = resume.get("personal_info", {}).get("email", None)

    for match in results:
        if match["similarity_score"] >= 0.2 and email:
            subject = "Interview Invitation - Tech Role"
            content = (
                f"Hi,\n\nWe were impressed by your resume and would love to schedule an interview.\n"
                f"📅 Date: 8th April 2025\n"
                f"⏰ Time: 11:00 AM IST\n"
                f"💻 Format: Google Meet\n"
                f"\nPlease confirm your availability.\n\nRegards,\nHR Team"
            )
            send_email(email, subject, content)
        else:
            print(f"❌ Similarity too low or email missing for: {match['document']}")
