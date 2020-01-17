import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def update_target():
    r = requests.get(url=node + "/last_proof")
    data = r.json()
    return data.get('proof')

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()
    attempts = 0

    print("Searching for next proof")
    magnitude = 666
    direction = -1
    proof = magnitude
    last_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()

    while True:
        magnitude += random.randint(0, 99999)
        proof = random.choice([1, -1]) * magnitude
        guess = str(proof)
        if valid_proof(last_hash, guess):
            print("Proof found: " + str(proof) + " in " + str(timer() - start))
            return proof
        else:
            attempts += 1
            if attempts % 323456 == 0:
                last_proof = update_target()
                last_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()
                print('updated last_proof:', str(last_proof))
            if attempts % 1234567 == 0:
                print('attempts:', attempts, '\nlast try:', proof)


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """

    # TODO: Your code here!
    encoded = proof.encode()
    hashed = hashlib.sha256(encoded).hexdigest()
    return last_hash[-6:] == hashed[:6]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        # r = requests.get(url=node + "/last_proof")
        # data = r.json()
        new_proof = proof_of_work(update_target())

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
            with open('record', 'a') as f:
                f.write(str(coins_mined))
        else:
            print(data.get('message'))
