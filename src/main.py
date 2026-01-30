from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Any, Dict

from .llm_client import generate_first_reply
from .linkedin_client import send_linkedin_message, get_conversation_messages

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/webhook/linkedin")
async def linkedin_webhook(request: Request):
    """
    Webhook appelé par Unipile/LinkUp à chaque nouveau message LinkedIn.
    Le payload exact dépend du provider ; adapter les champs.
    """
    body: Dict[str, Any] = await request.json()

    try:
        event_type = body.get("event_type")
        if event_type != "message_created":
            return JSONResponse({"ignored": True})

        conversation_id = body["conversation_id"]
        message_id = body["message_id"]
        sender_id = body["sender_id"]
        sender_name = body.get("sender_name")
        text = body["text"]
        is_from_me = body.get("is_from_me", False)

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")

    # Ne pas répondre à tes propres messages
    if is_from_me:
        return {"status": "ignored_own_message"}

    # Vérifier si c'est le premier message de la conversation
    convo_messages = await get_conversation_messages(conversation_id)
    # À adapter selon la forme de la réponse API
    messages = convo_messages.get("messages", [])
    my_messages = [m for m in messages if m.get("is_from_me")]
    if my_messages:
        # Tu as déjà répondu dans cette conversation → on ne fait rien
        return {"status": "already_replied"}

    # Générer la réponse avec LLM
    reply_text = await generate_first_reply(text, sender_name=sender_name)

    # Envoyer la réponse via l'API LinkedIn
    await send_linkedin_message(recipient_id=sender_id, text=reply_text)

    return {"status": "replied", "conversation_id": conversation_id, "message_id": message_id}
