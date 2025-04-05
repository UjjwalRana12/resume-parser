import os
import json
from dotenv import load_dotenv
from pdf_loader import resume_text  
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", 
    google_api_key=google_api_key,
    temperature=0.1
)

class PersonalInfo(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address of the candidate")
    phone: str = Field(description="Phone number of the candidate")
    location: str = Field(description="Location/address of the candidate")

class WorkExperience(BaseModel):
    company: str = Field(description="Company name")
    title: str = Field(description="Job title")
    duration: str = Field(description="Duration of employment")
    responsibilities: List[str] = Field(description="List of job responsibilities")

class Education(BaseModel):
    degree: str = Field(description="Degree obtained")
    institution: str = Field(description="Name of the educational institution")
    graduation_year: str = Field(description="Year of graduation")

class ResumeData(BaseModel):
    personal_info: PersonalInfo = Field(description="Personal information of the candidate")
    work_experience: List[WorkExperience] = Field(description="Work experience details")
    education: List[Education] = Field(description="Education details")
    skills: List[str] = Field(description="List of skills")
    TechStack: List[str] = Field(description="List of technologies used")
    Achievements: List[str] = Field(description="List of achievements")
    Certifications: List[str] = Field(description="List of certifications")


structured_model = model.with_structured_output(ResumeData)


try:
   
    prompt = f"""
    Extract the structured information from this resume:
    
    {resume_text}
    
    Provide the information in a structured format with personal info, work experience, education, and skills.
    """
    

    result = structured_model.invoke(prompt)
    
    if result:
        
        result_dict = result.dict()
        print(json.dumps(result_dict, indent=2))
        
        
        with open("parsed_resume.json", "w") as f:
            json.dump(result_dict, f, indent=2)
        print("Results saved to parsed_resume.json")
        
except Exception as e:
    print(f"Error parsing resume: {e}")





