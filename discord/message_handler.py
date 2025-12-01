from transcribe_audio import transcribe_audio_with_speakers
import os


async def detect_message_type(message):
    types = []
    
    # Verifica se tem texto
    if message.content:
        types.append("text")
    
    # Verifica anexos
    if message.attachments:
        for attachment in message.attachments:
            # Verifica o tipo MIME ou extensão do arquivo
            content_type = attachment.content_type
            
            if content_type:
                if content_type.startswith("image/"):
                    types.append("image")
                    print(f"Anexo de imagem detectado: {attachment.url}")
                elif content_type.startswith("audio/"):
                    types.append("audio")
                    print(f"Anexo de áudio detectado: {attachment.url}")
                elif content_type.startswith("video/"):
                    types.append("video")
                    print(f"Anexo de vídeo detectado: {attachment.url}")
                else:
                    types.append("file")
                    print(f"Anexo de arquivo genérico detectado: {attachment.url}")
            else:
                # Fallback: verifica pela extensão
                filename = attachment.filename.lower()
                if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    types.append("image")
                elif filename.endswith(('.mp3', '.wav', '.ogg', '.m4a', '.flac')):
                    types.append("audio")
                elif filename.endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                    types.append("video")
                else:
                    types.append("file")
    
    # Verifica stickers
    if message.stickers:
        types.append("sticker")
    
    # Verifica embeds (links com preview, etc)
    if message.embeds:
        types.append("embed")
    
    return list(set(types))  # Remove duplicatas
    
async def handle_message_by_type(message):
    print("Detectando tipos de conteúdo na mensagem...")
    
    message_text = message.content + "\n"
    content_types = await detect_message_type(message)
    
    if "audio" in content_types:
        print("Processando mensagem de áudio...")
        os.makedirs("./temp", exist_ok=True)
        
        for att in message.attachments:
            if att.content_type and att.content_type.startswith("audio/"):
                audio_path = f"./temp/{att.filename}"
                
                try:
                    await att.save(audio_path)
                    transcription = await transcribe_audio_with_speakers(audio_path)
                    message_text += "Áudio transcrito: " + transcription + "\n"
                except Exception as e:
                    print(f"Erro ao processar áudio: {e}")
    
    print(message_text)
    return message_text 