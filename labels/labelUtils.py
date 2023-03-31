names = []
labels = open('../labels/labels.txt').readlines()
for label in labels:
    names.append(label)
output = ''
for name in names:
    output += '"' + name.replace('\n', '') + '"' + ','
print(output)
