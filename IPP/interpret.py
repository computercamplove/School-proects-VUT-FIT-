import sys
import re
import xml.etree.ElementTree as ET
#author - Abikenova Zhamilya

#class to labels from program
class LabelStack:
    labels_stack = {}
    call_stack = []

    def add_label(self, value, order):
        if value not in self.labels_stack:
            self.labels_stack[value] = int(order)
        else:
            error_code("Value already exists.", 52)

class InstructionClass:
    def __init__(self, instruction):
        self.opcode = ""
        self.var_type = []
        self.var_value = []

        self.gs_var = []
        self.glob_stack = []
        self.stack_value = []

        self.opcode = instruction.attrib["opcode"].upper()
        self.order = instruction.attrib["order"]
        for arg in instruction:
            self.var_type.append(arg.attrib["type"])
            self.var_value.append(arg.text)
            if arg.attrib["type"] == 'var':
                self.gs_var = arg.text.split("@", 1)
                self.glob_stack.append(self.gs_var[0])
                self.stack_value.append(self.gs_var[1])

    #methods to check right value
    def int_type(self, index):
        if self.var_type[index] == 'int':
            if re.search(r"^[-|+]?[0-9]+$", self.var_value[index]):
                return True
        return False

    def bool_type(self, index):
        if self.var_type[index] == 'bool':
            if self.var_value[index].lower() == 'true' or self.var_value[index].lower() == 'false':
                return True
        return False

    def nil_type(self, index):
        if self.var_type[index] == 'nil':
            if re.search(r"^nil$", self.var_value[index].lower()):
                return True
        return False

    def string_type(self, index):
        if self.var_type[index] == 'string':
            if re.search(r"^([^#\\]|\\\d\d\d)*$", str(self.var_value[index])):
                return True
        return False

    def var_type_method(self, index):
        if self.var_type[index] == 'var':
            if re.search(r"^(GF|LF|TF)$", self.var_value[index][:2]):
                if re.search(r"^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$", self.var_value[index][3:].lower()):
                    return True
        return False

    def label_type(self, index):
        if self.var_type[index] == 'label':
            if re.search(r"[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$", self.var_value[index].lower()):
                return True
        return False

    def type_type(self, index):
        if self.var_type[index] == 'type':
            if re.search(r"^(string|int|bool)$", self.var_value[index].lower()):
                return True
        return False
    #methods to check right amount of parameters for instructions
    def arg_zero(self):
        if not (len(self.var_type) == 0):
            error_code("arg_zero()", 32)

    def arg_two(self):
        if len(self.var_type) == 2:
            if re.search(r"^(MOVE|NOT|INT2CHAR|STRLEN|TYPE)$", self.opcode):
                if self.var_type_method(0):
                    if not (self.int_type(1) or self.bool_type(1) or self.string_type(1) or self.nil_type(1) or self.var_type_method(1)):
                        error_code("arg_two()", 32)
                else:
                    error_code("arg_two()", 32)
            elif self.opcode == 'READ':
                if self.var_type_method(0):
                    if not self.type_type(1):
                        error_code("arg_two()", 32)
                else: error_code("arg_two()", 32)
            else:
                error_code("arg_two()", 32)
        else:
            error_code("arg_two()", 32)

    def arg_one(self):
        if len(self.var_type) == 1:
            if re.search(r"^(DEFVAR|POPS)$", self.opcode):
                if not self.var_type_method(0):
                    error_code("arg_one()", 32)
            elif re.search(r"^(CALL|LABE|JUMP)$", self.opcode):
                if not self.label_type(0):
                    error_code("arg_one()", 32)
            elif re.search(r"^(PUSHS|WRITE|EXIT|DPRINT)$", self.opcode):
                if not (self.int_type(0) or self.bool_type(0) or self.string_type(0) or self.nil_type(0) or self.var_type_method(0)):
                    error_code("arg_one()", 32)
        else:
            error_code("arg_one()", 32)

    def arg_three(self):
        if len(self.var_type) == 3:
            if re.search(r"^(JUMPIFEQ|JUMPIFNEQ)$", self.opcode):
                if not (self.label_type(0) and (self.int_type(1) or self.bool_type(1) or self.string_type(1) or self.nil_type(1) or self.var_type_method(1))
                        and (self.int_type(2) or self.bool_type(2) or self.string_type(2) or self.nil_type(2) or self.var_type_method(2))):
                    error_code("arg_three()", 32)
            elif self.var_type[0] == 'var':
                if not (self.var_type_method(0) and (self.int_type(1) or self.bool_type(1) or self.string_type(1) or self.nil_type(1) or self.var_type_method(1))
                        and (self.int_type(2) or self.bool_type(2) or self.string_type(2) or self.nil_type(2) or self.var_type_method(2))):
                    error_code("arg_three()", 32)
            else: error_code("arg_three()", 32)
        else:
            error_code("arg_three()", 32)

    #method to checks Instructions
    def arg_count(self):
        if re.search(r"^(MOVE|NOT|INT2CHAR|READ|STRLEN|TYPE)$", self.opcode):
            self.arg_two()
        elif re.search(r"^(CREATEFRAME|PUSHFRAME|POPFRAME|RETURN|BREAK)$", self.opcode):
            self.arg_zero()
        elif re.search(r"^(DEFVAR|CALL|PUSHS|POPS|WRITE|LABEL|JUMP|EXIT|DPRINT)$", self.opcode):
            self.arg_one()
        elif re.search(r"^(ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|STRI2INT|CONCAT|GETCHAR|SETCHAR|JUMPIFEQ|JUMPIFNEQ)$", self.opcode):
            self.arg_three()
        else:
            error_code("Instruction doesn't exist", 32)

