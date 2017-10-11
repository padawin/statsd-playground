#!/usr/bin/env python
import sys
from functools import reduce
import statsd

class Calc(object):
    INVALID_OPERATOR = 1
    INVALID_TYPE_MEMBER = 2
    INVALID_NUMBER_MEMBERS = 3
    INVALID_DIVISION_BY_ZERO = 4

    def __init__(self, stats_client):
        self.stats_client = stats_client

    def do_operation(self, operation):
        self.stats_client.incr('operation')
        res = None
        try:
            members = [int(member) for member in operation[1:]]
        except ValueError:
            self.stats_client.incr('operation.error.member')
            return (False, Calc.INVALID_TYPE_MEMBER)

        if len(members) < 2 or operation[0] == '/' and len(members) != 2:
            self.stats_client.incr('operation.error.member_count')
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

        if res is None:
            self.stats_client.incr('operation.error.operator')
            return (False, Calc.INVALID_OPERATOR)
        else:
            return (True, res)

    def add(self, members):
        self.stats_client.incr('operation.sum')
        return sum(members)

    def sub(self, members):
        self.stats_client.incr('operation.sub')
        return reduce(lambda x, y: x - y, members)

    def mult(self, members):
        self.stats_client.incr('operation.mult')
        return reduce(lambda x, y: x*y, members)

    def div(self, member1, member2):
        self.stats_client.incr('operation.div')
        return member1 / member2

if __name__ == '__main__':
    stats_client = statsd.StatsClient(sys.argv[1], 8125)
    c = Calc(stats_client)
    res = c.do_operation(sys.argv[2:])
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
