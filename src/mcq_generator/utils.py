import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def get_table_data(quiz_dict):
    try:
        quiz_table_data = []

        for _, value in quiz_dict.items():
            quiz_table_data.append({
                "Question": value["question"],
                "Choice1": value["options"].get("A", ""),
                "Choice2": value["options"].get("B", ""),
                "Choice3": value["options"].get("C", ""),
                "Choice4": value["options"].get("D", ""),
                "Correct": value["answer"]
            })

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None
