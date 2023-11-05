import os
import backoff
import openai
from openai.error import RateLimitError


@backoff.on_exception(backoff.expo, RateLimitError)
def chat(system, prompt, stop, model="gpt-3.5-turbo"):
    # print("Chatting with GPT-3.5 Turbo")
    openai.api_key = "OPENAI_API_KEY"
    openai.organization = "OPENAI_ORG_ID"
    
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    print(model)
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1,
        # max_tokens=768,
        top_p=0.95,
        stop=stop
    )["choices"][0]["message"]["content"]


@backoff.on_exception(backoff.expo, RateLimitError)
def chat4(system, prompt, model="gpt-4"):
    # print("Chatting with GPT-3.5 Turbo")
    openai.api_key = "OPENAI_API_KEY"
    openai.organization = "OPENAI_ORG_ID"
    
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ]

    print(model)
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1,
        # max_tokens=768,
        top_p=0.95,
        # stop=stop
    )["choices"][0]["message"]["content"]


@backoff.on_exception(backoff.expo, RateLimitError)
def cgptazure(system, prompt):
    engine = "athena-gpt-35-turbo"
    openai.api_type = "azure"
    openai.api_base = "https://inferenceendpointeastus.openai.azure.com/"
    openai.api_version = "2022-12-01"
    openai.api_key = "OPENAI_API_KEY"
    openai.organization = "OPENAI_ORG_ID"
    
    # system = """You are an intelligent code AI assistant. Answer with only markdown formatted python code."""

    prompt = f"""
<|im_start|>system
{system}
<|im_end|>
<|im_start|>user
{prompt}
<|im_end|>
<|im_start|>assistant
"""
    return openai.Completion.create(
        engine="athena-gpt-35-turbo",
        prompt=prompt,
        temperature=0,
        # max_tokens=350,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["<|im_end|>"]
    )["choices"][0]["text"]
