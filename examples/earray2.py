#!/usr/bin/env python

""" Small example that shows how to work with extendeable arrays of
different types, strings included. """

from numpy import *
from tables import *

# Open a new empty HDF5 file
filename = "earray2.h5"
fileh = open_file(filename, mode = "w")
# Get the root group
root = fileh.root

# Create an string atom
a = StringAtom(itemsize=1)
# Use it as a type for the enlargeable array
hdfarray = fileh.create_earray(root, 'array_c', a, (0,), "Character array")
hdfarray.append(array(['a', 'b', 'c']))
# The next is legal:
hdfarray.append(array(['c', 'b', 'c', 'd']))
# but these are not:
#hdfarray.append(array([['c', 'b'], ['c', 'd']]))
#hdfarray.append(array([[1,2,3],[3,2,1]], dtype=uint8).reshape(2,1,3))

# Create an atom
a = UInt16Atom()
hdfarray = fileh.create_earray(root, 'array_e', a, (2, 0, 3),
                              "Unsigned short array")

# Create an enlargeable array
a = UInt8Atom()
hdfarray = fileh.create_earray(root, 'array_b', a, (2, 0, 3),
                              "Unsigned byte array", Filters(complevel = 1))

# Append an array to this table
hdfarray.append(array([[1, 2, 3], [3, 2, 1]], dtype=uint8).reshape(2, 1, 3))
hdfarray.append(array([[1, 2, 3], [3, 2, 1], [2, 4, 6], [6, 4, 2]],
                      dtype=uint8).reshape(2, 2, 3)*2)
# The next should give a type error:
#hdfarray.append(array([[1,0,1],[0,0,1]], dtype=Bool).reshape(2,1,3))

# Close the file
fileh.close()

# Open the file for reading
fileh = open_file(filename, mode = "r")
# Get the root group
root = fileh.root

a = root.array_c.read()
print "Character array -->", repr(a), a.shape
a = root.array_e.read()
print "Empty array (yes, this is suported) -->", repr(a), a.shape
a = root.array_b.read(step=2)
print "Int8 array, even rows (step = 2) -->", repr(a), a.shape

print "Testing iterator:",
#for x in root.array_b.iterrows(step=2):
for x in root.array_b:
    print "nrow-->", root.array_b.nrow
    print "Element-->", x

print "Testing getitem:"
for i in range(root.array_b.shape[0]):
    print "array_b["+str(i)+"]", "-->", root.array_b[i]
# The nrows counts the growing dimension, which is different from the
# first index
for i in range(root.array_b.nrows):
    print "array_b[:,"+str(i)+",:]", "-->", root.array_b[:, i,:]
print "array_c[1:2]", repr(root.array_c[1:2])
print "array_c[1:3]", repr(root.array_c[1:3])
print "array_b[:]", root.array_b[:]

print repr(root.array_c)
# Close the file
fileh.close()
