
import streamlit as st
from gtts import gTTS
from groq import Groq
import io

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SAAD AI - Text to Voice",
    page_icon="🎙️",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10152b, #202b49);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #8b9cff;
}

.subtitle {
    text-align: center;
    color: #c4cbe8;
    font-size: 17px;
}

.stButton button {
    background: linear-gradient(90deg, #675cff, #a14cff);
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
    height: 45px;
    font-weight: bold;
}

.stButton button:hover {
    border: 1px solid white;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">🎙️ SAAD AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI Powered Text to Voice Converter</div>',
    unsafe_allow_html=True
)

st.write("")

st.info("Convert your written text into natural-sounding speech!")

# ---------------- GROQ CLIENT ----------------

def improve_text(text):
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        raise ValueError("Groq API key is missing!")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Improve the provided text for clear speech. "
                    "Fix grammar and punctuation while preserving "
                    "the original meaning and language. "
                    "Return only the improved text."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content.strip()


# ---------------- LANGUAGE OPTIONS ----------------

languages = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Turkish": "tr",
    "Portuguese": "pt",
    "Russian": "ru",
    "Punjabi": "pa",
    "Bengali": "bn"
}

# ---------------- USER INPUT ----------------

st.subheader("📝 Enter Your Text")

user_text = st.text_area(
    "Write something you want to convert into voice:",
    height=180,
    placeholder="Enter your text here..."
)

st.write("")

col1, col2 = st.columns(2)

with col1:
    selected_language = st.selectbox(
        "Select Language",
        list(languages.keys())
    )

with col2:
    speech_speed = st.selectbox(
        "Voice Speed",
        ["Normal", "Slow"]
    )

st.write("")

use_ai = st.checkbox(
    "✨ Improve my text using Groq AI",
    value=False
)

# ---------------- CONVERSION ----------------

if st.button("🎙️ Convert Text to Voice"):

    if not user_text.strip():
        st.warning("Please enter some text first!")

    else:
        try:
            final_text = user_text

            with st.spinner("Processing your text..."):

                # AI TEXT IMPROVEMENT
                if use_ai:
                    final_text = improve_text(user_text)

                    st.success("Text improved successfully!")

                    st.subheader("✨ Improved Text")
                    st.write(final_text)

                # TEXT TO SPEECH
                audio = gTTS(
                    text=final_text,
                    lang=languages[selected_language],
                    slow=(speech_speed == "Slow")
                )

                audio_buffer = io.BytesIO()
                audio.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

            st.success("Your voice is ready!")

            st.subheader("🔊 Listen to Your Voice")

            st.audio(
                audio_buffer,
                format="audio/mp3"
            )

            st.download_button(
                label="⬇️ Download MP3 Audio",
                data=audio_buffer.getvalue(),
                file_name="saad_ai_voice.mp3",
                mime="audio/mpeg"
            )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

# ---------------- FOOTER ----------------

st.write("---")

st.markdown(
    "<center>Made with ❤️ by SAAD KHAN | Powered by Groq AI</center>",
    unsafe_allow_html=True
)
