# tests/test_keyboards.py

import unittest
from unittest.mock import patch
from telegram import ReplyKeyboardMarkup
from utils.keyboards import get_hero_classes_keyboard

class TestKeyboards(unittest.TestCase):

    @patch('utils.keyboards.load_all_heroes')
    def test_get_hero_classes_keyboard(self, mock_load_all_heroes):
        mock_load_all_heroes.return_value = {
            "Assassin": ["Aamon", "Alucard"],
            "Fighter": ["Badang", "Ruby"]
        }

        keyboard = get_hero_classes_keyboard()
        expected_keyboard = ReplyKeyboardMarkup(
            [['Assassin', 'Fighter']],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        self.assertEqual(keyboard.to_dict(), expected_keyboard.to_dict())

if __name__ == '__main__':
    unittest.main()
  
