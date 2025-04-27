import os
from openai import OpenAI


def get_ai_response(prompt: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": """Você é um assistente de IA que responde Perguntas sobre a biblia, você é Cristão Protestante Reformado. Você deve responder de forma simples e objetiva, e sempre que possível, fornecer referências bíblicas. Responda sempre em português brasileiro.
                
                se não souber a resposta, responda que não sabe.

                muito importante: sempre forneça as referências bíblicas e sempre esteja alinhado com os princípios Biblicos/Protestantes.
                """,
            },
            {"role": "user", "content": prompt},
        ],
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if __name__ == "__main__":
    os.system("cls")
    print("Bem-vindo ao assistente de IA da biblia!")
    while True:
        i = input("Digite sua pergunta: ")
        stream = get_ai_response(i)
        for chunk in stream:
            print(chunk, end="", flush=True)
        print("\n")
