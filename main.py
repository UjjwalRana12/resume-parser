import json
from agents.resume_parser import parse_resume_file
from utils.similiarity import compare_with_resume
from utils.mailer import send_email
from utils.db import Session, Resume


resume_path = "harsh_resume.pdf"  
parsed_resume = parse_resume_file(resume_path)


job_descriptions = [
    "Looking for a backend developer skilled in Python, Django, and PostgreSQL.",
    "Hiring frontend developer experienced with React and modern CSS frameworks.",
    "We need a full stack engineer with experience in AWS, Docker, and microservices."
]


results = compare_with_resume(parsed_resume, job_descriptions)


session = Session()
top_match = results[0]
similarity_score = top_match["similarity_score"]
email = parsed_resume["personal_info"].get("email")
name = parsed_resume["personal_info"].get("name")

print(f"Top Similarity Score: {similarity_score * 100:.2f}%")

Threshold = 40
if similarity_score * 100 >= Threshold:
    resume_entry = Resume(
        name=name,
        email=email,
        similarity_score=similarity_score,
        data=parsed_resume
    )
    session.merge(resume_entry)
    session.commit()

    subject = "Interview Invitation for Your Resume"
    content = f"""
Hi {name},

We were impressed by your resume and would like to invite you for an interview.

📅 Date: 10th April 2025  
🕒 Time: 11:00 AM  
📍 Mode: Google Meet (link will be shared soon)

Please confirm your availability by replying to this email.

Best regards,  
Recruitment Team
"""
    try:
        send_email(email, subject, content)
    except Exception as e:
        print(f"❌ Error sending email: {e}")
else:
    print("Similarity score too low. No email sent.")
