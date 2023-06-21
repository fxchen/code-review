#!/usr/bin/env python3

import argparse
import os
import git
import subprocess

REQUEST = "Reply on how to improve the code for style, clarity, comments, and tests (below)\n"

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
  prompt = f"{args.persona}.{args.style}.{REQUEST}\n{diff}"
  print(f"PROMPT:\n{prompt}")

  # Set environment variables
  os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
  os.environ["MODEL"] = "gpt-3.5-turbo"
  os.environ["PERSONA"] = args.persona
  os.environ["STYLE"] = args.style

  # Call action_code_review.py with the prompt as input
  process = subprocess.run(["python3", "action_code_review.py"], input=prompt, text=True, capture_output=True)
  print(process.stdout)

if __name__ == "__main__":
  main()
