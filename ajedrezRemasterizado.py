class Piece:
    def __init__(self, col, row, letter, color):
        self.row = row
        self.col = col
        self.letter = letter
        self.color = color
        self.movement_history_list = [[self.col, self.row]]

    def add_movement_history(self, object_to_append):
        self.movement_history_list.append(object_to_append)

    def first_movement(self):
        return len(self.movement_history_list) == 1

    def print_mov_history(self):
        print("printing moving history")
        for i in range(len(self.movement_history_list)):
            print(self.movement_history_list[i])

    def expel(self):
        self.row = -11
        self.col = -1

    def get_ren_board(self):
        return abs(self.row - 9)

    def get_position(self):
        return [self.col, self.row]

    def set_position(self, col, row):
        self.col = col
        self.row = row

    def current_valid_pos(self):
        self.col = self.movement_history_list[len(self.movement_history_list) - 1][0]
        self.row = self.movement_history_list[len(self.movement_history_list) - 1][1]

    def show_piece_data(self):
        print("- INFORMACIÓN PIEZA -")
        print("col:", self.col)
        print("ren: ", self.row)
        print("Color: ", self.color)
        print("Letra: ", self.letter)


class Pawn(Piece):
    def __init__(self, row, col, letter, color):
        Piece.__init__(self, row, col, letter, color)

    def validate_mov(self, target_col, target_row):
        pawnRow = self.row
        pawnCol = self.col
        if self.color == "black":
            pawnRow = abs(self.row - 9)
            target_row = abs(target_row - 9)

        if self.en_passant_pawn(target_col, target_row):
            return True

        if pawnRow + 1 == target_row and (pawnCol + 1 == target_col or pawnCol - 1 == target_col):
            if [target_col, target_row] in all_pieces_pos():
                return True
        if self.first_movement():
            if pawnRow+2 == target_row and pawnCol == target_col and [target_col, target_row+1] not in all_pieces_pos():
                return True
        if pawnRow + 1 == target_row and pawnCol == target_col:
            return True
        return False

    def pawn_promotion(self):
        print("Coronación de peon, escriba la letra de la pieza que desea invocar")

        chosen_piece = input()
        while chosen_piece.upper() not in ["C", "A", "T", "Q"]:
            print("Las opciones disponibles son: 'A', 'C', 'T', 'Q'")
            chosen_piece = input()

        if chosen_piece == "C":
            new_piece = Knight(self.row, self.col, "C", self.color)

        elif chosen_piece == "A":
            new_piece = Bishop(self.row, self.col, "A", self.color)

        elif chosen_piece == "T":
            new_piece = Tower(self.row, self.col, "T", self.color)

        else:
            new_piece = Queen(self.row, self.col, "Q", self.color)

        if self.color == "white":
            whitePieces.append(new_piece)
        else:
            blackPieces.append(new_piece)
        allPieces.append(new_piece)
        self.expel()

    def en_passant_pawn(self, target_col, target_row):
        passedPawn = pieceMoveList[-1]
        if self.color == "white" and passedPawn.letter.lower() == "p" and passedPawn.row == 5:
            if passedPawn.row == self.row and (passedPawn.col == self.col + 1 or passedPawn.col == self.col - 1):
                if self.row == target_row + 1 and (self.col == target_col + 1 or self.col == target_col - 1):
                    return True
        if self.color == "black" and passedPawn.letter.lower() == "p" and passedPawn.row == 4:
            if passedPawn.row == self.row and (passedPawn.col == self.col + 1 or passedPawn.col == self.col - 1):
                if self.row == target_row - 1 and (self.col == target_col + 1 or self.col == target_col - 1):
                    return True


class Knight(Piece):
    def __init__(self, row, col, letter, color):
        Piece.__init__(self, row, col, letter, color)

    def validate_mov(self, target_col, target_row):
        if ((target_row + 2 == self.row or target_row - 2 == self.row)
                and (target_col + 1 == self.col or target_col - 1 == self.col)
                or (target_row + 1 == self.row or target_row - 1 == self.row)
                and (target_col + 2 == self.col or target_col - 2 == self.col)):
            return True
        return False


