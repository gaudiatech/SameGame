import random
import katagames_sdk.engine as kataen
from glvars import GameStates
from katagames_sdk.engine import EventReceiver, EngineEvTypes, BaseGameState, CgmEvent
from katagames_sdk.engine import gui, BIOS_BG_COL_DESC, BIOS_FG_COL_DESC
import katagames_sdk.api as katapi
import glvars


pygame = kataen.import_pygame()


def cb_playgame():
    if glvars.mobi_balance >= glvars.challengeprice:
        tmp = katapi.pay_for_challenge(glvars.acc_id)
        # tmp contains payment_feedback, numero_challenge, chall_seed
        if not tmp[0]:
            print('something s wrong with starting the challenge!')
        else:
            glvars.challenge_id = tmp[1]
            random.seed(tmp[2])  # seed has been set (constant random gen. for 1 challenge)
            print('challenge is starting...')
            kataen.get_manager().post(CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Play))


class IntroView(EventReceiver):
    def __init__(self):
        super().__init__()
        self._ft = pygame.font.Font(None, 33)
        self.txt_color = pygame.color.Color(BIOS_FG_COL_DESC)
        self._lbl = self._ft.render(
            'each attempt costs {} MOBI'.format(glvars.challengeprice), False, self.txt_color
        )

        self._bgcolor = pygame.color.Color(BIOS_BG_COL_DESC)
        scr_size = kataen.get_screen().get_size()
        w, h = self._lbl.get_size()
        self.blit_pos = [
            (scr_size[0] - w)//2, (scr_size[1] - h)//2
        ]
        self.blit_pos[0] -= 170
        self.blit_pos[1] -= 125

        self._balance_lbl = None
        bt_pos = (self.blit_pos[0], self.blit_pos[1]+200)
        self.lbl2_pos = (self.blit_pos[0], 180)

        # create buttons
        self._bt_play = gui.Button(self._ft, 'Confirm and play', bt_pos, callback=cb_playgame)

        def back_effect():
            kataen.get_manager().post(CgmEvent(EngineEvTypes.POPSTATE))
        self._bt_cancel = gui.Button(self._ft, 'Go back', (bt_pos[0], bt_pos[1]+90), callback=back_effect)

    def turn_on(self):
        super().turn_on()
        self._bt_play.turn_on()
        self._bt_cancel.turn_on()

    def turn_off(self):
        super().turn_off()
        self._bt_play.turn_off()
        self._bt_cancel.turn_off()

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bgcolor)

            ev.screen.blit(self._lbl, self.blit_pos)
            if self._balance_lbl is None:
                self._balance_lbl = self._ft.render(
                    'you now have {} MOBI'.format(glvars.mobi_balance), False, self.txt_color
                )
            ev.screen.blit(self._balance_lbl, self.lbl2_pos)

            # buttons
            ev.screen.blit(self._bt_play.image, self._bt_play.position)
            ev.screen.blit(self._bt_cancel.image, self._bt_cancel.position)


class IntroState(BaseGameState):
    """
    the goal of this state is to display a helpful msg
    in the case the user is "broke" and has no more credits to play.
    Otherwise we just ask for spending confirmation
    """

    def _refresh_katagames_info(self):
        glvars.mobi_balance = katapi.get_user_balance(glvars.acc_id)
        katapi.set_curr_game_id(glvars.UNIQUE_GAME_ID)
        glvars.challengeprice = katapi.get_challengeprice()

    def resume(self):
        self._refresh_katagames_info()
        self.v = IntroView()
        self.v.turn_on()

    def enter(self):
        self.resume()

    def pause(self):
        self.v.turn_off()
        # to be 100% sure we dont have a bug with buttons, we add:
        kataen.get_manager().soft_reset()

    def release(self):
        self.v.turn_off()
        self.v = None
