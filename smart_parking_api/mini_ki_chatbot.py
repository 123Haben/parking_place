from openai import OpenAI

# Stelle sicher, dass du deine OpenAI-API-Key hast
client = OpenAI(api_key="DEIN_API_KEY_HIER")

while True:
    frage = input("Du: ")
    if frage.lower() in ["exit", "quit", "stop"]:
        break

    antwort = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein hilfsbereiter Assistent."},
            {"role": "user", "content": frage}
        ]
    )

    print("KI:", antwort.choices[0].message.content)
