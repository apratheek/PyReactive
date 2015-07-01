import unittest
from pyreactive import *

class Observe(Observe):
    def notify(self):
        #print("Updated")
        pass

class PyReactiveTests(unittest.TestCase):
    """Tests for all PyReactive objects"""


    ########################################################################################################

    #TESTS FOR LISTS


    def test_basic_list_len(self):
        #Test 1
        a = List([1, 2, 3])
        b = Observe(a, method='len')
        self.assertEqual(b.value, 3)
        a.append(4)
        self.assertEqual(b.value, 4)

    def test_basic_list_count(self):
        #Test 2
        a = List([1, 2, 3])
        b = Observe(a, method='count', methodParameter=2)
        self.assertEqual(b.value, 1)
        a.pop()
        self.assertEqual(b.value, 1)
        a.extend(List([2, 5]))
        self.assertEqual(b.value, 2)
        a.remove(2)
        self.assertEqual(b.value, 1)

    def test_basic_list_reverse_firstel(self):
        #Test 3
        a = List([1, 2, 3])
        b = Observe(a, method='reverse')
        c = Observe(b, method='firstel')
        self.assertEqual(c.value, 3)
        self.assertEqual(b.value, List([3, 2, 1]))
        a.append(4)
        self.assertEqual(b.value, List([4,3,2,1]))
        self.assertEqual(c.value, 4)
        a.insert(2, 2.5)
        self.assertEqual(b.value, List([4, 3, 2.5, 2, 1]))
        c.modifyMethod(method='slice', methodParameter=(2, 3))
        self.assertEqual(c.value[0], 2.5)

    def test_basic_list_reverse_lastel(self):
        #Test 4
        a = List([1, 2, 3])
        b = Observe(a, method='reverse')
        c = Observe(b, method='lastel')
        self.assertEqual(c.value, 1)
        self.assertEqual(b.value, List([3, 2, 1]))
        a.append(4)
        self.assertEqual(b.value, List([4, 3, 2, 1]))
        self.assertEqual(c.value, 1)
        a.insert(2, 2.5)
        self.assertEqual(b.value, List([4, 3, 2.5, 2, 1]))
        c.modifyMethod(method='slice', methodParameter=
        (2, 3))
        self.assertEqual(c.value[0], 2.5)

    def test_basic_list_sort(self):
        #Test 5
        a = List([8, 45, 21])
        b = Observe(a, method='sort')
        self.assertEqual(b.value, List([8, 21, 45]))
        c = Observe(b, method='firstel')

    def test_basic_list_set(self):
        #Test 6
        a = List([1, 1, 2, 4, 3, 3, 5, 6, 5, 7])
        b = Observe(a, method='set')
        self.assertEqual(b.value, Set({1, 2, 3, 4, 5, 6, 7}))
        a.append(6)
        self.assertEqual(b.value, Set({1, 2, 3, 4, 5, 6, 7}))
        a.append(8)
        self.assertEqual(b.value, Set({1, 2, 3, 4, 5, 6, 7, 8}))

    def test_basic_list_max_min(self):
        #Test 7
        a = List([1, 1, 2, 4, 3, 3, 5, 6, 5, 7])
        b = Observe(a, method='max')
        c = Observe(a, method='min')
        self.assertEqual(b.value, 7)
        self.assertEqual(c.value, 1)

        a.extend([-1, 20])
        self.assertEqual(b.value, 20)
        self.assertEqual(c.value, -1)

    def test_basic_list_sum(self):
        #Test 8
        a = List([1, 2, 3, 4])
        b = Observe(a, method='sum')
        self.assertEqual(b.value, 10)
        a.extend([5, 6, 7])
        self.assertEqual(b.value, 28)
        ########################################################################################################

    #TESTS FOR SETS

    def test_basic_set_len_sum_max_min(self):
        #Test 9
        a = Set({1, 2, 3, 4, 5, 6, 7})
        b = Observe(a, method='sum')
        c = Observe(a, method='len')
        d = Observe(a, method='max')
        e = Observe(a, method='min')

        self.assertEqual(b.value, 28)
        self.assertEqual(c.value, 7)
        self.assertEqual(d.value, 7)
        self.assertEqual(e.value, 1)

        a.update({-9, 10})

        self.assertEqual(b.value, 29)
        self.assertEqual(c.value, 9)
        self.assertEqual(d.value, 10)
        self.assertEqual(e.value, -9)

    def test_basic_set_operations(self):
        #Test 10
        set1 = Set({1, 2, 3, 4, 5, 6, 7})
        set2 = Set({3, 4, 5, 6, 7, 8, 9})

        diff = Observe(set1, method='difference', methodParameter=set2)
        intersection = Observe(set1, method='intersection', methodParameter=set2)
        isdisjoint = Observe(set1, method='isdisjoint', methodParameter=set2)
        issubset = Observe(set1, method='issubset', methodParameter=set2)
        issuperset = Observe(set1, method='issuperset', methodParameter=set2)
        symm_diff = Observe(set1, method='symmetric_difference', methodParameter=set2)
        union = Observe(set1, method='union', methodParameter=set2)

        self.assertEqual(diff.value, {1, 2})
        self.assertEqual(intersection.value, {3, 4, 5, 6, 7})
        self.assertFalse(isdisjoint.value)
        self.assertFalse(issubset.value)
        self.assertFalse(issuperset.value)
        self.assertEqual(symm_diff.value, {1, 2, 8, 9})
        self.assertEqual(union.value, {1, 2, 3, 4, 5, 6, 7, 8, 9})

        set1.remove(1)
        set1.remove(2)




        self.assertEqual(diff.value, Set({}))
        self.assertEqual(intersection.value, {3, 4, 5, 6, 7})
        self.assertFalse(isdisjoint.value)
        self.assertTrue(issubset.value)
        self.assertFalse(issuperset.value)
        self.assertEqual(symm_diff.value, {8, 9})
        self.assertEqual(union.value, set2)

        set1.add(1)
        set1.add(2)
        set1.remove(3)
        set1.remove(4)
        set1.remove(5)
        set1.remove(6)
        set1.remove(7)

        self.assertTrue(isdisjoint.value)

