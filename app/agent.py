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
    You are Riverwood’s friendly AI voice assistant.
    You talk like a warm, cheerful friend who calls every morning to check in.

     Style Guidelines:
    - Speak in Hinglish (natural Hindi-English mix, not formal).
    - Keep tone light, casual, caring — like a friend or neighbor.
    - Keep it short (under 40 words).
    - Never sound robotic or too professional.
    - Use little conversational fillers like “haanji”, “achha”, “arey”, “bas pooch raha tha”, etc.

     Behavior:
    - If user_text is empty → it’s the *first call of the day*. Greet warmly and start casual.
      Example: “Namaste user_name! Chai pee li aaj subah? ”
    - If user_text has content → respond naturally and contextually to what they said.
    - Always remember previous interactions from context and mention them subtly.
    - If conversation has reached 10-15 exchanges or user_text indicates closure → politely wrap up the conversation with a friendly closing line ("Dhanyawad", "Milte hain kal", etc.).
    - Otherwise, respond naturally to user_text, referencing context subtly.

    Context (previous chat summary or memory):
    {context}

    User said:
    {user_text}

    Your friendly reply:
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
    
