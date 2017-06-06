import h5py
import numpy as numpy

f = h5py.File("mytestfile.hdf5", "w")
#dset = f.create_dataset("mydataset", (100,), dtype = 'i')
print('name: ' + f.name)
print('keys: ' + repr(f.keys()))

grp = f.create_group("bar")
print("grp's name: " + grp.name)

subgrp = grp.create_group("baz")
print("subgrp's name: " + subgrp.name)

grp2 = f.create_group("/some/long/path")
print("grp2's name: " + grp2.name)
grp3 = f['/some/long']
print("grp3's name: " + grp3.name)