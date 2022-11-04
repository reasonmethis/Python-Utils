from bisect import bisect_left, bisect_right
from itertools import tee
import operator 

def is_sorted(iterable, compare=operator.le):
    '''Return True if the iterator is sorted'''
    #TODO in 3.10 use itertools.pairwise:
    #all(x <= y for x, y in pairwise([1, 2, 3, 5, 6, 7]))
    a, b = tee(iterable)
    next(b, None)
    return all(map(compare, a, b))

def interpolate(x: float, x_l: list[float], y_l: list[float]):
    '''If given x is one of the values in the list of xs, return the corresponding y from the list of ys,
    otherwise linearly interpolate using the two closest xs. 
    
    The two lists are assumed to have the same length and the list of xs is assumed to be sorted with no repeats'''
    indclosestright = bisect_left(x_l, x) #bigger of the two indices of x_l with the two xs closest to x ()
    if indclosestright == 0:
        indclosestright = 1
    elif indclosestright == len(x_l):
        indclosestright -= 1
    #To interpolate, note that the line passing through the two closest xs satisfies:
    #ax1 + b = y1, ax2 + b = y2. Subtracting, we get:
    #a(x1 - x2) = y1 - y2, so a = dy/dx, b = y1 - dy/dx x1
    #so y = (y1 - y2) / (x1 - x2) * (x - x2) + y2
    x2, y2 = x_l[indclosestright], y_l[indclosestright]
    return (y_l[indclosestright - 1] - y2) / (x_l[indclosestright - 1] - x2) * (x - x2) + y2  

def interpolate_restricted(x: float, x_l: list[float], y_l: list[float]):  
    '''If given x is one of the values in the list of xs, return the corresponding y from the list of ys,
    if x is smaller than all of xs in the list, return the first y in the list (similarly if x is bigger),
    otherwise linearly interpolate using the two closest xs.  
    
    The two lists are assumed to have the same length and the list of xs is assumed to be sorted with no repeats'''
    indclosestright = bisect_left(x_l, x) #bigger of the two indices of x_l with the two xs closest to x ()
    if indclosestright == 0:
        return y_l[0]
    elif indclosestright == len(x_l):
        return y_l[-1]
    x2, y2 = x_l[indclosestright], y_l[indclosestright]
    return (y_l[indclosestright - 1] - y2) / (x_l[indclosestright - 1] - x2) * (x - x2) + y2  

def num_to_bucket(num, bucket_l):
    '''Return the bucket number num belongs to, for example if bucket list is [1, 10, 100], then
    0.5 is in zeroth bucket, 1 in first, 55 in second, 100 and over in third'''
    return bisect_right(bucket_l, num) #should be same as code below 
    for i, b in enumerate(bucket_l):
        if (num < b):
            return i
    return len(bucket_l)

def find_closest_elem_ind(my_list, my_number):
    """ Assumes my_list is sorted. Returns index of closest value to my_number.
    If two numbers are equally close, return the smaller index """
    pos = bisect_left(my_list, my_number) #index of leftmost elem where number can be inserted
    #with the list remaining sorted. In other words, all elements to its left will be smaller
    if pos == 0:
        return 0
    if pos == len(my_list):
        return pos - 1
    return pos if my_list[pos] - my_number < my_number - my_list[pos - 1] else pos - 1

def find_duplicates(itrbl):
    cnt_d = {}
    pastset = set()
    for el in itrbl:
        if el in pastset:
            cnt_d[el] = cnt_d.get(el, 1) + 1
        else:
            pastset.add(el)
    return cnt_d

def find_matching_xs(x_l, x_to_match_l, no_dup=True):
    '''find an element of second array closest to each element of first array
    both are assumed to be sorted, return pair of index lists'''
    if not (nj := len(x_to_match_l)): return [], []
    i_l = []; j_l = []
    j = 0; jprev = dbestprev = -1234
    #dbest_init = max(x_l[-1], x_to_match_l[-1]) - min(x_l[0], x_to_match_l[0]) + 12345
    for i, x in enumerate(x_l):
        dbest = abs(x - x_to_match_l[j])
        while j != nj - 1:
            if (d := abs(x - x_to_match_l[j + 1])) > dbest: 
                break #dist stopped improving as we move to the right 
            dbest = d
            j += 1
        #we found the best j for current i, dbest is the corresponding distance 
        if not no_dup:
            i_l.append(i); j_l.append(j)
            continue
        if j == jprev:
            if dbest >= dbestprev:
                continue
            i_l.pop(); j_l.pop()
        i_l.append(i); j_l.append(j)
        jprev = j; dbestprev = dbest
    return i_l, j_l

if __name__ == '__main__':
    xs = [1,3,7]
    ys = [10,30,70]
    while True:
        xst = input('x: ')
        if not xst:
            exit()
        print(interpolate(float(xst), xs, ys))