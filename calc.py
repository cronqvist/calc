import sys




# How to add more operators... just provide a callable and map it to a name
# add_operation('add', lambda lhs, rhs: lhs + rhs)
# add_operation('subtract', lambda lhs, rhs: lhs - rhs)
# add_operation('multiply', lambda lhs, rhs: lhs * rhs)
# add_operation('division', lambda lhs, rhs: lhs / rhs)

class Register():

    def __init__(self):
        self.children = list()

    # checks wheter the child is already inside the parent
    def check_children(self, parent):
        children = parent.get_all_children()
        # print(type(children))
        
        # for child in children:
        #     print(child.name)

        if self in children:
            # print("error, cyclic dependency")
            return False

        return True


    def valid_add(self, operation):
        if isinstance(operation.val, Register):

            # checks whether both child and parent register contains eachother
            if not self.check_children(operation.val) or not operation.val.check_children(self):
                return False

        return True

    def add(self, operation):
        if self.valid_add(operation):
            # print("adding")
            self.children.append(operation)
        
        return True

    def get_all_children(self):
        children = list()

        for operation in self.children:
            if isinstance(operation.val, Register):
                children.append(operation.val)

                for child in operation.val.get_all_children():
                    children.append(child) # flatten...

        return children


    def eval(self, symbols):
        sum = 0
        for operation in self.children:
            # looks up the operation and calls the appropriate function
            sum = symbols[operation.op](sum, operation.eval(symbols))

        return sum
 


class Operation():
    op = None
    val = None # can either be a numberic value or a register

    def __init__(self, op, val):
        self.op = op
        self.val = val

    def eval(self, symbols):
        # if it's a Register object do a recursive call down the tree
        if isinstance(self.val, Register):
            return self.val.eval(symbols)
        else:
            return self.val

class Calculator():


    def add_operation(self, op, func):
        self.symbols[op] = func

    def __init__(self):
        self.registers = {} 
        self.symbols = {} 

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
                val = self.registers[reg].eval(self.symbols)
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
            # print(line.rstrip())
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

    # return output 


# The program should either take its input from the standard input stream, or from a file. When
# the program is launched with one command line argument, input should be read from the file
# specified in the argument.
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         f = open(sys.argv[1], 'r')
#         # maybe check if file exists...
#     else:
#         f = sys.stdin

#     calc = Calculator()
#     output = calc.handle_input(f)

#     for val in output:
#         print(val)
#     print(output)
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

# print(len(result.get_all_children()))

# costs.add(Operation("add", result))

# cyclic
r1 = Register()
r2 = Register()
r3 = Register()

r1.add(Operation("add", r2))
r2.add(Operation("add", r3))

# should fail
r3.add(Operation("add", r1))
r2.add(Operation("add", r1))

# r1 = Register("r1")
# r2 = Register("r2")
# r3 = Register("r3")

# r1.add(Operation("add", r2))
# r2.add(Operation("add", r3))
# r3.add(Operation("add", r1))

