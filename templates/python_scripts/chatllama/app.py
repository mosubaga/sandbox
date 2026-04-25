import time

import streamlit as st

from llm_backend import DEFAULT_BASE_URL, DEFAULT_MODEL, invoke_ollama

st.set_page_config(page_title="ChatLlama", page_icon="ll", layout="wide")

st.markdown(
    """
<style>
    .block-container {
        max-width: 900px;
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        letter-spacing: -0.02em;
    }
    .top-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .top-subtitle {
        color: #4b5563;
        margin-bottom: 1rem;
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }
</style>
""",
    unsafe_allow_html=True,
)


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "model" not in st.session_state:
        st.session_state.model = DEFAULT_MODEL
    if "base_url" not in st.session_state:
        st.session_state.base_url = DEFAULT_BASE_URL


def render_sidebar() -> None:
    with st.sidebar:
        st.header("Settings")
        st.session_state.base_url = st.text_input("Ollama Base URL", st.session_state.base_url)
        st.session_state.model = st.text_input("Model", st.session_state.model)
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def stream_text(text: str) -> None:
    placeholder = st.empty()
    out = ""
    for token in text.split(" "):
        out += token + " "
        placeholder.markdown(out)
        time.sleep(0.02)
    placeholder.markdown(text)


def main() -> None:
    init_state()
    render_sidebar()

    st.markdown('<div class="top-title">ChatLlama</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="top-subtitle">Local LLM chat powered by Ollama + LangChain</div>',
        unsafe_allow_html=True,
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input("Send a message")
    if not user_prompt:
        return

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = invoke_ollama(
                    user_prompt,
                    model=st.session_state.model,
                    base_url=st.session_state.base_url,
                    temperature=0,
                )
            stream_text(answer)
    except Exception as exc:  # noqa: BLE001
        answer = f"Request failed: {exc}"
        with st.chat_message("assistant"):
            st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
