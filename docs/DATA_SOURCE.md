# 数据来源与共享范围

Enron-Spam preprocessing corpus, Enron1 subset. 原始下载入口：
https://www2.aueb.gr/users/ion/data/enron-spam/preprocessed/enron1.tar.gz

SHA256：3d6a1fcced6c30b1701a3fd04c6b912d7046208f6ef6f4fdcf022f64bdc6c32f

保持原 revised 的 Latin-1 解码、移除 Subject 行、lowercase+空白归一去重、冲突组丢弃和 seed42 分层60/20/20。不同规范化或划分会改变数据，不应混用结果。

本地检查包包含原始下载档和邮件日志，目的是小组复核。尚未确认明确的开放再分发许可证；“网上可下载”不等于可以任意公开再分发。GitHub 的建议提交范围排除原始档、正文、人工评分原文和完整失败案例；保留来源、哈希、下载说明、统计指标和无正文预测。老师要求保留输入与复现证据，可通过原始来源与本地受控材料复现；如 TA 要求托管输入，应先确认许可和访问范围。
