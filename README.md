# Tech-debt

A simple tool to quantify your technical debt

## Installation  

requirements : python 3 


pip install techdebt

## Usage 


1. Adding debpt annotation

add debt annotations in your project files to mark technical debt:

- @debt() 
- @debt("debt_type") or 
- @debt("debt_type":"comment")
  

Let's say you have a python file with some debt : 

```bash
#@debt("implementation")
def poor_function():
    
    #@debt("implementation": "variable naming")
    bla = 2
    return bla
```

2. Project configuration

Adapt the following configuration file and put 
it in your project folder (cf config_example.yml)
 
```yaml

folder:
  included:
    - test_project/subA
    - test_project/subB

  excluded:
    - vendor
    - node_modules
    - var
    - web
    - nbproject
    - public
    - .git
    - __pycache__

extensions:
  - .py
  - .js
  - .md
  - .php

scores:
  api: 5
  implementation: 3

```

3. Run

```bash
techdebt --conf="path/to/config_file.yml" #default is "techdebt.yml"
```

## Roadmap 

- adding line file of annotation
- better reporting
- tracking debt over time
- adding estimation range
- Incorporating other tools in debt computing like static code analysis


## Testing 

pytest -s src/lib.py
