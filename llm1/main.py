import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from psycopg2.extras import execute_values
from  ingest_data import *
from get_similar_embeddings import *
from ask_llm import *

from code_execution.main import run_command
from chat_history.main import save_response
from chat_history.main import get_similar_chats


if __name__ == "__main__":

    # code_directory ="/home/rajneesh/Desktop/Enigma"
    # code_directory ="/home/rajneesh/IdeaProjects/SkillShare"
    code_directory = "/home/rajneesh/raapid-audit-apigateway"
    process_and_ingest_data(code_directory)

    
    while True:
        query_prompt = input("\n\nenter your query : ")
        intial_query=query_prompt


        query_embedding = generate_embedding_locally(query_prompt)
        similar_embeddings = find_similar_embeddings(query_embedding)
        similar_past_chats = get_similar_chats(query_prompt)

        # print(similar_embeddings)
        for _, _, file_content in similar_embeddings:
            print(file_content)
        print("\n\n")
        print(similar_past_chats)
        print("\n\n\n")

        # print("hi\n")
        context = "\n\n".join([f"File: {file_path}\nContent: {file_content}" for _, file_path, file_content in similar_embeddings])
        past_context = "\n\n".join([f"Past prompt: {query}\nResponse: {response}\n Similarity:  {similarity}" for _, query, response, similarity in similar_past_chats])
        # print("hi1\n")
        
        query_prompt = f"{query_prompt}\n\nContext from past conversation:\n{past_context}\n\nContext from the memory:\n{context}"
        response = llm_response(query_prompt)

        print("\nResponse:\n", response)

        feedback= input("\n\n\nhow helpful was it ? rate from 1 to 5 :)")
        feedback_text = input ("\n\nwhat could have been done better... where i made mistakes/or skipped somtthing ? :")

        chat_record = {
            "query": intial_query,
            "response": response,
            "feedback": feedback,
            "feedback_text": feedback_text
        }
        #  save only good response
        if int(feedback)>=3 :
            save_response(chat_record)
        