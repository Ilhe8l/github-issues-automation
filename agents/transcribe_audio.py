import google.generativeai as genai
from agents.config import GEMINI_API_KEY
import os
from dotenv import load_dotenv

load_dotenv()

# Configurar a API Key
genai.configure(api_key=GEMINI_API_KEY)

def transcribe_audio_with_speakers(audio_path, language="português", include_timestamps=True, output_format="texto"):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {audio_path}")
    
    print("Fazendo upload do arquivo...")
    audio_file = genai.upload_file(audio_path)
    print(f"Upload concluído: {audio_file.uri}")
    
    # Usar modelo atualizado disponível
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    
    # Criar prompt para diarização de speakers
    if output_format == "json":
        prompt = f"""Transcreva o áudio fornecido em {language} e identifique os diferentes falantes.
        Retorne a transcrição em formato JSON com a seguinte estrutura:
        {{
        "falantes": ["Falante 1", "Falante 2", ...],
        "transcricao": [
            {{
            "falante": "Falante 1",
            "timestamp": "00:00",
            "texto": "texto da fala"
            }},
            ...
        ]
        }}
        Se conseguir identificar nomes dos falantes pelo contexto, use os nomes reais.
        Caso contrário, use "Falante 1", "Falante 2", etc."""
    else:
        prompt = f"""Transcreva o áudio fornecido em {language} e identifique os diferentes falantes.
Para cada pessoa que falar, identifique-a como "Falante 1", "Falante 2", etc.
Se conseguir identificar nomes pelo contexto da conversa, use os nomes reais.
"""
    
    if include_timestamps:
        prompt += "\nInclua marcações de tempo (MM:SS) no início de cada fala."
        prompt += "\n\nFormate a transcrição assim:\n[Falante 1] (00:00): Texto da fala\n[Falante 2] (00:15): Texto da fala"
    
    print("Transcrevendo áudio com identificação de falantes...")
    response = model.generate_content([prompt, audio_file])
    
    # Limpar arquivo após uso
    try:
        genai.delete_file(audio_file.name)
    except Exception as e:
        print(f"Aviso: Não foi possível deletar o arquivo: {e}")
    
    return response.text

    # Substitua pelo caminho do seu arquivo de áudio
    audio_path = "audio.mp3"
    
    try:
        # Transcrição com identificação de falantes
        transcription = transcribe_audio_with_speakers(
            audio_path, 
            language="português",
            include_timestamps=True,
            output_format="texto"  # Use "json" para saída estruturada
        )
        print(transcription)
        
    except Exception as e:
        print(f"Erro ao transcrever: {e}")