#!/usr/bin/env python3

import argparse
import os
import subprocess
from typing import List

DEFAULT_PERSONA = "kent_beck"
DEFAULT_STYLE = "concise"
DEFAULT_MODEL = "gpt-4-1106-preview"
DEFAULT_BRANCH = "main"


def get_file(filename: str) -> str:
    """Get the contents of the specified file."""
    try:
        with open(filename, "r") as file:
            file_str = file.read()
            return f"\n{filename}\n```\n{file_str}\n```"
    except FileNotFoundError:
        print(f"WARNING: File {filename} not found")
        return ""
    except UnicodeDecodeError:
        print(
            f"WARNING: File {filename} could not be read due to encoding issues. Skipping this file."
        )
        return ""


def construct_git_diff_command(branch: str, exclude_files: List[str]) -> str:
    """Construct the git diff command."""
    exclude_str = (
        " ".join(f"':!{file}' " for file in exclude_files)
        if exclude_files
        else " "
    )
    return f"git diff --merge-base origin/{branch} HEAD -- . {exclude_str}"


def execute_command(command: str) -> str:
    """Execute a shell command and handle potential errors."""
    try:
        return subprocess.check_output(command, shell=True).decode()
    except subprocess.CalledProcessError as e:
        return (
            f"An error occurred while trying to execute the command: {str(e)}"
        )


def get_diff_from_file(diff_file: str) -> str:
    """Get the diff from a provided file."""
    return get_file(diff_file)


def get_diff_from_git(branch: str, exclude_files: List[str]) -> str:
    """Get the diff between the current branch and the specified branch."""
    diff_command = construct_git_diff_command(branch, exclude_files)
    return execute_command(diff_command)


def get_diff(
    diff_file: str = None, branch: str = "main", exclude_files: List[str] = None
) -> str:
    """Get the diff either from git or a file."""
    if diff_file:
        return get_diff_from_file(diff_file)
    else:
        return get_diff_from_git(branch, exclude_files)


def main():
    # Get arguments
    parser = argparse.ArgumentParser(
        description="Improve your pull requests and code base with AI-assisted code reviews"
    )
    parser.add_argument(
        "--persona",
        default=DEFAULT_PERSONA,
        help="The persona to use in the prompt (developer, kent_beck, marc_benioff, yoda)",
    )
    parser.add_argument(
        "--style",
        default=DEFAULT_STYLE,
        help="The style of output to use (concise, zen)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="The model to use for the OpenAI API call",
    )
    parser.add_argument(
        "--branch",
        default=DEFAULT_BRANCH,
        help="The branch to diff against (defaults to main)",
    )
    parser.add_argument(
        "--filename",
        default=None,
        help="Optional filename to use instead of git diff",
    )
    parser.add_argument(
        "--directory",
        type=str,
        default=None,
        help="Optional directory to use instead of git diff",
    )
    parser.add_argument(
        "--include-files",
        default="false",
        type=str,
        help="Whether to include full files in addition to the diff",
    )
    parser.add_argument(
        "--exclude-files",
        default="",
        type=str,
        help='A list of files to exclude from the action (comma separated). E.g. "package.json,pyproject.toml"',
    )
    parser.add_argument(
        "--api-to-use",
        default="openai",
        help="The API to use for code review (openai, anthropic)",
    )
    args = parser.parse_args()

    # Parse exclude_files argument as a list
    exclude_files = (
        [file.strip() for file in args.exclude_files.split(",")]
        if args.exclude_files
        else None
    )

    # Switch on directory
    if args.directory:
        diff = ""
        if os.path.isdir(args.directory):
            for root, dirs, files in os.walk(args.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    diff += get_diff(file_path, exclude_files=exclude_files)
        else:
            print(f"The provided directory {args.directory} does not exist.")
    else:
        diff = get_diff(args.filename, args.branch, exclude_files=exclude_files)

    # Set environment variables
    os.environ["MODEL"] = args.model
    os.environ["PERSONA"] = args.persona
    os.environ["STYLE"] = args.style
    os.environ["INCLUDE_FILES"] = args.include_files
    os.environ["API_TO_USE"] = args.api_to_use

    # Call action_code_review.py with the diff as input from the correct directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    process = subprocess.run(
        ["python3", "action_code_review.py"],
        input=diff,
        text=True,
        capture_output=True,
        cwd=script_dir,
    )
    print(process.stdout)


if __name__ == "__main__":
    main()