class Bishop(Piece):
    def __init__(self, row, col, letter, color):
        Piece.__init__(self, row, col, letter, color)
        self.checkSquares = []
    
    def validate_mov(self, target_col, target_row):
        if abs(target_row - self.row) != abs(target_col - self.col):
            return False

        row = self.row
        col = self.col
        check_squares = []
        for i in range(abs(target_row - self.row)-1):
            if target_col > self.col and target_row < self.row:  # seccion 4
                col += 1
                row -= 1
            elif target_col < self.col and target_row < self.row:  # seccion 3
                col -= 1
                row -= 1
            elif target_col < self.col and target_row > self.row:  # seccion 2
                col -= 1
                row += 1
            else:  # seccion 1
                col += 1
                row += 1

            check_squares.append([col, row])

            if [col, row] in all_pieces_pos():
                return False
            self.checkSquares = check_squares
        return True


class Tower(Piece):
    def __init__(self, row, col, letter, color):
        Piece.__init__(self, row, col, letter, color)
        self.checkSquares = []

    def validate_mov(self, target_col, target_row):
        if target_col != self.col and target_row != self.row:
            return False

        row = self.row
        col = self.col
        checkSquares = []
        distancia = abs(target_col - self.col) + abs(target_row - self.row) - 1
        for i in range(distancia):
            if target_col == self.col:
                if target_row - self.row > 0:
                    row += 1
                else:
                    row -= 1
            else:
                if target_col - self.col > 0:
                    col += 1
                else:
                    col -= 1
            checkSquares.append([col, row])
            if [col, row] in all_pieces_pos():
                return False
            self.checkSquares = checkSquares
        return True


class Queen(Tower, Bishop, Piece):
    def __init__(self, row, col, letter, color):
        Piece.__init__(self, row, col, letter, color)

    def validate_mov(self, target_col, target_row):
        if Bishop.validate_mov(self, target_col, target_row):
            return True
        elif Tower.validate_mov(self, target_col, target_row):
            return True
        return False


class King(Queen, Piece):
    def __init__(self, row, col, letter, color):
        Piece.__init__(self, row, col, letter, color)

    def validate_mov(self, target_col, target_row):
        if self.color == "white":
            if [target_col, target_row] in white_pieces_pos():
                return False
        else:
            if [target_col, target_row] in black_pieces_pos():
                return False

        if target_row - self.row > 1 or target_col - self.col > 1:
            if self.castle(target_col, target_row):
                return True

        if abs(target_row - self.row) < 2 and abs(target_col - self.col) < 2:
            return Queen.validate_mov(self, target_col, target_row)
        else:
            return False

    def castle(self, target_col, target_row):
        if check_evaluation():
            return False

        if self.color == "white":
            if target_col == 7 and target_row == 1:
                if self.first_movement() and whiteTower2.first_movement():
                    if [6, 1] in all_pieces_pos() or [7, 1] in all_pieces_pos():
                        return False
                    for i in range(2):
                        self.col = i + 6
                        if check_evaluation():
                            return False
                        else:
                            whiteTower2.col = 6
                            whiteTower2.add_movement_history([6, whiteTower2.row])
                            return True

            if target_col == 3 and target_row == 1:
                if self.first_movement() and whiteTower1.first_movement():
                    if [2, 1] in all_pieces_pos() or [3, 1] in all_pieces_pos() or [4, 1] in all_pieces_pos():
                        return False
                    for i in range(2):
                        self.col = 4 - i
                        if check_evaluation():
                            return False
                        else:
                            whiteTower1.col = 4
                            whiteTower1.add_movement_history([4, whiteTower2.row])
                            return True

        else:
            if target_col == 7 and target_row == 8:
                if self.first_movement() and blackTower2.first_movement():
                    if [6, 8] in all_pieces_pos() or [7, 8] in all_pieces_pos():
                        return False
                    for i in range(2):
                        self.col = i + 6
                        if check_evaluation():
                            return False
                        else:
                            blackTower2.col = 6
                            blackTower2.add_movement_history([6, blackTower2.row])
                            return True

            if target_col == 3 and target_row == 8:
                if self.first_movement() and blackTower1.first_movement():
                    if [2, 8] in all_pieces_pos() or [3, 8] in all_pieces_pos() or [4, 8] in all_pieces_pos():
                        return False
                    for i in range(2):
                        self.col = 4 - i
                        if check_evaluation():
                            return False
                        else:
                            blackTower1.col = 4
                            blackTower1.add_movement_history([4, blackTower1.row])
                            return True

    def has_king_available_squares(self):
        kingSquares = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]

        for i in range(len(kingSquares)):
            col = kingSquares[i][0] + self.col
            row = kingSquares[i][1] + self.row
            if 0 < col < 9 and 0 < row < 9:
                if self.validate_mov(col, row):
                    self.set_position(col, row)
                    if not check_evaluation():
                        self.set_position(self.movement_history_list[-1][0], self.movement_history_list[-1][1])
                        return True
        self.set_position(self.movement_history_list[-1][0], self.movement_history_list[-1][1])
        return False


