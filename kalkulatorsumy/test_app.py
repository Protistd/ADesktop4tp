import unittest
from app import SumApp

class TestSumApp(unittest.TestCase):

    def setUp(self):
        self.app = SumApp()
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()

    def test_correct_sum(self):
        """Test 1: 5 + 10 = 15"""
        self.app.entry1.insert(0, "5")
        self.app.entry2.insert(0, "10")

        self.app.btn.invoke()

        result = self.app.result_label.cget("text")
        self.assertEqual(result, "15.0")

    def test_invalid_input(self):
        """Test 2: 'abc' + 5 -> Błąd danych"""
        self.app.entry1.insert(0, "abc")
        self.app.entry2.insert(0, "5")

        self.app.btn.invoke()

        result = self.app.result_label.cget("text")
        self.assertEqual(result, "Błąd danych")

    def test_empty_fields(self):
        """Test 3: puste pola -> Błąd danych"""
        self.app.btn.invoke()

        result = self.app.result_label.cget("text")
        self.assertEqual(result, "Błąd danych")


if __name__ == "__main__":
    unittest.main()
