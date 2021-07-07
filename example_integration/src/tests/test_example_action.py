from src.example_action import ExampleAction
import unittest


class TestExampleAction(unittest.TestCase):
    def test_get_domain_report(self):
        api_key = "1234"
        sample_input = "abcd"
        action = ExampleAction({"conf": {"api_key": api_key}})
        result = action.run(sample_input)
        self.assertTrue(result)
        self.assertEqual(result.get("sample_output"), sample_input)
        self.assertEqual(result.get("api_key"), api_key)
