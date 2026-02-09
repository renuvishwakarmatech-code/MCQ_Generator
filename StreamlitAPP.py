from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
from dotenv import load_dotenv
import json
import traceback
import streamlit as st
from src.mcq_generator.logger import logging
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.MCQGenerator import generate_evaluate_chain

#loading json data from file
with open("Response.json","r") as file:
    RESPONSE_JSON=json.load(file)

#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)

    # Quiz level
    level=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    #Add Button
    button=st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and level:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                response=generate_evaluate_chain.invoke(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "level": level,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    #Extract the quiz data from the response
                    table_data=get_table_data(response)
                    if table_data is not None:
                        df=pd.DataFrame(table_data)
                        df.index=df.index+1
                        st.table(df)
                    else:
                        st.error("Error in the table data")

                else:
                    st.write(response)