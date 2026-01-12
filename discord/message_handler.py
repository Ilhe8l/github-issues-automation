async def handle_message_by_type(message) -> str:

    # processa mensagem do discord e extrai conteúdo de texto

    message_text = message.content or ""
    has_valid_content = bool(message_text.strip())
    
    # verificar se há conteúdo não suportado
    if message.stickers or message.embeds:
        raise ValueError("conteúdo não suportado: stickers e embeds não são aceitos")
    
    # processa anexos
    if message.attachments:
        for att in message.attachments:
            filename = att.filename.lower()
            
            # aceita apenas .txt e .md
            if filename.endswith((".txt", ".md")):
                try:
                    data = await att.read()
                    file_content = data.decode("utf-8", errors="ignore")
                    message_text += f"\n[conteudo do arquivo {att.filename}]:\n{file_content}\n"
                    has_valid_content = True
                except Exception as e:
                    print(f"[x] erro ao ler arquivo {att.filename}: {e}")
            else:
                # arquivo não suportado
                raise ValueError(f"tipo de arquivo não suportado: {att.filename}")
    
    if not has_valid_content:
        raise ValueError("mensagem vazia ou sem conteúdo válido")
    
    return message_text

