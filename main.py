from collections import defaultdict
import csv
import re

WHAT_LANG = 'Якою мовою пишете для роботи зараз?'

# Languages
BIG_LANGS = ['Java', 'JavaScript', 'C#', 'PHP', 'Python', 'C++']
ALL = 'Всі'
OTHER = 'Інші'
BIG_LANGS_ALL = BIG_LANGS + [OTHER, ALL]

# candidates
UNDEF = 'Не визначився'
BIG_CANDS = ['Порошенко Петро', 'Зеленський Володимир', 'Гриценко Анатолiй', UNDEF]

candidates = {UNDEF}
votes = defaultdict(list)

# Parse candaidates set and vodes dict
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

# rating

# 
def single_vote(ballot):
    votes = [b[0] for b in ballot]
    max_vote = max(votes)
    if max_vote <= 0 or votes.count(max_vote) > 1:
        return UNDEF
    for v, n in ballot:
        if v == max_vote:
            return n

ratings = {}
for lang, ballots in votes.items():
    rating = {c:0 for c in candidates}
    for ballot in ballots:
        v = single_vote(ballot)
        rating[v] = rating[v] + 1
    for c in candidates:
        rating[c] = 100 * float(rating[c]) / len(ballots)
    ratings[lang] = rating

for cand in BIG_CANDS:
    print('<strong>{}</strong>'.format(cand))
    for lang in BIG_LANGS_ALL:
        if lang != ALL:
            print('{} {:.0f}%'.format(lang, ratings[lang][cand]))
        else:
            print('<i>{} {:.0f}%</i>'.format(lang, ratings[lang][cand]))
    print('')
