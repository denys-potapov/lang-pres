from collections import defaultdict
import csv
import re

WHAT_LANG = 'Якою мовою пишете для роботи зараз?'
OTHER = 'Інші'
BIG_LANGS = ['Java', 'JavaScript', 'C#', 'PHP', 'Python', 'C++']
ALL = 'Всі'

candidates = set()
votes = defaultdict(list)

# fill candaidates set and vodes dict
lines = csv.DictReader(open('data.csv'))
for line in lines:
    lang = line[WHAT_LANG]
    ballot = []
    for key, vote in line.items():
        names = re.findall('\[(.*)\]', key)
        if len(names) != 1:
            continue
        name = names[0]
        candidates.add(name)
        if vote == '':
            vote = '0'
        vote = int(vote)
        ballot.append((vote, name))

    votes[lang].append(ballot)
    votes[ALL].append(ballot)
    if lang not in BIG_LANGS:
        votes[OTHER].append(ballot)

    print(votes)
    print(candidates)
    exit(0)
