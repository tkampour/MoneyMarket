import re
format = r"(finance.yahoo.com\/q\?s=[A-Z]*\.AT)"
patt = re.compile(format, re.I|re.U)

f = open('workfile', 'r')

for line in f:
    for m in patt.findall(line.rstrip()):
        print m
