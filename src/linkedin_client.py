import httpx
from .config import LINKEDIN_API_BASE, LINKEDIN_API_KEY

HEADERS = {
    "Authorization": f"Bearer {LINKEDIN_API_KEY}",
    "Content-Type": "application/json",
}

async def send_linkedin_message(recipient_id: str, text: str):
    """
    Envoie un message sur LinkedIn via Unipile/LinkUp.
    - recipient_id : identifiant du contact ou id de conversation selon l’API.
    """
    url = f"{LINKEDIN_API_BASE}/linkedin/messages"  # adapter au path exact
    payload = {
        "recipient_id": recipient_id,
        "text": text,
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(url, json=payload, headers=HEADERS)
        resp.raise_for_status()
        return resp.json()

async def get_conversation_messages(conversation_id: str):
    """
    Optionnel : récupérer les messages d’une conversation pour vérifier si c’est le premier.
    """
    url = f"{LINKEDIN_API_BASE}/linkedin/conversations/{conversation_id}/messages"
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json()
