// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract NewContract {
  uint x = 4;
  uint y = 2;
  constructor() public {
  }
  
  function getnumber(uint _x, uint _y) public {
        x = _x;
        y = _y;
  }

  function getexp() public view returns (uint){
    return x**y;
  }
}
