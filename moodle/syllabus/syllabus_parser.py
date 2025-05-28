from google import genai
import pdfplumber
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

pdf_file = "./moodle/syllabus/test_syllabus.pdf"

with pdfplumber.open(pdf_file) as pdf:
    extracted_text = ''
    for page in pdf.pages:
        extracted_text += page.extract_text()

client = genai.Client(api_key=os.getenv("genai_api"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"Give me the answer as a json file only. You need to analyze this text and give information of every assigment that affects the grade as a json file. Give information about assignment name, its weight and date (if none, then none). Also add info about attendance, also in json (maximum absence, and penalty as an object too, to easily read json). Here the texts itself:\n {extracted_text}",
)

print(response.text)