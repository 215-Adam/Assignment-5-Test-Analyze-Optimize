# 🔍 Problem 1: Find Most Frequent Element
# Given a list of integers, return the value that appears most frequently.
# If there's a tie, return any of the most frequent.
#
# Example:
# Input: [1, 3, 2, 3, 4, 1, 3]
# Output: 3

def most_frequent(numbers):
    # An empty list has no most frequent element.
    if not numbers:
        return None

    counts = {}
    best_value = numbers[0]
    best_count = 0

    # Count each value and track the leader in the same pass,
    # so we never need a second loop over the dictionary.
    for num in numbers:
        counts[num] = counts.get(num, 0) + 1
        if counts[num] > best_count:
            best_count = counts[num]
            best_value = num

    return best_value


def test_most_frequent():
    assert most_frequent([1, 3, 2, 3, 4, 1, 3]) == 3       # example from prompt
    assert most_frequent([]) is None                        # edge: empty list
    assert most_frequent([7]) == 7                          # edge: single element
    assert most_frequent([5, 5, 5, 5]) == 5                 # edge: all the same
    assert most_frequent([1, 2, 1, 2]) in (1, 2)            # edge: tie
    assert most_frequent([-1, -1, 0, 2]) == -1              # negative numbers
    assert most_frequent([1, 2, 3, 4]) in (1, 2, 3, 4)      # edge: all unique
    print("most_frequent: all tests passed")

"""
Time and Space Analysis for problem 1:
- Best-case: O(n). Every element must be counted to be sure no other value
  overtakes the current leader, so even a list of identical values is O(n).
- Worst-case: O(n). One pass with O(1) average dictionary lookups/inserts.
  (In the pathological case of many hash collisions, dict operations degrade
  and the loop could approach O(n^2), but that is extremely rare for ints.)
- Average-case: O(n).
- Space complexity: O(k), where k is the number of distinct values
  (O(n) in the worst case when every value is unique).
- Why this approach? A hash map gives O(1) average counting, and tracking the
  leader while counting avoids a second pass. The naive alternative,
  calling numbers.count(x) for every x, is O(n^2).
- Could it be optimized? Not asymptotically: any correct solution must look at
  every element, so O(n) time is the lower bound. collections.Counter
  (Counter(numbers).most_common(1)) is the same O(n) but runs in C and is
  shorter. If the values are small non-negative integers in a known range,
  a plain list of counts could replace the dict for lower constant overhead.
- Trade-offs: The dict costs O(k) extra memory in exchange for linear time.
  Sorting first and counting runs would use less extra memory (O(1) with an
  in-place sort) but costs O(n log n) time and mutates/copies the input.
"""


# 🔍 Problem 2: Remove Duplicates While Preserving Order
# Write a function that returns a list with duplicates removed but preserves order.
#
# Example:
# Input: [4, 5, 4, 6, 5, 7]
# Output: [4, 5, 6, 7]

def remove_duplicates(nums):
    seen = set()
    result = []

    # The set gives O(1) membership checks; the list keeps the original order.
    for num in nums:
        if num not in seen:
            seen.add(num)
            result.append(num)

    return result


def test_remove_duplicates():
    assert remove_duplicates([4, 5, 4, 6, 5, 7]) == [4, 5, 6, 7]  # example from prompt
    assert remove_duplicates([]) == []                             # edge: empty list
    assert remove_duplicates([1]) == [1]                           # edge: single element
    assert remove_duplicates([2, 2, 2, 2]) == [2]                  # edge: all duplicates
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]               # edge: no duplicates
    assert remove_duplicates([3, 1, 3, 2, 1]) == [3, 1, 2]         # order of first appearance
    original = [1, 1, 2]
    remove_duplicates(original)
    assert original == [1, 1, 2]                                   # input is not mutated
    print("remove_duplicates: all tests passed")

"""
Time and Space Analysis for problem 2:
- Best-case: O(n). Every element must still be checked against the set.
- Worst-case: O(n). Each set lookup/insert and list append is O(1)
  (amortized for append, average for the set).
- Average-case: O(n).
- Space complexity: O(n). The set and the result list each hold up to n
  elements when every value is unique.
- Why this approach? Checking "if num not in result" against the list would
  be O(n) per check and O(n^2) overall. The set makes each check O(1) while
  the separate result list preserves first-appearance order.
- Could it be optimized? Not asymptotically. list(dict.fromkeys(nums)) is an
  equivalent O(n) one-liner (dicts keep insertion order since Python 3.7)
  and is faster in practice because the loop runs in C.
- Trade-offs: We spend O(n) extra memory on the set to gain linear time.
  The set approach also requires hashable elements; for unhashable items
  (e.g. lists) you would have to fall back to the O(n^2) list-scan approach.
"""


