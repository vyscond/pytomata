# pytomata

DFA validator based on .yml files

# install

# Usage

## Validating "aabb"

- `aabb.yml`

```yml
alphabet:
    - a
    - b

states:
    - begin
    - first_a
    - second_a
    - first_b
    - second_b

initial_state: begin

final_states:
    - second_b

transitions:
    - begin    * a  = first_a
    - first_a  * a  = second_a
    - second_a * b  = first_b
    - first_b  * b  = second_b
```

- validating

```python
import pytomata

a = pytomata.Automata('aabb.yml')

if a.validate('aabb') == True:
    print('Valid program')
else:
    print('Not valid program')

```
