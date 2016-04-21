from one_time_pad import *
import unittest

class TestBreakHelperMethods(unittest.TestCase):
    def setUp(self):
        print "="*10 + self._testMethodName
        self.ops = MyOperations()
        VARIABLES = {}
        
    def test_decode_params(self):
        VARIABLES["a"] = "234"
        p = decode_params(["123", "123"])
        self.assertEqual(["123", "123"], p)
        
    def test_decode_params_one_var(self):
        VARIABLES["a"] = "234"
        p = decode_params(["123", "a"])
        self.assertEqual(["123", "234"], p)
        
    def test_decode_params_all_var(self):
        VARIABLES["a"] = "234"
        p = decode_params(["a", "a"])
        self.assertEqual(["234", "234"], p)
        
    def test_decode_params_all_var_no_replace(self):
        VARIABLES["a"] = "234"
        p = decode_params(["*a", "a"])
        self.assertEqual(["a", "234"], p)

    def test_unpack_expected_params(self):
        params_err, s = unpack_expected_params(["a", "a"], 2)
        self.assertEqual("", params_err)
        self.assertEqual(["a", "a"], s)
        
    def test_unpack_expected_params_0(self):
        params_err, s = unpack_expected_params([], 0)
        self.assertEqual("", params_err)
        self.assertEqual([], s)
        
    def test_unpack_expected_params_err_more_than_expected(self):
        params_err, s = unpack_expected_params(["a", "a"], 3)
        self.assertEqual("Bad params: 3 expected, 2 received", params_err)
        self.assertEqual([0,1,2], s)
        
    def test_unpack_expected_params_err_less_than_expected(self):
        params_err, s = unpack_expected_params(["a"], 2)
        self.assertEqual("Bad params: 2 expected, 1 received", params_err)
        self.assertEqual([0,1], s)
        
    def test_separate_operation_params_no_params(self):
        op,p = separate_operation_params("op")
        self.assertEqual("op", op)
        self.assertEqual([], p)

    def test_separate_operation_params_one_param(self):
        op,p = separate_operation_params("op(1)")
        self.assertEqual("op", op)
        self.assertEqual(["1"], p)
        
    def test_separate_operation_params_two_params(self):
        op,p = separate_operation_params("op(1,2)")
        self.assertEqual("op", op)
        self.assertEqual(["1","2"], p)
        
    def test_parse_operation_help(self):
        self.assertFalse("Bad operation" in parse_operation("help"))
        self.assertFalse("Bad operation" in parse_operation("help()"))
        
    def test_parse_operation_exit(self):
        self.assertFalse("Bad operation" in parse_operation("exit"))
        self.assertFalse("Bad operation" in parse_operation("exit()"))
        
    def test_parse_operation_store(self):
        self.assertEqual("VARIABLES[a] = 2", parse_operation("store(*a,2)"))
        self.assertEqual("2", VARIABLES["a"])
        
    def test_parse_operation_hex(self):
        hex_value = "7061756c"
        simple_value = "paul"
        self.assertEqual(hex_value, parse_operation("to_hex(" + simple_value + ")"))
        self.assertEqual(simple_value, parse_operation("from_hex(" + hex_value + ")"))

        
if __name__ == '__main__':
    unittest.main()