# Workshop-Energy-Cost-Estimator
A command-line tool that calculates workshop electricity costs per machine using tariff, power, and runtime inputs, highlighting peak expenses and potential savings.

# Workshop Energy Cost Calculator

A command-line tool that helps a workshop owner or student see how much each
machine contributes to the electricity bill. Enter the electricity tariff,
working days per month, and each machine's power and daily operating hours. The
calculator reports daily and monthly energy use, monthly cost, the most
expensive machine, and a possible saving from reducing its use.

## Run

Use Python 3.10 or later:

```text
python energy_calculator.py
```

Enter the tariff in your local currency per kWh. The calculator uses the same
currency for the displayed costs.

## Example

For a tariff of `0.30` per kWh and 22 working days, a 1,500 W table saw used
for 6 hours each working day consumes 9 kWh per day and 198 kWh per month.

```text
Monthly energy and cost
Machine               Power (W)  Hours/day   Daily kWh   Monthly kWh   Monthly cost
----------------------------------------------------------------------------------
Table saw                1500.0        6.0        9.00        198.00          59.40
----------------------------------------------------------------------------------
TOTAL                                            9.00        198.00          59.40

Most expensive machine: Table saw (59.40 per month).
It accounts for 100.0% of the total monthly bill.
Warning: Table saw accounts for more than half of the bill. Review its usage for savings.
Running it one hour less per working day could save 9.90 per month.
```

## Input checks and calculation

The program re-prompts for non-numeric entries and values outside the allowed
ranges. Electricity tariff, machine power, and daily operating hours must be
positive; daily machine hours may not exceed 24; and working days must be from
1 to 31. Zero, negative, and non-numeric entries are rejected where they are
not allowed.

- Daily energy (kWh) = power (W) / 1,000 × hours per working day
- Monthly energy (kWh) = daily energy × working days per month
- Monthly cost = monthly energy × tariff per kWh
- One-hour monthly saving = power (kW) × tariff × working days

The one-hour saving is shown only when the most expensive machine runs at least
one hour per working day. It assumes the machine is used one fewer hour on each
working day.

The calculator reports the most expensive machine's percentage of the total
monthly bill. It warns when that share is over 50%, suggests reviewing usage
when it is over 25%, and reassures the user when no machine exceeds 25%.

## Test

```text
python -m unittest
```

## Possible next steps

- Save estimates to a file.
- Support separate peak and off-peak tariffs.
- Add a chart comparing machine costs.
