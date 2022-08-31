# Name: Trace Sweeney
# OSU Email: sweenetr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: June 3, 2022
# Description: In this program I will be implementing a hash map 
# using open addressing.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """This method takes a key and inserts a value to it
        using a hash map structure.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        #add a new value to the map
        index = self._hash_function(key) % self._capacity
        original_index = index
        quadratic_counter = 1
        while self._buckets[index] is not None and self._buckets[index].is_tombstone != True:
            #check to see if the key is equal to a key thats already in it
            if self._buckets[index].key == key:
                self._buckets[index].value = value
                return
            #check to see if the index is a tombstone and if it is replace it
            elif self._buckets[index].is_tombstone == True:
                self._buckets.set_at_index(index, HashEntry(key, value))
                return
            else:
                index = (original_index + (quadratic_counter * quadratic_counter)) % self._capacity
                quadratic_counter += 1
        #if we exit it means we found an open spot
        self._buckets.set_at_index(index, HashEntry(key, value))
        self._size += 1

    def table_load(self) -> float:
        """This function returns the total amount of elements in the
        table divided by the number of buckets.
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """This function returns the total amount of empty buckets
        in the hash map.
        """
        empty_buckets = 0
        counter = 0
        while counter < self._capacity:
            hash = self._buckets.get_at_index(counter)
            if hash == None:
                empty_buckets += 1
            counter += 1
        return empty_buckets

    def resize_table(self, new_capacity: int) -> None:
        """This function resizes the table and moves the elements 
        that already exist into the corresponding spot.
        """
        #check to make sure new_capacity is valid
        if new_capacity < 1 or new_capacity < self._size:
            return
        old_buckets = self._buckets
        old_capacity = self._capacity
        self._capacity = new_capacity
        self._size = 0
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

        counter = 0
        #now that you have a new capacity table move 
        #all the stuff from the old table to the new one
        while counter < old_capacity:
            hash = old_buckets[counter]
            if hash == None or hash.is_tombstone == True:
                counter += 1
            else:
                self.put(hash.key, hash.value)
                counter += 1

    def get(self, key: str) -> object:
        """This function returns the value associated with the key
        given, if the value does not exist it returns none
        """
        index = self._hash_function(key) % self._capacity
        quadratic_counter = 1
        original_index = index
        while self._buckets[index] != None and self._buckets[index].key != key:
            index = original_index + (quadratic_counter * quadratic_counter)
            if index >= self._capacity:
                index = index % self._capacity
            quadratic_counter += 1
        if self._buckets[index] == None or self._buckets[index].is_tombstone == True:
            return None
        else: 
            return self._buckets[index].value 


    def contains_key(self, key: str) -> bool:
        """this function returns True if the hash map contains
        the key and false otherwise
        """
        index = self._hash_function(key) % self._capacity
        quadratic_counter = 1
        original_index = index
        while self._buckets[index] != None and self._buckets[index].key != key:
            index = original_index + (quadratic_counter * quadratic_counter)
            if index >= self._capacity:
                index = index % self._capacity
            quadratic_counter += 1
        if self._buckets[index] == None or self._buckets[index].is_tombstone == True:
            return False
        else: 
            return True

    def remove(self, key: str) -> None:
        """this function removes a value from the hash map and
        replaces its value with __tombstone__ if it is in the middle of
        the array.
        """
        #find the index
        index = self._hash_function(key) % self._capacity
        #now loop through, if you reach None then it doesnt exist and you need
        #to just return
        quadratic_counter = 1
        original_index = index
        while self._buckets[index] != None and self._buckets[index].key != key:
            index = (original_index + (quadratic_counter * quadratic_counter)) % self._capacity
            quadratic_counter += 1
        #if the hash is equal to None it means that the value is not there
        if self._buckets[index] == None or self._buckets[index].is_tombstone == True:
            return
        #if it is here it means that the hash does not equal None
        self._buckets[index].is_tombstone = True
        self._size -= 1

    def clear(self) -> None:
        """This function clears all the buckets in the array
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """This function returns a dynamic array of all of the
        keys in the function.
        """
        counter = 0
        keys_da = DynamicArray()
        while counter < self._capacity:
            if self._buckets[counter] == None or self._buckets[counter].is_tombstone == True:
                counter += 1
            else:
                keys_da.append(self._buckets[counter].key)
                counter += 1
        return keys_da


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())