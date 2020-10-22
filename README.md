![Run unit tests for pkmodel](https://github.com/D-own-T-o-P-rogramme/PK_Model/workflows/Run%20unit%20tests%20for%20pkmodel/badge.svg)

[![BCH compliance](https://bettercodehub.com/edge/badge/Down-To-Programme/PK_Model?branch=master)](https://bettercodehub.com/)

[![codecov](https://codecov.io/gh/Down-To-Programme/PK_Model/branch/master/graph/badge.svg?token=UXOY8KCZQI)](undefined)


# PK_Model, a pharmacokinetic model developed by students on the Oxford Interdisciplinary Bioscience DTP


This is a package to run a user-specifed pharmacokinetic model (PK model). The user can specify the number of peripheral compartment around a central compartment, a dosing type (I.V. or S.C.), and a dosing protocol. A solver will solve the differential equations that model the pharmacokinetics of the compartments, and graphs comparing the solutions of different model paramters will be outputted.  

The package can be run on the latest windows, ubuntu and macos operating systems.


## Quickstart 

1. First clone or fork this repository and navigate to the repository's top directory

`git clone https://github.com/Down-To-Programme/PK_Model.git`

`cd PK_Model`

2. We recommend that you create a virtual environment with python versons 3.6+ to use our package. Our code runs tests continuously on these python versions and so you should not encounter any problems.

`python3 –m venv venv` 

`source venv/bin/activate`

3. To install requirements and dependencies, you can use our setup.py file by typing:

`pip install –e .` 

### Running the model

You can run the model from the command line with:

`python try_out_script.py`


### Raising issues 

If you spot an issue and would like us to fix it, use

1. Pull changes from the master branch to avoid conflicts:

`git pull origin master` 

2. Create an issue on GitHub by navigating to the 'Issues' tab in the repository's home page 

3. Create a new branch corresponding to the issue with git

`git checkout -b <new-branch>`

4. Make your changes and then use git add, commit and push your changes to the repository on GitHub

`git add <file>`

(You can find out what files need to be added with `git status`)

`git commit –m "issue-number-comment"` 

`git push origin <new-branch> `

5. Make a pull request on GitHub

## License

This package was created under the MIT License. Read more about this at https://github.com/Down-To-Programme/PK_Model/blob/master/LICENSE
