#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    for i, ticket in enumerate(tickets):
        if i > hashtable.capacity * 0.2:
            hash_table_resize(hashtable)
        hash_table_insert(hashtable, ticket.source, ticket.destination)

    location = "NONE"
    for i in range(len(route)):
        print(location)
        location = hash_table_retrieve(hashtable, location)
        route[i] = location

    return route


ticket_1 = Ticket("NONE", "PDX")
ticket_2 = Ticket("PDX", "DCA")
ticket_3 = Ticket("DCA", "NONE")

tickets = [ticket_1, ticket_2, ticket_3]

expected = ["PDX", "DCA", "NONE"]
print(reconstruct_trip(tickets, 3))