from promptflow import tool
import re

@tool
def my_python_tool(question: str) -> str:

    #remove all chars except those in square brackets
    question = re.sub('[^A-Za-z0-9 ,.?-@£]+', '', question)

    #Trim to 500 chars and return
    return question[0:200]
