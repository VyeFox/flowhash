import sys
import random

sys.path.append('../src/flowhash')

import flowhash


def main():

    # test that patterns do not persist in hash
    def pattern_destruction_test(pattern: list, max: int, modulos: list) -> float:
        hash_modulo_buckets = {modulo: [0] * modulo for modulo in modulos}
        for i in range(0, max):
            mh = flowhash.flowhash(256, pattern * i)
            for modulo in modulos:
                hash_modulo_buckets[modulo][mh % modulo] = hash_modulo_buckets[modulo][mh % modulo] + 1
        for modulo in modulos:
            expected = max / modulo
            chi = sum([(bucket - expected) ** 2 / expected for bucket in hash_modulo_buckets[modulo]])
            print(f"Pattern {pattern} produced distribution {hash_modulo_buckets[modulo]} for modulo {modulo} over {max} iterations. (expected value: {max/modulo})")
            print(f"This sampled distribution has chi-square value {chi} and {modulo - 1} degrees of freedom.")
    # testing body
    print("Testing hash security...")

    iters = 64

    #! Given the current performance of the hash function...
    #! it is not possible to be confident in any assertions...
    #! of security given by the following pattern destruction tests.
    print("\nEdge case patterns")

    pattern_destruction_test([0], iters, [2, 3, 5, 7, 16])
    pattern_destruction_test([255], iters, [2, 3, 5, 7, 16])
    pattern_destruction_test([0, 255], iters, [2, 3, 5, 7, 16])
    pattern_destruction_test([255, 0], iters, [2, 3, 5, 7, 16])

    pattern_destruction_test([1], iters, [2, 3, 5, 7, 16])
    pattern_destruction_test([254], iters, [2, 3, 5, 7, 16])
    pattern_destruction_test([1, 254], iters, [2, 3, 5, 7, 16])
    pattern_destruction_test([254, 1], iters, [2, 3, 5, 7, 16])

if __name__ == "__main__":
    main()
    sys.exit(0)

