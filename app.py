import streamlit as st
from st_audiorec import st_audiorec
import requests
import os
from dotenv import load_dotenv
import tempfile
import google.generativeai as genai
import time
from threading import Thread

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter chaves de API
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Substitua conforme a API usada para o Gemini

# Verifique se as chaves de API estão definidas
if not GROQ_API_KEY:
    st.error("A chave da API da Groq não está definida no arquivo .env.")
if not GEMINI_API_KEY:
    st.error("A chave da API do Gemini não está definida no arquivo .env.")

# Configurar o layout da página para centralizar o conteúdo
st.set_page_config(
    page_title="🎤 Gravador de Voz com Transcrição e Relatório",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Adicionar estilo CSS personalizado para melhorar a aparência
# Adicionar estilo CSS personalizado para centralizar elementos
st.markdown(
    """
    
    """,
    unsafe_allow_html=True
)



# Função para iniciar o contador de tempo
def start_timer(container, stop_event):
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = int(time.time() - start_time)
        mins, secs = divmod(elapsed_time, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        container.metric("⏱ Tempo de Gravação", time_str)
        time.sleep(1)


# Função para gravar áudio e contar o tempo
def record_audio():
    stop_event = st.session_state.get('stop_event', None)
    if stop_event:
        stop_event.set()
    # Reiniciar a sessão de estado
    st.session_state['stop_event'] = stop_event = st.session_state.get('stop_event', Thread())

    audio_data = st_audiorec()
    return audio_data


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


# Função para gerar relatório com Gemini
def generate_report(transcription_text):
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"Erro ao configurar a API do Gemini: {e}")
        return ""

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    except Exception as e:
        st.error(f"Erro ao inicializar o modelo Gemini: {e}")
        return ""

    try:
        response = model.generate_content(
            f"Você gera relatórios de reuniões, destaca os pontos importantes debatidos e etc. Por favor, gere um relatório detalhado baseado no seguinte texto transcrito em Português: {transcription_text}"
        )
        report = response.text
        return report
    except Exception as e:
        st.error(f"Erro ao gerar o relatório com o Gemini: {e}")
        return ""


# Função para estilizar a interface usando container centralizado
def main():
    with st.container():
        st.title("🎤 Meeting Transcorder")
        st.write("Grave seu áudio, transcreva-o e gere um relatório automaticamente.")

        # Container para o contador de tempo
        timer_container = st.empty()
        stop_event = st.session_state.get('stop_event', None)

        # Exibir o componente de gravação de áudio
        wav_audio_data = st_audiorec()

        # Verificar se o áudio foi gravado
        if wav_audio_data is not None:
            # Iniciar o contador de tempo
            stop_event = st.session_state.get('stop_event', None)
            if not stop_event:
                st.session_state['stop_event'] = stop_event = Thread()
                stop_event.start()

            # Reproduzir o áudio gravado
            st.audio(wav_audio_data, format='audio/wav')

            # Adicionar botão para baixar o áudio
            st.download_button(
                label="📥 Baixar Áudio",
                data=wav_audio_data,
                file_name="gravacao.wav",
                mime="audio/wav",
                key="download-audio"
            )

            # Salvar o áudio em um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
                temp_audio_file.write(wav_audio_data)
                temp_audio_path = temp_audio_file.name

            st.write("Enviando áudio para transcrição...")

            # Enviar o áudio para a API da Groq para transcrição
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

                st.write("Gerando relatório a partir da transcrição...")

                # Gerar o relatório
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

            # Parar o contador de tempo
            if stop_event and stop_event.is_alive():
                stop_event.join()


if __name__ == "__main__":
    main()
