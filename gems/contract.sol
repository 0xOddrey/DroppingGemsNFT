// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

import "@openzeppelin/contracts@4.4.2/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.4.2/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@4.4.2/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";


contract DroppingGems is ERC721, ERC721URIStorage, Ownable {
    using SafeMath for uint256;
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    string public baseTokenURI;
    uint256 public constant MAX_TOKENS = 1000;
    address public transferWallet;
    uint256 private mintPrice = 25000000000000000; // 0.025 Ether

    constructor(
        string memory baseURI,
        address _tranferWallet
    ) ERC721("DroppingGems", "GEMS") {
        setBaseURI(baseURI);
        transferWallet = _tranferWallet;
    }

    function setBaseURI(string memory baseURI) public onlyOwner {
        baseTokenURI = baseURI;
    }

    function totalSupply() public view override returns (uint256) {
        return _tokenIdCounter.current();
    }

    function mint(address _to, uint256 _count) external payable  {
        require(_count > 0, "Mint count should be greater than zero");
        uint256 numTokens = _tokenIdCounter.current();
        require(numTokens <= MAX_TOKENS, "Sale ended");
        require(numTokens + _count <= MAX_TOKENS, "Max limit");
        require(msg.value >= mintPrice.mul(_count), "Insufficient funds");

        for (uint256 i = 0; i < _count; i++) {
            _mintOneItem(_to);
        }

    }


    function _mintOneItem(address _to) private {
        _tokenIdCounter.increment();
        uint256 tokenId = _tokenIdCounter.current();
        _safeMint(_to, tokenId);
        _setTokenURI(
        tokenId,
        string(abi.encodePacked(Strings.toString(tokenId), ".json"))
        );
    }


    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function withdrawAll() public payable onlyOwner {
        uint256 balance = address(this).balance;
        require(balance > 0);
        _withdraw(transferWallet, balance);
    }

    function _withdraw(address _address, uint256 _amount) private {
        (bool success, ) = _address.call{ value: _amount }("");
        require(success, "Transfer failed.");
    }

}
