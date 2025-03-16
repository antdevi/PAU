from openai import OpenAI

client = OpenAI()

def query_aiengines(user_message, system_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message},
                    {"role": "system", "content": system_prompt},
                  
                  ],
        temperature = 0
    )
    return response.choices[0].message.content