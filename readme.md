# Crazyrouter API setup and model directory

## Practical guides / 实操入口

- [任务导航 / Choose a task](docs/start-here.zh-CN.md) · [English](docs/start-here.md)
- [五类故障复现 / Troubleshooting](docs/troubleshooting.md)
- [离线优先的 API 诊断工具 / API doctor](tools/doctor.py)


English · [简体中文](readme_cn.md)

Updated 2026-10-12. Crazyrouter is an independent third-party AI API gateway. The original repository name is retained for existing links; Claude Opus 4.5 / GPT 5.2 in its name is not the current model catalogue.

## Get started

1. [Register or sign in](https://crazyrouter.com/register?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_01__en&utm_medium=github_readme), then [create an API key](https://crazyrouter.com/console/token?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_02__en&utm_medium=github_readme).
2. Check exact model IDs, protocols and capabilities in the [live model directory](https://crazyrouter.com/en/models?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_03__en&utm_medium=github_readme).
3. Review [current prices](https://crazyrouter.com/en/pricing?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_04__en&utm_medium=github_readme). Trial credits, payment methods and minimum deposits are shown in your account.
4. Configure your client using the table below. Keep marketing parameters out of API base URLs.

## API base URLs

| Client / protocol | Base URL | Request path |
|---|---|---|
| OpenAI SDK / Chat Completions | `https://crazyrouter.com/v1` | `POST /v1/chat/completions` |
| Claude Code / Anthropic SDK | `https://crazyrouter.com` | `POST /v1/messages` |
| Codex / Responses | `https://crazyrouter.com/v1` | `POST /v1/responses` |

The API host `cn.crazyrouter.com` is also available. Use the main website for account management. A request to the host root or bare `/v1` does not test inference; use authenticated `/v1/models`.

## Integration guides

- [Claude Code](https://crazyrouter.com/en/integrations/claude-code?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_05__en&utm_medium=github_readme)
- [Codex CLI](https://crazyrouter.com/en/integrations/codex?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_06__en&utm_medium=github_readme)
- [Hermes Agent](https://crazyrouter.com/en/integrations/hermes?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_07__en&utm_medium=github_readme)
- [API documentation](https://docs.crazyrouter.com?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_08__en&utm_medium=github_readme)

## Minimal Python example

Install `openai`, set `CRAZYROUTER_API_KEY` locally, then run:

```python
import os
from openai import OpenAI

client = OpenAI(base_url="https://crazyrouter.com/v1", api_key=os.environ["CRAZYROUTER_API_KEY"])
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Reply OK"}],
    max_tokens=16,
)
print(response.choices[0].message.content)
```

Minimal requests for this Chat Completions model, `claude-opus-4-8` on Messages, and `gpt-5.6-sol` on Responses returned HTTP 200 on 2026-10-12. This is a dated connection check, not a test of every model, tool call or long-context workload.

## Models and billing

Copy exact API model IDs from the live catalogue. Chat, image, video and audio models have different protocols and billing units. Do not send every video or Midjourney request to chat completions or image generations.

Prices can depend on input, output, caching, context length, resolution and duration. Consult model details and account charges; there is no universal discount or unlimited-concurrency guarantee. [Public pricing JSON](https://crazyrouter.com/api/pricing).

## Troubleshooting

| Status | Check |
|---|---|
| 400 | Protocol, exact model ID, required fields, supported parameters and context length; reduce to a minimal request |
| 401 | Key validity, provider and authentication header |
| 403 | Account/key permissions or regional access policy; a blocked website does not establish an inference outage |
| 404 | Endpoint path and duplicated `/v1` segments |
| 429 | Quota, rate limits and upstream capacity; respect retry guidance |
| 5xx | Save the time, model, request ID and redacted error for support |

Use a client you trust and current API documentation. Do not enter API keys into public third-party demo sites.
