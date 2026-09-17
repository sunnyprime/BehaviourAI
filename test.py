import subprocess

result = subprocess.run(
    ["ollama", "ps"],
    capture_output=True,
    text=True
)

print(result.stdout)