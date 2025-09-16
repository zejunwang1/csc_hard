# coding=utf-8

import argparse
import json
import jieba
import random
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--confusion_set", type=str, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--N", type=int, default=1)
    args = parser.parse_args()
    return args

def isChinese(word):
    for ch in word:
        cp = ord(ch)
        if cp >= 0x4E00 and cp <= 0x9FA5:
            continue
        return False
    return True

def load_confusion_set(path):
    confusion_set = {}
    with open(path, mode='r', encoding='utf-8') as handle:
        for line in handle:
            line = line.strip().split()
            assert len(line) > 1
            confusion_set[line[0]] = line[1:]
    return confusion_set

def do_mask(sent, args, output):
    # jieba分词
    hits = []
    cws = jieba.lcut(sent)
    for i in range(len(cws)):
        word = cws[i]
        if len(word) > 2 or not isChinese(word):
            continue
        if word not in args.confusion_set:
            continue
        hits.append(i)

    if hits:
        random.shuffle(hits)
        for j in hits:
            word = cws[j]
            target = random.choice(args.confusion_set[word])
            if word not in args.replace:
                args.replace[word] = 0
            else:
                args.replace[word] += 1
            if args.replace[word] < args.N:
                cws[j] = target
                source = ''.join(cws)
                label = int(source != sent)
                output.write(
                    json.dumps({"source": source, "target": sent, "label": label}, ensure_ascii=False)
                )
                output.write("\n")
                break

if __name__ == "__main__":
    args = parse_args()
    random.seed(args.seed)

    # 混淆集
    args.confusion_set = load_confusion_set(args.confusion_set)

    sents = []
    with open(args.input, mode='r', encoding='utf-8') as handle:
        for line in handle:
            sent = line.strip()
            if len(sent) < 4:
                continue
            sents.append(sent)

    # do shuffle
    random.shuffle(sents)
    args.replace = {}
    output = open(args.output, mode='w')
    for sent in tqdm(sents):
        do_mask(sent, args, output)

