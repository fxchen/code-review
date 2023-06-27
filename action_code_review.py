#!/usr/bin/env python3
import os
import sys
import openai
import re

def extract_filenames_from_diff(diff_text):
  """
  This function extracts filenames from git diff text using regular expressions.
  
  :param diff_text: str, git diff text
  :return: list of str, list of filenames
  """

  # Pattern for lines that start with '+++ b/', which are lines that contain filenames
  # of the "new version" files in the diff. The parentheses (.) create a group that
  # captures the filename that follows '+++ b/'.
  pattern = r'\+\+\+ b/(.*)'

  # re.findall function finds all matches of the pattern in the diff_text
  # and returns them as a list.
  filenames = re.findall(pattern, diff_text)

  return filenames

def format_file_contents(filenames):
  """
  This function iteratively goes through each filename and concatenates
  the filename and its content in a specific markdown format.

  :param filenames: list of str, list of filenames
  :return: str, formatted string
  """
  files_str = ""
  for filename in filenames:
    with open(filename, 'r') as file:
      content = file.read()
    files_str += f"\n{filename}\n```\n{content}\n```\n"
  return files_str

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
include_files = os.environ["INCLUDE_FILES"] == "true"

# Read in the diff
diff = sys.stdin.read()

prompt = f"{persona}.{style}.{REQUEST}\n{diff}"

kwargs = {'model': model}
kwargs['temperature'] = 0.5
kwargs['max_tokens'] = 2048
kwargs['messages']=[{"role": "system", "content": prompt}]

# Optionally include files from the diff
if include_files:
  filenames = extract_filenames_from_diff(diff_text)
  formatted_str = format_file_contents(filenames)
  new_message = {"role": "user", "content": formatted_str}
  kwargs['messages'].append(new_message)
  
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
