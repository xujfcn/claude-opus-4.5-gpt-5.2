# Five reproducible failure patterns / 五类可复现问题

Python 3.10+; run commands from the repository root. The intentionally invalid commands below exit 1 before any network call. They are failure demonstrations, not configuration templates.

## 1. UTM accidentally copied into the API base

```bash
python tools/doctor.py --base-url "https://crazyrouter.com/v1?utm_source=github"
```

Expected: remove query parameters. Marketing links identify page visits; API clients append endpoint paths and need a clean base. Fix to `https://crazyrouter.com/v1` and rerun offline, then `--online`.

## 2. Repeated /v1 or wrong protocol base

```bash
python tools/doctor.py --base-url https://crazyrouter.com/v1/v1
python tools/doctor.py --protocol messages --base-url https://crazyrouter.com/v1
```

Expected: Chat needs exactly one /v1; Messages needs a root URL. Check the final request path, not only the text field in the UI. A 404 can also be an unknown model or unavailable channel, so retain the redacted API error code when diagnosing manually.

## 3. A model is visible but the client still fails

Discovery, endpoint support and complete client behavior are different. Codex sends Responses; a successful Chat request does not prove Responses compatibility. Use `--protocol responses --online`, then an explicit `--inference` check. Only after that test the CLI's streaming, tools and actual task. Check exact ID and account restrictions.

Conversely, public catalogue absence is not sufficient evidence to delete an alias: `gemini-3.1-pro-preview` returned Chat HTTP 200 during the 2026-10-12 audit despite its absence from the public pricing snapshot. This result is not a permanent availability promise.

## 4. A new key did not fix a 401

Start with the environment of the same process launching the client. The doctor reports `key_present`, not the key. A missing variable in a newly opened terminal is different from an invalid key. Check saved account login, selected provider and its env_key before rotating credentials. Discovery 401 stops the doctor before inference; a 403 can also involve permissions or regional policy. Do not paste an auth.json into an issue.

## 5. HTTP 200, but no useful text or image

Inspect the response schema, finish reason and output budget. The doctor requires a text-bearing response, not simply HTTP 200. A reasoning-only Responses result is not a text answer. Image models may return a URL or base64 bytes; a text-only MCP client may not render inline images. Use the [image download workflow](https://github.com/xujfcn/crazyrouter-mcp/blob/main/examples/README.md) to save a validated file.

## Retry decisions

400/401/403/404 generally need a configuration, permission or routing check before retrying. For 429 inspect quota and Retry-After; for network/5xx failures use bounded retries only where the API supports them safely. A timeout does not prove a billable image/video job was never created. Record the request/job ID privately and check status before creating another task.

## Useful issue report

Include OS, Python/client version, exact model, protocol, timestamp, expected behavior, actual status and redacted doctor JSON. Keep credentials, private prompts, customer data and signed asset URLs out of public issues. [Dated minimal checks](../evidence/connectivity-2026-10-12.json) describe what has actually been tested.
