# logic.py (c) 2024 Gregory L. Magnusson MIT license
# store log in ./memory/truth as ./memory/truth/logiclogs.txt and in ./mindx/logiclog.txt
#### handling belief, contigent, fact and truth as MEMORY in ./memory/truth ####
# logic BELIEF
# store belief as belief in {datetime.datetime.now().isoformat()}_belief.json
# logic CONTINGENT
# store not tautology as contingent in {contingent_data['timestamp']}_contingent.json
# logic FACT
# store modus ponens as fact in {fact_data['timestamp']}_fact.json
# logic TRUTH
# store truth as truth in {truth_data['timestamp']}_truth.json
import itertools
import logging
import datetime
import pathlib
import json
from memory.memory import create_memory_folders, save_valid_truth, store_in_stm, DialogEntry

class LogicTables:
    def __init__(self):
        self.variables = []
        self.expressions = []
        self.valid_truths = []
        self.logger = logging.getLogger('LogicTables')
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all logs

        # Ensure directories exist
        general_log_dir = './mindx/errors'
        memory_log_dir = './memory/truth'
        pathlib.Path(general_log_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(memory_log_dir).mkdir(parents=True, exist_ok=True)

        # General log file for mindx
        file_handler_mindx = logging.FileHandler(f'{general_log_dir}/log.txt')
        file_handler_mindx.setLevel(logging.DEBUG)
        file_formatter_mindx = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler_mindx.setFormatter(file_formatter_mindx)

        # Log file for memory/truth
        file_handler_memory = logging.FileHandler(f'{memory_log_dir}/logs.txt')
        file_handler_memory.setLevel(logging.DEBUG)
        file_formatter_memory = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler_memory.setFormatter(file_formatter_memory)

        self.logger.addHandler(file_handler_mindx)
        self.logger.addHandler(file_handler_memory)

        # Remove any other handlers (like StreamHandler) if they exist
        self.logger.propagate = False

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

        # Ensure the directory exists
        pathlib.Path(general_log_path).parent.mkdir(parents=True, exist_ok=True)

        with open(general_log_path, 'a') as file:
            file.write(f"{level.upper()}: {message}\n")

    def store_log_in_memory(self, message, level):
        memory_log_path = './memory/truth/logs.txt'

        # Ensure the directory exists
        pathlib.Path(memory_log_path).parent.mkdir(parents=True, exist_ok=True)

        with open(memory_log_path, 'a') as file:
            file.write(f"{level.upper()}: {message}\n")

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

    def output_belief(self, belief):
        belief_path = './memory/truth'

        # Ensure the directory exists
        pathlib.Path(belief_path).mkdir(parents=True, exist_ok=True)

        belief_file = f"{belief_path}/{datetime.datetime.now().isoformat()}_belief.json"
        with open(belief_file, 'w') as file:
            json.dump({"belief": belief, "timestamp": datetime.datetime.now().isoformat()}, file)

    def output_truth(self, variables, expressions, truth_table):
        truth_path = './memory/truth'

        # Ensure the directory exists
        pathlib.Path(truth_path).mkdir(parents=True, exist_ok=True)

        truth_data = {
            "belief": {
                "variables": variables,
                "expressions": expressions,
                "truth_table": truth_table
            },
            "timestamp": datetime.datetime.now().isoformat()
        }

        truth_file = f"{truth_path}/{truth_data['timestamp']}_truth.json"
        with open(truth_file, 'w') as file:
            json.dump(truth_data, file)

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
        self.output_truth(self.variables, self.expressions, truth_table)
        return truth_table

    def display_truth_table(self):
        truth_table = self.generate_truth_table()
        headers = self.variables + self.expressions
        print("\t".join(headers))
        for row in truth_table:
            print("\t".join(str(row[var]) for var in headers))

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

    def get_valid_truths(self):
        self.log("Retrieving valid truths.")
        return self.valid_truths

    def tautology(self, expression):
        truth_table = self.generate_truth_table()
        for row in truth_table:
            if not self.evaluate_expression(expression, row):
                self.log(f"Expression '{expression}' is not a tautology.", level='info')
                return False
        self.log(f"Expression '{expression}' is a tautology.", level='info')
        return True

    def modus_ponens(self, fact1, fact2):
        if fact1['type'] == 'fact' and fact2['type'] == 'rule':
            if self.unify_variables(fact1, fact2):
                conclusion = {'type': 'fact', 'relation': fact2['relation'][1:], 'arguments': fact1['arguments']}
                return conclusion
        return None

    def unify_variables(self, fact1, fact2):
        if (set(fact1['arguments']).intersection(set(fact2['relation'])) or
            set(fact2['arguments']).intersection(set(fact1['relation']))):
            return False
        return True

# Memory folder creation at module load
create_memory_folders()

# Example usage
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

