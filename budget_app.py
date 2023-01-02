class Category:
    def __init__(self, description) -> None:
        self.description = description
        self.ledger = []
        self.balance : float = 0.0

    def __repr__(self):
        ledger = ''
        head = self.description.center(30, '*')
        for i in self.ledger:
            desc = i['description'][:23] + ' ' * (30 - len(i['description'][:23]) - len(str("{:.2f}".format(i['amount']))[:7])) + str("{:.2f}".format(i['amount'])[:7]) + '\n'
            ledger += desc
        tail = f'Total: {self.balance}'
        return head + '\n' + ledger + tail
    
    
    def deposit (self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw (self, amount, description = ''):
        if self.balance - amount >= 0:
            self.ledger.append({'amount': -1 * amount, 'description': description})
            self.balance -= amount

            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, another_category):
        if self.withdraw(amount, f'Transfer to {another_category.description}'):
            another_category.deposit(amount, f'Transfer from {self.description}')
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.balance:
            return False
        else:
            return True

def create_spend_chart(lst:list) -> str:
    header = 'Percentage spent by category\n'
    lines = '    ' + '-' * (3*(len(lst)) + 1) + '\n'
    footer = ''
    footer_lst = []
    
    spent_cat = []
    spent_cat_str = ''
    for i in lst:
        total_spent = 0
        for x in i.ledger:
            if x['amount'] < 0:
                total_spent += abs(x['amount'])
        spent_cat.append(total_spent)
    total_spent = sum(spent_cat)
    def spent_to_perc(lst, num):
        string_cat = ''
        for i in lst:
            if int((i/total_spent)*100) <= num:
                string_cat += '   '
            else:
                string_cat += ' o '
        return string_cat
        

    for i in reversed(range(0,101, 10)):
        spent_cat_str += f'{i}|'.rjust(4) + spent_to_perc(spent_cat, i) + '\n'
  
    descriptions = list(map(lambda cat: cat.description, lst))
    max_len = max(map(lambda desc: len(desc), descriptions))
    descriptions = list(map(lambda desc: desc.ljust(max_len), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return header + spent_cat_str + lines + footer


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)
print(create_spend_chart([food, clothing, auto]))