blackPawn1 = Pawn(1, 7, 'p', 'black')
blackPawn2 = Pawn(2, 7, 'p', 'black')
blackPawn3 = Pawn(3, 7, 'p', 'black')
blackPawn4 = Pawn(4, 7, 'p', 'black')
blackPawn5 = Pawn(5, 7, 'p', 'black')
blackPawn6 = Pawn(6, 7, 'p', 'black')
blackPawn7 = Pawn(7, 7, 'p', 'black')
blackPawn8 = Pawn(8, 7, 'p', 'black')
whitePawn1 = Pawn(1, 2, 'P', 'white')
whitePawn2 = Pawn(2, 2, 'P', 'white')
whitePawn3 = Pawn(3, 2, 'P', 'white')
whitePawn4 = Pawn(4, 2, 'P', 'white')
whitePawn5 = Pawn(5, 2, 'P', 'white')
whitePawn6 = Pawn(6, 2, 'P', 'white')
whitePawn7 = Pawn(7, 2, 'P', 'white')
whitePawn8 = Pawn(8, 2, 'P', 'white')

blackKnight1 = Knight(2, 8, 'c', 'black')
blackKnight2 = Knight(7, 8, 'c', 'black')
whiteWorse1 = Knight(2, 1, 'C', 'white')
whiteWorse2 = Knight(7, 1, 'C', 'white')

blackBishop1 = Bishop(3, 8, 'a', 'black')
blackBishop2 = Bishop(6, 8, 'a', 'black')
whiteBishop1 = Bishop(3, 1, 'A', 'white')
whiteBishop2 = Bishop(6, 1, 'A', 'white')

blackTower1 = Tower(1, 8, 't', 'black')
blackTower2 = Tower(8, 8, 't', 'black')
whiteTower1 = Tower(1, 1, 'T', 'white')
whiteTower2 = Tower(8, 1, 'T', 'white')

blackQueen = Queen(4, 8, 'q', 'black')
whiteQueen = Queen(4, 1, 'Q', 'white')

blackKing = King(5, 8, 'k', 'black')
whiteKing = King(5, 1, 'K', 'white')

blackPieces = [blackPawn1, blackPawn2, blackPawn3, blackPawn4, blackPawn5, blackPawn6, blackPawn7, blackPawn8,
               blackKnight1, blackKnight2, blackBishop1, blackBishop2, blackTower1, blackTower2, blackQueen, blackKing]
whitePieces = [whitePawn1, whitePawn2, whitePawn3, whitePawn4, whitePawn5, whitePawn6, whitePawn7, whitePawn8,
               whiteWorse1, whiteWorse2, whiteBishop1, whiteBishop2, whiteTower1, whiteTower2, whiteQueen, whiteKing]
