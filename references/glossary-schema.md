# Versioned concept glossary and alignment contract

统一使用 schema_version "2.0"，不再混用 original/translation 与 term_zh/term_en。
旧表导入时显式迁移并保留旧文件；不得把解析失败当作“全部术语合规”。

## Glossary JSON

顶层：schema_version、project、version、terms；全文翻译另需 approval。
每条必需字段：
- concept_id：项目内唯一标识；同中文不同概念分开。
- source_forms：中文出现形式数组。
- canonical：一个规范名词/短语，不用 "A / B" 表示任意互换。
- allowed_forms：批准的词形、动词和缩写，可为空。
- forbidden_aliases：仅适用于此概念的误译，可为空。
- context：定义、领域与适用范围。
- status：author_confirmed / verified / provisional。
- evidence：对象数组，字段 kind、locator、note；kind 为 author/source/standard/paper/official。
- notes：歧义、词形适用条件、查询 ID。
- abbreviation / full_form：有关键缩写时两者同时填写，并将缩写与完整英文登记到 canonical/allowed_forms；不凭模型记忆扩写项目自造缩写。

verified 仅表示外部用法已核验，不等于作者已批准；作者命名用 author_confirmed。provisional 可以作为候选交作者，不可进入已放行的全文词表。
作者对整表的确认记录在顶层 approval，作用于全部条目；编辑任一条目、扩写或源文快照后须重新核对锁定指纹。
合并以 concept_id+语境为准，不能按中文字符串去重或来源数量投票。
示例表仅演示字段，不是已核验的通用专业词典。

## 全稿提取、审阅表与审批门槛

先收集作者已有 Excel/CSV/Markdown 术语表，再扫描**可获得的全稿**：标题、摘要、正文、表格/图注与图中文字、公式说明、算法、附录，以及每处首次定义。若图中文字不可提取或附录缺失，表中标出未覆盖范围，不能写“全稿已扫描”。
同一概念只保留一行；中文同形异义拆成不同 concept_id，跨学科同名缩写需请作者消歧。优先收录方法/组件/数据集/指标/威胁模型/专业操作/关键缩写；普通学术词不逐个审批。

交给作者的 `terminology-review.md` 或可编辑表格至少有下列列。先提供**表格**，再等待作者明确批注；没有回复不等于同意。

| ID | 中文或原文形式 | 语境与位置 | 规范英文 | 缩写 | 完整英文 | 准用词形 | 待决问题/证据 | 作者决定 |
|---|---|---|---|---|---|---|---|---|
| rag.name | 检索增强生成 | 摘要、正文 | Retrieval-Augmented Generation | RAG | Retrieval-Augmented Generation | RAG | 首次定义策略待确认 | 待审阅 |

表格应保留作者原有固定译法及出处，不机械重翻。作者可逐项确认/修改，或明确声明整表为最终版；后一种情形仍要合并全稿扫描发现的新词并请作者决定。只有全部关键候选、缩写全称和冲突完成确认，才构建已批准词表。不同章节的首次定义由模板/作者要求决定，不能为“固定”而把后续缩写全部强改为全称。

全文翻译使用同一份原文文本快照（包含已提取的非正文术语）；其 SHA-256 与已批准词表指纹一起构成锁定记录。`approval` 示例：

```json
{
  "status": "approved",
  "glossary_version": "paper-1",
  "source_sha256": "<check_glossary_gate.py --fingerprint 的输出>",
  "terms_sha256": "<同上>",
  "approved_term_count": 168,
  "author_reference": "作者确认消息或已签批表格的可定位位置"
}
```

`--fingerprint` 只计算候选表和原文快照的校验值，不代表审批。**先取得作者真实确认，再记录 approval**；不得由 Agent 自行填写一个“批准”来绕过等待。

```bash
python3 <skill-dir>/scripts/check_glossary_gate.py terminology-glossary.json --source source-snapshot.txt --fingerprint
python3 <skill-dir>/scripts/check_glossary_gate.py terminology-glossary.json --source source-snapshot.txt
```

第二条返回 0 才可派发正式翻译；1 表示审批/版本/术语有待处理，2 表示输入无效。脚本能检查记录和指纹，不能证明“作者确认消息”真的来自作者；主控必须核对该消息本身。
改动原稿但没有新增或改变术语时，重扫变动范围并记录新快照；对已有作者决定无需重复提问。发现新词或变更既定词时，只暂停受影响的片段、增量审阅、升级 version，再重译/重审已受影响内容。

## Alignment JSON

同一份文件容纳逐单元对应关系与需人工检查的概念使用。例：
```json
{
  "segments": [
    {
      "id": "methods.p1",
      "source": "授权用户解封装数据密钥，然后解密载荷。",
      "target": "The authorized user decapsulates the data key and then decrypts the payload.",
      "term_uses": [
        {
          "concept_id": "kem.decapsulation",
          "source_start": 4,
          "source_span": "解封装",
          "target_start": 20,
          "target_span": "decapsulates"
        }
      ]
    }
  ]
}
```

term_uses 由人工/Agent 对照原文建立；source_start/target_start 是相应单元内从0开始的 Unicode 字符偏移，不是字节偏移。
source_span 必须是该概念的源文出现形式，target_span 是该概念对应的完整实际译法。
一个概念出现多次时逐次登记不同位置，不能重复占用相同位置。脚本校验切片、英文词边界和位置重复。
不要把整句当 target_span，也不能截取 chunking 内的 chunk 来假装规范词形已出现。
没有 term_uses 不代表没有术语，必须由 Reviewer 检查覆盖。
脚本核验连续非空白字符序列能否与输入文件对应（只忽略单元切分带来的空白）；多种源格式转换应先形成可追溯的同格式文本。
默认逐单元检查可见数值、常见 LaTeX 保护片段、基本结构；同句指标互换等仍需语义审校。

## 准用词形与禁用别名

decapsulation → decapsulate / decapsulates / decapsulated 可按语法批准；
decapsulation→decryption 是概念替换，不是词形变化。
同句中对载荷的 decryption 不违规。chunk 与 chunking 是产物与动作，可分 concept 或明确说明关系。
LSSS span test、span solving 不能仅因同义近似合并；capacity tier 与 profile 亦然。
