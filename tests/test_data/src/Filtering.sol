pragma solidity ^0.8.0;

interface IMockERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

contract Filtering {
    address owner;
    IMockERC20 token;
    uint256 balance;
    mapping(address => uint256) tokenBalances;

    constructor(address _token) {
        owner = msg.sender;
        token = IMockERC20(_token);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner!");
        _;
    }

    modifier enforceTransferFrom(uint256 amount) {
        _;
        token.transferFrom(msg.sender, address(this), amount);
    }

    function iAmPayable() public payable {
        balance += msg.value;
    }

    function iAmRestricted() public onlyOwner {
        (bool success,) = msg.sender.call{value: balance}("");
        require(success, "Failed transfer");
        balance = 0;
    }

    function depositWithModifier(uint256 amount) public enforceTransferFrom(amount) {
        tokenBalances[msg.sender] += amount;
    }

    function depositNoModifier(uint256 amount) public {
        tokenBalances[msg.sender] += amount;
        token.transferFrom(msg.sender, address(this), amount);
    }

    function withdraw(uint256 amount) public {
        require(tokenBalances[msg.sender] >= amount, "Not enough balance");
        tokenBalances[msg.sender] -= amount;
        token.transfer(msg.sender, amount);
    }
}