# -*- coding: utf-8 -*-
from web3 import Web3
from ethereum_input_decoder import ContractAbi
from eth_account import Account
from eth_account.messages import encode_defunct
import time, json, requests, datetime, logging, threading


def log_info(*msg, with_logging=True):
    print(datetime.datetime.now().strftime("%H:%M:%S"), "|", *msg)
    if with_logging:
        logging.info('{} | {}'.format(datetime.datetime.now().strftime("%H:%M:%S"), *msg))

def log_error(*msg, with_logging=True):
    print(datetime.datetime.now().strftime("%H:%M:%S"), "|", *msg)
    if with_logging:
        logging.error('{} | {}'.format(datetime.datetime.now().strftime("%H:%M:%S"), *msg))


class GameFiBuy(threading.Thread):
    def __init__(self, captcha_key, account, activation_timestamp, sitekey="d3e990d8-fd9f-4cd7-b7de-850dc0c4f77a") -> None:
        super().__init__()
        self.captcha_key = captcha_key
        self.account = account
        self.activation_timestamp = activation_timestamp
        self.sitekey = sitekey
        self.contraсt = self.account["account_params"]["contrant"]
        self.token = self.account["account_params"]["token"]
        self.private_key = self.account["account_params"]["private_key"]
        self.chainId = self.account["account_params"]["chainId"]
        self.url = "https://hub.gamefi.org"
        self.rpc = self.account["account_params"]["rpc"]
        self.gas = self.account["account_params"]["gas"]
        self.id = self.account["account_params"]["id"]

        self.abi_check = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]')
        self.abi_apr = json.loads('[{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
        self.abi_main = json.loads('[{"inputs":[{"internalType":"address","name":"_beneficiary","type":"address"},{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_candidate","type":"address"},{"internalType":"uint256","name":"_maxAmount","type":"uint256"},{"internalType":"uint256","name":"_minAmount","type":"uint256"},{"internalType":"bytes","name":"_signature","type":"bytes"}],"name":"buyTokenByTokenWithPermission","outputs":[],"stateMutability":"nonpayable","type":"function"}]')


    def solve_v3(self):
        s = requests.Session()
        data_post = {
            "clientKey": self.captcha_key,
            "task":
                {
                    "type": "HCaptchaTaskProxyless",
                    "websiteURL": self.url,
                    "websiteKey": self.sitekey
                }
        }
        captcha_id = s.post("https://api.capmonster.cloud/createTask", json=data_post).json()
        data_get = {
            "clientKey": self.API_KEY,
            "taskId": captcha_id['taskId']
        }
        captcha_answer = s.get("https://api.capmonster.cloud/getTaskResult", json=data_get).json()
        while captcha_answer['status'] == "processing":
            time.sleep(0.5)
            result = s.get("https://api.capmonster.cloud/getTaskResult", json=data_get).json()   
        return {"status": True, "captcha": result["code"]}

    def user_info(self):
        web3 = Web3(Web3.HTTPProvider(self.rpc))
        print(web3.isConnected())
        #print(self.private_key)
        acct = Account.from_key(self.private_key)
        account = acct.address
        contractt = web3.eth.contract(address=self.token, abi=self.abi_check)
        amount = contractt.functions.balanceOf(account).call()
        name = contractt.functions.name().call({'chainId':self.chainId})
        balance = web3.fromWei(amount, 'ether')
        num = self.account['tag']

        log_info(f'[INFO] | Аккаунт№{num}: {account} | Баланс: {balance} {name} |')

        contracttt = web3.eth.contract(address=self.token, abi=self.abi_apr)
        nonce = web3.eth.get_transaction_count(account)

        token_tx = contracttt.functions.approve(self.contraсt, 99999999999999999999999999999999999999999999).buildTransaction({
            'chainId':self.chainId, 'gas': 300000,'gasPrice': web3.toWei(self.gas,'gwei'), 'nonce':nonce
        })

        signed_txn = web3.eth.account.sign_transaction(token_tx, private_key=self.private_key)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        Tx = web3.toHex(tx_token)
        log_info(f'[INFO] Approve | Аккаунт№{num}": {account} |", "TX", {Tx} |')

    def Buy(self, captcha_code):
        web3 = Web3(Web3.HTTPProvider(self.rpc))
        print(web3.isConnected())
        msg = "GameFi User Signature"
        message = encode_defunct(text=msg)
        acct = Account.from_key(self.private_key)
        account = acct.address

        signed_message =  web3.eth.account.sign_message(message, private_key=self.private_key)
        a = signed_message['signature']
        signature = web3.toHex(a)
        #print(signed_message)

        header = {
            "clienttype": "web",
            "content-type": "application/json",
            "cookie": "_ga=GA1.1.272241580.1636727295; _ga_747PVNBV6B=GS1.1.1640099004.15.1.1640099005.0; adonis-session=c713c364016dfd98dec57ccb121837d5XrKXKVlsehp6qmBC7fAyoONASEsfCBG4lXWKlKwI%2BuffLraAiDWqXj2PuLGfHsnvkIUibyAwC21Rlgx7fDnSbIb2KaSHMt3UBHjHjaU9p%2F%2BED84TTIJbBpzhj%2ByLlRQT; XSRF-TOKEN=dda34b4e0c9c6e719d40fcc9fbbdbd6fXry2vNuoE8APVrT6LTIQliFoNm%2B9edo9BgRkTfKNyj8n0fQQgeSkICSxOVme6h12jOH6M0djsA4CJJ3XFjYEiecglQuKmHrIeA0RvLyuipHsWR42fbAly969rvUBz04a; adonis-session-values=a18b43388e7c14bbc12fda0f584ce9a9BScYhLE9xz3bUi3CFquPwI2%2Bbkf%2BWGPasRBhqwEAdmVJdCAs29hJQ%2FOZty1xd%2FwpISXIFKKhsK%2FB6fAvkZ%2BfwjyIiY05N6fwelTnwT5bgWoV5Dy73NU8jyUPgx7rkIvyYencyFumwXo%2FNcnHqOjJStSJxJqeCm4ea96HUGp9%2FOA%3D",
            "msgsignature": "GameFi User Signature",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
        }

        data = {
            "campaign_id": self.id,
            "signature": signature,
            "wallet_address": account,
            "captcha_token": captcha_code
        }

        client = requests.session()
        rr = client.post("https://hub.gamefi.org/api/v1/user/deposit", headers=header, data=json.dumps(data))

        resp_json = json.loads(rr.text)
        sig = resp_json['data']["signature"]
        buyy = resp_json['data']["max_buy"]
        minn = resp_json['data']["min_buy"]
        buy = int(buyy)
        
        contract = web3.eth.contract(address=self.contraсt, abi=self.abi_main)
        nonce = web3.eth.get_transaction_count(account)

        token_tx = contract.functions.buyTokenByTokenWithPermission(account, self.token, 20000000000000000000, account, buy, minn, sig).buildTransaction({
            'chainId':self.chainId, 'gas': 300000,'gasPrice': web3.toWei(self.Gas,'gwei'), 'nonce':nonce
        })

        signed_txn = web3.eth.account.sign_transaction(token_tx, private_key=self.private_key)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        Tx = web3.toHex(tx_token)
        num = self.account['tag']
        log_info(f'[INFO] Buy |"Аккаунт№{num}: {account}) |", "TX", {Tx} |')
        #print(web3.toHex(tx_token))

    def run(self):
        self.user_info()
        while True:
            if int(time.time()) >= (self.activation_timestamp):
                captcha = self.solve_v3()
                if not captcha["status"]:
                    continue
                else:
                    captcha_code = captcha["captcha"]
                    self.Buy(captcha_code)
    
            else:
                continue