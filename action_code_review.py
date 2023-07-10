#!/usr/bin/env python3
import os
import sys
import openai
import string
import re
from typing import List

# Make sure the necessary environment variables are set
if "OPENAI_API_KEY" not in os.environ:
  print("The OPENAI_API_KEY environment variable is not set.")
  sys.exit(1)

def validate_filename(filename: str) -> bool:
    """
    Validates a filename by checking for directory traversal and unusual characters.

    Args:
      filename: str, filename to be validated

    Returns:
      bool: True if the filename is valid, False otherwise
    """
    # Check for directory traversal
    if ".." in filename or "/" in filename:
        return False

    # Check for unusual characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    for char in filename:
        if char not in valid_chars:
            return False

    return True

def extract_filenames_from_diff_text(diff_text: str) -> List[str]:
  """
  Extracts filenames from git diff text using regular expressions.

  Args:
    diff_text: str, git diff text

  Returns:
    List of filenames
  """
  pattern = r'\+\+\+ b/(.*)'
  filenames = re.findall(pattern, diff_text)
  sanitized_filenames = [fn for fn in filenames if validate_filename(fn)]
  return sanitized_filenames

def format_file_contents_as_markdown(filenames: List[str]) -> str:
  """
  Iteratively goes through each filename and concatenates
  the filename and its content in a specific markdown format.

  Args:
    filenames: List of filenames

  Returns:
    Formatted string
  """
  formatted_files = ""
  for filename in filenames:
    try:
      with open(filename, 'r') as file:
        file_content = file.read()
      formatted_files += f"\n{filename}\n```\n{file_content}\n```\n"
    except Exception as e:
      print(f"Could not read file {filename}: {e}")
  return formatted_files

REQUEST = "Reply on how to improve the code (below). Think step-by-step. Give code examples of specific changes\n"

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
model = os.environ.get("MODEL", "gpt-3.5-turbo-16k")
persona = PERSONAS.get(os.environ.get("PERSONA"), PERSONAS["kent_beck"])
style = STYLES.get(os.environ.get("STYLE"), STYLES["concise"])
include_files = os.environ.get("INCLUDE_FILES", "false") == "true"

# Read in the diff
diff = sys.stdin.read()

prompt = f"{persona}.{style}.{REQUEST}\n{diff}"

kwargs = {'model': model}
kwargs['temperature'] = 0.1
kwargs['max_tokens'] = 2048
kwargs['messages']=[{"role": "system", "content": prompt}]

# Optionally include files from the diff
if include_files:
  filenames = extract_filenames_from_diff_text(diff)
  formatted_files = format_file_contents_as_markdown(filenames)
  new_message = {"role": "user", "content": formatted_files}
  kwargs['messages'].append(new_message)

try:
  response = openai.ChatCompletion.create(**kwargs)
  if response.choices:
    if 'text' in response.choices[0]:
      review_text = response.choices[0].text.strip()
    else:
      review_text = response.choices[0].message.content.strip()
  else:
    review_text = f"No response from OpenAI\n{response.text}"
    sys.exit(1)
except Exception as e:
  review_text = f"OpenAI failed to generate a review: {e}"
  sys.exit(1)

print(f"{review_text}")
