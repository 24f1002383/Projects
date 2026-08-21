class Expense:
    def __init__(self, amount, category, description, date):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def __str__(self):
        return (
            f"Amount: {self.amount}, "
            f"Category: {self.category}, "
            f"Description: {self.description}, "
            f"Date: {self.date}"
        )