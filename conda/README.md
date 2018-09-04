# What is this stuff?

Whatever you do, do it in a reproducible way. In order to ease the life of the folks using your stuff (provided your stuff is *that* good),
you should provide your stuff and the ecosystem your stuff requires to work correctly.
When it comes to machine learning this means the right version of the libraries your stuff is using.
When it comes to stuff different from machine learning, there should be no f*ing difference. Just be reproducible.

Use conda.

Conda is a package and environment management system that can be used for python packages and other things (even R, if you're still considering R for
anything that makes sense... in production...)

You can use a conda system by installing it in three different ways: anaconda, miniconda, anaconda enterprise. 
Starting with miniconda is usually a good idea.
The package and environment system, conda, is the same in the three installers. Miniconda just takes less space (because it installs less packages, of
course, not because of the Pied Piper compressor :/)
Anaconda is about six times larger and it installs a GUI to manage environments and packages. Nothing that cannot be done from the lovely terminal.

Follow the installation instructions at https://conda.io/docs/user-guide/install/index.html depending on your system and move on.

Once you are done with conda, you need the root environment. This environment contains a version of Python and some packages. You can create other
environments with different and conflicting versions of Python... finally your machine will be in good hands and your folks happy not to share your
most painful shitty experiences with python 2.7, 3.3, 3.4, 3.5, 3.6, 3.6.2, 3.6.3.... and all their packages

The Conda system can be installed anywhere. I installed it in my home directory `~/miniconda3`


## Create a new environment

From the terminal 

`$ conda create --name generic-dev python=3.6`

or (better) from a configuration file like `generic-dev.yml`

```
name: generic-dev 
dependencies:
  - python=3.6.3
  - pip:
    - tensorflow
    - keras
    - sklearn
    - faker
    - pandas
    - numpy
    - scipy
    - filemagic
    - pprint
    - merkletools
    - merkle    
    - Pillow
    - rlp
```

`$ conda env create -f generic-dev.yml`

Now you can list all your environments with

`$ conda env list`

In order to use that environment you need to activate it with

`$ source activate my_python_env_36`

and when you are done, just deactivate with

`$ source deactivate`

Search a new package with

`$ conda search -f package_name`

and install it specifing the version (optional)

`$ conda install package_name=x.y.z`

Sometimes you might want to update all the packages of the active environment with

`$ conda update`

or just the package of your choice with

`$ conda update package_name`

Needless to say, you can remove packages with

`$ conda remove package_name`






## Delete an environment


`$ conda env remove --name environment_name`


https://conda.io/docs/_downloads/conda-cheatsheet.pdf


