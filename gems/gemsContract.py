from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/nFzmfPoiMWnPgTBNZWU9JGmkWSAeoVIt'))



def get_gem_contract():
    json_data = open('gems/files/gem_contract.json').read()   
    contractABI = json.loads(json_data)
    contractAddress = Web3.toChecksumAddress("0x0b5ddeff4d54c1b1ee635657c17cf54135e5db30")
    gem_contract = w3.eth.contract(address=contractAddress, abi=contractABI["abi"])
    return(gem_contract)