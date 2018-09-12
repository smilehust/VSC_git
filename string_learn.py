import string

s = 'The quick brown fox jumped over the lazy dog.'
print(string.capwords(s))  # capwords() 将字符串中所有单词的首字母大写
print(s.split('o'))        # 以‘o’为分隔符分割字符串，返回一个列表
