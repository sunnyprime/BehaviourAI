from app.llm import ask_llm
from app.profile_loader import BehaviorProfileLoader


QUESTION = "Bhai kya kar rahe ho?"


def test_without_profile():

    prompt = f"""
Respond naturally to this message:

{QUESTION}

Keep the answer short and conversational.
"""

    return ask_llm(prompt)


def test_with_profile():

    profile = (
        BehaviorProfileLoader(
            source="prototype"
        ).format_for_prompt()
    )

    prompt = f"""
You are a conversational AI using an observed
communication-style profile.

OBSERVED STYLE:

{profile}

USER MESSAGE:

{QUESTION}

Respond naturally using the observed style.

Do not copy the profile mechanically.
Do not invent memories or personal experiences.
Do not claim to be the represented person.
Keep the response short.
"""

    return ask_llm(prompt)


def main():

    print("================================")
    print("      STYLE COMPARISON TEST")
    print("================================")

    print("\nQUESTION:")
    print(QUESTION)

    print("\n-------------------------------")
    print("WITHOUT BEHAVIOR PROFILE")
    print("-------------------------------")

    response_1 = test_without_profile()

    print(response_1)

    print("\n-------------------------------")
    print("WITH BEHAVIOR PROFILE")
    print("-------------------------------")

    response_2 = test_with_profile()

    print(response_2)


if __name__ == "__main__":
    main()