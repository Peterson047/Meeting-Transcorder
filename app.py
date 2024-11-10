import streamlit as st
from st_audiorec import st_audiorec
import requests
import os
from dotenv import load_dotenv
import tempfile
from groq import Groq

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter chave de API da Groq
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Verificar se a chave de API está definida
if not GROQ_API_KEY:
    st.error("A chave da API da Groq não está definida no arquivo .env.")

# Configurar o layout da página
st.set_page_config(
    page_title="🎤 Gravador de Voz com Transcrição e Relatório",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Função para transcrever áudio
def transcribe_audio(audio_path):
    headers = {
        "Authorization": f"bearer {GROQ_API_KEY}"
    }

    data = {
        "model": "whisper-large-v3",
        "prompt": "Transcreva o áudio a seguir em Português.",
        "temperature": 0,
        "response_format": "json"
    }

    try:
        with open(audio_path, "rb") as audio_file:
            files = {
                "file": audio_file
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers=headers,
                files=files,
                data=data
            )
            response.raise_for_status()
            transcription_result = response.json()
            transcription_text = transcription_result.get("text", "")
            return transcription_text
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao transcrever o áudio: {e}")
        return ""

# Função para gerar relatório com a API da Groq
def generate_report(transcription_text):
    try:
        # Inicialize o cliente Groq com a chave de API
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.error(f"Erro ao configurar a API da Groq: {e}")
        return ""

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Você é um assistente que gera relatórios detalhados com base em transcrições de reuniões. Por favor, crie um relatório a partir do seguinte texto transcrito em Português: {transcription_text}"
                }
            ],
            model="llama3-8b-8192"
        )

        report = response.choices[0].message.content
        return report
    except Exception as e:
        st.error(f"Erro ao gerar o relatório com a Groq: {e}")
        return ""

# Função principal
def main():
    # Centralizar título e subtítulo
    st.markdown("<h1 style='text-align: center;'>🎤 Meeting Transcorder</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Grave seu áudio, transcreva-o e gere um relatório automaticamente.</h3>", unsafe_allow_html=True)

    # Adicionar linhas para delimitar os containers
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    st.markdown("---")

    # Coluna da esquerda: gravação e transcrição
    with col1:
        st.header("📼 Gravação e Transcrição")

        # Botão de envio de arquivo de áudio
        uploaded_audio_file = st.file_uploader("Envie um arquivo de áudio", type=["wav", "mp3", "m4a"])

        if uploaded_audio_file is not None:
            # Reproduzir o áudio enviado
            st.audio(uploaded_audio_file, format="audio/wav")

            # Salvar o áudio em um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
                temp_audio_file.write(uploaded_audio_file.read())
                temp_audio_path = temp_audio_file.name

            # Transcrever e mostrar a transcrição automaticamente
            st.write("Enviando áudio para transcrição...")
            transcription_text = transcribe_audio(temp_audio_path)

            if transcription_text:
                st.success("Transcrição concluída!")
                st.markdown("### Transcrição:")
                st.write(transcription_text)

                # Adicionar botão para baixar a transcrição
                st.download_button(
                    label="📥 Baixar Transcrição",
                    data=transcription_text,
                    file_name="transcricao.txt",
                    mime="text/plain",
                    key="download-transcription"
                )

                # Remover o arquivo temporário
                try:
                    os.remove(temp_audio_path)
                except PermissionError:
                    st.warning(
                        "Não foi possível remover o arquivo temporário. Por favor, feche qualquer programa que possa estar usando o arquivo e tente novamente."
                    )

        # Gravação de áudio
        st.write("Ou, grave um novo áudio abaixo:")
        wav_audio_data = st_audiorec()

        if wav_audio_data is not None:
            # Reproduzir o áudio gravado
            st.audio(wav_audio_data, format='audio/wav')

            # Adicionar botão para baixar o áudio
            st.download_button(
                label="📥 Baixar Áudio Gravado",
                data=wav_audio_data,
                file_name="gravacao.wav",
                mime="audio/wav",
                key="download-audio"
            )

            # Salvar o áudio em um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
                temp_audio_file.write(wav_audio_data)
                temp_audio_path = temp_audio_file.name

            # Transcrever automaticamente o áudio gravado
            st.write("Transcrevendo o áudio gravado...")
            transcription_text = transcribe_audio(temp_audio_path)

            if transcription_text:
                st.success("Transcrição concluída!")
                st.markdown("### Transcrição:")
                st.write(transcription_text)

                # Remover o arquivo temporário
                try:
                    os.remove(temp_audio_path)
                except PermissionError:
                    st.warning("Não foi possível remover o arquivo temporário. Tente novamente.")

    # Coluna da direita: relatório
    with col2:
        st.header("📝 Relatório")
        if 'transcription_text' in locals() and transcription_text:
            st.write("Gerando relatório a partir da transcrição...")
            report = generate_report(transcription_text)

            if report:
                st.success("Relatório gerado com sucesso!")
                st.markdown("### Relatório:")
                st.write(report)

                # Adicionar botão para baixar o relatório
                st.download_button(
                    label="📥 Baixar Relatório",
                    data=report,
                    file_name="relatorio.txt",
                    mime="text/plain",
                    key="download-report"
                )

if __name__ == "__main__":
    main()
