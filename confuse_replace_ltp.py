# coding=utf-8

import argparse
import json
import random
from ltp import LTP
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--confusion_set", type=str, required=True)
    parser.add_argument("--ltp_model", type=str, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--N", type=int, default=1)
    parser.add_argument("--pairwise", action="store_true")
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
    # 分词和词性标注
    cws, pos = args.ltp.pipeline(sent, tasks=["cws", "pos"], return_dict=False)

    hits = []
    for i in range(len(cws)):
        word = cws[i]
        if len(word) > 2 or not isChinese(word):
            continue
        # 人名地名
        if pos[i] in ['nh', 'ns']:
            continue
        # '地' + 动词
        #if pos[i] != 'u' or i == len(cws) - 1:   continue
        #if i < len(cws) - 1 and pos[i + 1][0] != 'v':   continue
        if word not in args.confusion_set:
            continue
        hits.append(i)

    if hits:
        target = ''.join(cws)
        random.shuffle(hits)
        for j in hits:
            word = cws[j]
            homophone = random.choice(args.confusion_set[word])
            key = word
            if args.pairwise:
                key = word + '_' + homophone
            if key not in args.replace:
                args.replace[key] = 0
            else:
                args.replace[key] += 1
            if args.replace[key] < args.N:
                cws[j] = homophone
                source = ''.join(cws)
                label = int(source != target)
                output.write(
                    json.dumps({"source": source, "target": target, "label": label}, ensure_ascii=False)
                )
                output.write("\n")
                break

if __name__ == "__main__":
    args = parse_args()
    random.seed(args.seed)

    # 混淆集
    args.confusion_set = load_confusion_set(args.confusion_set)

    # LTP/legacy
    args.ltp = LTP(args.ltp_model)
    
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

