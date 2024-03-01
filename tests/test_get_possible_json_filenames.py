import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from get_possible_json_filenames import get_possible_json_filenames

class TestGetPossibleJsonFilenames(unittest.TestCase):
    def test_get_possible_json_filenames(self):
        # Test when filename has a number in parentheses
        filename = "./photos/_MG_1978(1).JPG"
        expected_output = "./photos/_MG_1978.JPG(1).json"
        self.assertIn(expected_output, get_possible_json_filenames(filename))

        # Test when filename does not have a number in parentheses
        filename = "./photos/_MG_1978.JPG"
        expected_output = "./photos/_MG_1978.JPG.json"
        self.assertIn(expected_output, get_possible_json_filenames(filename))
        
        # Test when filename does not have a number in parentheses
        filename = "./photos/image000000(3).jpg"
        expected_output = "./photos/image000000(3).jpg.json"
        self.assertIn(expected_output, get_possible_json_filenames(filename))
        
        # Test when filename is longer than 46 characters
        filename = "./photos/00100lrPORTRAIT_00100_BURST20191119215144544_CO.jpg"
        expected_output = "./photos/00100lrPORTRAIT_00100_BURST20191119215144544_C.json"
        self.assertIn(expected_output, get_possible_json_filenames(filename))
        
        filename = "./photos/tH7opDHO7-vROHgrrh-COg20190306-17138-i6afjk.mp4"
        expected_output = "./photos/tH7opDHO7-vROHgrrh-COg20190306-17138-i6afjk.mp.json"
        self.assertIn(expected_output, get_possible_json_filenames(filename))
        
        # Test when filename has a .heic extension
        filename = "./photos/IMG_2720.heic"
        expected_output = "./photos/IMG_2720.heic.json"
        self.assertIn(expected_output, get_possible_json_filenames(filename))
        
        #Test for edited image files
        filename = "./photos/IMG_2720-edited.JPG"
        expected_output = "./photos/IMG_2720.JPG.json"
        self.assertIn(expected_output, get_possible_json_filenames(filename))

if __name__ == '__main__':
    unittest.main()