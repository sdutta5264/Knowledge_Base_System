import requests
import json

API_URL = "http://localhost:8000/documents/chat"

HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqeW90aUBtYWlsLmNvbSIsImV4cCI6MTc4NTAwNTYzN30.bjk3KCBBvCPazBkg1O5W1864X3-jpDd92E7N3hrQ1s0",
    "Content-Type": "application/json"
}

def run_chat():
    current_chat_history = []

    while True:
        user_input = input("Please Ask: ")
        if user_input.lower() in ['quit', 'exit']:
            break;

        payload = {
            "question": user_input,
            "chat_history": current_chat_history,
            "top_k": 3
        }

        try:
            response = requests.post(API_URL, json=payload, headers= HEADERS)
            response.raise_for_status()

            data = response.json()

            print(f"\n AI: {data['answer']}")
            print(f"Sources: {data['source_documents']}")

            current_chat_history = data['updated_chat_history']
            print(f"[Debug] Network Payload contains {len(current_chat_history)} messages.\n")

        except requests.exceptions.HTTPError as e:
            print(f"API error: {e.response.text}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_chat()