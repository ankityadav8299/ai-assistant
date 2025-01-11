import google.generativeai as genai

genai.configure(api_key="AIzaSyASTjhJI80UJvowouC55vNED4uY7ksYNR8")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)