from click import prompt
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Loading Local Embedding Model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model Loaded successfully...")

class AIService:
    @staticmethod
    def generate_embedding(text: str) -> list[float]:
        vector_array = model.encode(text)
        return vector_array.tolist()

    @staticmethod
    def generate_chat_response(system_prompt: str, chat_history: list, current_question:str):
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt
        )

        gemini_messages = []

        for msg in chat_history:
            mapped_role = "model" if msg.role == "assistant" else "user"

            if msg.role == "system":
                continue

            gemini_messages.append({
                "role": mapped_role,
                "parts": [msg.content]
            })

            try:
                response = model.generate_content(
                    gemini_messages,
                    generation_config=genai.GenerationConfig(temperature=0.2),
                    safety_settings= {
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                    }
                )
                print("response---->", response)
                return response.text
            except Exception as e:
                return f"Error connecting Gemini API: {str(e)}"

    @staticmethod
    def summarize_conversation(chat_history: list):
        model = genai.generative_model("gemini-2.5-flash")

        transcript = "\n".join([f"{msg.role.upper()}: {msg.content}" for msg in chat_history])
        prompt= f"Summarize this conversation into 3 concise bullet points focusing on key facts and user preference: \n\n{transcript}"

        try:
            response = model.generate_content(
                prompt,
                generation_config = genai.GenerationConfig(temprature=0.1)
            )
            return response.text
        except Exception as e:
            return "Previous Conversation summarized"