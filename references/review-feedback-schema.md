# Review feedback and release record

先记录 run ID、原稿/译文、术语版本、实际 Reviewer ID（不可用则 serial-self-review）、覆盖范围和未检查项。

## Issue record

| 字段 | 内容 |
|---|---|
| id | 稳定编号，例如 R-001 |
| severity | critical / major / minor |
| type | FABRICATION / OMISSION / CLAIM_STRENGTH / ACCURACY / TERMINOLOGY / STRUCTURE / STYLE |
| location | segment ID 或表格/行/列 |
| source / before | 对应原文与有问题的译文 |
| rationale / proposed_fix | 为什么不对、最小修正建议 |
| status | open / fixed / rechecked / author-decision / rejected-with-reason |
| after / recheck_evidence | 修订文本、复核位置/结果 |

严重度由影响决定，不按类型一刀切：否定反转、关键剂量/数量级、凭空安全保证可为 critical；
概念漂移、遗漏限定、数据与指标错绑通常为 major；uses→adopts 属可选风格。
不能将机器候选差异未经确认就计为翻译错误。

## 两个方向的覆盖表

| 源单元 | 目标单元 | 源→译完整性 | 译→源依据 | 术语/数据绑定 | 状态 |
|---|---|---|---|---|---|
| 实际 ID | 实际 ID | 检查结果 | 检查结果 | 检查结果 | 实际状态 |

另列结构清单和术语出现位置覆盖，含合并单元格内内容，不只核查表格总数。

## 结论

报告实际 inspected/total segments、critical/major/minor 未决数、作者问题、工具报告路径。
只有显式计数才能报比例，分母是已定义的 occurrence/segment，而非“读起来很好”。
区分结果：“待作者确认”“已完成所列语言/保真检查，待作者终审”。
即使 0 个已发现错误，也不声称零错误、学科专家认可、期刊录用或已通过未运行的编译。