#class for work with frames
class FramesClass:
    stack_ramce = []
    stack_data = []

    gf = {}
    lf = None
    tf = None

    def createTF(self):
        self.tf = {}

    #method for DEFVAR instruction to define new variable
    def defVar(self,frame,varname):
        if frame == "GF":
            if varname not in self.gf:
                self.gf[varname]=["", ""]
            else:
                error_code("Variable already exist. GF.", 52)
        elif frame == "TF":
            if self.tf == None:
                error_code("TF is None", 55)
            if varname not in self.tf:
                self.tf[varname]=["", ""]
            else:
                error_code("Variable already exist. TF.", 52)
        elif frame == "LF":
            if self.lf == None:
                error_code("LF is None", 55)
            if varname not in self.lf:
                self.lf[varname]=["", ""]
            else:
                error_code("Variable already exist. LF.", 52)
        else:
            error_code("Unknown frame", 32)
    #method which sets new value and type for variable
    def setVal(self,frame,varname,type,value):
        if frame == "GF":
            if varname in self.gf:
                self.gf[varname]=[type,value]
            else:
                error_code("Variable doesn't exist. GF.",54)
        elif frame=="LF":
            if self.lf == None:
                error_code("LF is None", 55)
            if varname in self.lf:
                self.lf[varname]=[type,value]
            else:
                error_code("Variable doesn't exist. LF.",54)
        elif frame=="TF":
            if self.tf == None:
                error_code("TF is None", 55)
            if varname in self.tf:
                self.tf[varname]=[type,value]
            else:
                error_code("Variable doesn't exist. TF.",54)
        else:
            error_code("Unknown frame", 32)

    def getVal(self, frame, varname):
        if frame == "GF":
            if varname in self.gf:
                return self.gf.get(varname)
            else:
                error_code("Variable doesn't exist. GF.",54)
        elif frame == "TF":
            if self.tf == None:
                error_code("TF is None", 55)
            if varname in self.tf:
                return self.tf.get(varname)
            else:
                error_code("Variable doesn't exist. TF.", 54)
        elif frame == "LF":
            if self.lf == None:
                error_code("LF is None",55)
            if varname in self.lf:
                return self.lf.get(varname)
            else:
                error_code("Variable doesn't exist. LF.", 54)
        else:
            error_code("Unknown frame", 32)