########################################################################################################

    #TESTS FOR DICTS

    def test_basic_dict_len_sum_max_min(self):
        #Test 11
        a = Dict({1:12, 2:13, 3:14, 4:15, 5:16, 6:17, 7:18})
        b = Observe(a, method='sum')
        c = Observe(a, method='len')
        d = Observe(a, method='max')
        e = Observe(a, method='min')

        self.assertEqual(b.value, 28)
        self.assertEqual(c.value, 7)
        self.assertEqual(d.value, 7)
        self.assertEqual(e.value, 1)

        a.update({-9:19, 10:20})

        self.assertEqual(b.value, 29)
        self.assertEqual(c.value, 9)
        self.assertEqual(d.value, 10)
        self.assertEqual(e.value, -9)

    def test_basic_dict_key(self):
        #Test 12
        a = Dict({1:12, 2:13, 3:14, 4:15, 5:16, 6:17, 7:18})
        b = Dict({30:a, 45:50})
        c = Observe(b, method='key', methodParameter=30)
        d = Observe(c, method='key', methodParameter=1)

        self.assertEqual(c.value, {1:12, 2:13, 3:14, 4:15, 5:16, 6:17, 7:18})
        self.assertEqual(d.value, 12)

        a[1] = (1, 2, 3)

        self.assertEqual(c.value, {1:(1, 2, 3), 2:13, 3:14, 4:15, 5:16, 6:17, 7:18})
        self.assertEqual(d.value, (1, 2, 3))

        ########################################################################################################

    #TESTS FOR BYTEARRAYS
    def test_basic_bytearray_replace(self):
        #Test 13
        a = ByteArray(b'Hey There')
        b = Observe(a, method='replace', methodParameter=(b'e', b'l'))

        self.assertEqual(b.value, b'Hly Thlrl')

        a.extend(b' electronics are integral')
        self.assertEqual(b.value, b'Hly Thlrl lllctronics arl intlgral')

    def test_basic_bytearray_reverse(self):
        #Test 14
        a = ByteArray(b'Hey')
        b = Observe(a, method='reverse')

        self.assertEqual(b.value, b'yeH')

        a.extend(b' There')

        self.assertEqual(b.value, b'erehT yeH')

    def test_basic_bytearray_remaining(self):
        #Test 15
        a = ByteArray(b'Hello')

        length = Observe(a, method='len')
        count = Observe(a, method='count', methodParameter=b'l')
        decoded = Observe(a, method='decode', methodParameter='UTF-8')
        endswith = Observe(a, method='endswith', methodParameter=b'o')
        find = Observe(a, method='find', methodParameter=b'l')
        index = Observe(a, method='index', methodParameter=b'e')
        isalnum = Observe(a, method='isalnum')
        isalpha = Observe(a, method='isalpha')
        isdigit = Observe(a, method='isdigit')
        islower = Observe(a, method='islower')
        isupper = Observe(a, method='isupper')
        lower = Observe(a, method='lower')
        maximum = Observe(a, method='max')
        minimum = Observe(a, method='min')
        sliced = Observe(a, method='slice', methodParameter=(1, 3))
        startswith = Observe(a, method='startswith', methodParameter=b'H')
        upper = Observe(a, method='upper')


        self.assertEqual(length.value, 5)
        self.assertEqual(count.value, 2)
        self.assertEqual(decoded.value, 'Hello')
        self.assertTrue(endswith.value)
        self.assertEqual(find.value, 2)
        self.assertEqual(index.value, 1)
        self.assertTrue(isalnum.value)
        self.assertTrue(isalpha.value)
        self.assertFalse(isdigit.value)
        self.assertFalse(islower.value)
        self.assertFalse(isupper.value)
        self.assertEqual(lower.value, b'hello')
        self.assertEqual(maximum.value, 111)
        self.assertEqual(minimum.value, 72)
        self.assertEqual(sliced.value, b'el')
        self.assertTrue(startswith.value)
        self.assertEqual(upper.value, b'HELLO')

        a.extend(b' There')

        self.assertEqual(length.value, 11)
        self.assertEqual(count.value, 2)
        self.assertEqual(decoded.value, 'Hello There')
        self.assertFalse(endswith.value)
        self.assertEqual(find.value, 2)
        self.assertEqual(index.value, 1)
        self.assertFalse(isalnum.value)
        self.assertFalse(isalpha.value)
        self.assertFalse(isdigit.value)
        self.assertFalse(islower.value)
        self.assertFalse(isupper.value)
        self.assertEqual(lower.value, b'hello there')
        self.assertEqual(maximum.value, 114)
        self.assertEqual(minimum.value, 32)
        self.assertEqual(sliced.value, b'el')
        self.assertTrue(startswith.value)
        self.assertEqual(upper.value, b'HELLO THERE')




########################################################################################################

    #TESTS FOR OBSERVE
    def test_basic_subscribe(self):
        #Test 16
        a = Observe(5)
        b = Observe(8)
        c = Observe(25)

        sub = Subscribe(var=(a, b, c), op=('*', '%'))

        self.assertEqual(sub.value, 15)

        a.changeTo(50)

        self.assertEqual(sub.value, 0)

if __name__ == '__main__':
    unittest.main()


    #'len', 'count', 'reverse', 'sort', 'lastel', 'firstel', 'slice', 'set', 'sum'
