import katagames_sdk.engine as kataen
from katagames_sdk.engine import EventReceiver, EngineEvTypes, BaseGameState
from my_events import MyEvTypes
from same.data.constants import ColourScheme
from same.model import SameBoard
from same.model import Scorer
from same.views.pygame_client import PyGameClient
import katagames_sdk.api as katapi
import glvars


pygame = kataen.import_pygame()


class AppView(EventReceiver):
    def __init__(self, board, a_gui_client):
        super().__init__()
        self.board = board
        self.gui = a_gui_client
        self.saved_score = False
        a_gui_client.draw_board(balls=board.get_balls(), boxes=board.get_boxes())
        a_gui_client.draw_score_board(
            score=board.get_current_score(),
            highest_score=board.get_high_score(),
            current_move_score=0,
            moves=board.num_moves
        )

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            self._draw_things()

        elif ev.type == MyEvTypes.BallClicked:
            # refresh board display
            self.gui.draw_board(balls=self.board.get_balls(), boxes=self.board.get_boxes())

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE and self.board.is_game_over():
                self.pev(EngineEvTypes.POPSTATE)

    def _draw_things(self):
        board = self.board

        current_move_score = board.calculate_score(ball_position=self.gui.get_current_ball())
        self.gui.draw_score_board(
            score=board.get_current_score(),
            highest_score=board.get_high_score(),
            current_move_score=current_move_score,
            moves=board.num_moves
        )

        if board.is_game_over():
            self.gui.game_over(score=board.get_current_score(), high_score=board.get_high_score())

            if not self.saved_score:
                # debug
                # print('gameover detected &we try to save score')
                self.saved_score = True
                curr_score = board.get_current_score()
                res = katapi.push_score(glvars.acc_id, glvars.username, glvars.challenge_id, curr_score)
                if not res:
                    print('->WARNING<- smth went wrong with api.push_score(...)')
                    print(glvars.acc_id, glvars.username, glvars.challenge_id, curr_score)

                if curr_score > board.get_high_score():
                    board.update_high_score(new_high_score=curr_score)


class AppFlowCtrl(EventReceiver):

    def __init__(self, board, ref_view):
        super().__init__()
        self.board = board
        self._view = ref_view

    def proc_event(self, ev, source):
        if ev.type == pygame.MOUSEBUTTONDOWN:
            bposition = self._view.gui.get_clicked_ball(ev.pos)
            if not self.board.is_game_over():
                self.board.make_move(position=bposition)
                self.pev(MyEvTypes.BallClicked, position=bposition)


class PlayState(BaseGameState):
    def __init__(self, gs_ident, name):
        super().__init__(gs_ident, name)
        self.board = self.view = self.app_ctrl = None

    def enter(self):
        print('    ** Entering PlayState **')
        num_columns = 16
        num_rows = 14
        size = 32

        # creating components related to the PlayState
        a_scorer = Scorer()
        self.board = SameBoard(num_rows=num_rows, num_columns=num_columns, num_colours=4, scorer=a_scorer)
        a_gui_client = PyGameClient(
            size=size, num_rows=num_rows, num_columns=num_columns, score_board_height=100,
            colours=ColourScheme.MONFAVORITE
        )
        self.view = AppView(self.board, a_gui_client)
        self.app_ctrl = AppFlowCtrl(self.board, self.view)

        self.view.turn_on()
        self.app_ctrl.turn_on()

    def release(self):
        print('    ** leaving PlayState **')
        self.view.turn_off()
        self.app_ctrl.turn_off()
        self.view = self.app_ctrl = self.board = None
