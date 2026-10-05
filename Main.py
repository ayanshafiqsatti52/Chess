# Creates a class for a piece and its attributes
class Piece:
    def __init__(self, piecetype, color):
        self.piece = piecetype  #Variable of type string
        self.color = color      #Variable of type string
        self.hasmoved = False   #Variable of type boolean

    # Returns possible destination coordinates for this piece
    def get_possible_move(self, r, c, board):
        possible_moves = []

        # Check the current position before accessing the board
        if (r < 0 or r > 7) or (c < 0 or c > 7):
            return possible_moves

        # ---- Pawn Definition ---- #
        if self.piece == "pawn":
            # White moves towards row 0; Black towards row 7
            direction = -1 if self.color == "white" else 1

            # Calculate the row directly ahead of the pawn
            next_row = r + direction

            # Check the destination is on the board
            if 0 <= next_row <= 7:

                # Pawns can move forward only into an empty square
                if board[next_row][c] == "":
                    move = True
                else:
                    move = False

                if move:
                    possible_moves.append((next_row, c))

                #If the pawn is at starting position it can move two positions
                startrow = 6 if self.color == "white" else 1
                if r == startrow and self.hasmoved == False and board[next_row][c] == "" and board[next_row + direction][c] == "":
                    move=True
                else:
                    move=False

                if move:
                    possible_moves.append((next_row+direction,c))

                #If there is  an opposite colored piece then we can capture it diagonally
                if 0 <= next_row <= 7 and 0 <= c - 1 <= 7 and board[next_row][c-1]!="" and board[next_row][c-1].color!=self.color:
                    possible_moves.append((next_row,c-1))
                if 0<=next_row<=7 and 0<=c+1<=7 and board[next_row][c+1]!="" and board[next_row][c+1].color!=self.color:
                    possible_moves.append((next_row,c+1))

        #-----Rook Definition-----#
        elif self.piece=="rook":
            #Checking forward vertical movements
            for x in range(r+1,8):
                if board[x][c]=="":
                    possible_moves.append((x, c))
                elif board[x][c].color!=self.color:
                    possible_moves.append((x, c))
                    break
                elif board[x][c].color==self.color:
                    break
            #Checking backward vertical movements
            for x in range(r-1,-1,-1):
                if board[x][c]=="":
                    possible_moves.append((x, c))
                elif board[x][c].color!=self.color:
                    possible_moves.append((x,c))
                    break
                elif board[x][c].color==self.color:
                    break
             #Checking horizontal movements right
            for x in range(c+1,8):
                if board[r][x]=="":
                    possible_moves.append((r,x))
                elif board[r][x].color!=self.color:
                    possible_moves.append((r,x))
                    break
                elif board[r][x].color==self.color:
                    break
            #Checking horizontal movements left
            for x in range(c-1,-1,-1):
                if board[r][x]=="":
                    possible_moves.append((r,x))
                elif board[r][x].color!=self.color:
                    possible_moves.append((r,x))
                    break
                elif board[r][x].color==self.color:
                    break
        #----Bishop Definition-----#
        elif self.piece =="bishop":
            directions=[
                (-1,1),     #Up-right
                (-1,-1),    #Up-right
                (1,1),      #Down-right
               (1,-1)       #Down-left
            ]
            for row_step,col_step in directions:
                #Start one square away in this direction
                check_row=r+row_step
                check_col=c+col_step

                #Keep checking while the square is on the board
                while 0<=check_row<=7 and 0<=check_col<=7:
                    target=board[check_row][check_col]
                    if target=="":
                        #Condition for empty square
                        possible_moves.append((check_row,check_col))
                    elif target.color!=self.color:
                        #Enemy finding condition
                        possible_moves.append((check_row,check_col))
                        break
                    elif target.color==self.color:
                        break

                    check_row+=row_step
                    check_col+=col_step

        elif self.piece=="queen":
            directions = [
                (-1, 1), (-1, -1), (1, 1), (1, -1),  # Diagonals
                (-1, 0), (1, 0), (0, -1), (0, 1)  # Up, down, left, right
            ]

            for row_step,col_step in directions:
                check_row=r+row_step
                check_col=c+col_step

                while 0<=check_row<=7 and 0<=check_col<=7:
                    target=board[check_row][check_col]
                    if target=="":
                        possible_moves.append((check_row,check_col))
                    elif target.color!=self.color:
                        possible_moves.append((check_row,check_col))
                        break
                    elif target.color==self.color:
                        break

                check_row += row_step
                check_col += col_step

        if self.piece=="knight":
            directions=[
                (2,1),(-2,1),
                (-2,-1),(2,-1),
                (1,2),(1,-2),
                (-1,-2),(-1,2)
            ]
            for row_step,col_step in directions:
                check_row=r+row_step
                check_col=c+col_step

            while 0<=check_row<=7 and 0<=check_col<=7:
                if board[row_step][col_step]=="":
                    possible_moves.append((check_row,check_col))
                elif board[row_step][col_step].color!=self.color:
                    possible_moves.append((row_step,col_step))
                    break
                elif board[row_step][col_step].color==self.color:
                    break

                check_row += row_step
                check_col += col_step

        if self.piece=="king":
            directions=[
                (0,1),(1,0),
                (-1,0),(0,-1),
                (1,1),(-1,-1),
                (1,-1),(-1,1)
            ]
            for row_step,col_step in directions:
                check_row=r+row_step
                check_col=c+col_step
                while 0<=check_row<=7 and 0<=check_col<=7:
                    if board[check_row][check_col]=="":
                        possible_moves.append((check_row,check_col))
                    elif board[check_row][check_col].color!=self.color:
                        possible_moves.append((check_row,check_col))
                        break
                    elif board[check_row][check_col].color==self.color:
                        break

                    check_row += row_step
                    check_col += col_step

        return possible_moves

    def is_square_attacked(self,r,c,board,attacking_color):
        if not(0<=r<=7 and 0<=c<=7):
            return False
        for row in range(8):
            for column in range(8):
                if board[row][column]!="" and board[row][column].color==attacking_color:
                    piece=board[row][column]
                    if piece.piece=="pawn":
                        direction=-1 if piece.color=="white" else 1
                        if r==row+direction and abs(c-column)==1:
                            return True
                    else:
                        Temp=piece.get_possible_move(row,column,board)
                        if  (r,c) in Temp:
                            return True
        return False

    def is_in_check(self,color,board):
        pass










# Create an 8×8 board with empty squares
Board = [["" for _ in range(8)] for _ in range(8)]




