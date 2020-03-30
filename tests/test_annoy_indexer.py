import os
import unittest

import numpy as np

from jina.executors.indexers import BaseIndexer
from jina.executors.indexers.annoy import AnnoyIndexer
from jina.executors.indexers.numpy import NumpyIndexer
from tests import JinaTestCase

vec_idx = np.random.randint(0, high=100, size=[1, 10])
vec = np.random.random([10, 5])
query = np.array(np.random.random([10, 5]), dtype=np.float32)


class MyTestCase(JinaTestCase):

    def test_simple_annoy(self):
        from annoy import AnnoyIndex
        _index = AnnoyIndex(5, 'angular')
        for j in range(3):
            _index.add_item(j, np.random.random((5,)))
        _index.build(4)
        idx1, _ = _index.get_nns_by_vector(np.random.random((5,)), 3, include_distances=True)

    def test_np_indexer(self):
        a = NumpyIndexer(index_filename='np.test.gz')
        a.add(vec_idx, vec)
        a.save()
        a.close()
        self.assertTrue(os.path.exists(a.index_abspath))
        # a.query(np.array(np.random.random([10, 5]), dtype=np.float32), top_k=4)

        b = BaseIndexer.load(a.save_abspath)
        idx, dist = b.query(query, top_k=4)
        print(idx, dist)
        self.assertEqual(idx.shape, dist.shape)
        self.assertEqual(idx.shape, (10, 4))
        self.add_tmpfile(a.index_abspath, a.save_abspath)

    def test_annoy_indexer(self):
        a = AnnoyIndexer(index_filename='annoy.test.gz')
        a.add(vec_idx, vec)
        a.save()
        a.close()
        self.assertTrue(os.path.exists(a.index_abspath))
        # a.query(np.array(np.random.random([10, 5]), dtype=np.float32), top_k=4)

        b = BaseIndexer.load(a.save_abspath)
        idx, dist = b.query(query, top_k=4)
        print(idx, dist)
        self.assertEqual(idx.shape, dist.shape)
        self.assertEqual(idx.shape, (10, 4))
        self.add_tmpfile(a.index_abspath, a.save_abspath)


if __name__ == '__main__':
    unittest.main()
