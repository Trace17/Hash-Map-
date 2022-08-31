# Name: Trace Sweeney
# OSU Email: sweenetr@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: June 3, 2022
# Description: In this program I will be implementing a hash map 
# using seperate chanining.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

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
        #find the index to insert at
        index = self._hash_function(key) % self._capacity
        #find the linked list corresponding to the index
        linked_list = self._buckets.get_at_index(index)
        node = linked_list.contains(key)
        #check to see if the call to contains returned a node
        if node != None:
            #if it did it means the key matched an existing key, update its value
            node.value = value
        #otherwise get the linked list and insert a node at it
        else:
            linked_list = self._buckets.get_at_index(index)
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """This function returns the total amount of empty buckets
        in the hash map.
        """
        empty_buckets = 0
        counter = 0
        while counter < self._capacity:
            node = self._buckets.get_at_index(counter)
            node_iterator = node.__iter__()
            try: 
                node_iterator.__next__()
            except: 
                empty_buckets += 1
            counter += 1
        return empty_buckets

    def table_load(self) -> float:
        """This function returns the total amount of elements in the
        table divided by the number of buckets.
        """
        load_factor = self._size / self._capacity
        return load_factor

    def clear(self) -> None:
        """This function clears the contents of the hash map
        """
        counter = 0
        while counter < self._capacity:
            self._buckets.set_at_index(counter, LinkedList())
            counter += 1
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """This function resizes the table and moves the elements 
        that already exist into the corresponding spot.
        """
        #check to make sure new_capacity is valid
        if new_capacity < 1:
            return
        #create a new dynamic array with the new capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())
        
        counter = 0
        #iterate through the current buckets
        while counter < self._capacity:
            #get the linked list for the index
            linked_list = self._buckets.get_at_index(counter)
            try:
                #try to see if the linked_list has a head
                iterator = linked_list.__iter__()
                head = iterator.__next__()
                while head.value != None:
                    #find the key for the value
                    key = head.key
                    #find the new_index to insert the value at
                    new_index = self._hash_function(key) % new_capacity
                    #find the linked list which corresponds to that index
                    new_linked_list = new_buckets.get_at_index(new_index)
                    #insert into that new index the new key and value pair
                    new_linked_list.insert(head.key,head.value)
                    head = iterator.__next__()
                counter += 1
            except:
                counter += 1
        #set the buckets to equal the new buckets and set the capacty
        #to equal the correct capacity.        
        self._buckets = new_buckets
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """This function returns the value associated with the key
        given, if the value does not exist it returns none
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets.get_at_index(index)
        node = linked_list.contains(key)
        if node == None:
            return None
        else:
            return node.value


    def contains_key(self, key: str) -> bool:
        """this function returns True if the hash map contains
        the key and false otherwise
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets.get_at_index(index)
        node = linked_list.contains(key)
        if node == None:
            return False
        else:
            return True


    def remove(self, key: str) -> None:
        """This function removes the key from the hash map if it
        exists, otherwise it does nothing.
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets.get_at_index(index)
        return_value = linked_list.remove(key)
        if return_value == False:
            return
        else:
            self._size -= 1

    
    def get_keys(self) -> DynamicArray:
        """This function returns a dymanic array which contains all the 
        keys in the hash map.
        """
        keys_dynamic_array = DynamicArray()
        counter = 0
        while counter < self._capacity:
            linked_list = self._buckets.get_at_index(counter)
            iterator = linked_list.__iter__()
            try:
                node = iterator.__next__()
                keys_dynamic_array.append(node.key)
                while node.value != None:
                    node = iterator.__next__()
                    keys_dynamic_array.append(node.key)
                counter += 1
            except:
                counter += 1
        return keys_dynamic_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """This function finds the mode of a function using the hash map 
    data structure and returns a dynamic array containing the mode and a 
    integer which represents how many time the mode/s were found.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)
    mode = 0
    mode_da = DynamicArray()
    counter = 0

    while counter < da.length():
        #find the key 
        key = da[counter]
        #get the linked list that is associated with this value,
        #if there isnt one insert it and set its value to 1
        value = map.get(key)
        if value == None:
            value = 1
            map.put(key, value)
        #if it does already exist, add 1 to its value
        else:
            value += 1
            map.put(key, value)
        #compare the value to the mode, if they equal add the new
        #value to the array
        if value == mode:
            mode_da.append(key)
        #otherwise replace the array and add the new value
        elif value > mode:
            mode = value
            mode_da = DynamicArray()
            mode_da.append(key)
        counter += 1

    return mode_da, mode
    
        


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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
