import httpx
from .config import OPENAI_API_KEY, BOT_PUBLIC_LINK

LLM_API_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = f"""
Tu es l’assistant LinkedIn officiel de MyPaddock, une application qui accompagne les particuliers et les professionnels dans la gestion, le suivi et la valorisation de leurs véhicules.
Tu réponds aux nouveaux messages exclusivement en français, avec un ton professionnel, chaleureux et orienté solution.
Tes réponses sont claires, concises et apportent une valeur immédiate.
Chaque message se termine impérativement par une phrase invitant à utiliser ce lien : {BOT_PUBLIC_LINK}.
Tu ne dépasses jamais 5 phrases.
"""

async def generate_first_reply(message_text: str, sender_name: str | None = None) -> str:
    user_context = f"Message reçu de {sender_name or 'un contact'} : {message_text}"
    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_context},
        ],
        "temperature": 0.6,
        "max_tokens": 300,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(LLM_API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
