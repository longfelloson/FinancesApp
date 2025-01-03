from enum import StrEnum


class OperationType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"


class Currency(StrEnum):
    EUR = "EUR"
    USD = "USD"
    