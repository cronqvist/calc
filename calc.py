import sys

class Register():

    def __init__(self):
        self.children = list()

    # checks wheter the child is already inside the parent
    def check_children(self, parent):
        children = parent.get_all_children()

        if self in children:
            # print("error, cyclic dependency")
            return False

        return True


    def valid_add(self, operation):
        if isinstance(operation.val, Register):

            # checks whether both child and parent register contains eachother, this can be
            # be done in a single bfs/dfs check. For every visited vertex 'v', if there is a child 'u' that is already visited
            # and 'u' is not a parent of 'v', then there is a cycle. But this will do fine for now.
            if not self.check_children(operation.val) or not operation.val.check_children(self):
                return False

        return True

    def add(self, operation):
        if self.valid_add(operation):
            self.children.append(operation)
        
        return True

    def get_all_children(self):
        children = list()

        for operation in self.children:
            if isinstance(operation.val, Register):
                children.append(operation.val)

                for child in operation.val.get_all_children():
                    children.append(child) # flatten the the list...

        return children


    def eval(self):
        sum = 0
        for operation in self.children:
            # looks up the operation and calls the appropriate function
            sum = Calculator.symbols[operation.op](sum, operation.eval())

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

class Calculator():
    symbols = {}

    def add_operation(self, op, func):
        self.symbols[op] = func

    def __init__(self):
        self.registers = {} 
        self.add_operation('add', lambda lhs, rhs: lhs + rhs)
        self.add_operation('subtract', lambda lhs, rhs: lhs - rhs)
        self.add_operation('multiply', lambda lhs, rhs: lhs * rhs)
        self.add_operation('division', lambda lhs, rhs: lhs / rhs)


    @staticmethod
    def valid_register_name(name):
        # Any name consisting of alphanumeric characters should be allowed as register names.
        return name.isalnum()

    def valid_operation(self, name):
        return name in self.symbols

    def register_exists(self, name):
        return name in self.registers
        
    def add_register(self, name):
        if self.valid_register_name(name):
            # print("adding register " + name)
            self.registers[name] = Register()

    def valid_command(self, line):
        command = line.lower().rstrip().split(" ")

        if len(command) == 1: # should be a quit command
            if (command[0] == "quit"):
                return True

        if len(command) == 2: # should be a print command
            reg = command[1]
            if self.register_exists(reg) and command[0] == "print":
                return True

        if len(command) == 3: # operation command, reg + op + reg/val
            dest = command[0]   
            src = command[2]
            op = command[1]

            if self.valid_register_name(dest) and self.valid_register_name(src) and self.valid_operation(op):
                if self.register_exists(dest) and self.register_exists(src):
                    # need to check for cycles if both registrers already exists.
                    dest_reg = self.registers[dest]
                    if not dest_reg.valid_add(Operation(op, self.registers[src])):
                        return False
                return True

        return False

    def run_command(self, line):
        # All input should be case insensitive, also removes trailing newlines from input...
        command = line.lower().rstrip().split(" ")

        if self.valid_command(line):
            if len(command) == 1: # quit
                #exit()
                return "quit"

            if len(command) == 2: # print 
                reg = command[1]
                val = self.registers[reg].eval()
                # print(val)
                return val

            if len(command) == 3:
                dest = command[0]
                op = command[1]
                src = command[2]

                if not self.register_exists(dest):
                    self.add_register(dest)
                dest_reg = self.registers[dest]

                if self.register_exists(src):
                    dest_reg.add(Operation(op, self.registers[src]))
                else:
                    if src.isnumeric(): # if no register previously exists and only numbers assume value-operation
                        dest_reg.add(Operation(op, int(src)))
                    else: # else create new register...
                        self.add_register(src)
                        dest_reg.add(Operation(op, self.registers[src]))

        else:
            # Invalid commands can be ignored, but should be logged to the console.
            return line.rstrip()


    def handle_input(self, istream):
        output = list()

        # reset old registers
        self.registers = {}

        # The program should either take its input from the standard input stream, or from a file. When
        # the program is launched with one command line argument, input should be read from the file
        # specified in the argument. When accepting input from file, it should not be necessary to include
        # quit to exit the program.

        # I interpret this as if quit is not supplied by stdin it should never exit? it sounds a bit strange so i just take whats given
        # and process it.

        for line in istream:
            # val = run_command(line)
            val = self.run_command(line)
            if val:
                if val == "quit":
                    return output

                output.append(val)
        return output


# The program should either take its input from the standard input stream, or from a file. When
# the program is launched with one command line argument, input should be read from the file
# specified in the argument.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
        # maybe check if file exists...
    else:
        f = sys.stdin

    calc = Calculator()
    output = calc.handle_input(f)

    for val in output:
        print(val)