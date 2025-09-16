# csc_hard: 高质量中文拼写纠错数据集

参考 [confuse](https://github.com/zejunwang1/confuse) 项目中的方法构建同音词混淆集 `jieba_homophones.txt`。

使用人民日报 2023 和 2024 年的新闻句子，自动化构建难区分的中文拼写纠错数据集：

```bash
python confuse_replace_jieba.py \
    --input people_daily_sents.txt \
    --output people_daily.jsonl \
    --confusion_set jieba_homophones.txt \
    --N 2 \
    --seed 37
```

`N` 表示混淆集中的每一行最多构造的包含拼写错误的样本数。