allPieces = blackPieces.copy() + whitePieces.copy()

turnCounter = 0
how_many_movements = 0
_50_movements_counter = 0
pieceMoveList = [whitePawn1]


def white_pieces_pos():
    return [x.get_position() for x in whitePieces]


def black_pieces_pos():
    return [x.get_position() for x in blackPieces]


def all_pieces_pos():
    return white_pieces_pos() + black_pieces_pos()


def get_piece_by_pos(position):
    return [x for x in allPieces if x.get_position() == position][0]


def format_input():
    inputCoordinates = input().lower()
    while inputCoordinates[0] not in "abcdefgh" or inputCoordinates[1] not in "12345678":
        print("Formato Incorrecto, vuelva a intentarlo")
        inputCoordinates = input().lower()
    return [int("abcdefgh".find(inputCoordinates[0]))+1, int(inputCoordinates[1])]


def user_select_piece():
    print("Ingrese las coordenadas de la pieza que desea mover")
    pos_piece_to_move = format_input()

    while (current_turn() == "white" and pos_piece_to_move not in white_pieces_pos()
            or current_turn() == "black" and pos_piece_to_move not in black_pieces_pos()):
        print("No se encuentra una pieza color", current_turn(), "en la casilla seleccionada")
        pos_piece_to_move = format_input()

    return [x for x in allPieces if x.get_position() == pos_piece_to_move][0]


def next_turn():
    global turnCounter
    turnCounter += 1


def current_turn():
    global turnCounter
    if turnCounter % 2 != 0:
        return "white"
    else:
        return "black"


def chess_board():
    chessBoard = []
    tiles = ["/", " ", "/", " ", "/", " ", "/", " ", "/", ""]
    numbers = [" ", 1, 2, 3, 4, 5, 6, 7, 8]
    alphabet = [" ", "a", "b", "c", "d", "e", "f", "g", "h"]

    for row in range(10):
        chessBoard.append([])
        for col in range(10):
            if row % 2 == 0:
                chessBoard[row].append(tiles[col - 1])
            if row % 2 != 0:
                chessBoard[row].append(tiles[col])
    for i in range(9):
        chessBoard[i][0] = (numbers[-i])
        chessBoard[i][9] = (numbers[-i])
        chessBoard[0][i] = (alphabet[i])
        chessBoard[9][i] = (alphabet[i])

    for i in range(len(allPieces)):
        if 0 < allPieces[i].row < 9 and 0 < allPieces[i].col < 9:
            row = allPieces[i].get_ren_board()
            col = allPieces[i].col
            chessBoard[row][col] = allPieces[i].letter

    for i in range(len(chessBoard)):
        for j in range(len(chessBoard[0])):
            print(chessBoard[i][j], end=" ")
        print()


def check_evaluation():
    global checkPieces
    if current_turn() == "white":
        checkPieces = [x for x in blackPieces if x.letter != "k" and x.validate_mov(whiteKing.col, whiteKing.row)]
        return bool(len(checkPieces))
    elif current_turn() == "black":
        checkPieces = [x for x in whitePieces if x.letter != "K" and x.validate_mov(blackKing.col, blackKing.row)]
        return bool(len(checkPieces))
    return False


def check_mate_evaluation():
    if check_evaluation():
        piece_making_check = checkPieces

    if current_turn() == "white":
        if whiteKing.has_king_available_squares():
            return
    else:
        if blackKing.has_king_available_squares():
            return

    if len(piece_making_check) == 1:
        piece_making_check = piece_making_check[0]

        squaresToOpposeCheck = [piece_making_check.get_position()]

        if not(piece_making_check.letter.lower() == "p" or piece_making_check.letter.lower() == "c"):
            squaresToOpposeCheck.extend(piece_making_check.checkSquares)

        for i in range(len(squaresToOpposeCheck)):
            if current_turn() == "white":
                for blackPiece in blackPieces:
                    if blackPiece.letter.lower() != "k":
                        if blackPiece.validate_mov(squaresToOpposeCheck[i][0], squaresToOpposeCheck[i][1]):
                            return
            else:
                for blackPiece in blackPieces:
                    if blackPiece.letter.lower() != "k":
                        if blackPiece.validate_mov(squaresToOpposeCheck[i][0], squaresToOpposeCheck[i][1]):
                            blackPiece.show_piece_data()
                            return

    print("JAQUE MATE CON TOMATE Y PATATAS FRITAS")
    exit()


