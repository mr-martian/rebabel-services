#!/usr/bin/env python3

from flask import Flask, request
from itertools import product
from collections import defaultdict

app = Flask('rebabel-service-baseline')

# TODO: these should be in config
SRC_FEATS = [('UD', 'xpos'), ('UD', 'lemma')]
DEST_FEAT = ('UD', 'upos')

# TODO: this should be in file probably
DATA = defaultdict(lambda: defaultdict(lambda: 0))
DATA[('', '')]['X'] = 1

@app.post('/predict')
def predict():
    blob = request.json
    feats = blob['unit']['layers']
    query = []
    for tier, feat in SRC_FEATS:
        query.append([feats.get(tier, {}).get(feat, '')])
        if query[-1] != '':
            query[-1].append('')
    for tup in product(*query):
        if tup in DATA:
            count = sum(DATA[tup].values())
            return {'features': [
                {
                    'id': blob['unit']['id'],
                    'tier': DEST_FEAT[0],
                    'feature': DEST_FEAT[1],
                    'values': [
                        {'value': k, 'probability': v/count}
                        for k,v in DATA[tup].items()
                    ],
                }
            ]}

@app.post('/correct')
def correct():
    global DATA
    blob = request.json
    feats = blob['unit']['layers']
    key = []
    for tier, feat in SRC_FEATS:
        key.append(feats.get(tier, {}).get(feat, ''))
    key = tuple(key)
    result = feats.get(DEST_FEAT[0], {}).get(DEST_FEAT[1], '')
    DATA[key][result] += 1
    return {'updated': True}
