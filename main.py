#!/usr/bin/env python
import calc
import statsd
import sys

if __name__ == '__main__':
    stats_client = statsd.StatsClient('localhost', 8125)
    c = calc.Calc(stats_client)
    res = c.do_operation(sys.argv[1:])
    if res[0]:
        print(res[1])
    elif res[1] == calc.Calc.INVALID_NUMBER_MEMBERS:
        print("Usage:")
        print(" + member1 member2 ... membern")
        print(" - member1 member2 ... membern")
        print(" x member1 member2 ... membern")
        print(" / member1 member2")
    elif res[1] == calc.Calc.INVALID_OPERATOR:
        print("Invalid operator {}".format(sys.argv[1]))
    elif res[1] == calc.Calc.INVALID_TYPE_MEMBER:
        print("All members must be integers")
    elif res[1] == calc.Calc.INVALID_DIVISION_BY_ZERO:
        print("Division by zero is not valid in this universe")
