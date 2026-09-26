"""Score predictions on RuDecide.

predictions.jsonl: one line per item {"id": ..., "probabilities": {option: p, ...}}
                   (or {"id": ..., "prediction": option}).
Usage: python score.py data/track_a_unseen.jsonl predictions.jsonl
Prints per-task accuracy, chance-normalized skill (acc - 1/K) / (1 - 1/K) and track means.
"""
import json, sys, collections

def options(q):
    if q['type'] == 'noul':
        return ['false', 'true']
    if q['type'] == 'score':
        return [str(i) for i in range(len(q['criteria']))]
    return list(q['criteria'])

gold = {}
for line in open(sys.argv[1], encoding='utf-8'):
    r = json.loads(line)
    gold[r['id']] = r
pred = {}
for line in open(sys.argv[2], encoding='utf-8'):
    p = json.loads(line)
    pred[p['id']] = p.get('prediction') or max(p['probabilities'], key=p['probabilities'].get)

by = collections.defaultdict(list)
for i, r in gold.items():
    k = len(options(r['question']))
    by[r['task']].append((str(pred.get(i)) == r['answer'], k))
missing = sum(1 for i in gold if i not in pred)
accs, skills = {}, {}
for t, v in sorted(by.items()):
    a = sum(x for x, _ in v) / len(v)
    ch = sum(1 / k for _, k in v) / len(v)
    accs[t], skills[t] = a, (a - ch) / (1 - ch)
    print(f'{t:26s} n={len(v):4d} acc={100 * a:5.1f} skill={100 * skills[t]:5.1f}')
print(f'MEAN acc={100 * sum(accs.values()) / len(accs):.1f} skill={100 * sum(skills.values()) / len(skills):.1f} missing={missing}')
