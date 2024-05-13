# Reference: https://arpitbhayani.me/blogs/consistent-hashing/

import hashlib
import requests
from bisect import bisect, bisect_left, bisect_right

class StorageNode:
    def __init__(self, name, host) -> None:
        self.name = name
        self.host = host
    
    def get_file(self, path):
        return requests.get(f'https://{self.host}:123/{path}').text
    
    def put_file(self, path):
        with open(path, 'r') as fp:
            content = fp.read()
            return requests.post(f'https://{self.host}:123/{path}', body=content).text

class ConsistentHashing:
    def __init__(self, total_slots) -> None:
        self.nodes = []
        self._keys = []
        self.total_slots = total_slots
    
    def add_node(self, node: StorageNode) -> int:
        if len(self._keys) == self.total_slots:
            raise Exception("Hash space is full")
        key = hash_fn(node.host, self.total_slots)

        index = bisect(self._keys, key)

        if index > 0 and self._keys[index - 1] == key:
            raise Exception("Collision occurred")

        self.nodes.insert(index, node)
        self._keys.insert(index, key)

        return key

    def remove_node(self, node: StorageNode) -> int:
        if len(self._keys) == 0:
            raise Exception("Hash is empty")
        
        key = hash_fn(node.host, self.total_slots)

        index = bisect_left(self._keys, key)

        if index >= self.total_slots and self._keys[index] != key:
            raise Exception("Node does not exist")

        self.nodes.pop(index)
        self._keys.pop(index)

        return key
    
    def assign(self, item: str) -> StorageNode:
        key = hash_fn(item, self.total_slots)

        index = bisect_right(self._keys, key) % len(self._keys)

        return self.nodes[index]


def hash_fn(key: str, total_slots: int) -> int:
    """
    This function calculate equivalent sha256 of given key 
    and returns modulo with total_slots.
    """
    hash = hashlib.sha256()
    hash.update(bytes(key.encode('utf-8')))
    return int(hash.hexdigest(), 16) % total_slots



def main():
    storage_nodes = [
        StorageNode("1", "host1"),
        StorageNode("5", "host5"),
        StorageNode("4", "host4"),
        StorageNode("3", "host3"),
        StorageNode("2", "host2")
    ]

    ch = ConsistentHashing(256)
    for storage_node in storage_nodes:
        ch.add_node(storage_node)
    
    # for storage_node in storage_nodes:
    #     ch.remove_node(storage_node)

    print(ch.assign("50").host)


main()