async def handle_message_by_type(message) -> str:
    # processa mensagem do discord e extrai conteúdo de texto
    message_text = message.content or ""
    if message.stickers: 
        raise ValueError("conteúdo não suportado: stickers não são aceitos")
    
    # processa anexos
    valid_attachments_found = False
    
    if message.attachments:
        for att in message.attachments:
            filename = att.filename.lower()
            
            # aceita apenas .txt, .md e .json
            if filename.endswith((".txt", ".md", ".json")):
                try:
                    data = await att.read()
                    file_content = data.decode("utf-8", errors="ignore")
                    message_text += f"\n\n[conteudo do arquivo {att.filename}]:\n{file_content}\n"
                    valid_attachments_found = True
                except Exception as e:
                    print(f"[x] erro ao ler arquivo {att.filename}: {e}")
            else:
                # apenas ignora arquivos não suportados
                print(f"[i] ignorando arquivo não suportado: {filename}")
                continue

    has_valid_content = bool(message_text.strip()) or valid_attachments_found

    if not has_valid_content:
        raise ValueError("mensagem vazia ou sem conteúdo válido (envie texto ou arquivos .txt, .md, .json)")
    
    return message_text
