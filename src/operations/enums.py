import enum


class OperationType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
