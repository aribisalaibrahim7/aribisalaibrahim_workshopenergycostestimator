"""Estimate workshop machine electricity use and cost."""

import math


def get_number(
    prompt: str,
    minimum: float | None = None,
    maximum: float | None = None,
    integer: bool = False,
    exclusive_minimum: bool = False,
) -> float | int:
    """Keep prompting until the user enters a number in the requested range."""
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not math.isfinite(value):
            print("Please enter a finite number.")
            continue
        if integer and not value.is_integer():
            print("Please enter a whole number.")
            continue
        if minimum is not None:
            below_minimum = value <= minimum if exclusive_minimum else value < minimum
            if below_minimum:
                comparison = "greater than" if exclusive_minimum else "greater than or equal to"
                print(f"Please enter a number {comparison} {minimum}.")
                continue
        if maximum is not None and value > maximum:
            print(f"Please enter a number less than or equal to {maximum}.")
            continue

        return int(value) if integer else value


def energy_and_cost(
    power_watts: float,
    hours_per_day: float,
    tariff_per_kwh: float,
    working_days: int,
) -> tuple[float, float, float]:
    """Return daily kWh, monthly kWh, and monthly cost for one machine."""
    daily_kwh = (power_watts / 1000) * hours_per_day
    monthly_kwh = daily_kwh * working_days
    monthly_cost = monthly_kwh * tariff_per_kwh
    return daily_kwh, monthly_kwh, monthly_cost


def main() -> None:
    print("Workshop Energy Cost Calculator")
    tariff = get_number(
        "Electricity tariff per kWh: ", minimum=0, exclusive_minimum=True
    )
    working_days = get_number(
        "Working days per month (1-31): ", minimum=1, maximum=31, integer=True
    )
    machine_count = get_number("Number of machines: ", minimum=1, integer=True)

    names: list[str] = []
    powers_watts: list[float] = []
    hours_per_day: list[float] = []

    for index in range(machine_count):
        print(f"\nMachine {index + 1}")
        while True:
            name = input("Machine name: ").strip()
            if name:
                break
            print("Machine name cannot be blank.")

        names.append(name)
        powers_watts.append(get_number("Power in watts: ", minimum=0.01))
        hours_per_day.append(
            get_number(
                "Hours used per working day (greater than 0, up to 24): ",
                0,
                24,
                exclusive_minimum=True,
            )
        )

    results = [
        energy_and_cost(power, hours, tariff, working_days)
        for power, hours in zip(powers_watts, hours_per_day)
    ]

    print("\nMonthly energy and cost")
    print(
        f"{'Machine':<20} {'Power (W)':>10} {'Hours/day':>10} "
        f"{'Daily kWh':>11} {'Monthly kWh':>13} {'Monthly cost':>14}"
    )
    print("-" * 82)

    for name, power, hours, (daily_kwh, monthly_kwh, monthly_cost) in zip(
        names, powers_watts, hours_per_day, results
    ):
        print(
            f"{name:<20.20} {power:>10.1f} {hours:>10.1f} "
            f"{daily_kwh:>11.2f} {monthly_kwh:>13.2f} {monthly_cost:>14.2f}"
        )

    total_daily_kwh = sum(result[0] for result in results)
    total_monthly_kwh = sum(result[1] for result in results)
    total_monthly_cost = sum(result[2] for result in results)
    print("-" * 82)
    print(
        f"{'TOTAL':<20} {'':>10} {'':>10} {total_daily_kwh:>11.2f} "
        f"{total_monthly_kwh:>13.2f} {total_monthly_cost:>14.2f}"
    )

    most_expensive_index = max(
        range(len(results)), key=lambda index: results[index][2]
    )
    most_expensive_name = names[most_expensive_index]
    most_expensive_cost = results[most_expensive_index][2]
    print(f"\nMost expensive machine: {most_expensive_name} ({most_expensive_cost:.2f} per month).")

    bill_share = most_expensive_cost / total_monthly_cost * 100
    print(f"It accounts for {bill_share:.1f}% of the total monthly bill.")
    if bill_share > 50:
        print(
            f"Warning: {most_expensive_name} accounts for more than half "
            "of the bill. Review its usage for savings."
        )
    elif bill_share > 25:
        print(
            f"Note: {most_expensive_name} accounts for more than a quarter "
            "of the bill. Consider reducing its running time."
        )
    else:
        print(
            "Your electricity use is spread across the machines, with no "
            "single machine accounting for more than a quarter of the bill."
        )

    if hours_per_day[most_expensive_index] >= 1:
        saving = (
            powers_watts[most_expensive_index]
            / 1000
            * tariff
            * working_days
        )
        print(
            f"Running it one hour less per working day could save "
            f"{saving:.2f} per month."
        )
    else:
        print(
            "It is already used for less than one hour per working day, "
            "so a one-hour reduction is not possible."
        )


if __name__ == "__main__":
    main()
