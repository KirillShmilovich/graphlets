graphlets
==============================
[//]: # (Badges)
[![Build Status](https://travis-ci.org/KirillShmilovich/graphlets.svg?branch=master)](https://travis-ci.org/KirillShmilovich/graphlets)

Small package for performing graphlet decomposition.

## Dependencies 

Make sure you have the following installed on your machine.

- A C++ compiler supporting C++11
- [scikit-learn](http://scikit-learn.org/stable/install.html)
- [joblib](https://joblib.readthedocs.io/en/latest/installing.html)
- [numpy](https://docs.scipy.org/doc/numpy/user/install.html)
- [networkx](https://networkx.github.io/documentation/stable/install.html)

## Installation 

With all the dependencies installed you can install the package by running: 

```bash
$ git clone https://github.com/KirillShmilovich/graphlets
$ cd graphlets
$ pip install -e .
```

## Usage 

The below examples shows how to compute a graphlet decomposition on a randomly generated set of points.

```python 
import graphlets
import numpy as np

# Create a randomly generaterd data set with dimensions (n_frames, n_objects, n_dims)
a = np.random.rand(1000, 100, 3)

# Instantiate a graphlet object using `a`
G = graphlets.Graphlets(a)

# Compute a graphlet decomposition, by default performing a
# node reduction outputing a vector of graphlet frequencies 
decomp = G.compute(r_cut = 0.1)
```

## Acknowledgements 

This package is shipped with the C++ code to perform graphlet decomposition available here:

- ORCA (https://github.com/thocevar/orca)

Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.

## References 

[1] Pržulj N, Biological Network Comparison Using Graphlet Degree Distribution, Bioinformatics 2007, 23:e177-e183.

[2] Tomaž Hočevar, Janez Demšar, A combinatorial approach to graphlet counting, Bioinformatics, Volume 30, Issue 4, 15 February 2014, Pages 559–565

### Copyright

Copyright (c) 2019, Kirill Shmilovich
