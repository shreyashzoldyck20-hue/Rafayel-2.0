import httpx
from . import config

class ProviderError(Exception):
    pass

async def chat(messages: list[dict]) -> tuple[str, str]:
    # Prefer cloud when configured; if it fails, try local Ollama.
    if config.CLOUD_BASE_URL and config.CLOUD_API_KEY and config.CLOUD_MODEL:
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                r = await client.post(
                    f"{config.CLOUD_BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {config.CLOUD_API_KEY}"},
                    json={"model": config.CLOUD_MODEL, "messages": messages, "temperature": 0.7}
                )
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"], "cloud"
        except Exception:
            pass

    try:
        async with httpx.AsyncClient(timeout=90) as client:
            r = await client.post(
                f"{config.OLLAMA_BASE_URL}/api/chat",
                json={"model": config.OLLAMA_MODEL, "messages": messages, "stream": False}
            )
            r.raise_for_status()
            return r.json()["message"]["content"], "ollama"
    except Exception as exc:
        raise ProviderError(
            "No AI provider responded. Configure CLOUD_BASE_URL/CLOUD_API_KEY/CLOUD_MODEL "
            "in backend/.env, or start Ollama and pull the configured local model."
        ) from exc