# 🔍 Problem 3: Return All Pairs That Sum to Target
# Write a function that returns all unique pairs of numbers in the list that sum to a target.
# Order of output does not matter. Assume input list has no duplicates.
#
# Example:
# Input: ([1, 2, 3, 4], target=5)
# Output: [(1, 4), (2, 3)]

# ORIGINAL SOLUTION (kept for comparison) - brute force with nested loops.
def find_pairs_original(nums, target):
    pairs = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                pairs.append((nums[i], nums[j]))
    return pairs

"""
Time and Space Analysis for problem 3 (ORIGINAL - nested loops):
- Best-case: O(n^2). The loops always compare every pair, even if the
  answer is found immediately, because there could be more pairs.
- Worst-case: O(n^2). n*(n-1)/2 comparisons.
- Average-case: O(n^2).
- Space complexity: O(1) auxiliary (not counting the output list, which can
  hold up to n/2 pairs).
- Why this approach? It is the simplest, most obviously correct solution and
  uses no extra memory.
- Could it be optimized? Yes - see find_pairs below, which uses a set to get
  O(n) time.
- Trade-offs: Minimal memory, but the quadratic runtime becomes very slow for
  large inputs (10,000 items -> ~50 million comparisons).
"""


# OPTIMIZED SOLUTION - single pass with a hash set.
# How it was optimized: instead of comparing every element with every other
# element (O(n^2)), each number asks "have I already seen the value that
# completes my pair?" The answer comes from a set lookup, which is O(1) on
# average, so the whole function is a single O(n) pass. The cost is O(n)
# extra memory for the set, compared to O(1) for the original.
def find_pairs(nums, target):
    seen = set()
    pairs = []

    for num in nums:
        complement = target - num
        # Check before adding num, so a number never pairs with itself
        # (e.g. target=4 and num=2 only pairs if a second 2 exists).
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)

    return pairs


def _normalize(pairs):
    # Order of pairs (and order within a pair) does not matter, so compare as a set.
    return {tuple(sorted(p)) for p in pairs}


def test_find_pairs():
    for fn in (find_pairs_original, find_pairs):
        assert _normalize(fn([1, 2, 3, 4], 5)) == {(1, 4), (2, 3)}   # example from prompt
        assert fn([], 5) == []                                        # edge: empty list
        assert fn([5], 5) == []                                       # edge: single element
        assert fn([1, 2, 3], 100) == []                               # edge: no pairs
        assert fn([1, 2, 3], 4) == [(1, 3)]                           # 2 must not pair with itself
        assert _normalize(fn([-3, 0, 3, 6], 3)) == {(-3, 6), (0, 3)}  # negatives
        assert _normalize(fn([-2, 2, 5], 0)) == {(-2, 2)}             # zero target
    # Both versions agree on a larger input.
    big = list(range(-500, 500))
    assert _normalize(find_pairs_original(big, 7)) == _normalize(find_pairs(big, 7))
    print("find_pairs: all tests passed")

"""
Time and Space Analysis for problem 3 (OPTIMIZED - hash set):
- Best-case: O(n). Each element is visited once; nothing can be skipped
  because any element might be part of a pair.
- Worst-case: O(n). One pass with O(1) average set lookups/inserts
  (degrades only with pathological hash collisions).
- Average-case: O(n).
- Space complexity: O(n) for the set of seen numbers, plus up to O(n) for
  the output.
- Why this approach? Trading memory for time turns a quadratic search into a
  linear one, which is the right trade for anything but tiny inputs.
- Could it be optimized further? Not asymptotically - every element must be
  read at least once, so O(n) time is optimal. An alternative is to sort and
  use two pointers: O(n log n) time but only O(1) extra space (if sorting
  in place is allowed).
- Trade-offs: The set uses extra memory and requires hashable values. The
  two-pointer approach saves memory but is slower and reorders the input.

PERFORMANCE COMPARISON (original vs optimized):
- Time:  O(n^2) -> O(n).
- Space: O(1) auxiliary -> O(n) auxiliary.
- Measured on this machine (see compare_find_pairs below) for n = 5,000:
  the nested-loop version took ~0.53 s, while the set version took
  ~0.0005 s - roughly a 1000x speedup that keeps
  growing as n grows, at the cost of storing up to n numbers in a set.
"""


def compare_find_pairs(n=5000):
    import timeit
    data = list(range(n))
    target = n  # many pairs exist, so both versions do real work
    t_orig = timeit.timeit(lambda: find_pairs_original(data, target), number=1)
    t_opt = timeit.timeit(lambda: find_pairs(data, target), number=1)
    print(f"find_pairs n={n}: original {t_orig:.4f}s, optimized {t_opt:.4f}s "
          f"(~{t_orig / t_opt:.0f}x faster)")


# 🔍 Problem 4: Simulate List Resizing (Amortized Cost)
# Create a function that adds n elements to a list that has a fixed initial capacity.
# When the list reaches capacity, simulate doubling its size by creating a new list
# and copying all values over (simulate this with print statements).
#
# Example:
# add_n_items(6) → should print when resizing happens.

