import sys 
import os
sys.path.append(os.path.abspath("E:\\Infosec\\JComp\\Blockchain Creation and Testing\\1. Eth-tester API"))
import ethAPIexecution as eth
import pytest
import warnings


#tests
class TestClass:
    # 1. Successful transact
    def test_one(self):
        assert eth.transact(2,3) == "Successful transaction!"

    # 2. One Unsuccessful transact
    def test_two(self):
        msg = eth.transact(2,3)
        assert eth.transact(2,4) == "Balance is too low!!"

    # 3. IndexError
    def test_three(self):
        with pytest.raises(IndexError):
            eth.transact(12,3)

    # 4. Warning
    def test_four(self):
        with pytest.warns(UserWarning):
            eth.transact(1,4)



