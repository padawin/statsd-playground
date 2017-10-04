#!/usr/bin/env python
import sys
from functools import reduce

class Calc(object):
    INVALID_OPERATOR = 1
    INVALID_TYPE_MEMBER = 2
    INVALID_NUMBER_MEMBERS = 3
    INVALID_DIVISION_BY_ZERO = 4

    def do_operation(self, operation):
        res = None
        try:
            members = [int(member) for member in operation[1:]]
        except ValueError:
            return (False, Calc.INVALID_TYPE_MEMBER)

        if len(members) < 2 or operation[0] == '/' and len(members) != 2:
            return (False, Calc.INVALID_NUMBER_MEMBERS)

        if operation[0] == '+':
            res = self.add(members)
        elif operation[0] == '-':
            res = self.sub(members)
        elif operation[0] == 'x':
            res = self.mult(members)
        elif operation[0] == '/':
            try:
                res = self.div(members[0], members[1])
            except ZeroDivisionError:
                return (False, Calc.INVALID_DIVISION_BY_ZERO)

        return (False, Calc.INVALID_OPERATOR) if res is None else (True, res)

    def add(self, members):
        return sum(members)

    def sub(self, members):
        return reduce(lambda x, y: x - y, members)

    def mult(self, members):
        return reduce(lambda x, y: x*y, members)

    def div(self, member1, member2):
        return member1 / member2

if __name__ == '__main__':
    c = Calc()
    res = c.do_operation(sys.argv[1:])
    if res[0]:
        print(res[1])
    elif res[1] == Calc.INVALID_NUMBER_MEMBERS:
        print("Usage:")
        print(" + member1 member2 ... membern")
        print(" - member1 member2 ... membern")
        print(" x member1 member2 ... membern")
        print(" / member1 member2")
    elif res[1] == Calc.INVALID_OPERATOR:
        print("Invalid operator {}".format(sys.argv[1]))
    elif res[1] == Calc.INVALID_TYPE_MEMBER:
        print("All members must be integers")
    elif res[1] == Calc.INVALID_DIVISION_BY_ZERO:
        print("Division by zero is not valid in this universe")
