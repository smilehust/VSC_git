import string
s = 'The quick brown fox jumped over the lazy dog.'
# capwords() 将字符串中所有单词的首字母大写
print(string.capwords(s)) 
# 以‘o’为分隔符分割字符串，返回一个列表
print(s.split('o'))        


from itertools import *

# chain() 函数将几个迭代器作为参数，并返回一个迭代器。这个迭代器将会依次遍历那些作为输入的迭代器
for i in chain([1, 2, 3], ['a', 'b', 'c']):
    print(i, end=' ')
print()

# 甚至输入的那些迭代器也是动态生成的,用 chain.from_iterable() 来完成和 chain() 相类似的功能
def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ['a', 'b', 'c']
    yield ('A','B','C')
for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=' ')
print()

# 内置函数 zip() 返回一个迭代器，这个迭代器将同时遍历多个输入迭代器，
# 并返回一个由在这些迭代器中得到的元素所组合成的元组，按最短的迭代器截取。
# 返回一个只可以被遍历一次的可迭代对象
for i in zip([1, 2, 3], ['a', 'b', 'c','d'], 'ABCDE'):
    print(i)
print()

# zip() 将会在任意一个输入迭代器被遍历完时停止。
# 如果想完整的遍历所有的输入迭代器（即使它们有不同的长度），我们可以用zip_longest()函数
for i in zip_longest([1, 2, 3], ['a', 'b', 'c','d'], 'ABCDE'):
    print(i)
print()
# 默认情况下，zip_longest()函数将None作为缺省值。我们可以通过传入fillvalue参数来修改这个默认设定
for i in zip_longest([1, 2, 3], ['a', 'b', 'c','d'], 'ABCDE', fillvalue='Smile'):
    print(i)
print()

# islice() 函数将把输入迭代器的一部分作为其输出的迭代器
# islice() 和 slice 操作一样，将 start，stop 以及 step 作为输入参数。
# 其中 start 和 step 参数是可选的。。
print('By tens to 100:')
for i in islice(range(100), 0, 100, 10):
    print(i, end=' ')
print('\n')

# 基于输入，tee() 函数返回多个（默认两个）独立的迭代器
# tee() 函数将会基于它输入的迭代器返回多个和输入迭代器相同的迭代器，
# 这些迭代器可以被数并列地输入不同的算法。
# 这些由 tee() 返回的迭代器会共享它们的输入。所以在用 tee() 创建了一些新的迭代器之后，
# 通常原始的那个迭代器不应该再被使用，如果原始输入的迭代器中的一些数据被遍历了，
# 这些数据将不会出现在那些新的（返回的）迭代器中。
r = islice(count(), 5)
i1, i2 = tee(r)
print('i1:', list(i1))
print('i2:', list(i2))

# 内置函数 map() 会将一个函数分别作用到输入的一个迭代器的每个元素数，并将其以迭代器的形式返回。
# 这个迭代器会遍历完这个输入的迭代器。
def times_two(x):
    return 2 * x
for i in map(times_two, range(5)):
    print(i)