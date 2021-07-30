class GameState(object):
    boardWhite = [  # ???????????????????
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    boardBlack = [  # ???????????????????
        ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"],
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"]
    ]

    # board = [] - например boardWhite
    # nowMove = "w" or "b"  -  меняется каждый ход
    # startMove = "w" or "b" - начало игры
    #
    # lastMove = []

    def __init__(self, started):
        self.lastMove = []
        self.lastDoubleMoveW = []
        self.lastDoubleMoveB = []

        self.startRookMoves = [[[0, 0], False], [[0, 7], False], [[7, 0], False], [[7, 7], False]]
        self.startKing = {'w': False, 'b': False}

        if started == "w":
            self.board = GameState.boardWhite
            self.whiteK = (7, 4)
            self.blackK = (0, 4)
            self.nowMove = "w"
            self.startMove = "w"
        elif started == "b":
            self.board = GameState.boardBlack
            self.whiteK = (0, 4)
            self.blackK = (7, 4)
            self.nowMove = "b"
            self.startMove = "b"
        elif started[0] == "..":  # ".." <= [[], [], [], ... ] <- board situation (not start game)
            self.board = started[1]
        else:
            print("ERROR: Не понятно за какой цвет играть!")

    def getStartRookMoves(self, a, b):
        for el in self.startRookMoves:
            i = el[0]
            if i[0] == a and i[1] == b:
                return el[1]
        print("--------------ERROR-----getStartRookMoves-----------------------------")

    def setStartRookMoves(self, a, b, v):
        m = False
        for i in range(len(self.startRookMoves)):
            if self.startRookMoves[i][0][0] == a and self.startRookMoves[i][0][1] == b:
                self.startRookMoves[i][1] = v
                m = True
        if not m:
            print("---------------------ERROR------setStartRookMoves-----------------------------")

    def move(self, start, end):
        sym = self.board[start[0]][start[1]][1]
        # clr = self.board[start[0]][start[1]][0]
        # col -> start[1] and end[1]
        # row -> start[0] and end[0]
        # print(str(start) + " + " + str(end))

        _res = 0
        if sym == "p":
            _res = self.getPawnMoves(start, end)
        elif sym == "R":
            _res = self.getRookMoves(start, end)
        elif sym == "N":
            _res = self.getKnightMoves(start, end)
        elif sym == "B":
            _res = self.getBishopMoves(start, end)
        elif sym == "Q":
            _res = self.getQueenMoves(start, end)
        elif sym == "K":
            _res = self.getKingMoves(start, end)
        else:
            print("ERROR: Нет такой фигуры!")

        if not _res:
            return False

        # проверка: можно ли ходить (вдруг шах моему королю)
        # пожалуй сделаю проверку при начале хода следующего игрока!

        t = 0
        # рокировка
        if _res[0] == "castling":  # _res[1]["del"][0][0]
            # return ["castling", {"del": [[7, 0], [7, 4]], "K": [7, 2], "R": [7, 3]}]

            self.board[_res[1]["del"][0][0]][_res[1]["del"][0][1]] = "--"
            self.board[_res[1]["del"][1][0]][_res[1]["del"][1][1]] = "--"

            self.board[_res[1]["K"][0]][_res[1]["K"][1]] = (self.nowMove + "K")
            self.board[_res[1]["R"][0]][_res[1]["R"][1]] = (self.nowMove + "R")
            # #########################
            m = "w" if self.nowMove == "b" else "b"
            if m == "w":
                self.lastDoubleMoveW = []
            elif m == "b":
                self.lastDoubleMoveB = []
            self.nowMove = m
            t = 1
            return True
        # except Exception:
        #     print("Error " + str(Exception) + ": castling move (def move())")

        if t == 0:
            # Если ход может выполняться, то ниже происходит выполнение (не рокировки)
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = "--"

            self.lastMove = [start, end]

            ##############################################
            # ХОД ВЫПОЛНЕН, СИТУАЦИЯ НА ДОСКЕ ИЗМЕНИЛАСЬ #
            ##############################################

            #######################################
            # ниже ход передаётся, другой стороне #
            #######################################

            m = "w" if self.nowMove == "b" else "b"
            if m == "w":
                self.lastDoubleMoveW = []
            elif m == "b":
                self.lastDoubleMoveB = []
            self.nowMove = m
            return True
        # Конец выполнения

        # (i - 3.5) * _a + 3.5

    def getPawnMoves(self, _s, _e):
        _a: int = 1 if (self.startMove != self.nowMove) else -1
        eC = "b" if self.nowMove == "w" else "w"
        if _s[1] == _e[1]:
            # перемещаемся вперед
            if _a * (_e[0] - _s[0]) == 1 and self.board[_e[0]][_e[1]] == "--":
                return True  # 1 шаг вперед
            elif _a * (_e[0] - _s[0]) == 2 and self.board[_e[0] - _a][_e[1]] == "--" and self.board[_e[0]][_e[1]] == "--" and _s[0] == (-2.5 * float(_a)) + 3.5:
                # if self.nowMove == "w":
                #    self.lastDoubleMoveW = [_s[0] + _a, _s[1], _e[0], _e[1]]
                # elif self.nowMove == "b":
                #    self.lastDoubleMoveB = [_s[0] + _a, _s[1], _e[0], _e[1]]
                self.lastDoubleMoveW = [_s[0] + _a, _s[1], _e[0], _e[1]]
                return True  # 2 шага вперед (только в начале)
        elif (_e[0] - _s[0] == 1 * _a) and (_s[1] - _e[1] == 1 or _s[1] - _e[1] == -1):
            if self.board[_e[0]][_e[1]][0] == eC:
                return True
            elif self.nowMove == "w" and len(self.lastDoubleMoveB) != 0:
                if _e[0] == self.lastDoubleMoveB[0] and _e[1] == self.lastDoubleMoveB[1]:
                    self.board[self.lastDoubleMoveB[2]][self.lastDoubleMoveB[3]] = "--"
                    return True
            elif self.nowMove == "b" and len(self.lastDoubleMoveW) != 0:
                if _e[0] == self.lastDoubleMoveW[0] and _e[1] == self.lastDoubleMoveW[1]:
                    self.board[self.lastDoubleMoveW[2]][self.lastDoubleMoveW[3]] = "--"
                    return True

    def getRookMoves(self, _s, _e):
        _d = ((1, 0), (0, -1), (-1, 0), (0, 1))
        _moves = []
        eC = "b" if self.nowMove == "w" else "w"
        for _di in _d:
            for i in range(1, 8):
                endRow = _s[0] + _di[0] * i
                endCol = _s[1] + _di[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        _moves.append((endRow, endCol))
                    elif endPiece[0] == eC:
                        if endPiece[1] == "K":
                            # Игра окончена, победили _clr (w or b)
                            # тот случай когда ладья может бить вражеского короля
                            pass
                        else:
                            _moves.append((endRow, endCol))
                            break
                    else:
                        break
                else:
                    break

        for _i in _moves:
            if (_e[0], _e[1]) == _i:
                if (_s[0] == 0 or _s[0] == 7) and (_s[1] == 0 or _s[1] == 7):
                    if not self.getStartRookMoves(_s[0], _s[1]):
                        self.setStartRookMoves(_s[0], _s[1], True)
                return True
        return False

    def getKnightMoves(self, _s, _e):
        _d = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2))
        _moves = []
        for _di in _d:
            endRow = _s[0] + _di[0]
            endCol = _s[1] + _di[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != self.nowMove:
                    if endPiece[1] == "K":
                        # Игра окончена, победили _clr (w or b)
                        pass
                    else:
                        _moves.append((endRow, endCol))
        for _i in _moves:
            if (_e[0], _e[1]) == _i:
                return True
        return False

    def getBishopMoves(self, _s, _e):
        _d = ((1, -1), (1, 1), (-1, -1), (-1, 1))
        _moves = []
        eC = "b" if self.nowMove == "w" else "w"
        for _di in _d:
            for i in range(1, 8):
                endRow = _s[0] + _di[0] * i
                endCol = _s[1] + _di[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        _moves.append((endRow, endCol))
                    elif endPiece[0] == eC:
                        if endPiece[1] == "K":
                            # Игра окончена, победили _clr (w or b)
                            pass
                        else:
                            _moves.append((endRow, endCol))
                            break
                    else:
                        break
                else:
                    break
        for _i in _moves:
            if (_e[0], _e[1]) == _i:
                return True
        return False

    def getQueenMoves(self, _s, _e):
        if not self.getRookMoves(_s, _e):
            if not self.getBishopMoves(_s, _e):
                return False
        return True

    def getKingMoves(self, _s, _e):
        _d = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        _moves = []
        for i in range(0, 8):
            endRow = _s[0] + _d[i][0]
            endCol = _s[1] + _d[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != self.nowMove:
                    if endPiece[1] == "K":
                        print('-------------------------ERROR---------------getKingMoves------------------------')
                    else:
                        _moves.append((endRow, endCol))

        # ######################### РОКИРОВКА
        if not self.startKing[self.nowMove]:
            if self.nowMove == "w":  # ход белых (белый король и ладья)
                if self.startMove == "w":
                    if _e[0] == 7:
                        if _e[1] == 2:
                            if not self.getStartRookMoves(7, 0) and self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--":
                                self.setStartRookMoves(7, 0, True)
                                return ["castling", {"del": [[7, 0], [7, 4]], "K": [7, 2], "R": [7, 3]}]
                        elif _e[1] == 6:
                            if not self.getStartRookMoves(7, 7) and self.board[7][6] == "--" and self.board[7][5] == "--":
                                self.setStartRookMoves(7, 7, True)
                                return ["castling", {"del": [[7, 7], [7, 4]], "K": [7, 6], "R": [7, 5]}]
                else:
                    if _e[0] == 0:
                        if _e[1] == 1:
                            if not self.getStartRookMoves(0, 0) and self.board[0][1] == "--" and self.board[0][2] == "--":
                                self.setStartRookMoves(0, 0, True)
                                return ["castling", {"del": [[0, 0], [0, 3]], "K": [0, 1], "R": [0, 2]}]
                        elif _e[1] == 5:
                            if not self.getStartRookMoves(0, 7) and self.board[0][6] == "--" and self.board[0][5] == "--" and self.board[0][4] == "--":
                                self.setStartRookMoves(0, 7, True)
                                return ["castling", {"del": [[0, 7], [0, 3]], "K": [0, 5], "R": [0, 4]}]
            else:  # ход черных (черный король и ладья)
                if self.startMove == "w":
                    if _e[0] == 0:
                        if _e[1] == 2:
                            if not self.getStartRookMoves(0, 0) and self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--":
                                self.setStartRookMoves(0, 0, True)
                                return ["castling", {"del": [[0, 0], [0, 4]], "K": [0, 2], "R": [0, 3]}]
                        elif _e[1] == 6:
                            if not self.getStartRookMoves(0, 7) and self.board[0][6] == "--" and self.board[0][5] == "--":
                                self.setStartRookMoves(0, 7, True)
                                return ["castling", {"del": [[0, 7], [0, 4]], "K": [0, 6], "R": [0, 5]}]
                else:
                    if _e[0] == 7:
                        if _e[1] == 1:
                            if not self.getStartRookMoves(7, 0) and self.board[7][1] == "--" and self.board[7][2] == "--":
                                self.setStartRookMoves(7, 0, True)
                                return ["castling", {"del": [[7, 0], [7, 3]], "K": [7, 1], "R": [7, 2]}]
                        elif _e[1] == 5:
                            if not self.getStartRookMoves(7, 7) and self.board[7][6] == "--" and self.board[7][5] == "--" and self.board[7][4] == "--":
                                self.setStartRookMoves(7, 7, True)
                                return ["castling", {"del": [[7, 7], [7, 3]], "K": [7, 5], "R": [7, 4]}]
        # ######################### END

        for _i in _moves:
            if (_e[0], _e[1]) == _i:
                if not self.startKing[self.nowMove]:
                    self.startKing[self.nowMove] = True
                return True
        if self.startMove == "w":
            pass
        elif self.startMove == "b":
            pass
        return False


##################################
##################################

import pygame as P

chessWidth = chessHeight = 512  # 512 original
SQ_SIZE = chessWidth // 8  # размер одной ячейки доски
marginVisual = SQ_SIZE // 4  # отступ в приложении (от доски)
marginTop = 32
WIDTH = chessWidth + (marginVisual * 2)  # размеры окна приложения
HEIGHT = chessHeight + (marginVisual * 2)

MAX_FPS = 15  # больше и не надо

BACKGROUND_COLOR = (59, 60, 82)
CHESS_COLOR = "orig"
CHESS_COLORS = {  # [0] - white, [1] - black, [2] - ++sqSelected
    "orig": ((255, 255, 255), (128, 128, 128), (-60, -30, 0, 2)),
    "dark-blue": ((255, 255, 255), (64, 83, 179), (-60, -30, 0, 2)),
}

IMAGES = {}


def main():
    # START PRINT START
    befRun = True
    b = ""
    t = "Белыми или черными ('б, w' or 'ч, b')? "
    _p = ""  # main Class attribute
    while befRun:
        befRun = not befRun
        # a = ""
        # try:
        a = input(t)
        # except:
        #     raise SystemExit(1)

        if a.lower() == "w" or a.lower() == "б":
            _p = "w"
            b = "белых!"
        elif a.lower() == "b" or a.lower() == "ч":
            _p = "b"
            b = "черных!"
        else:
            befRun = not befRun
    print("Вы играете за " + b)
    del befRun, b, t
    # END PRINT START

    # main Class
    C = GameState(_p)
    del _p

    P.init()
    S = P.display.set_mode((WIDTH, HEIGHT))
    clock = P.time.Clock()
    S.fill(BACKGROUND_COLOR)

    # <LOAD IMAGES>
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = P.transform.scale(P.image.load("chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    del pieces
    # </END LOAD IMAGES>

    running = True
    sqSelected = ()

    clock_time = 0
    sqError = ()
    while running:
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
            elif e.type == P.MOUSEBUTTONDOWN:
                loc = P.mouse.get_pos()  # (x, y) mouse
                col = (loc[0] - marginVisual) // SQ_SIZE  # 0..7
                row = (loc[1] - marginVisual) // SQ_SIZE  # 0..7
                if marginVisual <= loc[0] <= chessWidth + marginVisual and marginVisual <= loc[1] <= chessHeight + marginVisual:
                    f = C.board[row][col][1] != "-"  # f = True когда поле заполнено
                    bw = C.board[row][col][0] == C.nowMove  # bw = True когда фигура твоя

                    ########################################

                    ########################################

                    if sqSelected == () and f and bw:  # если ничего не выбрано и выбираемое поле ВЫБРАТЬ МОЖНО
                        sqSelected = (row, col)  # поле выбрано
                    elif sqSelected != (row, col) and sqSelected != ():  # если ты атакуешь или перемещаешь
                        # print("( ['bw': " + str(bw) + "] or not ['f': " + str(f) + "] ) and " + str(sqSelected != (row, col)) + " = (" + str(bw or not f) + ") " + str(sqSelected != (row, col)) + " = " + str((bw or not f) and sqSelected != (row, col)))
                        # bw = C.board[sqSelected[0]][sqSelected[1]][0] == C.nowMove  # bw = True когда фигура твоя
                        if not bw:
                            res = C.move(sqSelected, (row, col))
                            sqSelected = ()
                            if res != True:
                                sqError = (row, col)
                                clock_time = 5
                        elif bw:
                            sqSelected = (row, col)

        # <START DRAW BOARD>
        colors = [CHESS_COLORS[CHESS_COLOR][0], CHESS_COLORS[CHESS_COLOR][1]]
        for r in range(8):
            for c in range(8):
                color = colors[((r + c) % 2)]
                d = 1
                if (r + c) % 2 == 0:
                    d = CHESS_COLORS[CHESS_COLOR][2][3]
                if sqSelected == (r, c):
                    color = (CHESS_COLORS[CHESS_COLOR][((r + c) % 2)][0] + (CHESS_COLORS[CHESS_COLOR][2][0] * d),
                             CHESS_COLORS[CHESS_COLOR][((r + c) % 2)][1] + (CHESS_COLORS[CHESS_COLOR][2][1] * d),
                             CHESS_COLORS[CHESS_COLOR][((r + c) % 2)][2] + (CHESS_COLORS[CHESS_COLOR][2][2] * d))
                if sqError == (r, c) and clock_time > 0:
                    color = (CHESS_COLORS[CHESS_COLOR][((r + c) % 2)][0],
                             CHESS_COLORS[CHESS_COLOR][((r + c) % 2)][1] - (64 * d),
                             CHESS_COLORS[CHESS_COLOR][((r + c) % 2)][2] - (64 * d))
                P.draw.rect(S, color, P.Rect((c * SQ_SIZE) + marginVisual, (r * SQ_SIZE) + marginVisual, SQ_SIZE, SQ_SIZE))
                piece = C.board[r][c]
                if piece != '--':
                    S.blit(IMAGES[piece],
                           P.Rect((c * SQ_SIZE) + marginVisual, (r * SQ_SIZE) + marginVisual, SQ_SIZE, SQ_SIZE))
        # </END DRAW BOARD>
        # .....
        # {UPDATE APP}
        clock.tick(MAX_FPS)
        if clock_time > 0:
            clock_time = clock_time - 1
        P.display.flip()


# if __name__ == '__main__':
#    main()
main()
