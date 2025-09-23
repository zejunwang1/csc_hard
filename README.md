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

- `--input`: 中文句子输入文件

- `--output`: 平行句对输出文件，jsonl 形式

- `--confusion_set`: 同音词混淆集文件

- `--N`: 每一行或每一对同音词最多构造的包含拼写错误的样本数

- `--pairwise`: 是否以同义词对的方式进行计数


