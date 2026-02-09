from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
from dotenv import load_dotenv
import json

load_dotenv()

RESPONSE_JSON = {
    "1":{
        "question" : "multiple choice question",
        "options" : {
            "A" : "option A",
            "B" : "option B",
            "C" : "option C",
            "D" : "option D"
        },
        "answer" : "correct option",
    },
    "2":{
        "question" : "multiple choice question",
        "options" : {
            "A" : "option A",
            "B" : "option B",
            "C" : "option C",
            "D" : "option D"
        },
        "answer" : "correct option",
    },
    "3":{
        "question" : "multiple choice question",
        "options" : {
            "A" : "option A",
            "B" : "option B",
            "C" : "option C",
            "D" : "option D"
        },
        "answer" : "correct option",
    }
}

TEMPLATE = """
Text:
{text}

You are an expert MCQ generator.

Create {number} multiple choice questions for {subject} students at {level} level.

Rules:
- Do NOT repeat questions
- Each question must have exactly 4 options (A, B, C, D)
- Answer must be one of A/B/C/D
- Output ONLY valid JSON
- Follow this structure exactly

JSON FORMAT:
{response_json}
"""

quiz_prompt = ChatPromptTemplate.from_template(TEMPLATE)

llm = ChatGroq(model="qwen/qwen3-32b", temperature=0, 
        model_kwargs={
        "response_format": {"type": "json_object"}
    })

quiz_chain = quiz_prompt | llm | JsonOutputParser()

file_path = 'experiment/data.txt'
with open(file_path, 'r') as file:
    TEXT = file.read()

json.dumps(RESPONSE_JSON)

NUMBER = 3
SUBJECT = "Machine Learning"
LEVEL = "beginner"

response = quiz_chain.invoke(
    {
        "text": TEXT,
        "number": NUMBER,
        "subject": SUBJECT,
        "level": LEVEL,
        "response_json": json.dumps(RESPONSE_JSON)
    }
)

rows = []

for q_id, q in response.items():
    rows.append({
        "question_id": q_id,
        "question": q["question"],
        "option_A": q["options"]["A"],
        "option_B": q["options"]["B"],
        "option_C": q["options"]["C"],
        "option_D": q["options"]["D"],
        "correct_answer": q["answer"]
    })

df = pd.DataFrame(rows)

df.to_csv("mcq_quiz.csv", index=False)
print("✅ CSV saved as mcq_quiz.csv")
