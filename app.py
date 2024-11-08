import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
import threading
import wave

st.title("🎤 Gravador de Voz com Streamlit")

# Configurações do WebRTC
WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"audio": True, "video": False},
)

# Lista para armazenar os frames de áudio
audio_frames = []
lock = threading.Lock()

def main():
    if 'recording' not in st.session_state:
        st.session_state['recording'] = False

    if st.button("Iniciar Gravação"):
        st.session_state['recording'] = True

    if st.button("Parar Gravação"):
        st.session_state['recording'] = False

    if st.session_state['recording']:
        webrtc_ctx = webrtc_streamer(
            key="key",
            mode=WebRtcMode.RECVONLY,
            client_settings=WEBRTC_CLIENT_SETTINGS,
            audio_receiver_size=256,
            media_stream_constraints={"audio": True, "video": False},
            async_processing=True,
        )

        if webrtc_ctx.audio_receiver:
            audio_receiver = webrtc_ctx.audio_receiver

            while True:
                if not st.session_state['recording']:
                    break
                try:
                    audio_frame = audio_receiver.get_frames(timeout=1)
                except:
                    continue
                if len(audio_frame) == 0:
                    continue
                frame = audio_frame[0]
                audio = frame.to_ndarray()
                with lock:
                    audio_frames.append(audio)

    if st.button("Salvar Gravação"):
        save_audio(audio_frames)
        st.success("Gravação salva com sucesso!")

def save_audio(frames):
    # Combinar todos os frames de áudio
    with lock:
        audio = np.concatenate(frames)

    # Configurações do arquivo WAV
    sample_rate = 48000  # Taxa de amostragem padrão
    sample_width = 2     # 2 bytes por amostra
    n_channels = 1       # Mono

    # Salvar em um arquivo WAV
    wf = wave.open("gravacao.wav", "wb")
    wf.setnchannels(n_channels)
    wf.setsampwidth(sample_width)
    wf.setframerate(sample_rate)
    wf.writeframes(audio.tobytes())
    wf.close()

if __name__ == "__main__":
    main()