def piece_movement_validation(piece_to_move):
    print("Ingrese las coordenadas a las que desea mover su pieza")
    pieceTargetPos = format_input()

    # Evaluate invalid move because of check
    piece_to_move.col = pieceTargetPos[0]
    piece_to_move.row = pieceTargetPos[1]
    if check_evaluation():
        print("No puede mover esa pieza pues pondria su rey en jaque")
        piece_to_move.current_valid_pos()
        return False
    piece_to_move.current_valid_pos()

    if pieceTargetPos == piece_to_move.get_position():
        print("No puede mover a la casilla de su pieza seleccionada")
        return False

    # No puede caputar una pieza de tu mismo color
    if (piece_to_move.color == "white" and pieceTargetPos in white_pieces_pos()
            or piece_to_move.color == "black" and pieceTargetPos in black_pieces_pos()):
        return False

    # Escenario al capturar una pieza
    isCapturedPiece = False
    if pieceTargetPos in all_pieces_pos():
        caputuredPiece = get_piece_by_pos(pieceTargetPos)
        isCapturedPiece = True

    # Movimiento de la pieza
    if piece_to_move.validate_mov(pieceTargetPos[0], pieceTargetPos[1]):
        piece_to_move.col = pieceTargetPos[0]
        piece_to_move.row = pieceTargetPos[1]
        piece_to_move.add_movement_history([piece_to_move.col, piece_to_move.row])
        global how_many_movements
        how_many_movements += 1

        global pieceMoveList
        pieceMoveList.append(piece_to_move)

        if piece_to_move.letter.lower() == "p" and piece_to_move.row == 8 or piece_to_move.row == 1:
            piece_to_move.pawn_promotion()
        
        if isCapturedPiece:
            global _50_movements_counter
            _50_movements_counter = 0
            caputuredPiece.expel()
        return True
    return False


def stale_mate():
    if current_turn() == "white":
        king = whiteKing
        pieces = whitePieces
    else:
        king = blackKing
        pieces = blackPieces

    if king.has_king_available_squares():
        return False

    nextSquares = [[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]
    for piece in pieces:
        for item in nextSquares:
            if piece.letter.lower() != "k" and piece.validate_mov(piece.col + item[0], piece.row + item[1]):
                piece.set_position(piece.col + item[0], piece.row + item[1])
                if not check_evaluation():
                    piece.current_valid_pos()
                    return False
            piece.current_valid_pos()
    print("TABLAS POR REY AHOGADO")
    exit()


def _50_movements():
    global _50_movements_counter
    if pieceMoveList[-1].letter.lower() != "p":
        _50_movements_counter += 1
    else:
        _50_movements_counter = 0

    if _50_movements_counter == 50:
        print("TABLAS POR REGLA DE 50 MOVIMIENTOS")
        exit()


def main():
    next_turn()
    chess_board()

    for i in range(1023):
        piece_to_move = user_select_piece()
        if piece_movement_validation(piece_to_move):
            chess_board()
            next_turn()
        else:
            print("Movimiento incorrecto, intente de nuevo")

        if check_evaluation():
            check_mate_evaluation()
            print("JAQUE")
        # Tablas
        stale_mate()
        _50_movements()


main()

# Elementos a probar:
# - Peon al paso ...
# - Rey Ahogado ...
# - Regla de los 50 movimientos ...
