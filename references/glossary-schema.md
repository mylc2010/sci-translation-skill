# Versioned concept glossary and alignment contract

统一使用 schema_version "2.0"，不再混用 original/translation 与 term_zh/term_en。
旧表导入时显式迁移并保留旧文件；不得把解析失败当作“全部术语合规”。

## Glossary JSON

顶层：schema_version、project、version、terms。
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

verified 必须有实际核对的来源及语境；作者命名用 author_confirmed，不标“外部验证”。
provisional 可以暂拟但阻止涉及关键定义的最终放行。
每次冻结记录 version；更新须记录原因和受影响 segment，审校旧版本的片段应重审。
合并以 concept_id+语境为准，不能按中文字符串去重或来源数量投票。
示例表仅演示字段，不是已核验的通用专业词典。

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
