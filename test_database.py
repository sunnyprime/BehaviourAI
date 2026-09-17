from memory.database import save_message, get_messages


conversation_id = "test-001"

save_message(
    conversation_id,
    "user",
    "My name is Rahul."
)

save_message(
    conversation_id,
    "assistant",
    "Nice to meet you, Rahul."
)

messages = get_messages(conversation_id)

for message in messages:
    print(message)