# Constructed illustration, not a model benchmark

下列为人工构造的教学示例，不是假称已经发表或经专家验收的真实实验。
示例术语是项目约定，不是通用权威词典；数据只用于演示源文保留。

## 中文输入

授权用户通过 CP-ABE-KEM 完成数据密钥解封装，随后解密载荷。
初步实验提示，该方案可能在所测配置下减少泄漏；我们尚未测试恶意服务器。
如图 1 所示，召回率为 93.6\%，Token F1 为 0.0711。

## 需要拦截的译法

The user decrypts the data key through CP-ABE-KEM and then decrypts the payload.
Experiments demonstrate that the scheme eliminates leakage against malicious servers.
As shown in Figure~\ref{fig:arch}, recall is 93.6\% and Token F1 is 0.0711.

问题：混淆 KEM 操作；删除初步性、可能性与配置限制；反转未测试范围；凭空添加引用标签。
保留数值不能抵消以上科学失真。

## 合理译稿示例

The authorized user decapsulates the data key through CP-ABE-KEM and then decrypts the payload.
Preliminary experiments suggest that the scheme may reduce leakage under the tested configurations; we have not yet tested malicious servers.
As shown in Figure 1, recall is 93.6\% and Token F1 is 0.0711.

保留图号而不猜标签。若源工程提供图号与 label 对应关系，可记录后采用该 label。
此处的 decryption/ decrypts 对载荷是合法的，不受 KEM 解封装概念的禁用词规则影响。

## 示范审校记录

| ID | 原因 | 处理 |
|---|---|---|
| R-001 | KEM 解封装被改成 decrypts | 改为 decapsulates，词形批准 |
| R-002 | “可能减少”被增强为 eliminates | 恢复 Preliminary / suggest / may / tested configurations |
| R-003 | “尚未测试恶意服务器”被改为已防御 | 恢复未测试陈述 |
| R-004 | 无依据生成 fig:arch | 恢复 Figure 1 |

这张表演示审校格式，不构成真实 Reviewer 执行记录。
