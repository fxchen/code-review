# code-review

Improve your pull requests and code base with AI-assisted code reviews

## Set up as Github Action

### 1. Add a workflow like this in your repo.

`.github/workflows/code-review.yml`

```
on: [pull_request]

jobs:
  code-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: fxchen/code-review@v0.1.0-alpha
        with:
          model: 'gpt-3.5-turbo-16k'
          openai-key: ${{ secrets.OPENAI_API_KEY }}
```

### 2. Permission configuration

Configure "Workflow permissions" inside your repository settings (Code and automation > Actions > General). https://github.com/{org}/{repo}/settings/actions
- "Workflow permissions" to Read and write permissions

![image](https://github.com/fxchen/code-review/assets/178719/c04067c9-9476-4474-85ca-854893466807)


### 3. Secret configuration

Configure an OPENAI_API_KEY secret inside your repository settings (Security > Secrets and variables > Actions) . https://github.com/{org}/{repo}/settings/secrets/actions
- Add your OpenAI API key from the API key section (https://platform.openai.com/account/api-keys)

![image](https://github.com/fxchen/code-review/assets/178719/3370b01a-6bb4-417d-a2ca-82507b5fc4b4)


## Set up as CLI tool

TBD
