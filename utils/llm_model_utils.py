"""LLM Loader"""
from langchain_aws import ChatBedrock
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

from utils.constants import REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
    AWS_SESSION_TOKEN


def load_model(model_id):
    """Loads llm model"""
    return ChatBedrock(model=model_id,
                       beta_use_converse_api=True,
                       region_name=REGION,
                       aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       aws_session_token=AWS_SESSION_TOKEN)


def load_embeddings(model_id):
    """Loads embedding llm model"""
    return BedrockEmbeddings(credentials_profile_name='default',
                             region_name=REGION,
                             model_id=model_id)


def load_chroma_vector_store(collection_name, embeddings, location):
    """Loads vector store"""
    return Chroma(collection_name=collection_name,
                  embedding_function=embeddings,
                  persist_directory=location,)

