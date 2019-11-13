"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 8 registers
        self.reg = [0] * 8

        # 256 bytes of memory
        self.ram = [0] * 256

        # pass

        # Internal Registers
        # Program counter, current index, pointer to currently executing instruction
        self.pc = 0
        self.fl = None  # FLAG
        self.sp = 0

        # op_codes
        self.op_codes = {
            0b00000001: 'HLT',
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b10100010: 'MUL'}

    def ram_read(self, MAR):
        return self.ram[MAR]

    def raw_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    if line[0].startswith('0') or line[0].startswith('1'):
                        line = line.split("#")[0]
                        line = line.strip()
                        self.ram[address] = int(line, 2)

                        address += 1

                        # Comment out hardcoded program
                        # For now, we've just hardcoded a program:

                        # program = [
                        #     # From print8.ls8
                        #     0b10000010,  # LDI R0,8
                        #     0b00000000,
                        #     0b00001000,
                        #     0b01000111,  # PRN R0
                        #     0b00000000,
                        #     0b00000001,  # HLT
                        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        except FileNotFoundError as e:
            print(e)
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        # Add 'MUL' to ALU operations
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halted = False

        while not halted:
            self.trace()
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # Memory address from pc stored in IR variable
            self.ir = self.ram[self.pc]
            op = self.op_codes[self.ir]
            #self.pc += 2
            if op == 'LDI':

                self.reg[operand_a] = operand_b
                self.pc += 3

            elif op == 'PRN':

                print(self.reg[operand_a])
                self.pc += 2

            elif op == 'MUL':
                reg_a = self.ram_read(self.pc+1)
                print(f"reg_a: {reg_a}")
                reg_b = self.ram_read(self.pc+2)
                print(f"reg_b: {reg_b}")

                self.alu(op, reg_a, reg_b)
                self.pc += 3

            elif op == 'HLT':

                halted = True

            else:
                print(f"Unknown instruction at index {op}")
                sys.exit(1)
