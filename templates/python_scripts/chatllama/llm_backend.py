import warnings

warnings.filterwarnings(
    "ignore",
    message=r"urllib3 v2 only supports OpenSSL 1\.1\.1\+.*",
    category=Warning,
)

from langchain_ollama import ChatOllama

DEFAULT_BASE_URL = "http://localhost:<port>"
DEFAULT_MODEL = "<model_name>"


def invoke_ollama(
    prompt: str,
    model: str = DEFAULT_MODEL,
    base_url: str = DEFAULT_BASE_URL,
    temperature: float = 0,
) -> str:
    llm = ChatOllama(model=model, base_url=base_url, temperature=temperature)
    response = llm.invoke(prompt)
    return response.content
