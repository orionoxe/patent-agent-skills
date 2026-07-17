# 专利代理 Agent Skills

[English](README.md)

用于专利翻译质量检查和审查意见答复起草的开放、可审计 Agent Skills。

> [!IMPORTANT]
> 这些 Skill 只生成草稿和审阅记录，不构成法律意见，不计算法定期限，也不代表已获得提交授权。所有实质性输出都必须由具备相应资质的专利专业人员复核。

## 包含的 Skill

| Skill | 作用 | 确定性校验门 |
|---|---|---|
| `patent-bilingual-qa` | 专利翻译、双语对齐、术语控制和保护范围校对 | 比较权利要求编号、附图标记、数值、单位和专利公开号 |
| `patent-office-action-response` | CNIPA、USPTO、EPO 审查意见拆解、权项映射、修改依据、策略和答复草稿 | 校验每项审查意见、修改依据、证据位置、复核人和关键风险是否闭环 |

两个 Skill 都会显式保留阻塞项；保护范围、法律、期限和提交决定必须由人工批准。

## 安装

Skills CLI 需要 Node.js 18 或更高版本。附带的确定性检查脚本需要 Python 3.9 或更高版本，只使用标准库。

先查看仓库中的 Skill：

```bash
npx skills add orionoxe/patent-agent-skills --list
```

全局安装指定 Skill：

```bash
npx skills add orionoxe/patent-agent-skills \
  --skill patent-bilingual-qa -g -y

npx skills add orionoxe/patent-agent-skills \
  --skill patent-office-action-response -g -y
```

通过交互选择安装：

```bash
npx skills add orionoxe/patent-agent-skills
```

## 使用示例

```text
对照这份英文专利申请和中文译文，先建立 segment map 和 termbase，
再按 P0/P1/P2 输出双语校对问题。
```

```text
结合申请原文分析这份 USPTO Office Action，完整列出审查意见，
映射审查员证据，并给出具有原始公开依据的答复方案。
```

每个 Skill 的输入要求、完成标准和输出契约见其目录中的 `SKILL.md`。

## 兼容性

- 已在 Codex 和 `skills` CLI 上完成本地验证。
- 使用通用 `SKILL.md` 格式，预期兼容 CLI 支持的其他 Agent。
- 未标记为“已验证”的平台尚未做端到端测试。

## 开发与发布

```bash
make test
make list
make package VERSION=v0.1.0
```

推送 `v0.1.0` 形式的标签后，GitHub Actions 会先运行完整检查，再发布两个独立 ZIP、合集 ZIP 和 `SHA256SUMS.txt`。`v0.*` 会标记为 Pre-release。

## 数据与官方来源

专利规则会变化。仓库只采用并记录 WIPO、CNIPA、USPTO、EPO 等官方来源及检索日期。法律规则更新必须说明影响的工作流行为。

公开 Issue 和 Pull Request 只能使用合成或完全去标识化的示例。不得上传未公开发明、客户通信、账号凭据、申请标识或期限信息。

使用或贡献前请阅读 [免责声明](DISCLAIMER.md)、[安全说明](SECURITY.md)和[贡献指南](CONTRIBUTING.md)。

## 许可证

Apache License 2.0，详见 [LICENSE](LICENSE)。
