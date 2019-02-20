from functools import reduce
from typing import List, Dict


def __sum_transaction(amount, transaction):
    return amount + transaction.amount


def __format_transaction_list(transaction_list: List) -> Dict:
    positions = {}

    for transaction in transaction_list:
        positions.setdefault(transaction.instrument, [])
        positions[transaction.instrument].append(transaction)

    return positions


def get_current_positions(transaction_list: List) -> Dict:
    transactions = __format_transaction_list(transaction_list)

    return {
        instrument: reduce(__sum_transaction, transaction_list, 0)
        for instrument, transaction_list in transactions.items()
    }
