import unittest
import random

from main.utils.transformer.PaddingUtils import PaddingUtils

class TestPaddingTestCase(unittest.TestCase):
    
    def test_no_padding(self):
        
        text = "No padding"
        is_padded, padded, pad_octet_count = PaddingUtils.pad_string(text, 10)
        
        self.assertEqual(padded, text.encode())
        self.assertFalse(is_padded)
        self.assertEqual(0, pad_octet_count)
        
    def test_one_octet_padding(self):
        
        text = "One padding"
        is_padded, padded, pad_octet_count = PaddingUtils.pad_string(text, 12)
        padding = 1
        self.assertEqual(padded, (text.encode() + padding.to_bytes(1, 'big')))
        self.assertTrue(is_padded)
        self.assertEqual(1, pad_octet_count)
        
    def test_multi_octet_padding(self):
        
        text = "multi padding"
        is_padded, padded, pad_octet_count = PaddingUtils.pad_string(text, 32)
        padding = 32 - len(text)
        self.assertEqual(padded, (text.encode() + bytearray(padding - 1) + padding.to_bytes()))
        self.assertTrue(is_padded)
        self.assertEqual(padding, pad_octet_count)
        

if(__name__ == '__main__'):
    unittest.main()