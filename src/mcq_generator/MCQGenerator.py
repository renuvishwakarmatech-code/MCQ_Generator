from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
from dotenv import load_dotenv
import json
from src.mcq_generator.logger import logging
from src.mcq_generator.utils import read_file, get_table_data

load_dotenv()

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

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, 
        model_kwargs={
        "response_format": {"type": "json_object"}
    })

generate_evaluate_chain = quiz_prompt | llm | JsonOutputParser()


