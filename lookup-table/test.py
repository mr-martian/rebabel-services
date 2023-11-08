#!/usr/bin/env python3

from requests import post

def check(label, url, inp, exp):
    print(label, end='\t')
    req = post(url, json=inp)
    out = req.json()
    if req.status_code != 200:
        print('ERROR CODE:', req.status_code)
        return
    def same(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            if len(a) != len(b):
                return False
            for k in a:
                if not same(a[k], b[k]):
                    return False
            return True
        else:
            return a == b
    if same(out, exp):
        print('SUCCESS')
    else:
        print('DIFFERENCE')
        print('Expected:', exp)
        print('Output:', out)

check('no prior input', 'http://localhost:5000/predict',
      {
          'unit': {
              'id': 'xyz',
              'layers': {
                  'UD': {
                      'xpos': 'NN',
                      'lemma': 'potato'
                  }
              }
          }
      },
      {
          'features': [
              {
                  'id': 'xyz',
                  'tier': 'UD',
                  'feature': 'upos',
                  'values': [{'value': 'X', 'probability': 1.0}]
              }
          ]
      }
)

check('first correction', 'http://localhost:5000/correct',
      {
          'unit': {
              'id': 'xyz',
              'layers': {
                  'UD': {
                      'xpos': 'NN',
                      'lemma': 'potato',
                      'upos': 'NOUN'
                  }
              }
          }
      },
      {'updated': True}
)

check('no prior input', 'http://localhost:5000/predict',
      {
          'unit': {
              'id': 'xyz',
              'layers': {
                  'UD': {
                      'xpos': 'NN',
                      'lemma': 'potato'
                  }
              }
          }
      },
      {
          'features': [
              {
                  'id': 'xyz',
                  'tier': 'UD',
                  'feature': 'upos',
                  'values': [{'value': 'NOUN', 'probability': 1.0}]
              }
          ]
      }
)
