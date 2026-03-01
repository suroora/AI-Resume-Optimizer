from preprocessing.resume_parser import parse_resume
from preprocessing.text_cleaning import clean_text

file_path = "sample_resume.pdf"

raw_text = parse_resume(file_path)

cleaned_text = clean_text(raw_text)

print(cleaned_text[:1000])