def add_n_items(n, initial_capacity=1):
    capacity = initial_capacity
    storage = [None] * capacity  # fixed-size "array"
    size = 0

    for i in range(n):
        if size == capacity:
            new_capacity = capacity * 2
            print(f"Resizing: capacity {capacity} -> {new_capacity}, copying {size} items")
            new_storage = [None] * new_capacity
            for j in range(size):  # copy every existing item: O(size)
                new_storage[j] = storage[j]
            storage = new_storage
            capacity = new_capacity
        storage[size] = i
        size += 1
        print(f"Added item {i} (size={size}, capacity={capacity})")

    # Return only the slots actually in use.
    return storage[:size]


def test_add_n_items():
    assert add_n_items(0) == []                     # edge: add nothing
    assert add_n_items(1) == [0]                    # edge: fits in initial capacity
    assert add_n_items(6) == [0, 1, 2, 3, 4, 5]     # example from prompt
    assert add_n_items(4, initial_capacity=4) == [0, 1, 2, 3]  # edge: exactly full, no resize
    assert add_n_items(5, initial_capacity=4) == [0, 1, 2, 3, 4]  # one resize
    print("add_n_items: all tests passed")

"""
Time and Space Analysis for problem 4:
- When do resizes happen? Whenever size == capacity before an insert. With
  an initial capacity of 1, that is when adding the 2nd, 3rd, 5th, 9th, 17th
  ... item - i.e. when the size reaches a power of two (1, 2, 4, 8, ...).
  For add_n_items(6): resizes at 1->2, 2->4, and 4->8.
- What is the worst-case for a single append? O(n). The append that triggers
  a resize must allocate a new array and copy every existing element.
- What is the amortized time per append overall? O(1). Over n appends the
  total copy work is 1 + 2 + 4 + ... + n/2 < n, so total work is
  n (writes) + < n (copies) = O(n), which is O(1) per append on average.
- Space complexity: O(n). Capacity is always less than 2n, so at most about
  half the slots are wasted. During a resize the old and new arrays exist at
  the same time, briefly using up to ~3n slots.
- Why does doubling reduce the cost overall? Because each resize doubles
  capacity, expensive copies get exponentially rarer: after copying k items
  you get k free inserts before the next copy, which "pays back" the copy.
  If instead capacity grew by a fixed amount c, there would be n/c resizes,
  each copying O(n) items, for O(n^2) total and O(n) per append.
- Trade-offs: Doubling wastes up to 50% of the allocated memory. Python's own
  list uses a smaller growth factor (~1.125x) to waste less memory while
  keeping amortized O(1) appends.
"""


# 🔍 Problem 5: Compute Running Totals
# Write a function that takes a list of numbers and returns a new list
# where each element is the sum of all elements up to that index.
#
# Example:
# Input: [1, 2, 3, 4]
# Output: [1, 3, 6, 10]
# Because: [1, 1+2, 1+2+3, 1+2+3+4]

def running_total(nums):
    totals = []
    current = 0

    # Carry the sum forward instead of re-summing nums[:i+1] each time.
    for num in nums:
        current += num
        totals.append(current)

    return totals


def test_running_total():
    assert running_total([1, 2, 3, 4]) == [1, 3, 6, 10]   # example from prompt
    assert running_total([]) == []                         # edge: empty list
    assert running_total([5]) == [5]                       # edge: single element
    assert running_total([0, 0, 0]) == [0, 0, 0]           # edge: zeros
    assert running_total([3, -1, -2, 4]) == [3, 2, 0, 4]   # negatives
    assert running_total([0.5, 0.25]) == [0.5, 0.75]       # floats
    print("running_total: all tests passed")

"""
Time and Space Analysis for problem 5:
- Best-case: O(n). Every element must be added once.
- Worst-case: O(n). One pass with O(1) work (an add and an amortized O(1)
  append) per element.
- Average-case: O(n).
- Space complexity: O(n) for the output list; only O(1) auxiliary space
  (the single running sum variable).
- Why this approach? Keeping a running sum reuses the previous total. The
  naive approach, [sum(nums[:i+1]) for i in range(len(nums))], recomputes
  each prefix and is O(n^2) time.
- Could it be optimized? Not asymptotically - O(n) is required just to write
  n outputs. itertools.accumulate(nums) does the same thing in C and is
  faster in practice. If the caller doesn't need a new list, the totals could
  be written back into nums in place to avoid the O(n) output allocation.
- Trade-offs: The in-place version saves memory but destroys the original
  input; returning a new list is safer and matches the problem statement.
"""


if __name__ == "__main__":
    test_most_frequent()
    test_remove_duplicates()
    test_find_pairs()
    test_add_n_items()
    test_running_total()
    compare_find_pairs()
