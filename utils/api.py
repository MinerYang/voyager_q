import openai

def make_api_request(client, user_input):
    try:
        response = client.chat.completions.create(
            # model="deepseek-reasoner", 
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": user_input,
                }
            ],
            max_tokens=500
        )
        text =  response.choices[0].message.content.strip()
        return text
    except openai.APIStatusError as e:
        return None
