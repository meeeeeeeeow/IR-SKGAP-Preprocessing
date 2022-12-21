import unittest
import test_cases


def test():
    runner = unittest.TextTestRunner()
    suite_all = get_test_suite()
    ret = runner.run(suite_all)
    if not ret.wasSuccessful():
        raise RuntimeError()


def get_test_suite():
    loader = unittest.TestLoader()
    suite_all = unittest.TestSuite()
    suite_all.addTests(loader.loadTestsFromModule(test_cases))
    return suite_all


if __name__ == "__main__":
    test()