#calculates and returns result for arithmetical instructions and LT, GT, EQ
def bool_f(instr, type1, type2, x, y):
    if instr == "LT":
        if type1 == 'int' and type2 == 'int':
            if int(x) < int(y):
                return True
            else: return False
        elif type1 == 'bool' and type2 == 'bool':
            if x < y:
                return True
            else:
                return False
        elif type1 == 'string' and type1 == 'string':
            if string_format(str(x)) < string_format(str(y)):
                return True
            else:
                return False
        else:
            error_code("Bad type", 53)
    elif instr == "GT":
        if type1 == 'int' and type2 == 'int':
            if int(x) > int(y):
                return True
            else: return False
        elif type1 == 'bool' and type2 == 'bool':
            if x > y:
                return True
            else:
                return False
        elif type1 == 'string' and type1 == 'string':
            if string_format(str(x)) > string_format(str(y)):
                return True
            else:
                return False
        else:
            error_code("Bad type GT", 53)
    elif instr == "ADD":
        if type1 == "int" and type2 == "int":
            return int(x) + int(y)
        else: error_code("Bad type for ADD", 53)
    elif instr == "MUL":
        if type1 == "int" and type2 == "int":
            return int(x) * int(y)
        else: error_code("Bad type for MUL", 53)
    elif instr == "SUB":
        if type1 == "int" and type2 == "int":
            return int(x) - int(y)
        else: error_code("Bad type", 53)
    elif instr == "IDIV":
        if type1 == "int" and type2 == "int":
            if int(y) == 0:
                error_code("IDIV",57)
            else:
                return int(int(x) // int(y))
        else:
            error_code("Bad type", 53)
    elif instr == "EQ":
        if type1 == 'int' and type2 == 'int':
            if int(x) == int(y):
                return True
            else:
                return False
        elif (type1 == 'bool' and type2 == 'bool'):
            if x == y:
                return True
            else:
                return False
        elif type1 == 'nil' or type2 == 'nil':
            if (type1 == type2) and (type1 == 'nil' and type2 =='nil'):
                return True
            elif (type1 != type2) and (type1 == 'nil' or type2 =='nil'):
                return False
            else:
                return False
        elif type1 == 'string' and type1 == 'string':
            if string_format(str(x)) == string_format(str(y)):
                return True
            else:
                return False
        else:
            error_code("Bad type - string", 53)
#checks and returns right type of value
def check_type(type, value):
    if type == '':
        value = ''
        return value
    elif type == "bool":
        if value == 'true':
            value = True
            return value
        else:
            value = False
            return value
    elif type == "string":
        if value == None:
            value = ''
            return string_format(str(value))
        else:
            return string_format(str(value))
    elif type == 'nil':
        return value
    elif type == 'int':
        return int(value)
    else:
        error_code("Not right type in check_type()", 53)

#function returns boolean results for ligic instructions
def logic(instr, var1, var2):
    if instr == 'AND':
        if var1 == var2:
            if var1 == True:
                return var1
            elif var1 == False:
                return var1
            else:
                error_code("Not right value of operand in AND.", 57)
        elif var1 != var2:
            return False
        else:
            error_code("Not right value of operand in AND.", 57)
    elif instr == "OR":
        if var1 == var2:
            if var1 == True:
                return var1
            elif var1 == False:
                return var1
            else:
                error_code("Not right value of operand in OR.", 57)
        elif var1 != var2:
            return True
        else:
            error_code("Not right value of operand in OR.", 57)
    else:
        error_code("Unknown instruction", 32)

#returns message and error codes
def error_code(text, num):
    sys.stderr.write('{} {}'.format(text, num))
    sys.exit(num)

#checks xml tree for right attributes and tags
def sort_xml(xml):
    order = []
    count=1

    if xml.tag != 'program':
        error_code("Bad xml tree", 32)
    if 'language' not in xml.attrib:
        error_code("Bad xml tree", 32)
    if xml.attrib['language'] != "IPPcode20":
        error_code("Bad language", 32)

    for instruction in xml:
        if instruction.tag != 'instruction':
            error_code("Bad xml tree", 32)
        if 'order' not in instruction.attrib:
            error_code("Bad xml tree ", 32)
        if 'opcode' not in instruction.attrib:
            error_code("Bad xml tree ", 32)

    for instruction in xml:
        if instruction.attrib['order'].isdigit() == False:
            error_code("Order is not digit or negative", 32)
        if int(instruction.attrib['order']) <= 0:
            error_code("Bad order", 32)
        ord = int(instruction.attrib['order'])
        order.append((ord, instruction))

    try:
        order.sort()
    except:
        error_code("Error in sort_xml() - not right orders. Dublicate", 32)
    xml[:] = [i[-1] for i in order]

    for instruction in xml:
        instruction[:] = sorted(instruction, key=lambda child: (child.tag))
        instruction.attrib['order']=count
        count+=1
        if len(instruction) == 1:
            if instruction[0].tag != 'arg1':
                error_code("Should be 1 argument", 32)
        elif len(instruction) == 2:
            if instruction[0].tag != 'arg1' or instruction[1].tag != 'arg2':
                error_code("Should be 2 arguments", 32)
        elif len(instruction) == 3:
            if instruction[0].tag != 'arg1' or instruction[1].tag != 'arg2' or instruction[2].tag != 'arg3':
               error_code("Should be 3 arguments", 32)
        for instr in instruction:
            if not (re.search(r"^(int|string|nil|bool|var|type|label)$", instr.attrib['type'])):
                error_code("Bad xml", 32)
    return xml

#convert escape sequences in string into the right char
def string_format(string):
    for num in re.findall(r"\\\d\d\d", string):
        char = chr(int(num[2:]))
        if char == '\\':
            char = re.escape(char)
        string = re.sub(re.escape(num), char, string)
    return string

#reads input file and files from sys.stdin
def file_read(file):
    string = ""
    if file == 'file':
        source = sys.argv[1][9:]
        try:
            File = open(source, 'r')
        except:
            error_code("Can't open file", 11)

        for line in File:
            string += line.strip()
        #checks right format of xml
        try:
            program = ET.fromstring(string)
        except:
            error_code("Bad XML format.", 31)
        File.close()

    if file == 'input':
        for line in sys.stdin:
            string += line.strip()
        try:
            program = ET.fromstring(string)
        except:
            error_code("Bad XML format.", 31)

    return program

#main functuin to check arguments and work with instructions
def main():
    frames = FramesClass()
    labels = LabelStack()

    if len(sys.argv) == 2:
        if sys.argv[1] == '--help':
            print("Program which executes the XML version of .IPPCode20 language.")
            print("How to use:")
            print("--source: file with xml code. If not defined - reads from standard input")
            print("--input: file with inputs for the actual interpretation of the given source code. If not defined - reads from standard input")
            sys.exit(0)

        elif sys.argv[1][:8] == '--source':
            program = file_read('file')
        elif sys.argv[1][:7] == '--input':
            try:
                sys.stdin = open(sys.argv[1][8:], 'r')
            except IOError:
                error_code("Can't read file", 11)
            program = file_read('input')
    elif len(sys.argv) == 3:
        if sys.argv[2][:7] == '--input' and sys.argv[1][:8] == '--source':
            try:
                sys.stdin = open(sys.argv[2][8:], 'r')
            except IOError:
                error_code("Can't read file", 11)
            program = file_read('file')

    else:
        error_code("Error: ", 12)

    program = sort_xml(program)

    #first cycle to store Labels
    count=0
    for instr in program:
        count+=1
        labels_instr = InstructionClass(instr)
        labels_instr.arg_count()
        if labels_instr.opcode == 'LABEL':
            if labels_instr.var_type[0] == 'label':
                labels.add_label(labels_instr.var_value[0], labels_instr.order)
            else:
                error_code("Bad type", 53)

    #second main cycle for work with every instruction in program
    order=0
    while order < count:
        line_object = InstructionClass(program[order])  # {'order': '1', 'opcode': 'DEFVAR'}
        line_object.arg_count()
        opcode = line_object.opcode

        if opcode == "DEFVAR":
            frames.defVar(line_object.glob_stack[0], line_object.stack_value[0])

        elif opcode == "CREATEFRAME":
            frames.createTF()

        elif opcode == "PUSHFRAME":
            if frames.tf is None:
                error_code("TF is None", 55)
            else:
                frames.stack_ramce.append(frames.tf)
                frames.lf = frames.stack_ramce[-1]
                frames.tf = None

        elif opcode == "POPFRAME":
            if frames.lf is None and frames.stack_ramce == []:
                error_code("LF is None, stack is empty", 55)
            else:
                frames.tf = frames.stack_ramce.pop()
                if frames.stack_ramce == []:
                    frames.lf = None
                else:
                    frames.lf = frames.stack_ramce[-1]

        elif opcode == "EXIT":
            if line_object.var_type[0] == "var":
                symb = frames.getVal(line_object.glob_stack[0], line_object.stack_value[0])
                if symb[0] == '':
                    error_code('Empty variable', 56)
                if symb[0] != 'int':
                    error_code("Not right type in EXIT.", 53)
                if int(symb[1]) < 0 or int(symb[1]) > 49:
                    error_code('Error. Can be 0-49', 57)
                else:
                    sys.exit(int(symb[1]))
            elif line_object.var_type[0] == 'int':
                symb_val = check_type(line_object.var_type[0], line_object.var_value[0])
                if symb_val < 0 or symb_val > 49:
                    error_code('Error. Can be 0-49', 57)
                else:
                    sys.exit(symb_val)
            else:
                error_code("Not right type in EXIT.", 53)

        elif opcode == "PUSHS":
            if line_object.var_type[0] == 'var':
                symb = frames.getVal(line_object.glob_stack[0], line_object.stack_value[0])
                if symb[0] == '':
                    error_code("Empty", 56)
                frames.stack_data.append(symb)
            elif re.search(r"^(string|bool|int|nil)$", line_object.var_type[0]):
                arg = check_type(line_object.var_type[0], line_object.var_value[0])
                frames.stack_data.append([line_object.var_type[0],arg])
            else:
                error_code("Not right type in PUSHS.", 53)

        elif opcode == "POPS":
            if line_object.var_type[0] == 'var':
                if frames.stack_data == []:
                    error_code("Data stack is empty. POPS.", 56)
                else:
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], frames.stack_data[-1][0], frames.stack_data[-1][1])
                    frames.stack_data.pop()
            else:
                error_code("Not right type in POPS.", 53)

        elif opcode == "JUMP":
            if line_object.var_type[0] == 'label':
                if line_object.var_value[0] not in labels.labels_stack:
                    error_code("Value not in stack", 52)
                else:
                    order = labels.labels_stack[line_object.var_value[0]]
                    order-=1
            else:
                error_code("Not right type in JUMP.", 53)

        elif opcode == "LABEL":
            if line_object.var_type[0] == 'label':
                pass
            else:
                error_code("Not right type in LABEL.", 53)

        elif opcode == "JUMPIFEQ" or opcode == "JUMPIFNEQ":
            symb1=[]
            symb2=[]
            if line_object.var_type[0] == 'label':
                if line_object.var_value[0] not in labels.labels_stack:
                    error_code('Not define label', 52)
                if line_object.var_type[1] == 'var' and line_object.var_type[2]!="var":
                    symb1=frames.getVal(line_object.glob_stack[0],line_object.stack_value[0])
                    symb2=[line_object.var_type[2],line_object.var_value[2]]

                elif line_object.var_type[1] != 'var' and line_object.var_type[2]=="var":
                    symb1=[line_object.var_type[1],line_object.var_value[1]]
                    symb2= frames.getVal(line_object.glob_stack[0],line_object.stack_value[0])

                elif line_object.var_type[1] == 'var' and line_object.var_type[2]=="var":
                    symb1 = frames.getVal(line_object.glob_stack[0],line_object.stack_value[0])
                    symb2 = frames.getVal(line_object.glob_stack[1],line_object.stack_value[1])

                elif line_object.var_type[1] != 'var' and line_object.var_type[2]!="var":
                    symb1 = [line_object.var_type[1],line_object.var_value[1]]
                    symb2 = [line_object.var_type[2], line_object.var_value[2]]
                else:
                    error_code("JUMPIFEQ|JUMPIFNEQ.", 53)

                if symb1[0] == '' or symb2[0] == '':
                    error_code("Error", 56)

                if symb1[0] != symb2[0] and symb1[0] != "nil" and symb2[0] != "nil":
                    error_code("Not same type in JUMPIFEQ|JUMPIFNEQ.", 53)
                symb1[1] = check_type(symb1[0], symb1[1])
                symb2[1] = check_type(symb2[0], symb2[1])

                if symb1[1] == symb2[1] and opcode == 'JUMPIFEQ':
                    order = labels.labels_stack[line_object.var_value[0]]
                    order -= 1
                elif symb1[1] != symb2[1] and opcode == 'JUMPIFNEQ':
                    order = labels.labels_stack[line_object.var_value[0]]
                    order -= 1
            else:
                error_code("Not right type in JUMPIFEQ|JUMPIFNEQ.", 53)

        elif opcode == "CALL":
            if line_object.var_type[0] == 'label':
                if line_object.var_value[0] not in labels.labels_stack:
                    error_code("Value not in stack", 52)
                else:
                    if order not in labels.call_stack:
                        labels.call_stack.append(order + 1)
                        order = labels.labels_stack[line_object.var_value[0]]
                        order -=1
                    else:
                        error_code("Variable already exist. CALL.", 52)
            else:
                error_code("Not right type in CALL.", 53)

        elif opcode == "RETURN":
            if labels.call_stack == []:
                error_code("Empty", 56)
            else:
                order = labels.call_stack.pop()
                order -=1

        elif opcode == "READ":
            if line_object.var_type[0] == 'var' and line_object.var_type[1] == 'type':
                arg = frames.getVal(line_object.glob_stack[0], line_object.stack_value[0])
                try:
                    variable_input = input()
                except:
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'nil', 'nil')
                    variable_input=""

                if variable_input == "":
                    pass
                elif line_object.var_value[1] == 'int':
                    if re.search(r'^[+|-]?\d+$', variable_input):
                        variable_input = variable_input.replace('\n', '').replace('\r', '')
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', int(variable_input))
                    else:
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'nil', 'nil')
                elif line_object.var_value[1] == 'string':
                    if re.search(r".*", variable_input):
                        variable_input = variable_input.replace('\n', '').replace('\r', '')
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', str(variable_input))
                    else:
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'nil', 'nil')
                elif line_object.var_value[1] == 'bool':
                    if re.search(r"^true\s*$", variable_input.lower()):
                        variable_input = variable_input.replace('\n', '').replace('\r', '')
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', True)
                    else:
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', False)
                else:
                    error_code("Not right type in READ instruction", 53)
            else:
                error_code("Not right type in READ instruction", 53)


        elif opcode == 'WRITE':
            if re.search(r"^(string|bool|int|nil)$", line_object.var_type[0]):
                if line_object.var_type[0] == 'nil':
                    print("", end='')
                elif line_object.var_type[0] == 'bool':
                    print("{}".format(str(line_object.var_value[0]).lower()), end='')
                else:
                    print("{}".format(string_format(line_object.var_value[0])), end='')
            elif line_object.var_type[0] == 'var':
                symb = frames.getVal(line_object.glob_stack[0], line_object.stack_value[0])
                if symb[0] == '':
                    error_code('Empty www', 56)
                if symb[0] == 'nil':
                    print("", end='')
                elif symb[0] == 'bool':
                    print("{}".format(str(symb[1]).lower()), end='')
                else:
                    print("{}".format(symb[1]), end='')
            else:
                error_code("Not right type in WRITE.", 53)

        elif opcode == "DPRINT":
            if re.search(r"^(string|bool|int|nil|var)$", line_object.var_type[0]):
                pass
            else:
                error_code("Not right type in DPRINT.", 53)

        elif opcode == "BREAK":
            pass

        elif opcode == "MOVE":
            if line_object.var_type[0] == 'var':
                if line_object.var_type[1] == 'var':
                    var_to_value=frames.getVal(line_object.glob_stack[1],line_object.stack_value[1])
                    if var_to_value[0] == '' and var_to_value[1] == '':
                        error_code('Empty variable ', 56)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0],var_to_value[0], check_type(var_to_value[0], var_to_value[1]))
                elif re.search(r"^(string|bool|int|nil)$", line_object.var_type[1]):
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], line_object.var_type[1], check_type(line_object.var_type[1], line_object.var_value[1]))
                else:
                    error_code("Not right type for <symb2> in MOVE.", 53)
            else:
                error_code("Not right type for <symb1> in MOVE.", 53)

        #Arithmetical functions, saves rusult to first parametr (+, -, //, *)
        elif re.search(r"^(ADD|SUB|IDIV|MUL)$", opcode):
            if line_object.var_type[0] == 'var':
                if line_object.var_type[1] == 'var' and line_object.var_type[2] == 'var':
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    arg2 = frames.getVal(line_object.glob_stack[2], line_object.stack_value[2])
                    if arg1[0] == '' or arg2[0] == '':
                        error_code('Empty variable', 56)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg1[0], bool_f(opcode, arg1[0], arg2[0], arg1[1], arg2[1]))
                elif line_object.var_type[1] == 'int' and line_object.var_type[2] == 'int':
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], line_object.var_type[1], bool_f(opcode, line_object.var_type[1], line_object.var_type[2], line_object.var_value[1], line_object.var_value[2]))
                elif line_object.var_type[1] == 'int' and line_object.var_type[2] == 'var':
                    arg2 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg2[0] == '':
                        error_code('Empty variable', 56)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], line_object.var_type[1], bool_f(opcode, line_object.var_type[1], arg2[0], line_object.var_value[1], arg2[1]))
                elif line_object.var_type[2] == 'int' and line_object.var_type[1] == 'var':
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg1[0] == '':
                        error_code('Empty variable', 56)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], line_object.var_type[2], bool_f(opcode, arg1[0], line_object.var_type[2], arg1[1], line_object.var_value[2]))
                else: error_code("Not right type for <symb2> in (ADD|SUB|IDIV|MUL).", 53)
            else:
                error_code("Not right type for <symb1> in (ADD|SUB|IDIV|MUL).", 53)
        #saves rusult to first parametr (<, >, ==)
        elif re.search(r"^(LT|GT|EQ)$", opcode):
            if line_object.var_type[0] == "var":
                if line_object.var_type[1] == 'var' and line_object.var_type[2] == 'var':
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    arg2 = frames.getVal(line_object.glob_stack[2], line_object.stack_value[2])
                    if arg1[0] == '' or arg2[0] == '':
                        error_code('Empty variable', 56)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', bool_f(opcode, arg1[0], arg2[0], arg1[1], arg2[1]))
                elif line_object.var_type[1] == 'var' and re.search(r"^(string|bool|int|nil)$", line_object.var_type[2]):
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg1[0] == '':
                        error_code('Empty variable', 56)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', bool_f(opcode, arg1[0], line_object.var_type[2], arg1[1], check_type(line_object.var_type[2], line_object.var_value[2])))
                elif line_object.var_type[2] == 'var' and re.search(r"^(string|bool|int|nil)$", line_object.var_type[1]):
                    arg2 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg2[0] == '':
                        error_code('Empty variable', 56)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', bool_f(opcode, arg2[0], check_type(line_object.var_type[1],line_object.var_value[1]), arg2[1]))
                elif re.search(r"^(string|bool|int|nil)$", line_object.var_type[2]) and re.search(r"^(string|bool|int|nil)$", line_object.var_type[1]):
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', bool_f(opcode, line_object.var_type[1], line_object.var_type[2], line_object.var_value[1], line_object.var_value[2]))
                else:
                    error_code("Not right type for <symb2> in (LT|GT|EQ).", 53)
            else:
                error_code("Not right type for <symb1> in (LT|GT|EQ).", 53)

        #logic instructions, calls function logic() to calculate and returns True or False
        elif re.search(r"^(AND|OR|NOT)$", opcode):
            if line_object.var_type[0] == 'var':
                #instruction NOT has two parameter
                if opcode == 'NOT':
                    if line_object.var_type[1] == 'var':
                        arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                        if arg1[0] == '' and arg1[1] == '':
                            error_code('Empty variable', 56)
                        if arg1[0] != 'bool':
                            error_code("Not right type NOT", 53)
                        if arg1[1] == True:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', False)
                        elif arg1[1] == False:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', True)
                        else:
                            error_code("Not right value of operand in (NOT).", 57)
                    elif line_object.var_type[1] == 'bool':
                        if check_type(line_object.var_type[1], line_object.var_value[1]) == True:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', False)
                        elif check_type(line_object.var_type[1], line_object.var_value[1]) == False:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', True)
                        else:
                            error_code("Not right value of operand in (NOT).", 57)
                    else:
                        error_code("Not right type for <symb1> in NOT.", 53)
                #coditions for AND and OR which have three parameter
                elif line_object.var_type[1] == 'var' and line_object.var_type[2] == 'var':
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    arg2 = frames.getVal(line_object.glob_stack[2], line_object.stack_value[2])
                    if arg1[0] == '' or arg2[0] == '':
                        error_code('Empty variable', 56)
                    if arg1[0] != arg2[0]:
                        error_code('Not the same type', 53)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', logic(opcode, arg1[1], arg2[1]))
                elif line_object.var_type[1] == 'var' and line_object.var_type[2] == 'bool':
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg1[0] == '':
                        error_code('Empty variable', 56)
                    if arg1[0] != line_object.var_type[2]:
                        error_code('Not the same type', 53)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', logic(opcode, arg1[1], check_type(line_object.var_type[2], line_object.var_value[2])))
                elif line_object.var_type[1] == 'bool' and line_object.var_type[2] == 'var':
                    arg2 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg2[0] == '':
                        error_code('Empty variable', 56)
                    if arg2[0] != line_object.var_type[1]:
                        error_code('Not the same type', 53)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', logic(opcode, check_type(line_object.var_type[1], line_object.var_value[1]), arg2[1]))
                elif line_object.var_type[1] == 'bool' and line_object.var_type[2] == 'bool':
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'bool', logic(opcode, check_type(line_object.var_type[1], line_object.var_value[1]), check_type(line_object.var_type[2], line_object.var_value[2])))
                else:
                    error_code("Not right type for <symb2> in (AND|OR).", 53)
            else:
                error_code("Not right type for <symb1> in (AND|OR).", 53)

        #convert integer to string by chr()
        elif opcode == "INT2CHAR":
            ch =""
            if line_object.var_type[0] == 'var':
                if line_object.var_type[1] == 'var':
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg1[0] == '' and arg1[1] == '':
                        error_code('Empty variable ', 56)
                    if arg1[0] == 'int':
                        try:
                            ch = chr(arg1[1])
                        except ValueError:
                            error_code("Indexing outside the given string in INT2CHAR", 58)
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', ch)
                    else:
                        error_code("INT2CHAR", 53)
                elif line_object.var_type[1] == 'int':
                    try:
                        ch = chr(check_type(line_object.var_type[1], line_object.var_value[1]))
                    except ValueError:
                        error_code("Indexing outside the given string in INT2CHAR", 58)
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', ch)
                else:
                    error_code("INT2CHAR", 53)
            else:
                error_code("INT2CHAR", 53)

        #convert char to integer by ord()
        elif opcode == "STRI2INT":
            if line_object.var_type[0] == 'var':
                if line_object.var_type[1] == "var" and line_object.var_type[2] == 'var':
                    symb1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    symb2 = frames.getVal(line_object.glob_stack[2], line_object.stack_value[2])
                    if symb1[0] == '' or symb2[0] == '':
                        error_code('Empty variable ', 56)
                    if symb1[0] == 'string' and symb2[0] == 'int':
                        if symb2[1] < 0 or len(symb1[1]) <= symb2[1]:
                            error_code("Indexing outside the given string in STRI2INT", 58)
                        else:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', ord(symb1[1][symb2[1]]))
                    else:
                        error_code("STRI2INT", 53)
                elif line_object.var_type[1] == "var" and line_object.var_type[2] == 'int':
                    symb1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    symb2_val = check_type(line_object.var_type[2], line_object.var_value[2])
                    if symb1[0] == '':
                        error_code('Empty variable ', 56)
                    if symb1[0] == 'string':
                        if symb2_val < 0 or len(symb1[1])<=symb2_val:
                            error_code("Indexing outside the given string in STRI2INT", 58)
                        else:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', ord(symb1[1][symb2_val]))
                    else:
                        error_code("STRI2INT", 53)
                elif line_object.var_type[1] == "string" and line_object.var_type[2] == 'int':
                    symb1_val = check_type(line_object.var_type[1], line_object.var_value[1])
                    symb2_val = check_type(line_object.var_type[2], line_object.var_value[2])
                    if symb2_val < 0 or len(symb1_val)<=symb2_val:
                        error_code("Indexing outside the given string in STRI2INT", 58)
                    else:
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', ord(symb1_val[symb2_val]))
                elif line_object.var_type[1] == "string" and line_object.var_type[2] == 'var':
                    symb1_val = check_type(line_object.var_type[1], line_object.var_value[1])
                    symb2 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if symb2[0] == '':
                        error_code('Empty variable ', 56)
                    if symb2[0] == 'int':
                        if symb2[1] < 0 or len(symb1_val)<=symb2:
                            error_code("Indexing outside the given string in STRI2INT", 58)
                        else:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', ord(symb1_val[symb2[1]]))
                    else:
                        error_code("STRI2INT", 53)
                else:
                    error_code("STRI2INT", 53)
            else:
                error_code("STRI2INT", 53)

        #concatenate two strings
        elif opcode == "CONCAT":
            if line_object.var_type[0] != 'var':
                error_code("CONCAT", 53)

            if line_object.var_type[1] == 'var' and line_object.var_type[2] == 'var':
                arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                arg2 = frames.getVal(line_object.glob_stack[2], line_object.stack_value[2])
                if arg1[0] == '' or arg2[0] == '':
                    error_code('Empty variable ', 56)
                if arg1[0] == 'string' and arg2[0] == 'string':
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg1[0], arg1[1] + arg2[1])
                else:
                    error_code("CONCAT",53)
            elif line_object.var_type[1] == 'string' and line_object.var_type[2] == 'string':
                symb1 = check_type(line_object.var_type[1], line_object.var_value[1])
                symb2 = check_type(line_object.var_type[2], line_object.var_value[2])
                frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], line_object.var_type[1], symb1 + symb2)
            elif line_object.var_type[1] == 'var' and line_object.var_type[2] == 'string':
                arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                if arg1[0] == '':
                    error_code('Empty variable ', 56)
                symb2 = check_type(line_object.var_type[2], line_object.var_value[2])
                if arg1[0] == 'string':
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg1[0], arg1[1] + symb2)
                else:
                    error_code("CONCAT",53)
            elif line_object.var_type[2] == 'var' and line_object.var_type[1] == 'string':
                arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                if arg1[0] == '':
                    error_code('Empty variable ', 56)
                symb1 = check_type(line_object.var_type[1], line_object.var_value[1])
                if arg1[0] == 'string':
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg1[1], symb1 + arg1[1])
                else:
                    error_code("CONCAT", 53)
            else:
                error_code("CONCAT", 53)
        #instruction works as a len(), returns amount of characters
        elif opcode == "STRLEN":
            if line_object.var_type[0] != 'var':
                error_code("STRLEN", 53)
            if line_object.var_type[1] == 'var':
                arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                if arg1[0] == '' and arg1[1] == '':
                    error_code("Empty variable ", 56)
                if arg1[0] != 'string':
                    error_code("STRLEN", 53)
                if arg1[1] is None:
                    arg1[1] = 0
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', 0)
                else:
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', len(arg1[1]))
            elif line_object.var_type[1] == 'string':
                if line_object.var_value[1] is None:
                    line_object.var_value[1] = 0
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', 0)
                else:
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'int', len(string_format(line_object.var_value[1])))
            else:
                error_code("STRLEN", 53)

        #instruction returns to first parameter one character from string (second parameter) with index from third parameter
        elif opcode == "GETCHAR":
            if line_object.var_type[0] == 'var':
                if line_object.var_type[1] == 'string' and line_object.var_type[2] == 'int':
                    if (int(line_object.var_value[2])) > len(line_object.var_value[1])-1 or int(line_object.var_value[2]) < 0:
                        error_code("Indexing outside the given string in GETCHAR", 58)
                    else:
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', line_object.var_value[1][int(line_object.var_value[2])])
                elif line_object.var_type[1] == 'var' and line_object.var_type[2] == 'int':
                    arg = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg[0] == '':
                        error_code('Empty variable', 56)
                    if arg[0] == 'string':
                        if (int(line_object.var_value[2])) > len(arg[1]) -1 or int(line_object.var_value[2]) < 0:
                            error_code("Indexing outside the given string in GETCHAR", 58)
                        else:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', arg[1][int(line_object.var_value[2])])
                    else:
                        error_code("GETCHAR", 53)
                elif line_object.var_type[1] == 'string' and line_object.var_type[2] == 'var':
                    arg = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg[0] == '':
                        error_code('Empty variable', 56)
                    if arg[0] == 'int':
                        if (int(arg[1])) > len(line_object.var_value[1])-1 or int(arg[1]) < 0:
                            error_code("Indexing outside the given string in GETCHAR", 58)
                        else:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', line_object.var_value[1][int(arg[1])])
                    else:
                        error_code("GETCHAR", 53)
                elif line_object.var_type[1] == 'var' and line_object.var_type[2] == 'var':
                    arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    arg2 = frames.getVal(line_object.glob_stack[2], line_object.stack_value[2])
                    if arg1[0] == '' or arg2[0] == '':
                        error_code('Empty variable', 56)
                    if arg2[0] == 'int' and arg1[0] == 'string':
                        if (int(arg2[1])) > len(arg1[1])-1 or int(arg2[1]) < 0:
                            error_code("Indexing outside the given string in GETCHAR", 58)
                        else:
                            frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', arg1[1][int(arg2[1])])
                    else:
                        error_code("GETCHAR", 53)
                else:
                    error_code("GETCHAR", 53)
            else:
                error_code("GETCHAR", 53)

        #changes character in string
        elif opcode == "SETCHAR":
            if line_object.var_type[0] == 'var':
                arg0 = frames.getVal(line_object.glob_stack[0], line_object.stack_value[0])
                if arg0[0] == '':
                    error_code('Empty variable', 56)
                if arg0[0] == 'string':
                    if arg0[1] == '':
                        error_code("Not right value of operand in SETCHAR.", 58)
                    if line_object.var_type[1] == 'var' and line_object.var_type[2] == 'var':
                        arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                        arg2 = frames.getVal(line_object.glob_stack[2], line_object.stack_value[2])
                        if arg1[0] == '' or arg2[0] == '':
                            error_code('Empty variable', 56)
                        if arg1[0] == 'int' and arg2[0] == 'string':
                            if arg2[1] == '':
                                error_code("Not right value of operand in SETCHAR.", 58)
                            if int(arg1[1]) > len(arg0[1]) - 1 or int(arg1[1]) < 0:
                                error_code("Indexing outside the given string in SETCHAR", 58)
                            else:
                                frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg0[0], arg0[1][:int(arg1[1])] + arg2[1][0] + arg0[1][int(arg1[1])+1:])
                        else:
                            error_code("SETCHAR", 53)

                    elif line_object.var_type[1] == 'var' and line_object.var_type[2] == 'string':
                        if line_object.var_value[2] == None:
                            error_code('Empty string for Setchar ', 58)
                        arg1 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                        if arg1[0] == '':
                            error_code('Empty variable', 56)
                        if arg1[0] == 'int':
                            if int(arg1[1]) > len(arg0[1]) - 1 or int(arg1[1]) < 0:
                                error_code("Indexing outside the given string in SETCHAR", 58)
                            else:
                                line_object.var_value[2] = string_format(line_object.var_value[2])
                                frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg0[0], arg0[1][:int(arg1[1])] + line_object.var_value[2][0] + arg0[1][int(arg1[1])+1:])
                        else:
                            error_code("SETCHAR", 53)

                    elif line_object.var_type[1] == 'int' and line_object.var_type[2] == 'string':
                        if line_object.var_value[2] == None:
                            error_code('Empty string for Setchar ', 58)
                        if line_object.var_value[2] != '':
                            if int(line_object.var_value[1]) < 0 or int(line_object.var_value[1]) > len(arg0[1]) - 1:
                                error_code("Indexing outside the given string in SETCHAR", 58)
                            else:
                                line_object.var_value[2] = string_format(line_object.var_value[2])
                                frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg0[0], arg0[1][:int(line_object.var_value[1])] + line_object.var_value[2][0] + arg0[1][int(line_object.var_value[1])+1:])
                        else:
                            error_code("Not right value of operand in SETCHAR.", 58)

                    elif line_object.var_type[1] == 'int' and line_object.var_type[2] == 'var':
                        arg2 = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                        if arg2[0] == '':
                            error_code('Empty variable', 56)
                        if arg2[0] == 'string':
                            if arg2[1] == '':
                                error_code("Not right value of operand in SETCHAR.", 58)
                            if int(line_object.var_value[1]) < 0 or int(line_object.var_value[1]) > len(arg0[1]) - 1:
                                error_code("Indexing outside the given string in SETCHAR", 58)
                            else:
                                frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], arg0[0], arg0[1][:int(line_object.var_value[1])] + arg2[1][0] + arg0[1][int(line_object.var_value[1])+1:])
                        else:
                            error_code("SETCHAR", 53)
                    else:
                        error_code("SETCHAR", 53)
                else:
                    error_code("SETCHAR", 53)
            else:
                error_code("SETCHAR", 53)
        #reterns type
        elif opcode == "TYPE":
            if line_object.var_type[0] == 'var':
                if line_object.var_type[1] == 'var':
                    arg = frames.getVal(line_object.glob_stack[1], line_object.stack_value[1])
                    if arg[0] == '':
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', '')
                    else:
                        frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', str(arg[0]))
                elif re.search(r"^(string|bool|int|nil)$", line_object.var_type[1]):
                    frames.setVal(line_object.glob_stack[0], line_object.stack_value[0], 'string', str(line_object.var_type[1]))
                else:
                    error_code("Not right type for <symb2> in TYPE.", 53)
            else:
                error_code("Not right type for <symb1> in TYPE.", 53)
        order+=1

if __name__ == '__main__':
    main()
