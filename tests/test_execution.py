import sys
import random

sys.path.append('../src/flowhash')

import flowhash


def main():

    # no - throw test for default hash combiner
    def test_default_hash_op(bit_count, runs):
        print(f"\nTesting default hash combiner {bit_count}")
        combiner = flowhash.FlowDigest.simple_hash_op(bit_count)
        for i in range(runs):
            state = random.randrange(0, 1 << bit_count)
            update = random.randrange(0, 1 << bit_count)
            # state #= update :: state = hash_op(state, update)
            new_state = None
            try:
                new_state = combiner(state, update)
            except Exception as ex:
                print(f"\n::: FAIL ::: Default hash combiner ({bit_count}) failed on trial {i} with state ({state}) and update ({update}) with exception: {ex}")
            print(f"Default hash combiner ({bit_count}) trial {i} with state ({state}) and update ({update}) successfully returned {new_state}")

    # compound main use case test
    def flow_digest_compound_test(address_size: int) -> None:
        flow = None
        try:
            flow = flowhash.FlowDigest(address_size, 256, list(range(1 << address_size)))
        except Exception as ex:
            print(f"::: FAIL ::: Creation of FlowDigest over range(1 << {address_size}) failed with exception: {ex}")
            return None
        try:
            flow.execute()
        except Exception as ex:
            print(f"::: FAIL ::: Execution of FlowDigest over range(1 << {address_size}) failed with exception: {ex}")
            return None
        try:
            flow.execute()
        except Exception as ex:
            print(f"::: FAIL ::: Aditional execution of FlowDigest over range(1 << {address_size}) failed with exception: {ex}")
            return None
        print(f"FlowDigest over range(1 << {address_size}) executed successfully.")

    # singleton flowhash test (address_size = 0)
    def flow_digest_singleton_test(hash_op) -> None:
        flow = None
        try:
            flow = flowhash.FlowDigest(0, 256, [0], hash_op)
        except Exception as ex:
            print(f"::: FAIL ::: Creation of singleton FlowDigest failed with exception: {ex}")
            return None
        print(str(flow))
        value = None
        try:
            value = flow.execute()
        except Exception as ex:
            print(f"::: FAIL ::: Execution of singleton FlowDigest failed with exception: {ex}")
            return None
        print(str(flow))
        print(f"Singleton FlowDigest executed successfully with value {value}")

    # flowhash function test
    def flowhash_hash_test(digest_length) -> None:
        digest = [random.randrange(0, 1 << 256) for _ in [None] * digest_length]
        value = None
        try:
            value = flowhash.flowhash(256, digest)
        except Exception as ex:
            print(f"::: FAIL ::: flowhash(256, [{digest_length}...]) failed with exception: {ex}")
            return None
        print(f"flowhash(256, [{digest_length}...]) executed successfully with value {value}")

    # testing body
    print("Running tests...")

    test_default_hash_op(256, 64)

    print("\nTesting FlowDigest for different address sizes")
    for i in range(8):
        flow_digest_compound_test(i)

    print("\nTesting singleton FlowDigest")
    flow_digest_singleton_test(flowhash.FlowDigest.simple_hash_op(256))

    print("\nTesting flowhash function")
    flowhash_hash_test(1)
    flowhash_hash_test(7)
    flowhash_hash_test(16)
    flowhash_hash_test(4)
    flowhash_hash_test(2)
    flowhash_hash_test(83)
    flowhash_hash_test(41)


if __name__ == '__main__':
    main()
    sys.exit(0)