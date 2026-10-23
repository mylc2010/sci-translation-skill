# sci-translation-skill

[![License: MIT](https://img.shields.io/badge/license-MIT-2ea44f)](#许可证)
[![Agent skill hosts](https://img.shields.io/badge/agents-Codex%20%7C%20Claude%20Code%20%7C%20OpenClaw%20%7C%20OpenCode%20%7C%20Hermes-20232a)](#支持的-agent)
[![Skills: 1](https://img.shields.io/badge/skills-1-159bd3)](#主要文件)
[![Language: 中文 | English](https://img.shields.io/badge/language-%E4%B8%AD%E6%96%87%20%7C%20English-2769c6)](#sci-translation-skill)

[English](README_EN.md) | [简体中文](README.md)

1.61：面向计算机、医学及其他理工科论文的中译英与译稿审校工作流。

目标：减少术语漂移、技术失真、遗漏和格式损坏，让译稿更接近作者可审查的投稿版本。

## 为什么不只写一句“帮我润色成SCI风格”

流畅不等于准确。常见风险包括：
- 同一概念在摘要、正文和图注中换了名字；
- “可能有效”被润色成“已证明有效”，条件和威胁模型随之丢失；
- 首译与审校都由同一轮输出完成，缺少独立检查与修改后复核；
- 数字没变，却被绑定到错误指标；公式个数相同，变量却变了；
- 译者为了“高级”加入冗余名词化、未经来源支持的机制或结论。

本 skill 保留学术英语的自然表达，同时将科学含义优先于修辞。

## 工作流

1. 保留全稿原文快照，合并作者已有词表，扫描正文、图表、算法与附录的专业词和重要缩写。
2. **先交作者可编辑的术语审阅表**；确认全部规范英文、缩写全称和争议项后锁定版本。确认前不启动正式译者。
3. 按同一词表试译或分块译全文；译者同时处理忠实表达与学术语域。
4. 独立审校原文与译文、全稿术语一致性、数据绑定和引用；仅对实际问题修订并复核。
5. 交付译文、已批准词表、必要审校记录和作者问题。

新论文在全稿术语表确认后试译 2–3 段方法/结果，再扩展全文，最后定稿摘要。独立短段只锁定该段术语，不宣称全文一致。

术语审阅表：单人审阅、约 30 项以内默认 Markdown；条目更多，或需要多人批注、筛选冲突项和跟踪逐项决定时用 Excel。协作复杂度比数量更重要；两种格式都对应同一份机器可读的锁定词表，作者的修改须同步后再重新锁定。

## 核心能力

| 能力 | 如何实现 | 边界 |
|---|---|---|
| 作者审批术语 | 全稿提取→表格审阅→版本/哈希锁定→所有 Agent 共用 | 未确认时不翻译；不能把外部查词当作者批准 |
| 多 Agent 协作 | 有真实工具时分配术语研究、翻译、独立审校 | 无工具则串行自审，明确披露 |
| 技术保真 | 逐段记录否定、条件、量词、证据强度 | 作者负责确认科学正确性 |
| 学术语域 | 借鉴 Nature 的准确、简洁与直接陈述；检查口语填充、冠词、单位和主谓关系 | 不套用硬性字数、拼写或夸大结论 |
| 读者导向编辑 | 按章节组织已有信息、明确主体与指代、降低句子负荷 | 不补意义、不跨段搬移、不硬性限制句长 |
| 分开评价 | 先检查保真门槛，再用例句评价阅读质量 | 零个已发现错误不自动等于满分 |
| 格式保护 | 必要的结构边界、公式/宏/引文及表格坐标核对 | 复杂格式还需人工/渲染验证 |
| 自动差异检查 | 数字、保护片段、引用次数、基本结构、对齐及登记术语 | 不等于自动语义审稿 |

“多 Agent”是多个独立任务上下文，不自动意味着多个不同模型或人类专家。
运行记录说明实际角色和版本，不写虚构团队日志。默认不另设 Language-editor，也不为每段强制生成多份文档。

## 适用领域

- 计算机/安全/AI：威胁模型、访问控制、KEM 与载荷解密、数学符号和技术边界。
- 医学/生物：研究设计、关联与因果、效应量/区间、样本、剂量、终点和时间点。
- 工程/材料：实验条件、单位/量纲、实测与仿真、误差和适用范围。

这些是新增审查规约，不是大规模跨领域实测结论；医学稿件需专业人员终审。

## 安装与运行时

将包含 SKILL.md 的 sci-translation-skill 目录放入宿主实际支持的技能目录，避免重复嵌套。

支持从仓库安装技能的宿主也可使用本仓库地址；是否能自动安装取决于宿主及其权限，不要把给出链接等同于安装成功。

需要手动安装的参考：

本地 Codex 的已使用位置是 ~/.codex/skills/sci-translation-skill/SKILL.md。

在本仓库根目录运行的安装示例（目标已有版本时先备份）：
```bash
mkdir -p ~/.codex/skills/sci-translation-skill
rsync -a --exclude '.git/' --exclude '.DS_Store' --exclude '__pycache__/' ./ ~/.codex/skills/sci-translation-skill/
```

安装后在宿主中刷新技能或新开会话，确认能够读取 SKILL.md；本文件不替代当前宿主配置文档。

### 支持的 Agent

下表表示这些宿主有加载 `SKILL.md` 目录的接口，**不是本 skill 在每个平台上的端到端实机认证**；当前仅 Codex 本地安装已使用。复制时保留 `references/`、`scripts/` 和 `examples/`。

| Agent | 技能目录或安装入口 | 本仓库验证状态 |
|---|---|---|
| Codex | `~/.codex/skills/sci-translation-skill/` | 已在本地使用 |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/sci-translation-skill/` | 官方支持该目录 |
| [OpenClaw](https://docs.openclaw.ai/tools/skills) | 通过 `openclaw skills install ./path/to/sci-translation-skill` 导入，或放入其技能目录 | 官方支持本地技能导入 |
| [OpenCode](https://opencode.ai/docs/skills) | `~/.config/opencode/skills/sci-translation-skill/` | 官方支持该目录 |
| [Hermes Agent](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills/) | `~/.hermes/skills/sci-translation-skill/` | 官方支持该目录 |

Antigravity、Cursor、Windsurf、Aider 等宿主须先确认其技能/规则加载接口，再显式加载入口及所需 references。Dify、FastGPT、Coze 或自建 Harness 还需自行实现角色节点、依赖、文件传递及运行记录；仅上传知识库不构成多 Agent 流水线。
技能不要求固定 Sonnet/Opus，不擅改宿主配置。脚本只需 Python 3 标准库。

## 可复制提示词

首次使用：先审术语，**本轮不要翻译**。
```text
使用 $sci-translation-skill，为这篇完整论文做翻译前术语锁定。
领域：[学科]；目标期刊：[名称或未定]；格式：[LaTeX/Word/纯文本]。
先读取我已有的术语表，再扫描标题、摘要、正文、公式说明、图表、算法和附录。
输出可供我审阅的表格：概念、语境/位置、唯一英文、缩写及全称、准用词形、疑问。
列出未覆盖内容。本轮只交术语表，等我确认后再开始 pilot 翻译。
```

确认表格后的第二条消息：
```text
这份术语表已确认：[路径/版本]；我修改了：[行号或“无”]。
请用 $sci-translation-skill 校验锁定版本，再试译[方法/结果2–3段]或继续全文。
所有译者与审校者使用同一词表，保留数值、限定、公式、引用与 LaTeX 宏。
用准确、简洁的学术英语，不用口语填充词；新术语先请我确认。
```

已有中英对照稿：
```text
使用 $sci-translation-skill 的 review 模式，对照中文逐段审校英文。
先查技术含义、术语、论断强度、数字/单位和引用，再查语言自然度。
只修复有证据的问题；将“uses→adopts”这类偏好与实质错误分开。
先检查阅读障碍再改句子；对照首译与编辑稿复核条件作用域、因果、指标和引用绑定。
每项列原文、现译、修订、理由，并在修改后复核。
```

全文：
```text
使用 $sci-translation-skill，先扫描全稿并交术语审阅表；如果我已明确批准这张完整表，校验后直接翻译全文。
在新目录交付，不覆盖原文。各块共享同一版本词表和研究上下文。
覆盖正文、图注、表格、公式说明、算法与附录；最后核对摘要的论断范围。
交付英文稿、锁定词表、必要的对齐/审校记录和待确认项，不强制生成空文件。
```


## 检查工具

```bash
bash references/test-skill-integrity.sh
python3 scripts/check_glossary_gate.py terminology-glossary.json --source source-snapshot.txt
python3 scripts/audit_translation.py source.tex target.tex \
  --glossary terminology-glossary.json \
  --alignment alignment.json \
  --output qa-report.json
```

术语门槛：0=审批记录与词表/原稿快照匹配；1=未放行；2=输入错误。译稿审计：0=已实现检查未发现差异；1=待核查；2=输入错误。
0 **不表示投稿就绪**。未提供 alignment 时，不声称完成逐段覆盖或术语合规检查。
有些正确的数字顺序/格式调整也可能触发差异，需要记录人工处置。

原 shell 入口仍可使用：
```bash
bash references/test-translation-structure.sh source.tex target.tex glossary.json
```

这两个 shell 测试脚本不做“AI味检测”，也不认证领域准确性。

## 主要文件

- [SKILL.md](SKILL.md)：入口与放行条件。
- [术语审批契约](references/glossary-schema.md)：审阅表、作者确认门槛、JSON schema 与 alignment 格式。
- [术语门槛脚本](scripts/check_glossary_gate.py)：校验版本、条目和原稿快照；不代替真实作者审批。
- [角色契约](references/agent-contracts.md)：真实工具和文件所有权。
- [语言指南](references/academic-phraseology-guide.md)：忠实、简洁与自然表达。
- [读者导向编辑](references/reader-oriented-editing.md)：章节、句内负荷、衔接与编辑后保真回查。
- [领域配置](references/domain-profiles.md)：各领域的重点风险。
- [行为评测](references/behavioral-evaluation.md)：模型行为验收方案。
- [示例词表](examples/terminology-glossary.sample.json)：字段演示，未外部核验，不自动套用。
- [翻译示例](examples/translation-diff-sample.md)：构造案例，不是已发表的效果证明。

## 1.61 更新

**全稿术语门槛**：摘要、正文、图表、附录使用同一版本，缩写全称与准用词形一并审定；新增术语走增量审批。
借鉴 translation-quality 的结构与独立审校，以及 nature-polishing 的读者路径、精准简洁和学术语域检查；不照搬前者“译者与术语研究并行启动”或后者的硬性句长、写作模板。
为减少耗时，将每段 claim-map/结构清单改为按风险建立，译者默认合并忠实翻译和语言整理，专门 Language-editor 只在需要时启用；脚本筛查后由 Reviewer 对全稿做有重点的语义核对。
参考 `nature-polishing` 的章节职责，在现有终稿复核中增加轻量的跨章节论断对齐：核对引言承诺与结果、摘要结论与证据、讨论局限与其所约束的具体结论；发现原文缺口只提作者问题，不擅自补写或重排正文。

## 许可证

README 当前声明 MIT License；
