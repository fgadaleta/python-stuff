# What is this stuff?

Whatever you do, do it in a reproducible way. In order to ease the life of the folks using your stuff
(provided your stuff is *that* good), you should provide your stuff and the ecosystem your stuff requires
to work correctly.
When it comes to machine learning this means you should provide the right version of the libraries your stuff is using.
When it comes to stuff other than machine learning, there should be no f*ing difference. Just be reproducible :)

Use [conda](https://conda.io/docs/).
Briefly speaking, conda is a package and environment management system that can be used for python packages and other things (like Scala, Java, JavaScript, Ruby, even R, if you're still considering R for
anything that makes sense... in production)

You can use a conda system by installing it in three different ways:
1. anaconda
2. miniconda
3. anaconda enterprise

Starting with miniconda is usually a good idea.
The package and environment system, conda, is the same in the three installers. Miniconda just takes less space (because it installs less packages, of
course, not because of the Pied Piper compressor :/)
Anaconda is about six times larger and it installs a GUI to manage environments and packages. Nothing that cannot be done from the lovely terminal.

If you're convinced to install, follow the installation instructions at https://conda.io/docs/user-guide/install/index.html depending on your system and continue reading.

Once you are done with conda, you need the **root** environment. This environment contains a version of Python and some packages. You can create other
environments with different and even conflicting versions of Python. With conda your machine will finally be in good hands and your folks happy not to share your
most painful shitty experiences with python 2.7, 3.3, 3.4, 3.5, 3.6, 3.6.2, 3.6.3.... and all their packages.

The Conda system can be installed anywhere. I installed it in my home directory `~/miniconda3`


## Create a new environment

You create a new environment when you want to develop software that requires a reproducible way to be installed with all its dependencies. For instance, if you want to create an environment for Python 3.6, fire up your terminal and type

`$ conda create --name generic-dev python=3.6`

or (better) do it from a configuration file like `generic-dev.yml` and maintain this file only. Your environment and your needs might change in the future. Keep them consistent with the configuration file, the only file you need to share with your folks to use your _amazing_ software

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

In my case this returns
```
conda env list
# conda environments:
#
base                  *  /Users/frag/miniconda3
generic-dev              /Users/frag/miniconda3/envs/generic-dev
```

In order to use that environment you need to activate it with

`$ source activate generic-dev`

and when you are done, just deactivate with

`$ source deactivate`

(don't just `$ exit` from your terminal. It will kill the session and you would just be more pissed than if you deactivated).

Search for a new package with

`$ conda search -f matplotlib`

```
Loading channels: done
# Name                  Version           Build  Channel             
matplotlib                1.1.1      np15py26_0  pkgs/free           
...                        ...             ...
matplotlib                2.2.3  py36h54f8f79_0  pkgs/main           
matplotlib                2.2.3  py37h54f8f79_0  pkgs/main   
```


and install it by specifying the version (optional)

`$ conda install matplotlib=2.2.3`

Sometimes you might want to update some packages of the active environment. Type something like

`$ conda update matplotlib`
(and change the package name to whatever you need to install)

Needless to say, you can remove packages with

`$ conda remove <package_name>`


## Delete an environment
When you're done with your experiments/coding and need to clean up everything, just delete your environment with

`$ conda env remove --name <environment_name>`
