from typing import Union
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from config import LLM_PROVIDER, LLM_MODEL, LLM_API_KEY


def create_llm(temperature: float = 0.3) -> Union[ChatOpenAI, ChatGoogleGenerativeAI]:
    # cria e retorna uma instância do llm configurado
   
    # gemini ainda não está funcionando
    if LLM_PROVIDER == "gemini":
        return ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            temperature=temperature,
        )
    
    elif LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            temperature=temperature,
        )
    
    else:
        raise ValueError(f"provedor de llm desconhecido: {LLM_PROVIDER}")
