import streamlit as st
import tempfile
import os
from agents.send_message import process_message
import asyncio
from agents.transcribe_audio import transcribe_audio_with_speakers

st.set_page_config(
    page_title="Automatização de Issues",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 Automatização de Issues")
st.markdown("Envie um áudio da reunião ou o texto transcrito para gerar issues automaticamente")

tab_text, tab_audio = st.tabs(["📝 Texto", "🎤 Áudio"])

with tab_text:
    st.subheader("Cole o texto da reunião")
    text_input = st.text_area(
        "Texto transcrito",
        placeholder="Cole aqui a transcrição da reunião...",
        height=300,
        help="Cole o texto completo da reunião ou ata"
    )
    
    if st.button("🚀 Processar Texto", type="primary", use_container_width=True):
        if text_input.strip():
            with st.spinner("Processando texto e gerando issues..."):
                try:
                    result = asyncio.run(process_message(text_input, "thread_text", "user_text"))   
                    st.success("Issues geradas com sucesso")
                    st.text(result["response"])
                except Exception as e:
                    st.error(f"Erro ao processar: {str(e)}")
        else:
            st.warning("Por favor, insira algum texto")

with tab_audio:
    st.subheader("Faça upload do áudio da reunião")
    uploaded_audio = st.file_uploader(
        "Escolha um arquivo de áudio",
        type=["mp3", "wav", "m4a", "ogg", "flac"],
        help="Formatos aceitos: MP3, WAV, M4A, OGG, FLAC"
    )
    
    if uploaded_audio is not None:
        st.audio(uploaded_audio, format=f"audio/{uploaded_audio.type.split('/')[-1]}")
        
        if st.button("🚀 Processar Áudio", type="primary", use_container_width=True):
            with st.spinner("Transcrevendo áudio e gerando issues..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_audio.name.split('.')[-1]}") as temp_file:
                        temp_file.write(uploaded_audio.getvalue())
                        temp_path = temp_file.name
                    
                    transcription_result = transcribe_audio_with_speakers(temp_path)
                    result = asyncio.run(process_message(transcription_result, "thread_audio", "user_audio"))
                    
                    os.unlink(temp_path)
                    
                    st.success("Áudio processado e issues geradas com sucesso")
                    st.json(result)
                except Exception as e:
                    st.error(f"Erro ao processar: {str(e)}")
                    if 'temp_path' in locals():
                        os.unlink(temp_path)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
    💡 Dica: Para melhores resultados, certifique-se de que o áudio está claro ou o texto está bem formatado
    </div>
    """,
    unsafe_allow_html=True
)
