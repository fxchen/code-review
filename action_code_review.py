#!/usr/bin/env python3
import os
import sys
import openai

REQUEST = "Reply on how to improve the code for style, clarity, comments, and tests (below)\n"

STYLES = {
"zen": "Format feedback in the style of a zen koan",
"concise": "Format feedback concisely with numbered list"
}

PERSONAS = {
"developer": "You are an experienced software developer in a variety of programming languages and methodologies. You create efficient, scalable, and fault-tolerant solutions",
"kent_beck": "You are Kent Beck. You are known for software design patterns, test-driven development (TDD), and agile methodologies",
"marc_benioff": "You are Marc Benioff, internet entrepreneur and experienced software developer",
"yoda": "You are Yoda, legendary Jedi Master. Speak like Yoda",
}

openai.api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["MODEL"]
persona = PERSONAS[os.environ["PERSONA"]]
style = STYLES[os.environ["STYLE"]]

prompt = f"{persona}.{style}.{REQUEST}\n```\n{diff}```"

diff = sys.stdin.read()

kwargs = {'model': model}
kwargs['temperature'] = 0.5
kwargs['max_tokens'] = 1024
kwargs['messages']=[{"role": "system", "content": prompt}]
try:
  response  = openai.ChatCompletion.create(**kwargs)
  if response.choices:
    if 'text' in response.choices[0]:
      review_text = response.choices[0].text.strip()
    else:
      review_text = response.choices[0].message.content.strip()
  else:
    review_text = f"No response from OpenAI\n{response.text}"
except Exception as e:
  review_text = f"OpenAI failed to generate a review: {e}"

print(f"{review_text}")
