import pickle

# write python dict to a file
mydict = {'a': 1, 'b': 2, 'c': 3}
output = open('myfile.pkl', 'wb')
pickle.dump(mydict, output)
output.close()

# read python dict back from the file
pkl_file = open('myfile.pkl', 'rb')
mydict2 = pickle.load(pkl_file)
pkl_file.close()

print(mydict)
print(mydict2)
