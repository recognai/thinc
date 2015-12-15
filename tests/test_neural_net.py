from __future__ import division

import pytest
import pickle
import io
import numpy as np
import random
from numpy.testing import assert_allclose

from thinc.api import NeuralNet
from thinc.api import Example

def test_create():
    model = NeuralNet(3, 4, (8,))

    assert model.nr_class == 3
    assert model.nr_embed == 4
    assert model.nr_layer == 2
    assert model.layer_dims == [(8, 4), (3, 8)]

#    instance = {1: {1: 1, 3: -5}, 2: {2: 4, 3: 5}}
#    for clas, feats in instance.items():
#        eg = Example.from_feats(model.nr_class, feats.items(), gold=clas)
#        model(eg)
#        model.updater(eg)
#    eg = Example.from_feats(3, [(0, 1), (0, 1), (2, 1)])
#    model(eg)
#    assert eg.guess == 2
#    eg = Example.from_feats(3, [(0, 1), (0, 1), (2, 1)])
#    model(eg)
#    assert eg.scores[1] == 0
#    eg = Example.from_feats(3, [(0, 1), (0, 1), (2, 1)])
#    model(eg)
#    assert eg.scores[2] > 0
#    eg = Example.from_feats(3, [(0, 1), (1, 1), (0, 1)])
#    model(eg)
#    assert eg.scores[1] > 0
#    eg = Example.from_feats(3, [(0, 1), (0, 1), (0, 1), (3, 1)])
#    model(eg)
#    assert eg.scores[1] < 0 
#    eg = Example.from_feats(3, [(0, 1), (0, 1), (0, 1), (3, 1)])
#    model(eg)
#    assert eg.scores[2] > 0 
#
#
#

def test_small_network():
    random.seed(0)
    Xs = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1] ])
    ys = np.asarray([0,1,1,0])
    model = NeuralNet(2, 3, (4,))

    assert model.nr_class == 2
    assert model.nr_embed == 3
    assert model.nr_layer == 2
    assert model.nr_dense == 30
    assert model.layer_dims == [(4, 3), (2, 4)]

    for _ in range(500):
        for i, x in enumerate(Xs):
            prev = model.Example(list(enumerate(x)), gold=ys[i])
            assert len(list(prev.scores)) == prev.nr_class == model.nr_class
            assert sum(prev.scores) == 0
            model(prev)
            assert_allclose([sum(prev.scores)], [1.0])
            eg = model.Example(list(enumerate(x)), gold=ys[i])
            model.train(eg)
            eg = model.Example(list(enumerate(x)), gold=ys[i])
            model(eg)
            assert prev.scores[ys[i]] < eg.scores[ys[i]]