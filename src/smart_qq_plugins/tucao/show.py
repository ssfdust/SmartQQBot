from six.moves import cPickle

tmp = dict()
with open("./200783396.tucao", "rb") as file:
    tmp = cPickle.load(file)
    print(tmp)
