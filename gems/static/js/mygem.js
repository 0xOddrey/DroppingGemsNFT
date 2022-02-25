"use strict";

/**
 * Example JavaScript code that interacts with the page and Web3 wallets
 */

// Unpkg imports

const Web3Modal = window.Web3Modal.default;
const WalletConnectProvider = window.WalletConnectProvider.default;
const Fortmatic = window.Fortmatic;
const evmChains = window.evmChains;
var account = null;
var contract = null;
const CONTRACT_ADDRESS = "0x0B5DdEFf4D54C1B1eE635657C17cF54135e5DB30";

window.userWalletAddress = null 

    
// Web3modal instance
let web3Modal

// Chosen wallet provider given by the dialog window
let provider;


// Address of the selected account
let selectedAccount;


/**
 * Setup the orchestra
 */
function init() {

// Check that the web page is run in a secure context,
// as otherwise MetaMask won't be available
//if(location.protocol !== 'https:') {
    // https://ethereum.stackexchange.com/a/62217/620
    //const alert = document.querySelector("#alert-error-https");
// alert.style.display = "block";
    //document.querySelector("#btn-connect").setAttribute("disabled", "disabled")
//return;
//}

// Tell Web3modal what providers we have available.
// Built-in web browser provider (only one can exist as a time)
// like MetaMask, Brave or Opera is added automatically by Web3modal
const providerOptions = {
    walletconnect: {
    package: WalletConnectProvider,
    options: {
        // Mikko's test key - don't copy as your mileage may vary
        infuraId: "5e150792adde4a1987fd58e73e20bfc4",
        qrcodeModalOptions: {
        mobileLinks: [
            "rainbow",
            "metamask",
            "argent",
            "trust",
            "imtoken",
            "pillar",
        ],
        },
    }
    },

};


web3Modal = new Web3Modal({
    cacheProvider: false, // optional
    providerOptions, // required
    disableInjectedProvider: false, // optional. For MetaMask / Brave / Opera.
});

console.log("Web3Modal instance is", web3Modal);
}

