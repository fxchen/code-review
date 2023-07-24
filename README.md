# Code Review Github Action

This action, authored by Frank Chen (@fxchen), improves your pull requests and code base by performing AI-assisted code reviews. It can analyze your pull requests and provide intelligent and insightful comments to help you maintain high code quality.

<details>
  <summary>Diagram for AI code review</summary>
  
```mermaid
sequenceDiagram
    participant GithubAction as Github Action
    participant action_code_review as action_code_review.py
    participant OpenAI_API as OpenAI API
    participant Claude_API as Claude API
    GithubAction->>action_code_review: main()
    Note over action_code_review: Get environment variables
    Note over action_code_review: Validate API, persona, and style
    Note over action_code_review: Read git diff from stdin
    action_code_review->>action_code_review: get_prompt()
    Note over action_code_review: Generate prompt for API
    action_code_review->>action_code_review: prepare_kwargs_func()
    Note over action_code_review: Prepare parameters for API call
    alt API to use is OpenAI
        action_code_review->>OpenAI_API: call_openai_api(kwargs)
        OpenAI_API-->>action_code_review: Review text
    else API to use is Claude
        action_code_review->>Claude_API: call_claude_api(kwargs)
        Claude_API-->>action_code_review: Review text
    end
    action_code_review-->>GithubAction: Review text
    Note over GithubAction: Sends the review text to the PR

```

</details>

# Setup

## 1. Add a workflow like this in your repo.

Example `.github/workflows/code-review.yml`

```
name: Code review
on: [pull_request]
jobs:
  code-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: fxchen/code-review@latest
        with:
          model: 'gpt-3.5-turbo-16k'
          openai-key: ${{ secrets.OPENAI_API_KEY }}
```

## 2. Secret configuration

Configure an OPENAI_API_KEY secret inside your repository settings (Security > Secrets and variables > Actions) . https://github.com/{org}/{repo}/settings/secrets/actions
- Add your OpenAI API key from the API key section (https://platform.openai.com/account/api-keys)

![image](https://github.com/fxchen/code-review/assets/178719/3370b01a-6bb4-417d-a2ca-82507b5fc4b4)


# Inputs

### `openai-key`
This is the OpenAI API key, and it's required for the action to operate.

### `github-token`
The token used to authenticate with the GitHub API. This is not required, as it defaults to the provided GitHub token.

### `model`
The OpenAI language model to use for the code review. This is not required, and defaults to 'gpt-3.5-turbo-16k'.

### `persona`
The persona to use in the prompt. Options include 'developer', 'kent_beck', 'marc_benioff', 'yoda', etc. This is not required, and defaults to 'developer'.

### `style`
The style of output to use. Options include 'concise', 'zen', etc. This is not required, and defaults to 'concise'.

### `include-full-files`
This flag determines whether to include full files in addition to the diff. This is helpful to create better reviews by including more context. It's not required and defaults to 'false'.

### `post-if-error`
This flag determines whether to post a comment if there was an error during execution. It's not required and defaults to 'false'.

### `exclude-files`
This is a comma-separated list of files to exclude from the action. It's not required and defaults to an empty string.
```exclude-files: 'file_to_exclude.py,another_file_to_exclude.py'```

# Options

## Only execute on draft PRs
This replaces `on: [pull_request]`. Example `.github/workflows/code-review.yml`
```
on:
  pull_request: # Filter out draft pull requests
     types:
     - opened
     - reopened
     - synchronize
     - ready_for_review
```

## Exclude dependabot
You probably don't want dependabot PRs reviewed. Example `.github/workflows/code-review.yml`
```
jobs:
  code-review:
    if: ${{ github.actor != 'dependabot[bot]' }}
    steps:
      - uses: fxchen/code-review@latest
```

## Set up as CLI tool

Set up a bash or zsh alias like `code_review` that maps to `code_review.py`. Mine is below

```
code_review='~/source/code-review/code_review.py'
```

<details>
  <summary>Diagram for AI code review on CLI</summary>
  
```mermaid
sequenceDiagram
    participant code_review as code_review.py
    participant action_code_review as action_code_review.py
    participant OpenAI_API as OpenAI API
    participant Claude_API as Claude API
    code_review->>code_review: main()
    Note over code_review: Parse arguments
    code_review->>code_review: get_diff()
    Note over code_review: Get git diff or file content
    code_review->>action_code_review: subprocess.run(["python3", "action_code_review.py"])
    Note over action_code_review: Get environment variables
    Note over action_code_review: Validate API, persona, and style
    Note over action_code_review: Read git diff from stdin
    action_code_review->>action_code_review: get_prompt()
    Note over action_code_review: Generate prompt for API
    action_code_review->>action_code_review: prepare_kwargs_func()
    Note over action_code_review: Prepare parameters for API call
    alt API to use is OpenAI
        action_code_review->>OpenAI_API: call_openai_api(kwargs)
        OpenAI_API-->>action_code_review: Review text
    else API to use is Claude
        action_code_review->>Claude_API: call_claude_api(kwargs)
        Claude_API-->>action_code_review: Review text
    end
    action_code_review-->>code_review: Review text
    Note over code_review: Prints the review text
```

</details>


# FAQ / Troubleshooting

## Permission configuration at the repository

Configure "Workflow permissions" inside your repository settings (Code and automation > Actions > General). https://github.com/{org}/{repo}/settings/actions
- "Workflow permissions" to Read and write permissions

![image](https://github.com/fxchen/code-review/assets/178719/c04067c9-9476-4474-85ca-854893466807)

