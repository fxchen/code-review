#!/usr/bin/env python3

import argparse
import subprocess
import requests
import os
import json
import git
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

def get_file(filename):
  """Get the contents of the specified file."""
  try:
    with open(filename, 'r') as file:
      file_str = file.read()
      return f"\n{filename}\n```\n{file_str}\n```"
  except FileNotFoundError:
    return f"File {filename} not found."

def get_diff(filename=None):
  """Get the diff between the current branch and the master branch or from a provided file."""
  if filename:
    return get_file(filename)
  else:
    try:
      repo = git.Repo(search_parent_directories=True)
      current_branch = repo.active_branch.name
      diff = repo.git.diff('origin/master..' + current_branch)
      
      if diff:
        return diff
      else:
        return "No differences between master and current branch."
    
    except git.GitError as e:
      return f"An error occurred while trying to get the git diff: {str(e)}"

def main():
  # Get arguments
  parser = argparse.ArgumentParser(description="Get the git diff from master of the current branch.")
  parser.add_argument('--persona', default='developer', help='The persona to use in the prompt (developer, kent_beck, marc_benioff, yoda)')
  parser.add_argument('--style', default='concise', help='The style of output to use (concise, zen)')
  parser.add_argument('--filename', default=None, help='Optional filename to use instead of git diff')
  parser.add_argument('--dir', type=str, default=None, help='Optional directory to use instead of git diff')


  args = parser.parse_args()

  # Switch on directory
  if args.dir:
    diff = ""
    if os.path.isdir(args.dir):
      for root, dirs, files in os.walk(args.dir):
        for file in files:
          file_path = os.path.join(root, file)
          diff += get_diff(file_path)
          # Further processing on diff
    else:
      print(f"The provided directory {args.dir} does not exist.")
  else:
    diff = get_diff(args.filename)

  # Set up prompt
  BACKGROUND = PERSONAS[args.persona]
  STYLE = STYLES[args.style]
  prompt = f"{BACKGROUND}.{STYLE}.{REQUEST}\n{diff}"
  print(f"PROMPT:\n{prompt}")

  # Set up request to OpenAI
  openai.api_key = os.getenv("OPENAI_API_KEY")
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    max_tokens=512,
    temperature=0.75,
    top_p=0.9,
    n=1
  )

  # Output response
  print(f"RESPONSE:\n{response}")
  completion_text = response.choices[0].text.strip()
  print(f"FORMATTED RESPONSE:\n{completion_text}")

if __name__ == "__main__":
  main()
