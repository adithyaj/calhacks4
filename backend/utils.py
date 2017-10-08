def load_keys():
    d = {}
    with open('secret.keys') as f:
        content = f.readlines()
    for line in content:
        line = line.split(',')
        d[line[0]] = line[1]
    return d

