import os, json
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_to_dict, messages_from_dict

MEMORY_DIR = "memories"
os.makedirs(MEMORY_DIR, exist_ok=True)

def save_memory_to_file(session_id: str, memory: ConversationBufferMemory):
    """Save memory of a user to a JSON file."""
    print(f">>> Saving session ID: {session_id}")
    filepath = os.path.join(MEMORY_DIR, f"{session_id}.json")
    with open(filepath, "w") as f:
        json.dump(messages_to_dict(memory.chat_memory.messages), f, indent=2)
    # print(f">>> Saved following memory content: \n{memory}")

def load_memory_from_file(session_id: str) -> ConversationBufferMemory:
    """Load memory of a user from a JSON file, or return fresh memory if none exists."""
    print(f">>> Loading session ID: {session_id}")
    session_ui_messages = []
    filepath = os.path.join(MEMORY_DIR, f"{session_id}.json")
    memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
            memory.chat_memory.messages = messages_from_dict(data)
            # print(f">>> load_memory_from_file: Loaded following chat messages:\n{memory.chat_memory.messages}")

            for chat in data:
                if chat['type'] == 'human':
                    session_ui_messages.append({"role": "user", "content": chat["data"]["content"]})
                else:
                    for line in eval(chat["data"]["content"]):
                        session_ui_messages.append({"role": "assistant", "content": line})
    return memory, session_ui_messages
