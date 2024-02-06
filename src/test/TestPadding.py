import unittest
import random

from main.utils.transformer.PaddingUtils import PaddingUtils

class TestPaddingTestCase(unittest.TestCase):
    
    def test_no_padding(self):
        
        print("### Test no padding ###")
        text = "No padding"
        is_padded, padded, pad_octet_count = PaddingUtils.pad_string(text, 10)
        
        self.assertEqual(padded, text.encode())
        self.assertFalse(is_padded)
        self.assertEqual(0, pad_octet_count)
        print("OK")
        
    def test_one_octet_padding(self):
        
        print("### Test 1o padding ###")
        text = "One padding"
        is_padded, padded, pad_octet_count = PaddingUtils.pad_string(text, 12)
        padding = 1
        self.assertEqual(padded, (text.encode() + padding.to_bytes()))
        self.assertTrue(is_padded)
        self.assertEqual(1, pad_octet_count)
        print("OK")
        
    def test_multi_octet_padding(self):
        
        print("### Test multi padding ###")
        text = "multi padding"
        is_padded, padded, pad_octet_count = PaddingUtils.pad_string(text, 32)
        padding = 32 - len(text)
        self.assertEqual(padded, (text.encode() + bytearray(padding - 1) + padding.to_bytes()))
        self.assertTrue(is_padded)
        self.assertEqual(padding, pad_octet_count)
        print("OK")
        

if(__name__ == '__main__'):
    unittest.main()