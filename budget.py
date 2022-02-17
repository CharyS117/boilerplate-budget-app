class Category:
    def __init__(self, name) -> None:
        self.name = name
        self.ledger = []

    def deposit(self, amount, description='') -> None:
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description='') -> bool:
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False

    def get_balance(self) -> float:
        balance = 0
        for record in self.ledger:
            balance = balance + record['amount']
        return balance

    def transfer(self, amount, budget2: 'Category') -> bool:
        if self.check_funds(amount):
            description1 = 'Transfer to ' + budget2.name
            description2 = 'Transfer from ' + self.name
            self.withdraw(amount, description1)
            budget2.deposit(amount, description2)
            return True
        else:
            return False

    def check_funds(self, amount) -> bool:
        if amount > self.get_balance():
            return False
        else:
            return True

    def __str__(self) -> str:
        name_len = len(self.name)
        output = (15 - name_len//2 - name_len % 2) * '*' + \
            self.name + (15-name_len//2) * '*'
        for record in self.ledger:
            description = record['description'][:23]
            amount = '{:.2f}'.format(record['amount'])
            output = output + '\n' + description + \
                (30 - len(description) - len(amount)) * ' ' + amount
        output = output + '\n' + 'Total: ' + \
            '{:.2f}'.format(self.get_balance())
        return output


def create_spend_chart(categories):
    withdrawals = []
    percents = []
    categories_name = []
    name_len_max = 0
    for category in categories:
        withdrawals.append(0)
        if len(category.name) > name_len_max:
            name_len_max = len(category.name)
        for record in category.ledger:
            if record['amount'] < 0:
                withdrawals[-1] = withdrawals[-1] - record['amount']
    withdrawal_sum = sum(withdrawals)
    for withdrawal in withdrawals:
        percents.append(withdrawal/withdrawal_sum*100)
    output = 'Percentage spent by category\n'
    y_axis = 100
    while y_axis >= 0:
        output = output + ' ' * (3 - len(str(y_axis))) + str(y_axis) + '| '
        for i in range(len(categories)):
            if percents[i] >= y_axis:
                output = output + 'o  '
            else:
                output = output + '   '
        y_axis = y_axis - 10
        output = output + '\n'
    output = output + ' '*4 + '-'*3*len(categories) + '-\n'
    for category in categories:
        categories_name.append(
            category.name+' '*(name_len_max - len(category.name)))
    for i in range(name_len_max):
        output = output + ' ' * 4
        for j in range(len(categories)):
            output = output + ' ' + categories_name[j][i] + ' '
        output = output + ' '
        if i != name_len_max-1:
            output = output + '\n'
    return output
