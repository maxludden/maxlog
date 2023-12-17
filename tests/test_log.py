# Generated by CodiumAI
import unittest

from maxlog.log import Log



class TestLog(unittest.TestCase):
    # The logger can be initialized with a default log level of 'INFO'.
    def test_default_log_level(self):
        log = Log()
        self.assertEqual(log.rich_level, 20)

    # The logger can be initialized with a custom log level specified as a string.
    def test_custom_log_level_string(self):
        log = Log(rich_level="DEBUG")
        self.assertEqual(log.rich_level, 10)

    # The logger can be initialized with a custom log level specified as an integer.
    def test_custom_log_level_integer(self):
        log = Log(rich_level=30)
        self.assertEqual(log.rich_level, 30)

    # The logger throws a ValueError if an invalid rich_level string is provided.
    def test_invalid_rich_level_string(self):
        with self.assertRaises(ValueError):
            Log(rich_level="INVALID")

    # The logger throws a ValueError if an invalid rich_level integer is provided.
    def test_invalid_rich_level_integer(self):
        with self.assertRaises(ValueError):
            Log(rich_level=60)

    # The logger throws a TypeError if the project_dir argument \
        # is not a string or Path object.
    def test_invalid_project_dir_type(self):
        with self.assertRaises(TypeError):
            Log(project_dir=123) # type: ignore
            