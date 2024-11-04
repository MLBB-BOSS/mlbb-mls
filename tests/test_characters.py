# tests/test_characters.py
import unittest
import asyncio
from handlers.characters import get_hero_info

class TestCharacters(unittest.TestCase):
    def test_get_hero_info_valid(self):
        hero_name = "Aldous"
        result = asyncio.run(get_hero_info(hero_name))
        self.assertIn("<b>Aldous</b>", result)

    def test_get_hero_info_invalid(self):
        hero_name = "UnknownHero"
        result = asyncio.run(get_hero_info(hero_name))
        self.assertEqual(result, "Інформація про героя недоступна.")

if __name__ == '__main__':
    unittest.main()
