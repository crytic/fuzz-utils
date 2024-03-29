pragma solidity ^0.8.0;

import {ERC20} from "solmate/tokens/ERC20.sol";

contract TestERC20 is ERC20 {
    constructor() ERC20("TestERC20", "TEST", 18) {}
}