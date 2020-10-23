![Run unit tests for pkmodel](https://github.com/D-own-T-o-P-rogramme/PK_Model/workflows/Run%20unit%20tests%20for%20pkmodel/badge.svg) [![BCH compliance](https://bettercodehub.com/edge/badge/Down-To-Programme/PK_Model?branch=master)](https://bettercodehub.com/) [![codecov](https://codecov.io/gh/Down-To-Programme/PK_Model/branch/master/graph/badge.svg?token=UXOY8KCZQI)](undefined) [![Documentation Status](https://readthedocs.org/projects/down-to-programmepkmodel/badge/?version=latest)](https://down-to-programmepkmodel.readthedocs.io/en/latest/?badge=latest) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)


# PK_Model, a pharmacokinetic model developed by students on the Oxford Interdisciplinary Bioscience DTP


This is a package to run a user-specifed pharmacokinetic model (PK model). The user can specify the number of peripheral compartment around a central compartment, a dosing type (I.V. or S.C.), and a dosing protocol. A solver will solve the differential equations that model the pharmacokinetics of the compartments, and graphs comparing the solutions of different model parameters will be outputted.  

The package is pip installable and can be run on the latest windows, ubuntu and macos operating systems.


# Quickstart 

1. First clone or fork this repository and navigate to the repository's top directory

```
git clone https://github.com/Down-To-Programme/PK_Model.git
cd PK_Model
```

2. We recommend that you create a virtual environment with python versons 3.6+ to use our package. Tests are run continuously on these python versions to ensure the package works, but previous versions are not tested. 

```
python3 –m venv venv
source venv/bin/activate
```

3. To install requirements and dependencies, you can use our setup.py file by typing:

`pip install –e .` 

## Running the model


\[Most user-friendly option:\] You can run an interactive script that will take you through the different steps needed to specify the parameters of the PK model. It will then generate a plot, giving you the options to compare two different models and to save the generated figure. 
Run this script from the command line with: 

`python interactive_pkmodel.py`

Or you can run an example model from the command line with:

`python try_out_script.py`


Alternatively you can pip install the dtp-pkmodel package with:

`pip install dtp-pkmodel`

open your python interpreter and import:

```
python
>>> import pkmodel
```

# Directory structure

```
.
├── LICENSE
├── README.md
├── build
│   ├── bdist.macosx-10.15-x86_64
│   └── lib
│       └── pkmodel
│           ├── __init__.py
│           ├── model.py
│           ├── protocol.py
│           ├── solution.py
│           ├── tests
│           │   ├── __init__.py
│           │   ├── test_model.py
│           │   ├── test_pipeline.py
│           │   ├── test_protocol.py
│           │   └── test_solution.py
│           └── version_info.py
├── dist
│   ├── dtp_pkmodel-1.0.1-py3-none-any.whl
│   └── dtp_pkmodel-1.0.1.tar.gz
├── docs
│   ├── Makefile
│   ├── conf.py
│   ├── index.rst
│   └── make.bat
├── dtp_pkmodel.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── requires.txt
│   └── top_level.txt
├── pkmodel
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   ├── model.cpython-38.pyc
│   │   ├── protocol.cpython-38.pyc
│   │   ├── solution.cpython-38.pyc
│   │   └── version_info.cpython-38.pyc
│   ├── model.py
│   ├── protocol.py
│   ├── solution.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   ├── test_model.cpython-38.pyc
│   │   │   ├── test_protocol.cpython-38.pyc
│   │   │   └── test_solution.cpython-38.pyc
│   │   ├── test_model.py
│   │   ├── test_pipeline.py
│   │   ├── test_protocol.py
│   │   └── test_solution.py
│   └── version_info.py
├── requirements.txt
├── interactive_pkmodel.py
├── setup.py
└── try_out_script.py
```

# Raising issues 

If you spot an issue and would like us to fix it, let us know by:

1. Pulling changes from the master branch to avoid conflicts:

`git pull origin master` 

2. Create an issue on GitHub by navigating to the 'Issues' tab in the repository's home page 

3. Create a new branch corresponding to the issue with git

`git checkout -b <new-branch>`

4. Make your changes and then use git add, commit and push your changes to the repository on GitHub

`git add <file>`

(You can find out what files need to be added with `git status`)

```
git commit –m "issue-number-comment" 
git push origin <new-branch>
```

5. Make a pull request on GitHub


# License

This package was created under the MIT License. Read more about this at https://github.com/Down-To-Programme/PK_Model/blob/master/LICENSE

# Links

* https://dtp-pk-model.readthedocs.io/en/latest/
* https://codecov.io/gh/Down-To-Programme/PK_Model
* https://bettercodehub.com/results/Down-To-Programme/PK_Model
