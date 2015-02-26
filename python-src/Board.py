from Cell import Cell
from Letter import CellLetter, Coordinates
from PySide import QtCore
__author__ = 'user1'


class Board(QtCore.QObject):

    def __init__(self):
        super(Board, self).__init__()
        self.__board__ = list()
        self.FIRST_PLAYER = 1
        self.SECOND_PLAYER = 2
        self.__current_player__ = self.FIRST_PLAYER
        self.__is_changed__ = False
        self.__is_approved__ = False

        self.WIDTH = 5
        self.HEIGHT = 5

        """signals to WordCollector"""

        self.commit_letter = QtCore.Signal(str)
        self.commit_x = QtCore.Signal(int)
        self.commit_y = QtCore.Signal(int)
        self.commit_word = QtCore.Signal()
        self.commit_new = QtCore.Signal()
        self.add_new_letter = QtCore.Signal(CellLetter)

        self.move_ended = QtCore.Signal(str)
        self.choose_error = QtCore.Signal(str)
        self.letter_chosen = QtCore.Signal(tuple)
        self.send_board_first = QtCore.Signal(list)
        self.reset_word_first = QtCore.Signal(Coordinates)

        self.move_ended_second = QtCore.Signal(str)
        self.choose_error_second = QtCore.Signal(str)
        self.letter_chosen_second = QtCore.Signal(tuple)
        self.send_board_second = QtCore.Signal(list)
        self.reset_word_second = QtCore.Signal(Coordinates)

        """signals to GameManager"""

        self.send_cells_number = QtCore.Signal(int)

    """Slots from WordCollector"""

    @QtCore.Slot(Coordinates)
    def reset_state(self, coordinates : Coordinates):
        self.__is_changed__ = False
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if self.get_letter(i, j) != '-':
                    self.set_marked(i, j, False)
        print("Reset state from", coordinates.x, coordinates.y)
        self.set_letter(coordinates.x, coordinates.y, '-')
        self.set_marked(coordinates.x, coordinates.y, False)
        if self.__current_player__ == self.FIRST_PLAYER:
            self.reset_word_first.emit(coordinates)
        else:
            self.reset_word_second.emit(coordinates)

    @QtCore.Slot(str)
    def remake_move(self, word):
        print("New move")
        self.__is_changed__ = False
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if self.get_letter(i, j) != '-':
                    self.set_marked(i, j, False)
        if self.__is_approved__:
            self.__is_approved__ = False
            self.__current_player__ = 3 - self.__current_player__
            if self.__current_player__ == 2:
                self.move_ended.emit(word)
            else:
                self.move_ended_second.emit(word)

    @QtCore.Slot()
    def set_approved(self):
        self.__is_approved__ = True

    """Slots from Player"""

    @QtCore.Slot(CellLetter)
    def choose_letter_first(self, letter : CellLetter):
        self.change_letter(letter.x, letter.y, letter.letter)
        print("GET")


    @QtCore.Slot(CellLetter)
    def choose_letter_second(self, letter: CellLetter):
        self.change_letter(letter.x, letter.y, letter.letter)

    @QtCore.Slot()
    def show_board_to_player(self):
        result = []
        for i in range(self.HEIGHT):
            #TODO Inspect for index order
            result.append([])
            for j in range(self.WIDTH):
                result[i].append(self.get_letter(i, j))
        if self.__current_player__ == self.FIRST_PLAYER:
            self.send_board_first.emit(result)
        else:
            self.send_board_second.emit(result)

    @QtCore.Slot(Coordinates)
    def push_letter_first(self, coordinates: Coordinates):
        self.push_letter(coordinates)

    @QtCore.Slot(Coordinates)
    def push_letter_second(self, coordinates: Coordinates):
        self.push_letter(coordinates)

    @QtCore.Slot()
    def got_commit_query(self):
        self.commit_word.emit()

    """Slots from GameManager"""

    @QtCore.Slot()
    def get_number_of_cells(self):
        cnt = 0
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                if self.get_letter(i, j) == '-':
                    cnt += 1
        self.send_cells_number.emit(cnt)

    @QtCore.Slot()
    def show_board_to_manager(self):
        self.show_board()

    """Public methods"""
    def send_error(self, message):
        if self.__current_player__ == self.FIRST_PLAYER:
            self.choose_error.emit(message)
        else:
            self.choose_error_second.emit(message)

    def range_check(self, x, y):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            self.send_error("Wrong range of cell")
            return False
        return True

    def set_first_player(self, player):
        self.__current_player__ = player

    def set_first_word(self, first_word: str):
        for i in range(self.HEIGHT):
            self.__board__[self.WIDTH // 2][i].set_letter(first_word[i])

    def setup_connection(self, word_collector):
        pass

    def connect_to_players(self, player1, player2):
        pass

    def connect_to_game_manager(self, game_manager):
        pass

    def show_board(self):
        cnt = 0
        for index_row in range(self.WIDTH):
            for index_cell in range(self.HEIGHT):
                print(self.__board__[index_row][index_cell].get_letter(), end=" ")
            print()


    def change_letter(self, x, y, letter):
        if self.has_changed():
            self.send_error("Cell has already chosen")
            return
        if not self.range_check(x, y):
            return
        if self.get_letter(x, y) != '-':
            self.send_error("Error cell chosen")
            return
        self.__board__[x][y].set_letter(letter)
        self.__is_changed__ = True
        self.show_board()
        send_letter = CellLetter(x, y, letter)
        self.add_new_letter.emit(send_letter)
        if self.__current_player__ == self.FIRST_PLAYER:
            self.letter_chosen.emit(send_letter)
        else:
            self.letter_chosen.emit(send_letter)

    def push_letter(self, coordinates: Coordinates):
        if not self.range_check(coordinates.x, coordinates.y):
            return
        if self.get_letter(coordinates.x, coordinates.y) == '-':
            return
        self.commit_letter.emit(self.get_letter(coordinates.x, coordinates.y))
        self.commit_x(coordinates.x)
        self.commit_y(coordinates.y)
        if self.is_marked(coordinates.x, coordinates.y):
            self.commit_new.emit(1)
        else:
            self.commit_new.emit(0)

    def is_marked(self, x, y):
        return self.__board__[x][y].is_marked()

    def set_marked(self, x, y, value):
        self.__board__[x][y].set_marked(value)

    def get_letter(self, x, y):
        return self.__board__[x][y]

    def set_letter(self, x, y, letter):
        self.__board__[x][y].set_letter(letter)

    def has_changed(self):
        return self.__is_changed__

    def init_board(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        for i in range(width):
            for j in range(height):
                self.__board__.append([])
                self.__board__[i].append(Cell('-'))

if __name__ == '__main__':
    b = Board()
    b.init_board(6, 5)
    b.set_first_word('carry')
    b.show_board()