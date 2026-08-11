from datetime import (
    date,
    datetime
)


def calculate_remaining_budget(
    budget_amount,
    total_spent
):
    """Calculate money remaining."""

    return budget_amount - total_spent


def calculate_days_remaining(
    end_date
):
    """Calculate how many budget days remain."""

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    ).date()

    today = date.today()

    days = (
        end - today
    ).days + 1

    return max(
        days,
        0
    )


def calculate_daily_allowance(
    remaining_budget,
    days_remaining
):
    """Calculate recommended daily spending."""

    if (
        remaining_budget <= 0
        or days_remaining <= 0
    ):
        return 0

    return (
        remaining_budget
        / days_remaining
    )


def check_affordability(
    remaining_budget,
    purchase_amount,
    days_remaining
):
    """Check whether a purchase fits the budget."""

    remaining_after = (
        remaining_budget
        - purchase_amount
    )

    affordable = (
        remaining_after >= 0
    )

    if affordable:

        daily_after = (
            calculate_daily_allowance(
                remaining_after,
                days_remaining
            )
        )

    else:

        daily_after = 0

    return (
        affordable,
        remaining_after,
        daily_after
    )