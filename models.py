class Expense:
    """
    Represents a single expense in the application.
    """

    def __init__(self, amount, category, description, date, expense_id=None):
        self.expense_id = expense_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date


class Budget:
    """
    Represents a weekly or monthly budget.
    """

    def __init__(
        self,
        amount,
        period,
        start_date,
        end_date,
        budget_id=None
    ):
        self.budget_id = budget_id
        self.amount = amount
        self.period = period
        self.start_date = start_date
        self.end_date = end_date