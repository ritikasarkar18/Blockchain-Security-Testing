#EthereumTester is the sole API entrypoint
from eth_tester import EthereumTester
import warnings

warnings.filterwarnings("ignore")


# working of the eth_tester API
def example_demo(t):
    t = EthereumTester()
    print("___The list of accounts known to the Ethereum tester are___")
    acct = t.get_accounts()
    for num,i in enumerate(acct):
        print(num,"->",i)

    #Add a new account for a given private key, the private key must be 32 bytes long
    print("\n__Add an account given a private key___")
    print("The Hex address of the added account is ",t.add_account('0x58d23b55bc9cdce1f18c2500f40ff4ab7245df9a89505e9b1fa4851f623d241d'))

    #Get the balance in wei for an account
    print("\n____Balance details____")
    print("a. Account[0] = ",acct[0])
    print("b. Balance = ",t.get_balance(acct[0])/1000000000000000000," Ether")

    #Send the provided transaction object, returning a unique transaction_hash
    hash1 = t.send_transaction({"from" : acct[0], "to" : acct[1], "gas":21000})
    print("\n___The unique hash for transaction between Account 0 and 1 = ",hash1)

    #Returns the transaction for a given hash, returns a Trnasaction not found exception if not found
    tran_details = t.get_transaction_by_hash(hash1)
    print("\n______Transaction details of the given hash______")
    for k,v in tran_details.items():
        print("->",k,"=",v)

    #Manual mining
    mined = t.mine_blocks(num_blocks = 2)
    print("\n___Newly mined blocks___")
    for i,j in enumerate(mined):
        print(i,"->",j)



# Here the a transaction will be sent from one account to another,
# but if the balance is too low, it will be unsuccessful
# may raise error
def transact(acc_no1, acc_no2):
    t1 = EthereumTester()
    accs = t1.get_accounts()
    msg = ""
    #try:
    bal1 = t1.get_balance(accs[acc_no1])/1000000000000000000
    if (bal1>=10000.0): #minimum balance
        t_obj = {"from" : accs[acc_no1], "to" : accs[acc_no1], "gas" : 22000, "gas_price" : 3}
        hash1 = t1.send_transaction(t_obj)
        rec = t1.get_transaction_receipt(hash1)
        msg = "Successful transaction!"
        #print("Estimated gas usage was ",t1.estimate_gas(t_obj))
        print("The block number is ",rec['block_number'])
    else:
        msg = "Balance is too low!!"

    return msg

    #except Exception as e:
     #   print("The following Exception object was thrown = ",e.args)

        
        


if __name__=="__main__":
    
    #creating an object of EthereumTester class
    t = EthereumTester()

    #no backend has been set in the constructor
    # uses Mock backend, has limited functionality. It cannot perform any VM computations. It mocks out all of the objects and interactions.
    example_demo(t)
    print(transact(2,3))

