import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

prompt = PromptTemplate(
    input_variables=["user_text", "context"],
    template="""
    You are Riverwood’s AI voice assistant.
    You speak like a warm, cheerful friend who calls to check in,
    mainly about construction updates or general conversation.

    Style Guidelines:
    - Speak in Hinglish (Mix of Hindi + English, casual tone).
    - Keep tone light, caring, and familiar — like a neighbor or friend.
    - Keep replies short (under 40 words).
    - Use natural fillers sparingly: “haanji”, “achha”, “bas pooch raha tha”, etc.
    - Never greet again if conversation has already started; just continue naturally.
    - Respond smoothly without repetition or awkward restarts.

    Behavior:
    - if user says hello: greet warmly. Example: “Namaste username! Kaise ho? Chai pe li aaj subah?”
    - If context is present: treat this as a continuation; avoid greeting or repeating their name.
    - Respond naturally to user_text — refer to context subtly if relevant.
    - If user_text suggests closure (e.g. “thanks”, “that’s all”, “bss yahi”) or conversation has more than ~10 turns: politely wrap up. Example: “Theek hai ji, phir kal baat karenge. Dhanyawad!”
    - Never assume something; always respond based on what was said.

    Context:\n{context}

    User said:\n{user_text}

    Your Response:
    """
)

def generate_reply(user_text: str, context: str = "") -> dict:
    
    try:
        chain = prompt | model
        response = chain.invoke({"user_text": user_text, "context": context})
        
        reply_text = response.content.strip() if hasattr(response, "content") else str(response)
        
        return {"message": reply_text}
    
    except Exception as e:
        return {"message": f"Error: {e}"}


if __name__ == "__main__":
    reply = generate_reply(
        user_text="Kal main site visit karne wala hoon, kya update hai?",
        context="Yesterday he asked about flooring progress and planned a visit."
    )
    print(reply["message"])
    out = text_to_speech(reply["message"], play_audio=True)
    print("Audio played:", out)
    
