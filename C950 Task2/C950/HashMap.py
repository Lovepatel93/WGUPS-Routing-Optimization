class HashMap:
    def __init__(self, initial_capacity: int = 20):
        """
        Initializes a HashMap with given initial capacity.

        :param initial_capacity: Initial size of the hash map. Default is 20.
        :type initial_capacity: int

        Time Complexity:
            O(n) where n is the initial_capacity. (For initializing the list of lists.)
        Space Complexity:
            O(n) where n is the initial_capacity.
        """
        self.buckets = [[] for _ in range(initial_capacity)]

    def insert(self, key, item) -> bool:
        """
        Inserts a new item into the hash table. If the key already exists, it updates the value.

        :param key: The key for the item.
        :param item: The item to be inserted/updated.
        :return: Always returns True for successful insert/update.

        Time Complexity:
            Average case: O(1)
            Worst case (if all keys collide): O(n) where n is the number of items with the same hash.
        Space Complexity:
            O(1)
        """
        bucket_index = hash(key) % len(self.buckets)
        bucket = self.buckets[bucket_index]

        for kv_pair in bucket:
            if kv_pair[0] == key:
                kv_pair[1] = item
                return True

        bucket.append([key, item])
        return True

    def lookup(self, key):
        """
        Looks up an item in the hash table using its key.

        :param key: The key to look for.
        :return: The corresponding item if found, otherwise None.

        Time Complexity:
            Average case: O(1)
            Worst case (if all keys collide): O(n) where n is the number of items with the same hash.
        Space Complexity:
            O(1)
        """
        bucket_index = hash(key) % len(self.buckets)
        bucket = self.buckets[bucket_index]

        for kv_pair in bucket:
            if kv_pair[0] == key:
                return kv_pair[1]

        return None  # Key was not found

    def hash_remove(self, key) -> bool:
        """
        Removes an item from the hash table using its key.

        :param key: The key for the item to remove.
        :return: True if the item was found and removed, False otherwise.

        Time Complexity:
            Average case: O(1)
            Worst case (if all keys collide): O(n) where n is the number of items with the same hash.
        Space Complexity:
            O(1)
        """
        bucket_index = hash(key) % len(self.buckets)
        bucket = self.buckets[bucket_index]

        for idx, kv_pair in enumerate(bucket):
            if kv_pair[0] == key:
                bucket.pop(idx)
                return True

        return False  # Key was not found
