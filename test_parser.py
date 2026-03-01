from preprocessing.resume_parser import parse_resume

# Put your resume file path here
file_path = "sample_resume.pdf"

text = parse_resume(file_path)

print(text[:1000])   # print first 1000 characters