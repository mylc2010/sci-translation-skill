# Runtime-independent agent contracts

以下是任务契约，不是假定存在的 API。主控读取当前工具描述后调用真实工具。
同一模型的两个独立上下文属于独立 Agent 审校，不是跨模型验证。
若无独立工具，采用串行自审并标注；不得虚构身份、执行日志或耗时。

## Lead

建立 source snapshot、structure-manifest、claim-map，收集偏好、检查工具。
分配角色及只读/可写路径，等待依赖，统一术语版本，合并对齐与复核证据。
不创建无关任务、修改运行时配置或升级模型；不上传未发表全文。
对跨角色冲突给出原文证据或 author query，不按角色地位投票。

## Term-researcher

输入：原文、作者词表、研究背景；输出：候选词表+冲突/证据。
仅核验必要术语，不借查词补全文献综述。
不将检索失败写成高置信；不能核实的项目缩写保留原写法。
在当前块冻结前完成该块核心词表；不写首译或终稿。

## Translator

输入：原文分块、context card、claim-map、冻结词表及版式规则。
输出：first-pass、alignment（含术语实际出现位置）、技术疑问；短段可在同一产物中提供。
只在负责路径写入；保留每个源命题，允许有依据的同段英文重组。
不以流畅度强改数据、hedging、因果和技术边界，不预填审核通过。

## Language-editor（按需）

复杂全文或用户需要独立语言编辑时可设此角色；短段由 Translator 分两遍完成，不为凑角色启动团队。
输入：原文、首译、context card、claim-map、冻结词表和授权范围。
读取 [reader-oriented-editing.md](reader-oriented-editing.md)，输出 edited-draft、关键编辑差异和作者问题。
只处理读者路径、主体/指代、句内负荷和段内衔接；不补证据、改术语或扩大结构授权。
编辑后更新目标单元对应关系，保留稳定源 ID，不能因拆合句丢失 alignment 的覆盖。
不作自己的最终放行人；最终 Reviewer 独立核对源文与编辑稿。

## Reviewer

输入：原文、编辑稿、词表/版本、结构清单、claim-map；先独立对照，不看译者/编辑者自评结论。
再检查首译与编辑稿的差异；若没有单独编辑角色，核查 Translator 清晰化后的版本。没有留存首译则明确该项未检查，不编造差异。
输出：带 ID 和定位的 review-feedback、覆盖表、author queries。
核查两个方向、数据绑定、术语与结构，再评价自然度。
分别报告保真门槛和阅读质量；若评价因编辑而改善，引用实际前后例句，不凭角色数量加分。
只提最小必要修复，区分作者原稿科学问题与翻译错误。
修订后再次核对，不仅发送一次意见就宣称闭环完成。

## Revision

可由原 Translator 承担。按 issue ID 记录 before/after；
不接受无依据的 reviewer 建议，退回说明；技术冲突交作者。
Lead/独立 Reviewer 复查最终版本并记录未决项。
