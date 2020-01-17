#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    for i, weight in enumerate(weights):
        partner = hash_table_retrieve(ht, limit - weight)
        if partner is not None:
            return max(i, partner), min(i, partner)
        else:
            if i > ht.capacity * 0.2:
                hash_table_resize(ht)
            hash_table_insert(ht, weight, i)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")

mock = [
    [[4, 4], 2, 8]
]

for args in mock:
    print(get_indices_of_item_weights(*args))