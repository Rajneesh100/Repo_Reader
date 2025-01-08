import os
import psycopg2
from psycopg2.extras import execute_values
import requests
import json
import numpy as np

from sentence_transformers import SentenceTransformer






POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "Rajneesh@2024"


# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding_locally(content):
    return embedding_model.encode(content).tolist()

def process_code_files(directory_path):
    data = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                embedding = generate_embedding_locally(content)
                data.append({
                    "file_path": file_path,
                    "file_content": content,
                    "embedding": embedding
                })
    ingest_data_to_postgres(data)





def ingest_data_to_postgres(data, table_name="code_vectors"):
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            file_path TEXT,
            file_content TEXT,
            embedding FLOAT8[]
        );
        """)
        conn.commit()

        values = [
            (item["file_path"], item["file_content"], item["embedding"])
            for item in data
        ]
        execute_values(cursor, f"INSERT INTO {table_name} (file_path, file_content, embedding) VALUES %s", values)
        conn.commit()

        cursor.close()
        conn.close()
        print("Data ingestion completed.")
    except Exception as e:
        print(f"Error ingesting data: {str(e)}")



def process_and_ingest_data(directory_path):
    data = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                # content = f.read()
                content = f.read().replace("\x00", "")
                embedding = generate_embedding_locally(content)
                data.append({
                    "file_path": file_path,
                    "file_content": content,
                    "embedding": embedding
                })
    ingest_data_to_postgres(data)