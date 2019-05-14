#!/usr/bin/env python3
import sys
import time
import random
import chess

MAX_DEPTH = 1
MAX_TIME_MS = 10000
DEBUG = 0

def col(b):
    if b.turn == 1:
        return "W"
    return "B"

def pb(b):
    print (b)

def log(b, lvl, text):
    if (DEBUG):
        print ("[",lvl,"][",col(b),"][",b.peek(),"]:", text)

def info(b, text):
    log(b, "I", text)

def warn(b, text):
    log(b, "W", text)

def err(b, text):
    log(b, "E", text)

def get_score(b, move, depth):
    # Get the score for the current move given a board
    score = 0
    b.push(move)

    if b.is_check():
        score += 10
    elif b.is_checkmate():
        info(b, "found a checkmate!")
        pb(b)
        score += 11000

    if b.is_attacked_by (not b.turn, move.to_square):
        info(b, "reducing score since check results in attack")
        score -= 1000

    b.pop()

    # Take into account the depth while calculating
    # score for this move
    #return score * (MAX_DEPTH - depth)
    return score

def move_recursion(b, score, depth):
    score = 0

    if b.legal_moves.count() == 0:
        pb(b)
        warn(b, "ran out of legal moves")
        return 0, None

    move = random.choice(list(b.legal_moves))

    # go over all moves and see which one generates
    # the highest score.
    for cur_mov in b.legal_moves:
        cur_score = get_score(b, cur_mov, depth)

        b.push(cur_mov)
        if depth >= MAX_DEPTH:
            b.pop()
            return cur_score, move
        else:
            # opponent makes a random move
            if b.legal_moves.count() == 0:
                #pb(b)
                warn(b, "ran out of legal moves for opponents")
                b.pop()
                return -1000, move

            b.push(random.choice(list(b.legal_moves)))
            next_score, next_move = move_recursion(b, score, depth+1)

            if next_move == None:
                warn(b, "next_move is none, need to move on")
                b.pop()
                continue

            cur_score += next_score
            b.pop()

        if cur_score > score:
            score = cur_score
            move = cur_mov

        b.pop()

    return score, move


def get_move(b, limit=None):
  # TODO: Fill this in with a BETTER chess engine

  try:
    score, move = move_recursion(b, 0, 0)
  except:
    pb(b)
    raise

  if move == None:
      err(b, "NONE FROM ENGINE")
      return random.choice(list(b.legal_moves))

  print("playing", move, file=sys.stderr)
  return move

if __name__ == "__main__":
  print("welcome to the greatest chess engine", file=sys.stderr)
  while 1:
    cmd = input().split(" ")
    #print(cmd, file=sys.stderr)

    if cmd[0] == "uci":
      print("uciok")
    elif cmd[0] == "ucinewgame":
      pass
    elif cmd[0] == "isready":
      print("readyok")
    elif cmd[0] == "position":
      if cmd[1] == "startpos":
        b = chess.Board()
        if len(cmd) > 2 and cmd[2] == "moves":
          for m in cmd[3:]:
            b.push(chess.Move.from_uci(m))
    elif cmd[0] == "go":
      if len(cmd) > 1 and cmd[1] == "movetime":
        move = get_move(b, limit=int(cmd[2]))
      else:
        move = get_move(b)
      print("bestmove %s" % move)
    elif cmd[0] == "quit":
      exit(0)
      
