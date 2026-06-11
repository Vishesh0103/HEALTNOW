
import streamlit as st
import google.generativeai as genai

gemini_api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel("gemini-3.5-flash")

SYSTEM_PROMPT = """
You are a health-focused AI assistant.

Rules:
- Only answer questions related to health, fitness, nutrition, mental health, or medicine.
- If a question is unrelated to health, politely refuse and say:
  "I can only help with health-related questions."
- Give clear, simple, and accurate explanations.
- Avoid giving dangerous or unsafe medical advice.
- Suggest consulting a doctor for serious issues.
- Keep answers concise and easy to understand.
"""

st.set_page_config(page_title="HEALTHNOW")

st.title("HEALTHNOW")
st.subheader("VISHESH'S HEALTH BOT")
st.markdown(
    """
    <style>
    
    /* Main background */
    .stApp {
        background: linear-gradient(to right, #0f0f0f, #3b0000);
        color: white;
    }

    /* Header (top bar) */
    header {
        background-color: #7a0000 !important;
    }

    /* Footer (bottom bar) */
    footer {
        background-color: #4a0000 !important;
        color: white;
    }

    /* Optional: remove Streamlit branding spacing */
    footer:after {
        content: '';
        display: block;
        height: 0px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.info("""
⚠️ **Important Instructions**

- This chatbot is for informational purposes only.
- Always consult a qualified doctor for medical advice.
- Do not rely on this bot in emergencies.
- Avoid sharing sensitive personal health data.
- Follow basic hygiene and safety precautions.

Stay safe and use responsibly.
""")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    conversation_text = ""

    for message in st.session_state.chat_history:

        if message["role"] == "user":
            conversation_text += f"User: {message['content']}\n"

        else:
            conversation_text += f"Assistant: {message['content']}\n"

    full_prompt = f"""
{SYSTEM_PROMPT}

{conversation_text}

Assistant:
"""

    try:
        response = model.generate_content(full_prompt)
        assistant_reply = response.text

    except Exception as e:
        assistant_reply = f"Error: {str(e)}"

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    st.rerun()

if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
