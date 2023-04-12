import gym
import random
import requests
import numpy as np
import argparse
import sys
import math
from gym_connect_four import ConnectFourEnv

Rows_no = 6
Columns_no = 7
AI = 1
server = -1
DEPTH = 4
Cells = 4

env: ConnectFourEnv = gym.make("ConnectFour-v0")

SERVER_ADDRESS = "https://vilde.cs.lth.se/edap01-4inarow/"
API_KEY = 'nyckel'
STIL_ID = ["ze4126ka-s"] # TODO: fill this list with your stil-id's


def call_server(move):
   res = requests.post(SERVER_ADDRESS + "move",
                       data={
                           "stil_id": STIL_ID,
                           "move": move, # -1 signals the system to start a new game. any running game is counted as a loss
                           "api_key": API_KEY,
                       })
   # For safety some respose checking is done here
   if res.status_code != 200:
      print("Server gave a bad response, error code={}".format(res.status_code))
      exit()
   if not res.json()['status']:
      print("Server returned a bad status. Return message: ")
      print(res.json()['msg'])
      exit()
   return res

def check_stats():
   res = requests.post(SERVER_ADDRESS + "stats",
                       data={
                           "stil_id": STIL_ID,
                           "api_key": API_KEY,
                       })

   stats = res.json()
   return stats

"""
You can make your code work against this simple random agent
before playing against the server.
It returns a move 0-6 or -1 if it could not make a move.
To check your code for better performance, change this code to
use your own algorithm for selecting actions too
"""
def opponents_move(env):
   env.change_player() # change to oppoent
   avmoves = env.available_moves()
   if not avmoves:
      env.change_player() # change back to student before returning
      return -1

   # TODO: Optional? change this to select actions with your policy too
   # that way you get way more interesting games, and you can see if starting
   # is enough to guarrantee a win
   action = random.choice(list(avmoves))

   state, reward, done, _ = env.step(action)
   if done:
      if reward == 1: # reward is always in current players view
         reward = -1
   env.change_player() # change back to student before returning
   return state, reward, done

#Zeyad Kamals Code




def student_move(board):
   col, score = minimax(board, DEPTH, -math.inf, math.inf, True)
   return col

def get_valid_col(board):
   valid_loc = []
   for col in range(Columns_no):
      if (is_valid_col(board, col)):
         valid_loc.append(col)
   return valid_loc

def is_valid_col(board, col):
   return board[0][col] == 0

def play_turn(board, row, col, player):
       board[row][col] = player

def get_valid_row(board, col):
       for row in range(Rows_no-1, -1, -1):
             if board[row][col] == 0:
                   return row
       return  None
  

def player_will_win(board, player):
       for row in range(Rows_no): #Horizontal Win
             for col in range( Columns_no - 3):
                   if board[row][col]  == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                         return True

       for row in range(Rows_no-3): #Vertical Win
             for col in range(Columns_no):
                   if board[row][col]  == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                         return True

       for row in range(Rows_no- 3):  # Negative diaganols Win
             for col in range(Columns_no -3):
                   if board[row][col]  == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                         return True

       for row in range(Rows_no - 3):  # Positive diaganols Win
             for col in range(3, Columns_no):
                   if board[row][col]  == player and board[row+1][col-1] == player and board[row+2][col-2] == player and board[row+3][col-3] == player:
                         return True
       return False

