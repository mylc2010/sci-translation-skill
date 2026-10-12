# Evidence-preserving academic English

本指南改变表达，不改变研究结果。任何建议都服从源文与冻结术语表。
“更正式”“更长”“更像顶刊”不是正确性的证据，不存在跨学科通用禁词表。

## 优先规则

- 用明确主体和实义动词，去掉无信息引子，避免译入新主体。
- 合理重复技术术语；不为了多样化切换概念名字。
- 在同段内拆分过长句、改变语序；保持条件与被限定断言相邻。
- 主动/被动按主题安排，不强制全部主动。动词准确比主动形式本身重要。
- 普通技术名词通常小写：large language models、data owners、approximate nearest neighbor；专名和正式命名按词表。
- 缩写首次定义后按文档策略使用；摘要与正文是否分别定义由模板决定。
- 删除连接词前检查递进、转折、因果是否仍清楚。However、Moreover 不是错误或 AI 证据。
- 允许正常 scientific hedging。may、suggest、preliminary、under the tested conditions 不是要消除的“学生腔”。

## 用户 A/B 反馈的可迁移规律

| 表达选择 | 决策依据 |
|---|---|
| access structure / access policy | 如果指 LSSS 表达的数学访问结构，structure 更精确；具体授权规则仍可为 policy。不能全文查找替换。 |
| raw / original embedding vectors | raw 适合未保护/未变换表示；original 适合强调与变换后相对的原始对象。先看定义。 |
| end-to-end privacy protection | 仅当原文和链路范围支持时使用。不能将局部表示保护升级为全链路保证。 |
| To address this gap / problem | 确有前文研究缺口时 gap 合适；问题、约束或挑战可能更适合 problem/constraint/challenge。 |
| adopts / uses | 两者都可用；adopts 暗含采用某设计。避免把词汇偏好评为技术胜负。 |
| decapsulates / performs decapsulation | 主体确实执行动作时优先 decapsulates；如描述流程阶段，名词 decapsulation 可保留。 |
| 敏感场景主语 | “Highly sensitive settings often require ...”可比“In ... settings, however, applications often need to ...”更紧凑；保留原文的转折。 |

## 安全的精简与不安全的增强

- 原文：“值得一提的是，本结果仅在所测配置下成立。”
  可译：“This result holds only under the tested configurations.”
  不可译：“This result holds.” 删除垫话不删除 only。
- 原文：“初步结果提示该方法可能降低误差。”
  可译：“Preliminary results suggest that the method may reduce error.”
  不可译：“The results demonstrate that the method reduces error.”
- 原文：“授权用户完成数据密钥解封装。”
  在对应 KEM 定义已确认时：“The authorized user decapsulates the data key.”
- 原文若本身声称“证明”却只给经验结果：忠实翻译并另列论证强度疑问，不偷偷改成更弱/更强而宣称无修改。

## 不应采取的捷径

不把“plays a role”机械换成“provides security guarantees”；不把“groundbreaking”机械换成仍无依据的“novel”。
不补一个新百分比来替换空洞形容词；只用原文已有数据。
不凭句式推断作者身份、不做 AI 检测承诺，不用“权威句式库”填入威胁模型、p 值、机制或引用。
