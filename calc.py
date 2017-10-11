from functools import reduce

class Calc(object):
    INVALID_OPERATOR = 1
    INVALID_TYPE_MEMBER = 2
    INVALID_NUMBER_MEMBERS = 3
    INVALID_DIVISION_BY_ZERO = 4

    def __init__(self, stats_client=None):
        self.stats_client = stats_client or 'localhost'

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
                self.stats_client.incr('operation.error.division_by_0')
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
