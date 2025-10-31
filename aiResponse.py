from openai import OpenAI
import os
from prompts import basic
import SQLFuntime

# Reads OPENAI_API_KEY from your environment
client = OpenAI(api_key = "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")
            #user_text: str, 
def ai_reply(num) -> str:
    messagesArr = SQLFuntime.get_messages(num)
    messages = ""

    for message in messagesArr:
        messages = messages + message + "\n\n"
    resp = client.responses.create(
        model="gpt-5",               # pick your model
        input=f"{basic.basicPromt}  {messages}"
    )
    SQLFuntime.insert_message(num, "Sarah: " + resp.output_text.strip())
    return resp.output_text.strip()

if __name__ == "__main__":
    print(ai_reply("Hey, are you open on weekends?"))