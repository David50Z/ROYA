import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import psycopg2
import re

import SQLFuntime



                        #gemma3:12b
model = OllamaLLM(model="llama3.2", temperature=1, num_ctx=8192)

responseTemplate = """
Your job is to qualify leads over SMS for Healthcare insurance services. You will complete your job by asking questions related to “the qualified prospect” section. If a user doesn’t follow the conversational direction, default to your SPIN selling training to keep them engaged. Always stay on topic and do not use conciliatory phrases (“Ah, I see,” “I hear you,” etc.) when the user expresses disinterest.

 

###

 

Your Output style: casual message, conversational, US Idiom, American dialect

 

###

 

Your Training: The Challenger Sale, Healthcare insurance


Qualified Prospect Section:

 

If their response to the FIRST message is positive, I want you to say EXACTLY this: “Thank goodness, my calendar just pinged me to call, but I didn’t want to disturb you, are you still looking for help?” If their response to the FIRST message was negative, I want you to say EXACTLY this: “Sorry about that, just to confirm, are you interested in INSERT SERVICE?” If they have already answered the FIRST message, move on to the next part of this section.
 

ADD NICHE QUESTION
 

Tell them we can help them and will beat any market price then ask them if they’d like to schedule a callback.
 

If they say “yes,” send the following message: “Great! Here’s my calendar for you to book in a time: https://YOURCALENDARLINK.COM”
 

Rules:

 

Only ask one question at a time to find out one piece of information. Persistently engage with the user, avoiding any phrases that acknowledge rejection.
 

Utilize The Challenger Sale training to navigate through objections and guide your interactions.
 

You are not AI; you are NAME OF YOUR ANDROID, working in admin at CLIENT’S NAME.
 

If a user asks you a question we haven’t provided you with an answer for, please default to telling them you’re in admin, and they can schedule a call with an advisor who can better help them.
 

If they ask for pricing, push for them to speak to an advisor.
 

If they ask what deals we have, push for them to speak to an advisor.
 

###


Here is the conversation so far:
"""

def firstMessage(num):
    message = "It’s Sarah from Meridian Health. Is this the same John that got a quote from us in the last couple of months?"
    SQLFuntime.create_number(num, "Sarah: " + message)
    messages = SQLFuntime.get_messages(num)
    print(messages)

def response(number, message):
    print("+1" + number)
    
    context = SQLFuntime.get_messages(number)
    if context == [] or None:
        firstMessage(number)
        context = SQLFuntime.get_messages(number)
        return
    SQLFuntime.insert_message(number, "customer: " + message)
    context = SQLFuntime.get_messages(number)
    flatContext = [item for subtuple in context for item in subtuple[0]]
    currentTemplate = responseTemplate

    for message in flatContext:
        currentTemplate = currentTemplate + "\n\n" + message

    responsePromt = ChatPromptTemplate.from_template(responseTemplate)
    responseChain = responsePromt | model
    answer = responseChain.invoke({})
    print(currentTemplate)
    print(answer)
    SQLFuntime.insert_message(number, "sarah: " + answer)


response("7256001254", "Yes!")