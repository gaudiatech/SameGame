import katagames_sdk.engine as kataen
from katagames_sdk.engine import EventReceiver, EngineEvTypes
from my_events import MyEvTypes
from same.data.constants import ColourScheme
from same.model import SameBoard
from same.model import Scorer
from same.views.pygame_client import PyGameClient


pygame = kataen.import_pygame()
game_over = False


class AppFlowCtrl(EventReceiver):
    def __init__(self, board, a_gui_client):
        super().__init__()

        self.board = board
        self.changed = False

        a_gui_client.draw_board(balls=board.get_balls(), boxes=board.get_boxes())
        a_gui_client.draw_score_board(
            score=board.get_current_score(),
            highest_score=board.get_high_score(),
            current_move_score=0,
            moves=board.num_moves
        )
        self._view = a_gui_client

    def proc_event(self, ev, source):
        global game_over

        if ev.type == pygame.QUIT:
            game_over = True

        if ev.type == pygame.MOUSEBUTTONDOWN:
            self.pev(
                MyEvTypes.BallClicked, position=self._view.get_clicked_ball(ev.pos)
            )

        elif ev.type == MyEvTypes.BallClicked:
            self.board.make_move(position=ev.position)
            self.changed = True

        elif ev.type == EngineEvTypes.PAINT:
            self._do_paint()

    def _do_paint(self):
        board = self.board

        if self.changed:
            self._view.draw_board(balls=board.get_balls(), boxes=board.get_boxes())
            self.changed = False

        current_move_score = board.calculate_score(ball_position=self._view.get_current_ball())
        self._view.draw_score_board(
            score=board.get_current_score(),
            highest_score=board.get_high_score(),
            current_move_score=current_move_score,
            moves=board.num_moves
        )

        if board.is_game_over():
            self._view.game_over(score=board.get_current_score(), high_score=board.get_high_score())
            if board.get_current_score() > board.get_high_score():
                board.update_high_score(new_high_score=board.get_current_score())


def run_game():
    global game_over
    num_columns = 16
    num_rows = 14
    size = 32

    kataen.init(kataen.HD_MODE)

    a_scorer = Scorer()
    board = SameBoard(num_rows=num_rows, num_columns=num_columns, num_colours=4, scorer=a_scorer)
    a_gui_client = PyGameClient(
        size=size, num_rows=num_rows, num_columns=num_columns, score_board_height=100, colours=ColourScheme.MONFAVORITE
    )

    app_ctrl = AppFlowCtrl(board, a_gui_client)
    gctrl = kataen.get_game_ctrl()
    app_ctrl.turn_on()
    gctrl.turn_on()

    gctrl.loop()
    kataen.cleanup()


if __name__ == '__main__':
    run_game()
