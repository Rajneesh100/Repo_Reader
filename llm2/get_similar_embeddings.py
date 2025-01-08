

import os
import psycopg2
from psycopg2.extras import execute_values
import requests
import json
import numpy as np


from  ingest_data import *



POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "Rajneesh@2024"

def find_similar_embeddings(query_embedding, table_name="code_vectors", top_k=5):
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        
        # Query to find the most similar embeddings
        cursor.execute(f"""
        SELECT file_path, file_content, embedding 
        FROM {table_name};
        """)
        rows = cursor.fetchall()

        # Calculate cosine similarity
        similarities = []
        for file_path, file_content, embedding in rows:
            embedding_np = np.array(embedding)
            similarity = np.dot(query_embedding, embedding_np) / (np.linalg.norm(query_embedding) * np.linalg.norm(embedding_np))
            similarities.append((similarity, file_path, file_content))
        
        # Sort by similarity and return top_k results
        similarities.sort(reverse=True, key=lambda x: x[0])
        return similarities[:top_k]
    except Exception as e:
        print(f"Error querying database: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()