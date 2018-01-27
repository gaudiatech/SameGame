import sys

from same.controller import Board
from same.controller import Scorer
from same.data.constants import ColourScheme
from same.views.pygame_client import PyGameClient
from same.views.events import BallClickedEvent
from same.views.events import GameQuit

# These are the settings for pyinstaller
 # we are running in a bundle if sys.frozen else normal python
BASE_DIR = sys._MEIPASS if getattr(sys, 'frozen', False) else '.'  # pylint: disable=E1101, protected-access


class SameGame:

    def __init__(self, board, gui_client, scorer):
        self.board = board
        self.gui_client = gui_client
        self.scorer = scorer

    def play_game(self):
        changed = False
        self.gui_client.draw_board(balls=self.board.get_balls(), boxes=self.board.get_boxes())
        current_move_score = 0#self.board.get_score(position=self.gui_client.get_current_ball())
        self.gui_client.draw_score_board(score=self.board.get_current_score(), highest_score=self.board.get_high_score(), current_move_score=current_move_score)
        while True:
            # self.gui_client.draw_board(balls=self.board.get_balls(), boxes=self.board.get_boxes())

            # handle events
            for event in self.gui_client.get_events():
                if isinstance(event, BallClickedEvent):
                    self.board.make_move(position=event.position)
                    changed = True
                elif isinstance(event, GameQuit):
                    self.gui_client.end_game()
        #     # draw the board again
            if changed:
                self.gui_client.draw_board(balls=self.board.get_balls(), boxes=self.board.get_boxes())
                changed = False
            current_move_score = self.board.get_score(position=self.gui_client.get_current_ball())
            self.gui_client.draw_score_board(score=self.board.get_current_score(), highest_score=self.board.get_high_score(), current_move_score=current_move_score)
            # quit if the game is over
            if self.board.is_game_over():
                self.gui_client.end_game()
                break


if __name__ == '__main__':
    num_columns = 16
    num_rows = 14
    aScorer = Scorer()  # pylint: disable=invalid-name
    aBoard = Board(num_rows=num_rows, num_columns=num_columns, num_colours=4, scorer=aScorer)  # pylint: disable=invalid-name
    aGuiClient = PyGameClient(size=32, num_rows=num_rows, num_columns=num_columns, board_position=(10, 10), score_board_height=100, colours=ColourScheme.MONFAVORITE)  # pylint: disable=invalid-name
    sameGame = SameGame(board=aBoard, gui_client=aGuiClient, scorer=aScorer)  # pylint: disable=invalid-name
    sameGame.play_game()
