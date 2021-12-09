// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract EthContract {
  
  string message = "hello! This is a smart contract";

  constructor() public {
  }

  function getmsg() public view returns (string memory){
    return message;
  }
}
