const EthContract = artifacts.require("EthContract");

/*
 * uncomment accounts to access the test accounts made available by the
 * Ethereum client
 * See docs: https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript
 */
contract("EthContract", accounts => {
  it("should assert true",  () => {
    EthContract.deployed()
    .then(function(contract){
      contract.getmsg.call();
    }).then(function(result){
        assert.equal(result == "hello! This is a smart contract");   
    });
  });
});
