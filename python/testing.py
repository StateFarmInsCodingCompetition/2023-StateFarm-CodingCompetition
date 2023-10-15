import operator
stats = { 'b': 3000, 'c': 100, 'a': 3000}
print(max(stats.items(), key=operator.itemgetter(1))[0])