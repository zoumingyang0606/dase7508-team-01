import csv
import math
from pathlib import Path
import unittest

from src.core import metrics


class PairedMetricTests(unittest.TestCase):
    def test_original_misses_do_not_count_as_bypasses(self):
        result = metrics(["spam", "spam", "spam"], ["ham", "ham", "spam"],
                         ["spam", "ham", "spam"])
        self.assertEqual(result["newly_bypassed_spam"], 1)
        self.assertEqual(result["initially_blocked_spam"], 2)
        self.assertEqual(result["conditional_asr"], 0.5)
        self.assertAlmostEqual(result["overall_miss_rate"], 2 / 3)

    def test_empty_conditional_denominator(self):
        result = metrics(["spam", "ham"], ["ham", "spam"], ["ham", "spam"])
        self.assertTrue(math.isnan(result["conditional_asr"]))

    def test_recovery_does_not_cancel_new_misses(self):
        result = metrics(["spam", "spam"], ["ham", "spam"], ["spam", "ham"])
        self.assertEqual(result["conditional_asr"], 1.0)

    def test_frozen_aggregate_rates(self):
        path = Path(__file__).resolve().parents[1] / "results" / "pooled_pair_metrics.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row["model"] for row in rows], list("ABC"))
        for row in rows:
            self.assertEqual(int(row["conditions"]), 45)
            self.assertAlmostEqual(float(row["conditional_asr"]),
                                   int(row["newly_bypassed_spam"]) / int(row["initially_blocked_spam"]))
            self.assertAlmostEqual(float(row["variant_miss_rate"]),
                                   int(row["variant_misses"]) / int(row["spam_observations"]))
