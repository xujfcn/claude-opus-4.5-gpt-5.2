# 先选任务，再选协议

[English](start-here.md) · [故障复现与排查](troubleshooting.md)

| 你要完成的事 | 直接入口 |
|---|---|
| 配好 Codex，并能恢复原配置 | [配置诊断与恢复](https://github.com/xujfcn/crazyrouter-codex-cli/blob/main/docs/config-doctor.md) |
| Claude Code 登录态或环境变量冲突 | [分层诊断](https://github.com/xujfcn/crazyrouter-claude-code/blob/main/docs/diagnose.md) |
| 产品描述生成文案和配图 | [完整 MCP 示例](https://github.com/xujfcn/crazyrouter-mcp/blob/main/examples/README.md) |
| 核算输入、输出和缓存费用 | [账本计算器](https://github.com/xujfcn/claude-code-pricing-guide/blob/main/docs/ledger.md) |
| 比较服务商公开承诺与实测证据 | [核对方法](https://github.com/xujfcn/awesome-claude-api-cn/blob/main/docs/methodology.md) |
| 做一个有固定输入和验收的 Agent 任务 | [Hermes 日志分类](https://github.com/xujfcn/crazyrouter-hermes/tree/main/examples/log-triage) |

## 本地诊断

克隆仓库，使用 Python 3.10+。下面的命令默认离线运行，不安装依赖，不改配置，不发送 API 请求。

```bash
python tools/doctor.py --protocol chat
python tools/doctor.py --protocol responses
python tools/doctor.py --protocol messages
python tools/doctor.py --protocol gemini
```

需要在线检查时，在本地终端设置 CRAZYROUTER_API_KEY。Bash 使用 export，PowerShell 使用 $env:；密钥不要写进 issue。

```bash
python tools/doctor.py --protocol chat --online
python tools/doctor.py --protocol messages --inference
```

`--online` 只查鉴权后的模型目录。`--inference` 额外发送一次可能计费的最小文本请求，不自动重试。报告不保存 Key、用户提示词、返回正文或账户信息。可用 `> diagnostic.json` 保存。

Chat/Responses 的 Base URL 以 `/v1` 结尾；Messages/Gemini 使用根地址。模型目录、密钥权限、端点协议和完整客户端功能是四层不同的验证，单次 200 不能替代后面三层。

本次查到的反例包括：根地址 404 但推理正常；公开目录未列出的兼容别名仍能返回 200。按实际请求排查，避免直接换 Key 或更换工具。
