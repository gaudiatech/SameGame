import katagames_sdk.engine as kataen
import glvars


def run_game():
    kataen.init(kataen.HD_MODE)
    kataen.tag_multistate(glvars.GameStates, glvars)

    gctrl = kataen.get_game_ctrl()
    gctrl.turn_on()
    gctrl.loop()


if __name__ == '__main__':
    run_game()
