import unittest
from brave_filter.processor import rewrite_host_rule, validate_rule, process_rules

class ProcessorTests(unittest.TestCase):
    def test_rewrite_host_rule(self):
        line = "0.0.0.0 example.com"
        self.assertEqual(rewrite_host_rule(line), "||example.com^")

    def test_validate_rule(self):
        self.assertFalse(validate_rule(""))
        self.assertFalse(validate_rule("# comment"))
        self.assertTrue(validate_rule("||ads.example.com^"))

    def test_process_rules(self):
        lines = [
            "0.0.0.0 example.com",
            "||ads.example.com^",
            "# ignored"
        ]
        result = process_rules(lines)
        self.assertIn("||example.com^", result)
        self.assertIn("||ads.example.com^", result)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
