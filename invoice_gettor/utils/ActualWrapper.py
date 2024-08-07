from actual import Actual
from actual.queries import get_transactions, create_transaction, get_accounts
from dotenv import load_dotenv
import os
import decimal
import datetime


class ActualWrapper:    
    def __enter__(self):
        load_dotenv()

        self.actual = Actual(
            base_url=os.getenv("base_url"),
            password=os.getenv("password"),
            encryption_password=os.getenv("encryption_password"),
            file=os.getenv("file"),
        )
        self.actual.__enter__()
        return self


    def listAllTransactions(self):
        transactions = get_transactions(self.actual.session)
        for t in transactions:
            account_name = t.account.name if t.account else None
            category = t.category.name if t.category else None
            print(t.date, account_name, t.notes, t.amount, category)


    def addOrder(self, date, notes, category, payment):
        t = create_transaction(
            self.actual.session, 
            date,
            get_accounts(self.actual.session, os.getenv("account"))[0],
            "Amazon",
            notes=notes,
            amount=payment
        )
        self.actual.commit()


    def __exit__(self, *args):
        self.actual.__exit__(*args)


# with ActualWrapper() as aw:
#     # aw.listAllTransactions()
#     aw.addOrder(notes="Test", payment=decimal.Decimal("-10.27"), date="", category="")