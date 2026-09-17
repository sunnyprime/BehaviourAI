from ollama import chat

response = chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": "Explain in simple words what an AI assistant is."
        }
    ]
)

print("\nAI Response:")
print(response["message"]["content"])