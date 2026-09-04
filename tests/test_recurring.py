from datetime import date
from dateutil.relativedelta import relativedelta
from app import crud, schemas

def test_monthly_recurring_date_advancement(db_session):
    # Test year rollover: Dec 31 to Jan 31
    base_date = date(2026, 12, 31)
    next_date = base_date + relativedelta(months=1)
    assert next_date == date(2027, 1, 31)

    # Test leap year adjustment: Jan 31 into Feb
    leap_date = date(2028, 1, 31)
    next_leap_date = leap_date + relativedelta(months=1)
    assert next_leap_date == date(2028, 2, 29)