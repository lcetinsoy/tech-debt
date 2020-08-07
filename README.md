# Tech-debt
A simple tool to quantify your technical debt


## Installation  



```bash

git clone https://github.com/lcetinsoy/tech-debt --depth=1

pip install pandas

```

Remark: proper install via pip comming soon


## Usage 


1. Adding debpt annotation

add debt annotations in your project files to mark technical debt:

- @debt() 
- @debt("debt_type") or 
- @debt("debt_type":"comment")
  

Let's say you have a python file with some debt : 

```python


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

python main.py --conf="path/to/config_file.yml" #default is "techdebt.yml" 

```


## Roadmap 

- better reporting
- tracking debt over time
- Incorporating other tools in debt computing like static code analysis


## Testing 

pytest -s techdebt/lib.py