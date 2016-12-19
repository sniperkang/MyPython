#-*- coding: utf-8 -*-

import re

str1 = 'imooc python'

str1.find('imooc')

str1 .startswith('imooc')

# r屏蔽转义
pattern = re.compile(r'imooc')
type(pattern)
match = pattern.match(str1)
#返回字符串或元组
match.group()
#返回索引
match.span()
#返回对应pattern
match.re
pattern1 = re.compile(r'_')
match1 = pattern1.match('_value')
match1.group()

pattern = re.compile(r'(imooc)', re.IGNORECASE)
match = pattern.match('ImoOc python')

#.不能匹配/n
match.group()
match = re.match(r'.', '0')

#{a/b/.../z/0-9}   {}中任意一个字符
match = re.match(r'{.}', '{b}')
#print match.group()
match = re.match(r'{..}', '{cc}')
#print match.group()

#{[a-z]}  []为字符集
match = re.match(r'{[abc]}', '{c}')
#print match.group()
match = re.match(r'{[a-z]}', '{o}')
#print match.group()
match = re.match(r'{[a-zA-Z]}', '{R}')
#print match.group()
#{[a-zA-Z0-9]}任意一个字符
match = re.match(r'{[a-zA-Z0-9]}', '{7}')
#print match.group()
match = re.match(r'{[\w]}', '{7}')#单词字符
#print match.group()
match = re.match(r'{[\W]}', '{ }')#非单词字符
#print match.group()
match = re.match(r'{[\d]}', '{7}')#数字
#print match.group()
match = re.match(r'{[\D]}', '{ }')#非数字
#print match.group()
match = re.match(r'{[\s]}', '{ }')#空白
#print match.group()
match = re.match(r'{[\S]}', '{7}')#非空白
#print match.group()
#match = re.match(r'[[\w]]', '[a]')#单词字符
#print match.group()
match = re.match(r'\[[\w]\]', '[a]')#\转义[]
#print match.group()

#[A-Z][a-z]...
match = re.match(r'')


