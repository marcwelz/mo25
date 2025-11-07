#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 07.11.2025 10:18
@author: marcwelz
@project: mo25
"""
import os
from openai import OpenAI

client:OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages:list = [ {"role": "system", "content":
              "You are a intelligent assistant."} ]

while True:
    user_input = input("User: ")
    if not user_input:
        continue
    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    print("ChatGPT: ", end="", flush=True)

    reply_content = ""

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=400,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            text_chunk = chunk.choices[0].delta.content
            print(text_chunk, end="", flush=True)
            reply_content += text_chunk

    print()

    messages.append({"role": "assistant", "content": reply_content})