# Crazyrouter API 接入与模型目录

## Practical guides / 实操入口

- [任务导航 / Choose a task](docs/start-here.zh-CN.md) · [English](docs/start-here.md)
- [五类故障复现 / Troubleshooting](docs/troubleshooting.md)
- [离线优先的 API 诊断工具 / API doctor](tools/doctor.py)


[English](readme.md) · 简体中文

更新：2026-10-12。Crazyrouter 是独立的第三方 AI API 聚合服务。本仓库保留原有名称以便已有链接继续访问；仓库名中的 Claude Opus 4.5 / GPT 5.2 不代表当前完整模型目录。

## 从这里开始

1. [注册或登录](https://crazyrouter.com/register?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_01__zh&utm_medium=github_readme)，在[控制台创建 API Key](https://crazyrouter.com/console/token?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_02__zh&utm_medium=github_readme)。
2. 在[当前模型目录](https://crazyrouter.com/zh/models?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_03__zh&utm_medium=github_readme)确认精确模型 ID、协议和能力。
3. 查看[当前价格](https://crazyrouter.com/zh/pricing?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_04__zh&utm_medium=github_readme)，根据实际需求充值。赠送额度、支付方式和最低充值金额以账户页面为准。
4. 按下表配置客户端；API 地址中不要添加推广参数。

## 接口与 Base URL

| 客户端或协议 | Base URL | 请求路径 |
|---|---|---|
| OpenAI SDK / Chat Completions | `https://crazyrouter.com/v1` | `POST /v1/chat/completions` |
| Claude Code / Anthropic SDK | `https://crazyrouter.com` | `POST /v1/messages` |
| Codex / Responses | `https://crazyrouter.com/v1` | `POST /v1/responses` |

也可将主机改为 `cn.crazyrouter.com`；它是 API 入口，注册和管理账户请使用主站。主机首页或裸 `/v1` 不是可用性测试接口，应请求带鉴权的 `/v1/models`。

## 配置指南

- [Claude Code](https://crazyrouter.com/zh/integrations/claude-code?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_05__zh&utm_medium=github_readme)
- [Codex CLI](https://crazyrouter.com/zh/integrations/codex?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_06__zh&utm_medium=github_readme)
- [Hermes Agent](https://crazyrouter.com/zh/integrations/hermes?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_07__zh&utm_medium=github_readme)
- [API 文档](https://docs.crazyrouter.com?utm_source=github&utm_campaign=claude-opus-4.5-gpt-5.2&utm_content=readme_08__zh&utm_medium=github_readme)

## Python 最小示例

安装 `openai`，在本机设置 `CRAZYROUTER_API_KEY`，然后运行：

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

2026-10-12 已验证该模型的 Chat Completions、`claude-opus-4-8` 的 Messages 和 `gpt-5.6-sol` 的 Responses 最小请求均返回 HTTP 200。这是当日连接检查，不代表所有模型、工具调用或长上下文场景都已测试。

## 模型与计费

按模型目录选择精确 ID，不要把显示名称当作 API 参数。聊天、图片、视频、音频的请求协议与计费单位不同；视频和 Midjourney 不应一律发送到聊天或图片接口。

价格可能按输入、输出、缓存、上下文长度、分辨率或时长计算。以模型详情和账户实际扣费为准，不承诺统一折扣、无限并发或固定可用性。[公开价格 JSON](https://crazyrouter.com/api/pricing)。

## 常见错误

| 状态 | 检查内容 |
|---|---|
| 400 | 协议、精确模型 ID、必填字段、参数支持情况和上下文长度；先缩减为最小请求 |
| 401 | API Key 是否有效、是否属于当前服务、鉴权头是否正确 |
| 403 | 账户/密钥权限或地区访问策略；网页被限制不等于推理接口故障 |
| 404 | 是否重复 `/v1`、是否请求了不存在的端点 |
| 429 | 账户额度、请求频率或上游容量；遵守重试提示 |
| 5xx | 记录时间、模型、request ID 与脱敏错误信息，交由支持排查 |

请勿将密钥粘贴到第三方公开演示站。使用自己信任的客户端，并按当前 API 文档配置。
