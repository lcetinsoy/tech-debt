# Tech-debt
A simple tool to quantify your technical debt


## Installation 


```bash

git clone https://github.com/lcetinsoy/tech-debt --depth=1

```
 
Remark: proper install via pip comming soon

## Usage

1. Adding debpt annotation

add @debt() or @debt("key":"value") in your project files
to mark some technical debt

2. Project configuration

Add the following configuration file in your project folder (cf config_example.yml)
 
```yaml

folder:
  included:
    - /path/to/project
  excluded:
    - vendor/
    - node_modules/

extensions:
  - .py
  - .js
  - .md
  - .php

```

2. Quantifying the debpt


python main.py --conf="/path/to/conf.yml"


## Roadmap 

- Attributing points to each debpt type
- Group statistics per folders
- Incorporating other tools in debt computing like static code analysis
