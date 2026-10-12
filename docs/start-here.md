# Choose a task, then use the matching protocol

[中文](start-here.zh-CN.md) · [Troubleshooting](troubleshooting.md) · [Dated evidence](../evidence/connectivity-2026-10-12.json)

| Your task | Start here | API protocol / base rule |
|---|---|---|
| Configure Codex | [Configuration doctor and restore](https://github.com/xujfcn/crazyrouter-codex-cli/blob/main/docs/config-doctor.md) | Responses; base ends in /v1 |
| Configure Claude Code | [Diagnosis and validation](https://github.com/xujfcn/crazyrouter-claude-code/blob/main/docs/diagnose.md) | Messages; root base |
| Produce copy and an image | [Runnable MCP workflows](https://github.com/xujfcn/crazyrouter-mcp/blob/main/examples/README.md) | Three implemented MCP tools; model-specific endpoints |
| Understand a task's cost | [Ledger calculator](https://github.com/xujfcn/claude-code-pricing-guide/blob/main/docs/ledger.md) | Separate input, output and cache billing |
| Compare service evidence | [Selection methodology](https://github.com/xujfcn/awesome-claude-api-cn/blob/main/docs/methodology.md) | Sources and verification level per claim |
| Try an Agent task | [Hermes log triage](https://github.com/xujfcn/crazyrouter-hermes/tree/main/examples/log-triage) | Fixed inputs and an output validator |

## Run a diagnostic before changing tools

Clone this repository and use Python 3.10+. No package installation is required.

```bash
python tools/doctor.py --protocol chat
python tools/doctor.py --protocol responses
python tools/doctor.py --protocol messages
python tools/doctor.py --protocol gemini
```

These commands check configuration offline. They do not call the API or modify your environment. The report records only whether a key is present, never its value. Set `CRAZYROUTER_API_KEY` in your local shell for network checks. PowerShell uses `$env:CRAZYROUTER_API_KEY`; Bash uses `export CRAZYROUTER_API_KEY`. Do not paste real keys into issues.

```bash
# Authenticated discovery only, no generation:
python tools/doctor.py --protocol chat --online
# One explicitly requested text generation; normal API charges may apply:
python tools/doctor.py --protocol messages --inference
# Save only the redacted diagnostic JSON:
python tools/doctor.py --protocol chat --online > diagnostic.json
```

The doctor accepts only Crazyrouter HTTPS hosts, refuses redirects and malformed bases, and does not send prompts from your files. No automatic inference retries are performed. A discovery failure stops the flow. A model missing from discovery is recorded, but does not prevent an explicitly requested alias test.

## Compare request shapes

| Protocol | Base | Relative request path | Minimum text input |
|---|---|---|---|
| Chat Completions | https://crazyrouter.com/v1 | /chat/completions | model + messages |
| Responses | https://crazyrouter.com/v1 | /responses | model + input |
| Anthropic Messages | https://crazyrouter.com | /v1/messages | model + messages + max_tokens |
| Gemini native | https://api.crazyrouter.com | /v1beta/models/MODEL:generateContent | contents[].parts[] |

[The runnable source](../tools/doctor.py) contains all four request bodies and authentication headers. A minimal text response only establishes that exact request at that time. Streaming, tool calls, vision, cache behavior and complete CLI tasks require separate tests.

## Reuse this evidence

The evidence JSON documents a dated connection check, not an uptime guarantee or model-identity certification. Open an issue with the client version, protocol, exact model ID, timestamp and redacted doctor output. Share a minimal prompt only if it is public and non-sensitive.

[Current models](https://crazyrouter.com/en/models?utm_source=github&utm_medium=github_readme&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=task_hub_models) · [Create a key](https://crazyrouter.com/console/token?utm_source=github&utm_medium=github_readme&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=task_hub_key)
