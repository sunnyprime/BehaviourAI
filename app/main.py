from app.engine import AIEngine


def main():
    print("================================")
    print("        MemorialAI")
    print("================================")
    print("Type 'exit' to quit.\n")

    engine = AIEngine()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "exit()", "/bye", "quit", "quit()"}:
                print("Goodbye!")
                break

            if not user_input:
                continue

            response = engine.respond(user_input)

            print("\nAI:", response)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()