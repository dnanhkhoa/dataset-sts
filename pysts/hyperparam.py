"""
Toolkit for model hyperparameter search.
"""

from __future__ import division
from __future__ import print_function

import json
import random


class RandomSearch:
    def __init__(self, logfile, **params):
        self.params = params
        self.rlog = open(logfile, 'a')

    def __call__(self):
        while True:
            pardict = dict()
            for p, vset in self.params.items():
                if isinstance(vset, dict):
                    v = dict()
                    for k, kset in vset.items():
                        vc = random.choice(kset)
                        if vc:
                            v[k] = vc
                    pardict[p] = v
                else:
                    pardict[p] = random.choice(vset)
            ps = json.dumps(dict([(k, str(v)) for k, v in pardict.items()]), sort_keys=True)
            h = hash(ps)
            print('%s %s' % (h, ps), file=self.rlog)
            self.rlog.flush()
            yield (ps, h, pardict)

    def report(self, ps, h, mrr):
        print('%s %f' % (h, mrr), file=self.rlog)
        self.rlog.flush()
