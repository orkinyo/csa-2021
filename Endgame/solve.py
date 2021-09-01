import operator
from varname.helpers import Wrapper
from Crypto.Util.number import long_to_bytes

with open("real_ins", "rb") as fd:
    instructions = fd.read()

instructions = instructions[2:-2]

ins_index = 0

##REGISTERS
_1A = Wrapper(0)
_1B = Wrapper(0)
_1C = Wrapper(0)
_1D = Wrapper(0)
_1E = Wrapper(0)
_1F = Wrapper(0)

registers_dict = {"0x1a" : _1A, "0x1b" : _1B, "0x1c" : _1C, "0x1d" : _1D, "0x1e" : _1E, "0x1f" : _1F}
operations_map = {"0xab" : operator.add, "0xba" : operator.sub, "0xcd" : operator.mul, "0xdc" : operator.floordiv}

setattr(_1A, "value", 0x1)

def set_register():
    global _1A, _1B, _1C, _1D, _1E, _1F, ins_index, instructions

    ##GET REGISTER ASSIGNMENT
    try:
        register_assignment = registers_dict[hex(instructions[ins_index])]
    except:
        return False
    ins_index += 1

    ##GET VALUE
    value = instructions[ins_index]
    setattr(register_assignment, "value", value)
    ins_index += 1

    return True

def execute_opcode():
    global _1A, _1B, _1C, _1D, _1E, _1F, ins_index, instructions
    
    ##GET OPERATOR
    try:
        operator = operations_map[hex(instructions[ins_index])]
    except:
        return False
    ins_index += 1

    #GET REGISTERS TO OPERATE ON
    reg_encode = instructions[ins_index]
    first_reg = registers_dict[hex((reg_encode >> 0x4) + 0x10)]
    second_reg = registers_dict[hex((reg_encode & 0xf) + 0x10)]
    ins_index += 1

    ##OPERATE
    setattr(first_reg, "value", operator(first_reg.value, second_reg.value))

    return True

def execute_ins():
    global _1A, _1B, _1C, _1D, _1E, _1F, ins_index, instructions
    
    if not set_register():
        if not execute_opcode():
            pass

   
while ins_index < len(instructions) - 1:
    execute_ins()

print(f"flag = {long_to_bytes(_1A.value).decode()}")