class Category:

  def __init__(self, category=None):
    self.ledger = []
    self.category = category.lower().capitalize()
    self.funds = None
    self.withdrawn = []

  def check_funds(self, amount):
    if self.funds < amount:
      return False
    else:
      return True

  def deposit(self, deposit_amount, deposit_descrip=None):
    self.deposit_amount = deposit_amount
    self.deposit_descrip = deposit_descrip
    self.funds = deposit_amount
    if deposit_descrip is not None:
      return self.ledger.append({"amount": self.deposit_amount, "description": deposit_descrip})
    else:
      return  self.ledger.append({"amount": self.deposit_amount, "description": ''})

  def withdraw(self, withdraw_amount, withdraw_descrip=None):
    self.withdraw_amount = -(withdraw_amount)
    self.withdraw_descrip = withdraw_descrip
    if self.check_funds(withdraw_amount) is False:
      return False
    self.funds = self.funds - withdraw_amount
    self.withdrawn.append(withdraw_amount)
    if withdraw_descrip is not None:
      self.ledger.append({"amount": self.withdraw_amount, "description": self.withdraw_descrip})
    else:
      self.ledger.append({"amount": self.withdraw_amount, "description": ''})
    return True

  def transfer(self, amount, category):
    if self.check_funds(amount) is False:
      return False
    self.funds = self.funds - amount
    self.transfered = category.deposit(amount, ("Transfer from " + self.category))
    self.to_category = category.category
    self.withdrawn.append(amount)
    self.ledger.append({"amount": -(amount), "description": ("Transfer to " + self.to_category)})
    return True


  def get_balance(self):
    return self.funds


  def __repr__(self):
    self.ledger.append({'balance': self.funds})
    ledger = []

    c = self.category
    stars = (int((30 - len(c))/2) * ("*")) + c + (int((30 - len(c))/2) * "*")
    ledger.append((stars + '\n'))

    for l in self.ledger:
      for k, v in l.items():
        if k == "description":
          amount = l["amount"]
          amount = str(f'{amount:.2f}')
          spacing = (int((30 - len(v) - len(amount))) * ' ')
          if v == []:
            spacing = (int((30 - len(v) - len(amount) - 2)) * ' ')
            v = str(v)
          if len(v) >= int(30 - len(amount)):
            v = v[0 : int(30- len(amount) -1)] + ' '
          ledger.append((str(v + spacing + amount) + '\n'))
        if k == "balance":
          amount = (len('balance') + len(str(v)))
          spacing = (int( 30 - amount) * ' ')
          ledger.append(("Total: " + str(v)))
    return ''.join(ledger).replace("'", '')


def create_spend_chart(categories):
  spacing = len(categories) * len(categories) + 1

  withdrawals = []
  if len(categories) > 1:
    for category in categories:
      category = category.withdrawn
      withdrawals.append(category)
  else:
    category = categories.withdrawn
    withdrawals.append(category)
  totals = 0
  for withdraw in withdrawals:
    for total in withdraw:
      totals = round(float(totals + total), 2)

  charts = []
  for categor in categories:
    amount = 0
    amount_category = categor.withdrawn
    for amount_categ in amount_category:
      amount = round(amount_categ + amount, 2)
      amount = int((amount / totals) * 100) 
      if amount >= 10:
        amount = round(amount, -1)  
      else:
        amount = round(amount, 0) 
    catty = {categor.category: amount}
    charts.append(catty)


  chart_2 = ["Percentage spent by category" '\n',]
  for percent in range(0, 110, 10):  
    bars = []
    for chart in charts:
      for k, v in chart.items(): 
        if percent <= v:
          bar = ' o '
        else:
          bar = 3 * ' '
        bars.append(bar)
    bars.append(' ')
    if len(str(percent)) < 3:
      if len(str(percent)) < 2:
        percent = '  ' + str(percent)
      else:
        percent = ' ' + str(percent)
    bar_chart = str(percent)+ '|' + (''.join(bars)) + '\n'
    chart_2.insert(1, bar_chart)
  chart_2.append((4 * ' ' + (spacing * '-') + '\n')) 

  cat_names = []
  longest = 0
  for names in categories:
    names = names.category
    cat_names.append(names)
    if longest < len(names):
      longest = len(names)

  vc = []
  l = longest
  for i in range(0, longest):
    l -= 1
    vc.append(4 * ' ')  

    for nam in cat_names:
      try: 
        if i <= len(nam):
            vc.append(' ' + nam[i] + ' ')
      except: 
        space = 3 * ' '
        vc.append(space)
      if i > len(nam):
        space = 3 * ' '
        vc.append(space)
    if l > 0: 
      vc.append(' \n')
    else: 
      vc.append(' ')
  chart_2.append(''.join(vc))

  return ''.join(chart_2)