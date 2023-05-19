#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import copy
import sys
import time
import numpy as np
import filecmp
import difflib

ROW = "ABCDEFGHI"
COL = "123456789"
row_squares ={"A":["A","B","C"], "B": ["A","B","C"], "C": ["A","B","C"], "D":["D","E","F"], "E":["D","E","F"], "F":["D","E","F"], "G":["G","H","I"], "H":["G","H","I"], "I":["G","H","I"]}
col_squares ={"1":["1","2","3"], "2": ["1","2","3"], "3": ["1","2","3"], "4":["4","5","6"], "5":["4","5","6"], "6":["4","5","6"], "7":["7","8","9"], "8":["7","8","9"], "9":["7","8","9"]}

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def initalize_domains(board, domains):
    domains = {}
    updates = {}
    for r in ROW:
        for c in COL:
            if board[r+c] == 0:
                domains[r+c] = [1,2,3,4,5,6,7,8,9]
            else:
                updates[r+c] = board[r+c]

    for k, v in updates.items():
        domains = find_new_domains(board, domains, v, k) #update domain values based on values assigned in board
        #currently getting nonetype error when initializing since find new domains is returning none at some point
    return domains

def find_new_domains(board, domains, new, pos):
    domain = copy.deepcopy(domains)
    row = pos[0:1]
    col = pos[1:]
    for c in COL:
        if row+c in domain.keys():
            list = domain[row+c]
            if new in list and row+c != pos:
                list.remove(new)
                if len(list) == 0:
                    return None
    for r in ROW:
        if r+col in domain.keys():
            list = domain[r+col]
            if new in list and r+col != pos:
                list.remove(new)
                if len(list) == 0:
                    return None

    rows = row_squares[row]
    cols = col_squares[col]
    for r in rows:
        for c in cols:
            if r+c in domain.keys():
                list = domain[r + c]
                if new in list and r+c != pos:
                    list.remove(new)
                    if len(list) == 0:
                        return None
    #go through the row, column and square of the pos
    #if new value is in the domain, remove it
    #if any domain becomes empty, return None

    return domain


def find_mrv(board, domain):
    #assuming domain is a dictionary where key is location and value is list of possible values
    min = 10
    min_space = ""
    for k, v in domain.items():
        if(len(v) < min):
            min = len(v)
            min_space = k
    return min_space

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    domain = initalize_domains(board, {})
    return backtrack(board, domain)


def backtrack(board, domain):
    if len(domain) == 0:
        return board
    #select unassigned space on the board (with smallest domain left)
    assigned = find_mrv(board, domain)
    values = list(domain[assigned])
    #for each value in the valid domain of values
    for value in values:
        temp = find_new_domains(board, domain, value, assigned)
        if temp is not None:
            board[assigned] = value
            del temp[assigned]
            result = backtrack(board, temp) #call backtrack if above does not return null
            if result != None:
                return result
            board[assigned] = 0
    return None



if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        # src_filename = 'sudokus_start.txt'
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        times = []
        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            # Solve with backtracking
            start_time  = time.time()
            solved_board = backtracking(board)
            end_time  = time.time()
            times.append(end_time - start_time)
            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Write board to file
            if len(board_to_string(solved_board)) > 81:
                print(len(board_to_string(solved_board)))
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        min = times[0]
        max = times.pop()
        std = np.std(times)
        mean = np.mean(times)

        file = open("README.txt", "w")
        file.write("Number of boards solved: " + str(400)) 
        file.write("\n")
        file.write("Minimum solve time: " + str(min))
        file.write("\n")
        file.write("Maximum solve time: " + str(max))
        file.write("\n")
        file.write("Mean solve time: " + str(mean))
        file.write("\n")
        file.write("Standard deviation of solve time: " + str(std))