from memory.service import MemoryService


def main():

    service = MemoryService()

    tests = [
        "My name is Rahul.",
        "I love cricket.",
        "What is the weather today?",
        "My father taught me cricket when I was eight.",
        "Can you explain React hooks?",
    ]

    for text in tests:

        print("\nUSER:", text)

        result = service.process_message(text)

        if result:
            print("SAVED:", result)
        else:
            print("NOT SAVED")


if __name__ == "__main__":
    main()