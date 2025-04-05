import os
import json
import tempfile
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.parser import ResumeData
from utils.pdf_loader import extract_text_from_pdf

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables")

# Initialize LangChain model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=google_api_key,
    temperature=0.1
)
structured_model = model.with_structured_output(ResumeData)

def parse_resume_file(file_path: str) -> Dict[str, Any]:
   
    if not file_path.lower().endswith('.pdf'):
        raise ValueError("Only PDF files are supported")

    try:
        # Extract text from PDF
        with open(file_path, 'rb') as file:
            pdf_text = extract_text_from_pdf(file)
            
        if not pdf_text:
            raise ValueError("Could not extract text from PDF")

        # Prepare the prompt
        prompt = f"""
        Extract structured resume data from the following text.

        Return the data as JSON in this format:
        - personal_info: includes name, email, phone, location
        - work_experience: list of companies, titles, durations, responsibilities
        - education: list of degrees, institutions, graduation years
        - skills: list of skills
        - tech_stack: list of technologies
        - achievements: list of achievements
        - certifications: list of certifications

        Resume Text:
        {pdf_text}
        """

        # Process with LLM
        result = structured_model.invoke(prompt)
        
        # Convert to dictionary
        try:
            result_data = result.model_dump()
        except AttributeError:
            # Fallback for older Pydantic
            result_data = result.dict()

        return result_data

    except Exception as e:
        print(f"Error parsing resume: {str(e)}")
        raise

def parse_resume_text(resume_text: str) -> Dict[str, Any]:
    """
    Parse resume text directly without requiring a PDF file
    
    Args:
        resume_text: Text content of the resume
        
    Returns:
        Dict containing structured resume data
    """
    try:
       
        prompt = f"""
        Extract structured resume data from the following text.

        Return the data as JSON in this format:
        - personal_info: includes name, email, phone, location
        - work_experience: list of companies, titles, durations, responsibilities
        - education: list of degrees, institutions, graduation years
        - skills: list of skills
        - tech_stack: list of technologies
        - achievements: list of achievements
        - certifications: list of certifications

        Resume Text:
        {resume_text}
        """

        # Process with LLM
        result = structured_model.invoke(prompt)
        
        # Convert to dictionary
        try:
            result_data = result.model_dump()
        except AttributeError:
            # Fallback for older Pydantic
            result_data = result.dict()

        return result_data

    except Exception as e:
        print(f"Error parsing resume text: {str(e)}")
        raise

def save_parsed_resume(parsed_data: Dict[str, Any], output_file: str) -> None:
    """
    Save parsed resume data to a JSON file
    
    Args:
        parsed_data: The parsed resume data dictionary
        output_file: Path to save the JSON file
    """
    with open(output_file, 'w') as f:
        json.dump(parsed_data, f, indent=2)
    print(f"Results saved to {output_file}")

# Example usage
if __name__ == "__main__":
    # Test with a sample resume
    sample_resume = "harsh_resume.pdf"  
    try:
        result = parse_resume_file(sample_resume)
        print(json.dumps(result, indent=2))
        
        # Save to file
        save_parsed_resume(result, "parsed_resume.json")
    except Exception as e:
        print(f"Failed to parse resume: {e}")

