from Board import Board
from Letter import CellLetter, Coordinates

__author__ = 'akhtyamovpavel'

from PySide import QtCore

class Player(QtCore.QObject):
    choose_letter = QtCore.Signal(CellLetter)
    push_letter = QtCore.Signal(Coordinates)
    commit_word = QtCore.Signal()
    move_ended = QtCore.Signal()

    show_board = QtCore.Signal()

    after_letter_chosen = QtCore.Signal(CellLetter)
    after_letter_pushed = QtCore.Signal(Coordinates)
    after_word_committed = QtCore.Signal(str)
    reset_word = QtCore.Signal(Coordinates)
    don_t_make_move = QtCore.Signal()

    def __init__(self):
        super(Player, self).__init__()

        self.__list_of_words__ = list()
        self.__is_chosen__ = False
        self.__score__ = 0

        self.__temp_committed__ = False
        self.__is_committed__ = False
        self.__board__ = list()

    @QtCore.Slot()
    def begin_step(self):
        pass

    @QtCore.Slot(str)
    def bad_choose_letter(self, message):
        print(message)

    @QtCore.Slot(CellLetter)
    def letter_chosen(self, letter: CellLetter):
        print('Letter chosen')
        self.__is_chosen__ = True
        self.after_letter_chosen.emit(letter)

    @QtCore.Slot(str)
    def approve_word(self, word):
        self.__is_committed__ = True
        self.score += len(word)
        self.__list_of_words__.append(word)
        print('Word approved')
        print('Your current score is', self.__score__)
        self.__is_committed__ = False
        self.__is_chosen__ = False
        self.__temp_committed__ = True
        self.move_ended.emit()
        self.after_word_committed(word)

    @QtCore.Slot(list)
    def set_current_board(self, data):
        self.__board__ = data

    @QtCore.Slot(Coordinates)
    def on_board_reset_word(self, coordinates: Coordinates):
        self.__is_chosen__ = False
        self.__is_committed__ = False
        self.reset_word.emit(coordinates)

    # Slots from GraphicBoard

    @QtCore.Slot(CellLetter)
    def on_letter_chosen(self, letter: CellLetter):
        if self.__is_chosen__:
            return
        self.choose_letter.emit(letter)

    @QtCore.Slot(Coordinates)
    def on_letter_pushed(self, coordinates: Coordinates):
        if not self.__is_chosen__:
            return
        self.push_letter.emit(coordinates)
        self.after_letter_pushed.emit(coordinates)

    @QtCore.Slot()
    def on_word_committed(self):
        self.commit_word.emit()

    @QtCore.Slot()
    def send_end(self):
        self.don_t_make_move.emit()


    #Connections

    def connect_to_board(self, board: Board):
        #TODO: WHY FIRST

        self.choose_letter.connect(board.choose_letter_first)
        self.push_letter.connect(board.push_letter_first)
        self.commit_word.connect(board.got_commit_query)
        self.show_board.connect(board.show_board_to_player)


    def connect_to_manager(self, game_manager):
        pass

    def connect_to_interface(self, graphic_board):
        pass

    def run_process(self):
        pass

    def get_score(self):
        return self.__score__


if __name__ == '__main__':
    b = Board()
    p = Player()
    p.connect_to_board(b)