def score_calculator(board, player):
   score = 0

   if len(get_valid_col(board)) == 0:
      return 0
   # Center column
   center_col = [int(i) for i in list(board[:, Columns_no//2])]
   center_count = center_col.count(player)
   score += center_count * 3

   ## Horizontal
   for row in range(Rows_no):
      row_array = [int(i) for i in list(board[row,:])]
      for col in range(Columns_no-3):
         cells = row_array[col:col+4]
         score += evaluate_cells(cells, player)

   ## Vertical
   for col in range(Columns_no):
      col_array = [int(i) for i in list(board[:,col])]
      for row in range(Rows_no-3):
         cells = col_array[row:row+4]
         score += evaluate_cells(cells, player)

   ## posiive diagonal
   for row in range(Rows_no-3):
      for col in range(Columns_no-3):
         cells = [board[row+i][col+i] for i in range(4)]
         score += evaluate_cells(cells, player)

  ## Negative diagonal
   for row in range(Rows_no-3):
      for col in range(Columns_no-3):
         cells = [board[row+3-i][col+i] for i in range(4)]
         score += evaluate_cells(cells, player)

   return score


def evaluate_cells(cells, player):
   score = 0
    
   if player == AI:
      opponent = server 
   else:
      opponent = AI


   if cells.count(player) == 4:
      score = 100000
   elif cells.count(player) == 3 and cells.count(0) == 1:
      score = 1000
   elif cells.count(player) == 2 and cells.count(0) == 2:
      score = 10
   elif cells.count(opponent) == 4:
      score = -100000
   elif cells.count(opponent) == 3 and cells.count(0) == 1:
      score = -1000
   elif cells.count(opponent) == 2 and cells.count(0) == 2:
      score = -10

   return score    

def is_terminal(board):
   return player_will_win(board, server) or player_will_win(board, AI) or len(get_valid_col(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
   valid_loc = get_valid_col(board)
   terminal = is_terminal(board)
   if terminal:
      if player_will_win(board, AI):
         return (None, 10000000)
      elif player_will_win(board, server):
         return (None, -100000000)
      else: 
         return (None, 0)
   elif depth == 0:
      return (None, score_calculator(board, AI))  
   
   if maximizingPlayer:
      value = -math.inf;
      column = random.choice(valid_loc)
      for col in valid_loc:
         row = get_valid_row(board, col)
         copy_board = board.copy()
         play_turn(copy_board, row, col, AI)
         new_score = minimax(copy_board, depth-1, alpha, beta, False)[1]
         if new_score > value:
            value = new_score
            column = col
         alpha = max(alpha, value)
         if alpha >= beta:
            break
      return column, value

   else: #Minimizig Player 
      value = math.inf
      column = random.choice(valid_loc)
      for col in valid_loc:
         row = get_valid_row(board, col)
         copy_board = board.copy()
         play_turn(copy_board, row, col, server)
         new_score = minimax(copy_board, depth-1, alpha, beta, True)[1]
         if new_score < value:
            value = new_score
            column = col
         beta = min(beta, value)
         if alpha >= beta:
            break
      return column, value

   """
   TODO: Implement your min-max alpha-beta pruning algorithm here.
   Give it whatever input arguments you think are necessary
   (and change where it is called).
   The function should return a move from 0-6
   """
  

def play_game(vs_server = False):
   """
   The reward for a game is as follows. You get a
   botaction = random.choice(list(avmoves)) reward from the
   server after each move, but it is 0 while the game is running
   loss = -1
   win = +1
   draw = +0.5
   error = -10 (you get this if you try to play in a full column)
   Currently the player always makes the first move
   """

   # default state
   state = np.zeros((6, 7), dtype=int)

   # setup new game
   if vs_server:
      # Start a new game
      res = call_server(-1) # -1 signals the system to start a new game. any running game is counted as a loss

      # This should tell you if you or the bot starts
      print(res.json()['msg'])
      botmove = res.json()['botmove']
      state = np.array(res.json()['state'])
      # reset env to state from the server (if you want to use it to keep track)
      env.reset(board=state)
   else:
      # reset game to starting state
      env.reset(board=None)
      # determine first player
      student_gets_move = random.choice([True, False])
      if student_gets_move:
         print('You start!')
         print()
      else:
         print('Bot starts!')
         print()

   # Print current gamestate
   print("Current state (1 are student discs, -1 are servers, 0 is empty): ")
   print(state)
   print()

   done = False
   while not done:
      # Select your move
      stmove = student_move(state) # TODO: change input here

      #print(stmove)

      # make both student and bot/server moves
      if vs_server:
         # Send your move to server and get response
         res = call_server(stmove)
         print(res.json()['msg'])

         # Extract response values
         result = res.json()['result']
         botmove = res.json()['botmove']
         state = np.array(res.json()['state'])
         # reset env to state from the server (if you want to use it to keep track)
         env.reset(board=state)
      else:
         if student_gets_move:
            # Execute your move
            avmoves = env.available_moves()
            if stmove not in avmoves:
               print("You tied to make an illegal move! You have lost the game.")
               break
            state, result, done, _ = env.step(stmove)

         student_gets_move = True # student only skips move first turn if bot starts

         # print or render state here if you like

         # select and make a move for the opponent, returned reward from students view
         if not done:
            state, result, done = opponents_move(env)

      # Check if the game is over
      if result != 0:
         done = True
         if not vs_server:
            print("Game over. ", end="")
         if result == 1:
            print("You won!")
         elif result == 0.5:
            print("It's a draw!")
         elif result == -1:
            print("You lost!")
         elif result == -10:
            print("You made an illegal move and have lost!")
         else:
            print("Unexpected result result={}".format(result))
         if not vs_server:
            print("Final state (1 are student discs, -1 are servers, 0 is empty): ")
      else:
         print("Current state (1 are student discs, -1 are servers, 0 is empty): ")

      # Print current gamestate
      print(state)
      print()

def main():
   # Parse command line arguments
   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group()
   group.add_argument("-l", "--local", help = "Play locally", action="store_true")
   group.add_argument("-o", "--online", help = "Play online vs server", action="store_true")
   parser.add_argument("-s", "--stats", help = "Show your current online stats", action="store_true")
   args = parser.parse_args()

   # Print usage info if no arguments are given
   if len(sys.argv)==1:
      parser.print_help(sys.stderr)
      sys.exit(1)

   if args.local:
      play_game(vs_server = False)
   elif args.online:
      #for i in range (20):
      play_game(vs_server = True)

   if args.stats:
      stats = check_stats()
      print(stats)

   # TODO: Run program with "--online" when you are ready to play against the server
   # the results of your games there will be logged
   # you can check your stats bu running the program with "--stats"

if __name__ == "__main__":
    main()
