
# Logic Module Documentation

## Overview
The `logic.py` module is integral to the easyAGI project, providing the foundational framework for formal logic systems and operations. It enables the system to structure its reasoning processes, ensuring clear, consistent, and logical decision-making throughout the project.

## Features
- **Logical Operations**: Implements fundamental logical operations such as AND, OR, NOT, and implications, facilitating complex logical reasoning.
- **Predicate Logic**: Supports predicate logic, allowing the system to deal with variables and quantify statements, enhancing its reasoning capabilities.
- **Proof System**: Incorporates a proof system to validate arguments and infer new information based on a set of premises and rules of inference.

## Usage
Utilize the Logic module in any component of the MASTERMIND framework that requires structured logical reasoning. It's particularly useful in areas such as decision-making, problem-solving, and data analysis.

## Example Implementation
```python
class LogicalOperator:
    def AND(self, a, b):
        return a and b

    def OR(self, a, b):
        return a or b

    def NOT(self, a):
        return not a

    def IMPLIES(self, a, b):
        return not a or b
```


Class LogicTables
Attributes

    variables: A list to store the variables involved in logical expressions.
    expressions: A list to store the logical expressions to be evaluated.
    valid_truths: A list to store expressions that have been validated as true.
    logger: A logging object to capture and store log messages.

# Initialization

```python
def __init__(self):
    self.variables = []
    self.expressions = []
    self.valid_truths = []
    self.logger = logging.getLogger('LogicTables')
    self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all logs
```

Upon initialization, the LogicTables class sets up logging mechanisms and ensures that necessary directories for logs are created.

# Logging Methods

```python
def log(self, message, level='info'):
    if level == 'info':
        self.logger.info(message)
    elif level == 'error':
        self.logger.error(message)
    elif level == 'warning':
        self.logger.warning(message)
    self.store_log_in_mindx(message, level)
    self.store_log_in_memory(message, level)

def store_log_in_mindx(self, message, level):
    general_log_path = './mindx/errors/log.txt'
    pathlib.Path(general_log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(general_log_path, 'a') as file:
        file.write(f"{level.upper()}: {message}\n")

def store_log_in_memory(self, message, level):
    memory_log_path = './memory/truth/logs.txt'
    pathlib.Path(memory_log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(memory_log_path, 'a') as file:
        file.write(f"{level.upper()}: {message}\n")
```

The logging methods ensure that messages are logged both to the general log file and the memory log file.

# Adding Variables and Expressions

```python
def add_variable(self, var):
    if var not in self.variables:
        self.variables.append(var)
        self.log(f"Added variable: {var}")
        self.output_belief(f"Added variable: {var}")
    else:
        self.log(f"Variable {var} already exists.", level='warning')

def add_expression(self, expr):
    if expr not in self.expressions:
        self.expressions.append(expr)
        self.log(f"Added expression: {expr}")
        self.output_belief(f"Added expression: {expr}")
    else:
        self.log(f"Expression {expr} already exists.", level='warning')
```
These methods add new variables and expressions to their respective lists and log the additions.

# Evaluating Expressions

```python
def evaluate_expression(self, expr, values):
    allowed_operators = {
        'and': lambda x, y: x and y,
        'or': lambda x, y: x or y,
        'not': lambda x: not x,
        'xor': lambda x, y: x ^ y,
        'nand': lambda x, y: not (x and y),
        'nor': lambda x, y: not (x or y),
        'implication': lambda x, y: not x or y
    }

    try:
        result = eval(expr, {"__builtins__": None}, {**allowed_operators, **values})
        self.log(f"Evaluated expression '{expr}' with values {values}: {result}")
        return result
    except Exception as e:
        self.log(f"Error evaluating expression '{expr}': {e}", level='error')
        return False
```

This method evaluates a logical expression using the provided values and logs the results.

# Generating and Displaying Truth Tables

```python
def generate_truth_table(self):
    n = len(self.variables)
    combinations = list(itertools.product([True, False], repeat=n))
    truth_table = []

    for combo in combinations:
        values = {self.variables[i]: combo[i] for i in range(n)}
        result = values.copy()
        for expr in self.expressions:
            result[expr] = self.evaluate_expression(expr, values)
        truth_table.append(result)

    self.log(f"Generated truth table with {len(truth_table)} rows")
    self.output_belief(f"Generated truth table with {len(truth_table)} rows")
    return truth_table

def display_truth_table(self):
    truth_table = self.generate_truth_table()
    headers = self.variables + self.expressions
    print("\t".join(headers))
    for row in truth_table:
        print("\t".join(str(row[var]) for var in headers))
```

These methods generate and display truth tables based on the current variables and expressions.

# Validating Truths

```python
def validate_truth(self, expression):
    if expression not in self.expressions:
        self.log(f"Expression '{expression}' is not in the list of expressions.", level='warning')
        return False

    truth_table = self.generate_truth_table()
    for row in truth_table:
        if not row[expression]:
            self.log(f"Expression '{expression}' is not valid.")
            return False

    self.log(f"Expression '{expression}' is valid.")
    self.save_valid_truth(expression)
    return True

def save_valid_truth(self, expression):
    timestamp = datetime.datetime.now().isoformat()
    valid_truth = {"expression": expression, "timestamp": timestamp}
    self.valid_truths.append(valid_truth)
    save_valid_truth(valid_truth)
    self.log(f"Saved valid truth: '{expression}' at {timestamp}")
```

# Additional Methods

    get_valid_truths: Retrieves all validated truths.
    tautology: Checks if an expression is a tautology.
    modus_ponens: Implements the modus ponens rule of inference.
    unify_variables: Unifies variables between facts and rules.

# Modus Ponens Rule of Inference

Modus ponens is a fundamental rule of logic that states if a conditional statement ("if p then q") and its antecedent (p) are both true, then the consequent (q) must also be true. This method checks if the facts and rules align to conclude a new fact based on this logical principle.

# example usage

```python
if __name__ == '__main__':
    lt = LogicTables()
    lt.add_variable('A')
    lt.add_variable('B')
    lt.add_expression('A and B')
    lt.add_expression('A or B')
    lt.add_expression('not A')
    lt.add_expression('A xor B')
    lt.add_expression('A nand B')
    lt.add_expression('A nor B')
    lt.add_expression('A implication B')
    lt.display_truth_table()

    expression_to_validate = 'A and B'
    is_valid = lt.validate_truth(expression_to_validate)
    print(f"Is the expression '{expression_to_validate}' valid? {is_valid}")

    valid_truths = lt.get_valid_truths()
    print("Valid truths with timestamps:")
    for truth in valid_truths:
        print(truth)
```

This example demonstrates how to use the LogicTables class to add variables and expressions, generate and display a truth table, and validate logical expressions. For a deeper understanding of the easyAGI workflow visit <a href="https://rage.pythai.net/logictables-module-documentation/">logictables</a>



    










The `logic.py` module is a fundamental component of the funAGI project, underpinning its ability to reason and make decisions in a logical and structured manner. Its comprehensive support for logical operations and predicate logic makes it an invaluable resource for building intelligent, rational systems.
