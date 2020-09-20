import sys

registers = {}
operations = {} # need renaming...

def add_operation(op, func):
    operations[op] = func

# How to add more operators... just provide a callable and map it to a name
add_operation('add', lambda lhs, rhs: lhs + rhs)
add_operation('subtract', lambda lhs, rhs: lhs - rhs)
add_operation('multiply', lambda lhs, rhs: lhs * rhs)
add_operation('division', lambda lhs, rhs: lhs / rhs)


class Register():

    def __init__(self):
        self.dependants = list()

    def valid_add(self, operation):
        if isinstance(operation.val, Register):
            children = operation.val.get_children()
            if self in children:
                print("error, cyclic dependency")
                return False
            
        return True

    def add(self, operation):
        if self.valid_add(operation):
            self.dependants.append(operation)
        
        return True

    def get_children(self):
        children = list()

        for operation in self.dependants:
            if isinstance(operation.val, Register):
                children.append(operation.val)

                children.append(operation.val.get_children())

        return children


    def eval(self):
        sum = 0
        for operation in self.dependants:
            # looks up the operation and calls the appropriate function
            sum = operations[operation.op](sum, operation.eval())

        return sum
 


class Operation():
    op = None
    val = None # can either be a numberic value or a register

    def __init__(self, op, val):
        self.op = op
        self.val = val

    def eval(self):
        # if it's a Register object do a recursive call down the tree
        if isinstance(self.val, Register):
            return self.val.eval()
        else:
            return self.val


def valid_operation(name):
    return name in operations

def valid_register(name):
    # Any name consisting of alphanumeric characters should be allowed as register names.
    return name.isalnum()

def register_exists(name):
    return name in registers
    
def add_register(name):
    if valid_register(name):
        # print("adding register " + name)
        registers[name] = Register()

def valid_command(command):
    if len(command) == 1: # should be a quit command
        if (command[0] == "quit"):
            return True

    if len(command) == 2: # should be a print command
        reg = command[1]
        if register_exists(reg) and command[0] == "print":
            return True

    if len(command) == 3: # operation command, reg + op + reg/val
        dest = command[0]   
        src = command[2]
        op = command[1]

        if valid_register(dest) and valid_register(src) and valid_operation(op):
            if register_exists(dest) and register_exists(src):
                # need to check for cycles if both registrers already exists.
                dest_reg = registers[dest]
                if not dest_reg.valid_add(Operation(op, registers[src])):
                    return False
            return True

    return False

def run_command(line):
    # All input should be case insensitive, also removes trailing newlines from input...
    command = line.lower().rstrip().split(" ")

    if valid_command(command):
        if len(command) == 1: # quit
            exit()

        if len(command) == 2: # print 
            reg = command[1]
            print(registers[reg].eval())

        if len(command) == 3:
            dest = command[0]
            src = command[2]
            op = command[1]

            if not register_exists(dest):
                add_register(dest)
            dest_reg = registers[dest]

            if register_exists(src):
                dest_reg.add(Operation(op, registers[src]))
            else:
                if src.isnumeric(): # if no register previously exists and only numbers assume value-operation
                    dest_reg.add(Operation(op, int(src)))
                else: # else create new register...

                    # also check so we dont get a cycle in the dependency tree
                    
                    add_register(src)
                    dest_reg.add(Operation(op, registers[src]))

    else:
        # Invalid commands can be ignored, but should be logged to the console.
        print(line.rstrip())


def handle_input(istream):
    for line in f:
        run_command(line)

    # When accepting input from file, it should not be necessary to include
    # quit to exit the program. Adding a quit command in the end to make sure the program exits.
    run_command("quit")




# The program should either take its input from the standard input stream, or from a file. When
# the program is launched with one command line argument, input should be read from the file
# specified in the argument.
if len(sys.argv) > 1:
    f = open(sys.argv[1], 'r')
    # maybe check if file exists...
else:
    f = sys.stdin

handle_input(f)

# for command in commands:
#     print(command)

# reg1 = Register("1")
# reg2 = Register("2")

# reg1.add(Operation("add", 5))
# reg1.add(Operation("multiply", reg2))
# reg2.add(Operation("add", 1))
# reg2.add(Operation("multiply", 10))

# print(reg1.eval())

# result = Register()
# revenue = Register()
# costs = Register()
# salaries = Register()

# result.add(Operation("add", revenue))
# result.add(Operation("subtract", costs))

# revenue.add(Operation("add", 200))
# costs.add(Operation("add", salaries))
# salaries.add(Operation("add", 20))
# salaries.add(Operation("multiply", 5))
# costs.add(Operation("add", 10))
# print(result.eval())

# print(len(result.get_children()))

# costs.add(Operation("add", result))