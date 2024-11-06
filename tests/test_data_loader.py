# tests/test_data_loader.py

import unittest
from unittest.mock import patch, mock_open
from utils.data_loader import load_all_heroes, load_heroes_data
from pathlib import Path

class TestDataLoader(unittest.TestCase):

    @patch('utils.data_loader.Path.iterdir')
    def test_load_all_heroes(self, mock_iterdir):
        # Налаштування моків
        class_dir = Path('data/heroes/Assassin')
        hero_dir = Path('data/heroes/Assassin/Aamon')
        mock_iterdir.return_value = [class_dir]

        with patch.object(class_dir, 'iterdir', return_value=[hero_dir]):
            with patch.object(hero_dir, 'glob', return_value=[Path('data/heroes/Assassin/Aamon/Aamon.json')]):
                heroes = load_all_heroes()
                self.assertIn('Assassin', heroes)
                self.assertIn('Aamon', heroes['Assassin'])

    @patch('utils.data_loader.Path.iterdir')
    @patch('builtins.open', new_callable=mock_open, read_data='{"name": "Aamon", "class": "Assassin"}')
    def test_load_heroes_data(self, mock_file, mock_iterdir):
        # Налаштування моків
        class_dir = Path('data/heroes/Assassin')
        hero_dir = Path('data/heroes/Assassin/Aamon')
        mock_iterdir.return_value = [class_dir]

        with patch.object(class_dir, 'iterdir', return_value=[hero_dir]):
            with patch.object(hero_dir, 'glob', return_value=[Path('data/heroes/Assassin/Aamon/Aamon.json')]):
                heroes_data = load_heroes_data()
                self.assertIn('Aamon', heroes_data)
                self.assertEqual(heroes_data['Aamon']['name'], 'Aamon')
                self.assertEqual(heroes_data['Aamon']['class'], 'Assassin')

if __name__ == '__main__':
    unittest.main()
  
