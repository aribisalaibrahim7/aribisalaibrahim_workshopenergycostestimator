import unittest
from unittest.mock import patch

from energy_calculator import energy_and_cost, get_number, main


class EnergyAndCostTests(unittest.TestCase):
    def test_energy_and_cost_matches_hand_calculation(self):
        self.assertEqual(energy_and_cost(1500, 6, 0.30, 22), (9.0, 198.0, 59.4))


class GetNumberTests(unittest.TestCase):
    @patch("builtins.input", side_effect=["abc", "-5", "4"])
    @patch("builtins.print")
    def test_reprompts_for_invalid_and_below_minimum_values(self, mock_print, _):
        self.assertEqual(get_number("Value: ", minimum=0), 4.0)
        self.assertEqual(mock_print.call_count, 2)

    @patch("builtins.input", side_effect=["0", "-2", "0.5"])
    @patch("builtins.print")
    def test_positive_value_reprompts_for_zero_and_negative(self, mock_print, _):
        self.assertEqual(
            get_number("Tariff: ", minimum=0, exclusive_minimum=True), 0.5
        )
        self.assertEqual(mock_print.call_count, 2)
        mock_print.assert_called_with("Please enter a number greater than 0.")

    @patch("builtins.input", side_effect=["25", "24"])
    @patch("builtins.print")
    def test_hours_may_be_24_but_not_more(self, mock_print, _):
        self.assertEqual(
            get_number(
                "Hours: ", minimum=0, maximum=24, exclusive_minimum=True
            ),
            24.0,
        )
        mock_print.assert_called_once_with(
            "Please enter a number less than or equal to 24."
        )

    @patch("builtins.input", side_effect=["2.5", "3"])
    @patch("builtins.print")
    def test_integer_input_must_be_whole(self, mock_print, _):
        self.assertEqual(get_number("Count: ", minimum=1, integer=True), 3)
        mock_print.assert_called_once_with("Please enter a whole number.")


class MainTests(unittest.TestCase):
    @patch(
        "builtins.input",
        side_effect=["0.30", "22", "1", "Table saw", "1500", "6"],
    )
    @patch("builtins.print")
    def test_prints_totals_bill_share_warning_and_one_hour_saving(
        self, mock_print, _
    ):
        main()
        output = "\n".join(str(call.args[0]) for call in mock_print.call_args_list)
        self.assertIn("9.00", output)
        self.assertIn("198.00", output)
        self.assertIn("59.40", output)
        self.assertIn("Most expensive machine: Table saw (59.40 per month).", output)
        self.assertIn("It accounts for 100.0% of the total monthly bill.", output)
        self.assertIn("accounts for more than half", output)
        self.assertIn("could save 9.90 per month.", output)

    def test_advice_uses_quarter_and_half_bill_thresholds(self):
        cases = [
            (
                "half",
                ["0.30", "22", "2", "Machine A", "50", "1", "Machine B", "50", "1"],
                "Note: Machine A accounts for more than a quarter",
                "50.0%",
            ),
            (
                "quarter",
                [
                    "0.30", "22", "4",
                    "Machine A", "25", "1",
                    "Machine B", "25", "1",
                    "Machine C", "25", "1",
                    "Machine D", "25", "1",
                ],
                "Your electricity use is spread across the machines",
                "25.0%",
            ),
            (
                "more than half",
                [
                    "0.30", "22", "2",
                    "Machine A", "60", "1",
                    "Machine B", "40", "1",
                ],
                "Warning: Machine A accounts for more than half",
                "60.0%",
            ),
        ]

        for label, inputs, expected_tip, expected_share in cases:
            with self.subTest(label=label), patch(
                "builtins.input", side_effect=inputs
            ), patch("builtins.print") as mock_print:
                main()
                output = "\n".join(
                    str(call.args[0]) for call in mock_print.call_args_list
                )
                self.assertIn(expected_tip, output)
                self.assertIn(expected_share, output)


if __name__ == "__main__":
    unittest.main()
