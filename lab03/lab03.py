import urllib.request
import unittest
from typing import TypeVar, Callable, List

T = TypeVar('T')
S = TypeVar('S')

# Alex Mcneilly <amcneilly@s207.org>

#################################################################################
# EXERCISE 1
#################################################################################
def mysort(lst: List[T], compare: Callable[[T, T], int]) -> List[T]:
    listLength = len(lst)
    # Insertion Sort
    for r in range(1, listLength): 
        for p in range(r, 0, -1):
            if compare(lst[p], lst[p-1]) == -1:
                ww = lst[p-1]
                lst[p-1] = lst[p]
                lst[p] = ww
            else:
                break
    return lst


def mybinsearch(lst: List[T], elem: S, compare: Callable[[T, S], int]) -> int:
    # implement a generic binary sort
    # Searches for value elem in the lst
    low = 0
    high = len(lst)-1
    mid = 0
    while low <= high:
        mid = low + high // 2

        if compare(lst[mid], elem) == 0:
            return mid

        elif compare(lst[mid], elem) == 1:
            high = mid -1

        else:
            low = mid +1

    return -1

class Student():
    """Custom class to test generic sorting and searching."""
    def __init__(self, name: str, gpa: float):
        self.name = name
        self.gpa = gpa

    def __eq__(self, other):
        return self.name == other.name

    

# 30 Points (total)
def test1():
    """Tests for generic sorting and binary search."""
    print(80 * "#" + "\nTests for generic sorting and binary search.")
    test1_1()
    test1_2()
    test1_3()
    test1_4()
    test1_5()

# 6 Points
def test1_1():
    """Sort ints."""
    print("\t-sort ints")
    tc = unittest.TestCase()
    ints = [ 4, 3, 7, 10, 9, 2 ]
    intcmp = lambda x,y:  0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(sortedints, [2, 3, 4, 7, 9, 10])

# 6 Points
def test1_2():
    """Sort strings based on their last character."""
    print("\t-sort strings on their last character")
    tc = unittest.TestCase()
    strs = [ 'abcd', 'aacz',  'zasa' ]
    suffixcmp = lambda x,y: 0 if x[-1] == y[-1] else (-1 if x[-1] < y[-1] else 1)
    sortedstrs = mysort(strs,suffixcmp)
    tc.assertEqual(sortedstrs, [ 'zasa', 'abcd', 'aacz' ])

# 6 Points
def test1_3():
    """Sort students based on their GPA."""
    print("\t-sort students on their GPA.")
    tc = unittest.TestCase()
    students = [ Student('Josh', 3.0), Student('Angela', 2.5), Student('Vinesh', 3.8),  Student('Jia',  3.5) ]
    sortedstudents = mysort(students, lambda x,y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1))
    expected = [ Student('Angela', 2.5), Student('Josh', 3.0), Student('Jia',  3.5), Student('Vinesh', 3.8) ]
    tc.assertEqual(sortedstudents, expected)

# 6 Points
def test1_4():
    """Binary search for ints."""
    print("\t-binsearch ints")
    tc = unittest.TestCase()
    ints = [ 4, 3, 7, 10, 9, 2 ]
    intcmp = lambda x,y:  0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(mybinsearch(sortedints, 3, intcmp), 1)
    tc.assertEqual(mybinsearch(sortedints, 10, intcmp), 5)
    tc.assertEqual(mybinsearch(sortedints, 11, intcmp), -1)

# 6 Points
def test1_5():
    """Binary search for students by gpa."""
    print("\t-binsearch students")
    tc = unittest.TestCase()
    students = [ Student('Josh', 3.0), Student('Angela', 2.5), Student('Vinesh', 3.8),  Student('Jia',  3.5) ]
    stcmp = lambda x,y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1)
    stbincmp = lambda x,y: 0 if x.gpa == y else (-1 if x.gpa < y else 1)
    sortedstudents = mysort(students, stcmp)
    tc.assertEqual(mybinsearch(sortedstudents, 3.5, stbincmp), 2)
    tc.assertEqual(mybinsearch(sortedstudents, 3.7, stbincmp), -1)

