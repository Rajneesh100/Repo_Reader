from .chat_processing import process_and_ingest_chat_data
from .chat_processing import find_similar_chat


def save_response(chat_record):
    process_and_ingest_chat_data(chat_record)

def get_similar_chats(query):
    return find_similar_chat(query)
