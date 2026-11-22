import unittest

from knuth_fisher_yates_shuffle_tools import shuffle


class TestShuffle(unittest.TestCase):
    def test_empty(self):
        seq = []
        shuffle(seq)
        self.assertEqual(seq, [])

    def test_single(self):
        seq = [42]
        shuffle(seq)
        self.assertEqual(seq, [42])

    def test_two_elements(self):
        # With a deterministic source that always picks index 0, the two
        # elements should swap.
        seq = [1, 2]
        shuffle(seq, rand=lambda n: 0)
        self.assertEqual(seq, [2, 1])

    def test_identity_with_max_choices(self):
        # If the random source always returns the maximum allowed index,
        # each swap is with itself, so the sequence is unchanged.
        seq = [10, 20, 30, 40]
        shuffle(seq, rand=lambda n: n - 1)
        self.assertEqual(seq, [10, 20, 30, 40])

    def test_all_permutations_possible(self):
        # For a three-element list, a source that cycles through all
        # possible indices for each i should produce all 6 permutations
        # over 6 calls.  We use a deterministic counter.
        perms = set()
        for seed in range(6):
            seq = [1, 2, 3]
            counter = [seed]

            def rand(n):
                # Deterministic but varies with seed.
                val = counter[0] % n
                counter[0] += 1
                return val

            shuffle(seq, rand=rand)
            perms.add(tuple(seq))
        self.assertEqual(len(perms), 6)
        self.assertEqual(perms, {
            (1, 2, 3),
            (1, 3, 2),
            (2, 1, 3),
            (2, 3, 1),
            (3, 1, 2),
            (3, 2, 1),
        })

    def test_immutable_raises(self):
        with self.assertRaises(TypeError):
            shuffle((1, 2, 3))
        with self.assertRaises(TypeError):
            shuffle("abc")

    def test_bad_random_source(self):
        seq = [1, 2, 3]
        with self.assertRaises(ValueError):
            shuffle(seq, rand=lambda n: n)
        with self.assertRaises(ValueError):
            shuffle(seq, rand=lambda n: -1)

    def test_in_place(self):
        seq = [1, 2, 3]
        result = shuffle(seq, rand=lambda n: 0)
        self.assertIsNone(result)
        self.assertEqual(seq, [2, 3, 1])

    def test_uses_randrange_by_default(self):
        # We cannot control the default random source, but we can verify
        # that shuffle accepts the default and produces a permutation.
        seq = list(range(10))
        shuffle(seq)
        self.assertCountEqual(seq, range(10))


if __name__ == '__main__':
    unittest.main()