#################################################################################
# EXERCISE 2
#################################################################################
class PrefixSearcher():

    def __init__(self, document, k):
        self.document = document
        self.maximum = k
        self.substrings = [document[i:i+j] for j in range(k,0,-1) for i in range(len(document))]

    def search(self, q):
        """
        Return true if the document contains search string q (of
        length up to n). If q is longer than n, then raise an
        Exception.
        """
        docu = self.document
        n = len(docu)

        if len(q) > len(self.document):
            raise Exception('q is longer than n')

        searchCMP = lambda a,b: 0 if (a[:len(q)] == b[:len(q)]) else (-1 if (a[:len(q)] < b[:len(q)]) else 1)

        mysort(lst = self.substrings, compare = searchCMP)
        return (mybinsearch(lst = self.substrings, elem=q, compare = searchCMP) != -1)
    

# 30 Points
def test2():
    print("#" * 80 + "\nSearch for substrings up to length n")
    test2_1()
    test2_2()

# 15Points
def test2_1():
    print("\t-search in hello world")
    tc = unittest.TestCase()
    p = PrefixSearcher("Hello World!", 1)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("e"))
    tc.assertFalse(p.search("h"))
    tc.assertFalse(p.search("Z"))
    tc.assertFalse(p.search("Y"))
    p = PrefixSearcher("Hello World!", 2)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("ll"))
    tc.assertFalse(p.search("lW"))

# 20 Points
def test2_2():
    print("\t-search in Moby Dick")
    tc = unittest.TestCase()
    md_url = 'https://www.gutenberg.org/files/2701/2701-0.txt'
    md_text = urllib.request.urlopen(md_url).read().decode()
    p = PrefixSearcher(md_text[0:1000],4)
    tc.assertTrue(p.search("Moby"))
    tc.assertTrue(p.search("Dick"))

#################################################################################
# EXERCISE 3
#################################################################################
class SuffixArray():

    def __init__(self, document: str):
        self.document = document
        #creates pre-suffix array
        self.suffixes = [document[j:] for j in range(len(document))]

        suffixCMP = lambda a,b: 0 if (a[1] == b[1]) else (-1 if (a[1] < b[-1]) else 1)
        listToSort = list(enumerate(self.suffixes))
        nextArray = mysort(lst = listToSort,compare=suffixCMP)
        self.suffixArray = [x for x,_ in nextArray]

    def positions(self, searchstr: str):
        docu = self.document
        out = list()
        searchLength = len(searchstr)
        positionsCMP = lambda a,b: 0 if (docu[a:a+searchLength] == b) else (-1 if (docu[a:a+searchLength < b]) else 1)
        findElement = mybinsearch(lst=self.suffixArray, elem=searchstr, compare=positionsCMP)
        if findElement == -1:
            return []
        for counter in range(0,len(self.suffixArray)):
            codety = self.suffixArray[counter]
            if docu[codety:codety+len(searchstr)] == searchstr:
                out.append(codety)
            else:
                break
        return out


        """
        Returns all the positions of searchstr in the documented indexed by the suffix array.
        """

    def contains(self, searchstr: str):
        docu = self.document
        searchLength = len(searchstr)
        containsCMP = lambda a,b: 0 if (docu[a:a+searchLength] == b) else (-1 if (docu[a:a+searchLength] < b) else 1)
        return (mybinsearch(lst=self.suffixArray, elem=searchstr, compare=containsCMP) != -1)

# 40 Points
def test3():
    """Test suffix arrays."""
    print(80 * "#" + "\nTest suffix arrays.")
    test3_1()
    test3_2()


# 20 Points
def test3_1():
    print("\t-suffixarray on Hello World!")
    tc = unittest.TestCase()
    s = SuffixArray("Hello World!")
    tc.assertTrue(s.contains("l"))
    tc.assertTrue(s.contains("e"))
    tc.assertFalse(s.contains("h"))
    tc.assertFalse(s.contains("Z"))
    tc.assertFalse(s.contains("Y"))
    tc.assertTrue(s.contains("ello Wo"))


# 20 Points
def test3_2():
    print("\t-suffixarray on Moby Dick!")
    tc = unittest.TestCase()
    md_url = 'https://www.gutenberg.org/files/2701/2701-0.txt'
    md_text = urllib.request.urlopen(md_url).read().decode()
    s = SuffixArray(md_text[0:1000])
    tc.assertTrue(s.contains("Moby-Dick"))
    tc.assertTrue(s.contains("Herman Melville"))
    posset = set(s.positions("Moby-Dick"))
    tc.assertEqual(posset, {355, 356})


#################################################################################
# TEST CASES
#################################################################################
def main():
    test1()
    test2()
    test3()

if __name__ == '__main__':
    main()
