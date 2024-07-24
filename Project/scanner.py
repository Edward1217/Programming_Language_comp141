import re

Identifier = r"[a-zA-z_](\w)*"
Number = r"^\d+$"
Symbol = r"^[\+\-\*\/\(\)]$"
Error = r"[]"
txt = 'a'
x = re.search(Symbol,txt)

if x:
    print("match")
else:
    print("no")