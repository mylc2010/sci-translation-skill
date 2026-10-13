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
STYLE 项必须指出实际阅读障碍（如主语切换不明、指代多义、信息负荷或段内断裂），并给出对应改法。
同样正确的可选措辞标 optional，不靠累计偏好意见制造“错误数量”。

## 两个方向的覆盖表

| 源单元 | 目标单元 | 源→译完整性 | 译→源依据 | 术语/数据绑定 | 状态 |
|---|---|---|---|---|---|
| 实际 ID | 实际 ID | 检查结果 | 检查结果 | 检查结果 | 实际状态 |

另列结构清单和术语出现位置覆盖，含合并单元格内内容，不只核查表格总数。

## 语言编辑差异

对拆合句、主体重组和承接调整记录：`segment ID | first-pass → edited | 阅读障碍/改法 | 不变的命题与限定 | recheck`。
重点核对编辑后条件作用域、引用支持对象和数值绑定；发现新错可重新打开已关闭的 issue。
短段可内联记录，不要求生成空的差异表；未保留首译时只能报告源文↔终稿检查。

比较多个版本时另列编辑质量，采用 [behavioral-evaluation.md](behavioral-evaluation.md) 的分级锚点；
已发现的保真缺陷数和阅读评分分栏，不相加抵消，不将零缺陷直接换算成满分。

## 结论

报告实际 inspected/total segments、critical/major/minor 未决数、作者问题、工具报告路径。
只有显式计数才能报比例，分母是已定义的 occurrence/segment，而非“读起来很好”。
区分结果：“待作者确认”“已完成所列语言/保真检查，待作者终审”。
即使 0 个已发现错误，也不声称零错误、学科专家认可、期刊录用或已通过未运行的编译。
