import socket
import threading
import tkinter as tk

class tic_tac_toe():
    def __init__(self):
        self.board = [["", "", ""],["","",""],["","",""]]
        self.turn = "X"
        self.opponent = "O"
        self.you = "X"
        self.winner = None
        self.game_over = False
        self.counter = 0
        self.move_row, self.move_col = 1,1
    def returner(self, row, col):
        self.move_row = row
        self.move_col = col
        self.win.destroy()
    def tkin(self):
        self.win = tk.Tk()
        self.win.title("Tic Tac Toe")
        self.win.geometry("600x600")
        self.button00 = tk.Button(self.win, text=f"{self.board[0][0]}", command=lambda: self.returner(0,0), width=20,height= 10, font=("Arial, 12"))
        self.button00.grid(row=0, column=0)
        self.button01 = tk.Button(self.win, text=f"{self.board[0][1]}", command=lambda: self.returner(0,1), width=20,height= 10, font=("Arial, 12"))
        self.button01.grid(row=0, column=1)
        self.button02 = tk.Button(self.win, text=f"{self.board[0][2]}", command=lambda: self.returner(0,2), width=20,height= 10, font=("Arial, 12"))
        self.button02.grid(row=0, column=2)
        self.button10 = tk.Button(self.win, text=f"{self.board[1][0]}", command=lambda: self.returner(1,0), width=20,height= 10, font=("Arial, 12"))
        self.button10.grid(row=1, column=0)
        self.button11 = tk.Button(self.win, text=f"{self.board[1][1]}", command=lambda: self.returner(1,1), width=20,height= 10, font=("Arial, 12"))
        self.button11.grid(row=1, column=1)
        self.button12 = tk.Button(self.win, text=f"{self.board[1][2]}", command=lambda: self.returner(1,2), width=20,height= 10, font=("Arial, 12"))
        self.button12.grid(row=1, column=2)
        self.button20 = tk.Button(self.win, text=f"{self.board[2][0]}", command=lambda: self.returner(2,0), width=20,height= 10, font=("Arial, 12"))
        self.button20.grid(row=2, column=0)
        self.button21 = tk.Button(self.win, text=f"{self.board[2][1]}", command=lambda: self.returner(2,1), width=20,height= 10, font=("Arial, 12"))
        self.button21.grid(row=2, column=1)
        self.button22 = tk.Button(self.win, text=f"{self.board[2][2]}", command=lambda: self.returner(2,2), width=20,height= 10, font=("Arial, 12"))
        self.button22.grid(row=2, column=2)
        self.win.mainloop()
    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client , addr = server.accept()
        threading.Thread(target=self.connection, args=(client, )).start()
        server.close()
    def connect(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.you= "O"
        self.opponent = "X"
        threading.Thread(target=self.connection, args=(client,)).start()
    

    def connection(self, client):
        while not self.game_over:
            if self.turn == self.you:
                self.tkin()
                move = f"{self.move_row},{self.move_col}"
                if self.check_validity(move.split(",")):
                    client.send(move.encode("utf-8"))
                    self.apply_move(move.split(","), self.you)
                    self.turn = self.opponent
                else:
                    print("Invalid Move!")
            else:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    print("Wait for opponent's turn")
                    self.apply_move(data.decode("utf-8").split(","), self.opponent)
                    self.turn = self.you
            print("\n")
        client.close()
    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter +=1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.winner_check():
            if self.winner == self.you:
                print("You won!")
                exit()
            elif self.winner == self.opponent:
                print("You lose! Boomer")
                exit()
        elif self.counter == 9:
            print("Its a tie boomers")
            exit()
    def check_validity(self, move):
        if (int(move[0]) < 3 and int(move[1]) <3) and (int(move[0]) >-1 and int(move[1]) >-1):
            return self.board[int(move[0])][int(move[1])] == ""
        else:
            return False
    def winner_check(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] ==self.board[row][2]!="":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for column in range(3):
            if self.board[0][column] == self.board[1][column] ==self.board[2][column]!="":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        return False
    def print_board(self):
        for col in range(3):
            print(" | ".join(self.board[col]))
            if col !=2:
                print("---------")
game = tic_tac_toe()
game.connect("localhost", 9999)