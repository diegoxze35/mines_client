import os
import pickle
import sys
import time
from socket import socket, AF_INET, SOCK_STREAM

from pyfiglet import figlet_format

from Difficulty import Difficulty


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    server_ip: str
    server_port: int
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
    except IndexError:
        exit("Usage: python main.py server_ip server_port")
    if server_port < 1024:
        exit('Server port must be at least 1024')
    with socket(AF_INET, SOCK_STREAM) as s:
        s.setblocking(True)
        s.connect((server_ip, server_port))
        title = figlet_format(text='MinesWeeper', font='larry3d', width=90)
        print(title)
        print(f'Welcome to MinesWeeper! at {server_ip}:{server_port}')
        print('Please select difficulty level:')
        print('1 - Easy')
        print('2 - Medium')
        level = input()
        difficulty: Difficulty
        match level.lower():
            case '1' | 'easy':
                difficulty = Difficulty(squares=9, mines=10)
            case '2' | 'medium':
                difficulty = Difficulty(squares=16, mines=40)
        s.send(pickle.dumps(difficulty))
        cls()
        start = time.time()
        while True:
            board = pickle.loads(s.recv(4096))
            if isinstance(board, tuple):
                message = figlet_format(text=board[0], font='slant')
                print(message)
                print(board[1])
                break
            print(board)
            x = int(input("X: "))
            y = int(input("Y: "))
            s.send(pickle.dumps((x, y)))
            cls()
    end = time.time()
    print(f'Time taken: {end - start} seconds')
