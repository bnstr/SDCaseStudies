#Design an iterator that supports the peek operation on an existing iterator in addition to the hasNext and the next operations.
import unittest


#Implement the PeekingIterator class:

#PeekingIterator(Iterator<int> nums) Initializes the object with the given integer iterator iterator.
# int next() Returns the next element in the array and moves the pointer to the next element.
# boolean hasNext() Returns true if there are still elements in the array.
# int peek() Returns the next element in the array without moving the pointer.

#   store the next element in advance without moving the iterator.
# use a variable _next to cache the value of the next element.


class Iterator:
    def __init__(self, nums):
        """
        Initializes an iterator object to the beginning of a list.
        """
        self.nums = nums
        self.index = 0

    def hasNext(self):
        """
        Returns true if the iteration has more elements.
        :rtype: bool
        """
        return self.index < len(self.nums)

    def next(self):
        """
        Returns the next element in the iteration.
        :rtype: int
        """
        if self.hasNext():
            current = self.nums[self.index]
            self.index += 1
            return current
        else:
            raise StopIteration()

class PeekingIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self._next = None
        if self.iterator.hasNext():
            self._next = self.iterator.next()

    def next(self):
        if not self.hasNext():
            raise StopIteration()

        current = self._next
        if self.iterator.hasNext():
            self._next = self.iterator.next()
        else:
            self._next = None
        return current

    def hasNext(self):
        return self._next is not None

    def peek(self):
        if not self.hasNext():
            raise StopIteration()
        return self._next

class PeekingIteratorTest(unittest.TestCase):

    def setUp(self):
        # Initialize a PeekingIterator with some test data
        self.peeking_iterator = PeekingIterator(iter([1, 2, 3]))

    def test_peek_returns_next_element_without_moving_pointer(self):
        # Test that peek() returns the correct element without moving the pointer
        self.assertEqual(self.peeking_iterator.peek(), 1, "peek() should return the first element")
        self.assertEqual(self.peeking_iterator.peek(), 1, "peek() should not move the pointer")

    def test_next_returns_next_element_and_moves_pointer(self):
        # Test that next() returns the correct element and moves the pointer
        self.assertEqual(self.peeking_iterator.next(), 1, "next() should return the first element")
        self.assertEqual(self.peeking_iterator.next(), 2, "next() should return the second element")

    def test_hasNext_returns_true_if_elements_remain(self):
        # Test that hasNext() returns True as long as there are elements
        self.peeking_iterator.next()  # Move to 1
        self.peeking_iterator.next()  # Move to 2
        self.assertTrue(self.peeking_iterator.hasNext(), "hasNext() should return True when there are more elements")
        self.peeking_iterator.next()  # Move to 3
        self.assertFalse(self.peeking_iterator.hasNext(), "hasNext() should return False when no elements remain")

    def test_peek_and_next_combination(self):
        # Test the combination of peek() and next()
        self.assertEqual(self.peeking_iterator.peek(), 1, "peek() should return the first element")
        self.assertEqual(self.peeking_iterator.next(), 1, "next() should return the first element and move the pointer")
        self.assertEqual(self.peeking_iterator.peek(), 2, "peek() should now return the second element")
        self.assertEqual(self.peeking_iterator.next(), 2, "next() should now return the second element and move the pointer")
        self.assertEqual(self.peeking_iterator.peek(), 3, "peek() should now return the third element")
        self.assertEqual(self.peeking_iterator.next(), 3, "next() should now return the third element")

    def test_empty_iterator(self):
        # Test behavior when iterator is empty
        empty_iterator = PeekingIterator(iter([]))
        self.assertFalse(empty_iterator.hasNext(), "hasNext() should return False for an empty iterator")
        with self.assertRaises(StopIteration):
            empty_iterator.peek()
        with self.assertRaises(StopIteration):
            empty_iterator.next()

if __name__ == '__main__':
    unittest.main()