async function loadContract() {
const web3 = new Web3(provider);
const contract = await new web3.eth.Contract([
{
"inputs": [
{
"internalType": "string",
"name": "baseURI",
"type": "string"
},
{
"internalType": "address",
"name": "_tranferWallet",
"type": "address"
}
],
"stateMutability": "nonpayable",
"type": "constructor"
},
{
"anonymous": false,
"inputs": [
{
"indexed": true,
"internalType": "address",
"name": "owner",
"type": "address"
},
{
"indexed": true,
"internalType": "address",
"name": "approved",
"type": "address"
},
{
"indexed": true,
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "Approval",
"type": "event"
},
{
"anonymous": false,
"inputs": [
{
"indexed": true,
"internalType": "address",
"name": "owner",
"type": "address"
},
{
"indexed": true,
"internalType": "address",
"name": "operator",
"type": "address"
},
{
"indexed": false,
"internalType": "bool",
"name": "approved",
"type": "bool"
}
],
"name": "ApprovalForAll",
"type": "event"
},
{
"anonymous": false,
"inputs": [
{
"indexed": true,
"internalType": "uint256",
"name": "id",
"type": "uint256"
}
],
"name": "GemDropped",
"type": "event"
},
{
"anonymous": false,
"inputs": [
{
"indexed": true,
"internalType": "address",
"name": "previousOwner",
"type": "address"
},
{
"indexed": true,
"internalType": "address",
"name": "newOwner",
"type": "address"
}
],
"name": "OwnershipTransferred",
"type": "event"
},
{
"anonymous": false,
"inputs": [
{
"indexed": true,
"internalType": "address",
"name": "from",
"type": "address"
},
{
"indexed": true,
"internalType": "address",
"name": "to",
"type": "address"
},
{
"indexed": true,
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "Transfer",
"type": "event"
},
{
"inputs": [],
"name": "MAX_TOKENS",
"outputs": [
{
"internalType": "uint256",
"name": "",
"type": "uint256"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "to",
"type": "address"
},
{
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "approve",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "owner",
"type": "address"
}
],
"name": "balanceOf",
"outputs": [
{
"internalType": "uint256",
"name": "",
"type": "uint256"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [],
"name": "baseTokenURI",
"outputs": [
{
"internalType": "string",
"name": "",
"type": "string"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "getApproved",
"outputs": [
{
"internalType": "address",
"name": "",
"type": "address"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "owner",
"type": "address"
},
{
"internalType": "address",
"name": "operator",
"type": "address"
}
],
"name": "isApprovedForAll",
"outputs": [
{
"internalType": "bool",
"name": "",
"type": "bool"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "_to",
"type": "address"
},
{
"internalType": "uint256",
"name": "_count",
"type": "uint256"
}
],
"name": "mint",
"outputs": [],
"stateMutability": "payable",
"type": "function"
},
{
"inputs": [],
"name": "name",
"outputs": [
{
"internalType": "string",
"name": "",
"type": "string"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [],
"name": "owner",
"outputs": [
{
"internalType": "address",
"name": "",
"type": "address"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "_to",
"type": "address"
},
{
"internalType": "uint256",
"name": "_count",
"type": "uint256"
}
],
"name": "ownerMintTransfer",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "ownerOf",
"outputs": [
{
"internalType": "address",
"name": "",
"type": "address"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [],
"name": "renounceOwnership",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "from",
"type": "address"
},
{
"internalType": "address",
"name": "to",
"type": "address"
},
{
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "safeTransferFrom",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "from",
"type": "address"
},
{
"internalType": "address",
"name": "to",
"type": "address"
},
{
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
},
{
"internalType": "bytes",
"name": "_data",
"type": "bytes"
}
],
"name": "safeTransferFrom",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "operator",
"type": "address"
},
{
"internalType": "bool",
"name": "approved",
"type": "bool"
}
],
"name": "setApprovalForAll",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "string",
"name": "baseURI",
"type": "string"
}
],
"name": "setBaseURI",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "_tranferWallet",
"type": "address"
}
],
"name": "setTransferWallet",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "bytes4",
"name": "interfaceId",
"type": "bytes4"
}
],
"name": "supportsInterface",
"outputs": [
{
"internalType": "bool",
"name": "",
"type": "bool"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [],
"name": "symbol",
"outputs": [
{
"internalType": "string",
"name": "",
"type": "string"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "tokenURI",
"outputs": [
{
"internalType": "string",
"name": "",
"type": "string"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "_owner",
"type": "address"
}
],
"name": "tokensOfOwner",
"outputs": [
{
"internalType": "uint256[]",
"name": "ownerTokens",
"type": "uint256[]"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [],
"name": "totalSupply",
"outputs": [
{
"internalType": "uint256",
"name": "",
"type": "uint256"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "from",
"type": "address"
},
{
"internalType": "address",
"name": "to",
"type": "address"
},
{
"internalType": "uint256",
"name": "tokenId",
"type": "uint256"
}
],
"name": "transferFrom",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "address",
"name": "newOwner",
"type": "address"
}
],
"name": "transferOwnership",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [],
"name": "transferWallet",
"outputs": [
{
"internalType": "address",
"name": "",
"type": "address"
}
],
"stateMutability": "view",
"type": "function"
},
{
"inputs": [],
"name": "withdrawAll",
"outputs": [],
"stateMutability": "payable",
"type": "function"
}
], '0x0B5DdEFf4D54C1B1eE635657C17cF54135e5DB30');

console.log(contract)
return contract
}

/**
* Kick in the UI action after Web3modal dialog has chosen a provider
*/
async function fetchAccountData() {

// Get a Web3 instance for the wallet
const web3 = new Web3(provider);

console.log("Web3 instance is", web3);

// Get connected chain id from Ethereum node
const chainId = await web3.eth.getChainId();
// Load chain information over an HTTP API
const chainData = evmChains.getChain(chainId);

// Get list of accounts of the connected wallet
const accounts = await web3.eth.getAccounts();

window.contract = await loadContract();
// MetaMask does not give you all accounts, only the selected account
console.log("Got accounts", accounts);
selectedAccount = accounts[0];
if (!selectedAccount) { return }
    if (chainId == 1) {
        window.userWalletAddress = accounts[0]
        window.userWalletAddress = accounts[0]
        if (window.userWalletAddress) {
        const wallet_addy = "{{ wallet_addy|safe }}"
        const twitterId = "{{ twitterId|safe }}"
        const twitterRef = "{{twitterRef|safe}}"
            if (wallet_addy === "none") { 
                var url = "/my-gems/" + window.userWalletAddress + "/" + twitterId + "/" + twitterRef
                window.location.replace(url);
            }
        }
    } else {
        alert("Please, Switch to Ethereum");
    }
    
// Because rendering account does its own RPC commucation
// with Ethereum node, we do not want to display any results
// until data for all accounts is loaded
}



async function refreshAccountData() {

await fetchAccountData(provider);
}

/**
* Connect wallet button pressed.
*/
async function onConnect() {

console.log("Opening a dialog", web3Modal);
console.log("Opening a dialog", web3Modal);
try {
    provider = await web3Modal.connect();
} catch(e) {
    console.log("Could not get a wallet connection", e);
    return;
}

// Subscribe to accounts change
provider.on("accountsChanged", (accounts) => {
    fetchAccountData();
});

// Subscribe to chainId change
provider.on("chainChanged", (chainId) => {
    fetchAccountData();
});

// Subscribe to networkId change
provider.on("networkChanged", (networkId) => {
    fetchAccountData();
});

await refreshAccountData();
document.querySelector("#view-gems").style.display = "block";

}


async function onDisconnect() {

console.log("Killing the wallet connection", provider);

// TODO: Which providers have close method?
if(provider.close) {
    await provider.close();

    // If the cached provider is not cleared,
    // WalletConnect will default to the existing session
    // and does not allow to re-scan the QR code with a new wallet.
    // Depending on your use case you may want or want not his behavir.
    await web3Modal.clearCachedProvider();
    provider = null;
}

selectedAccount = null;


}