from katagames_sdk.engine import enum_builder


# kata.games related
username = None
acc_id = None
mobi_balance = None
challengeprice = None
challenge_id = None

# specific
UNIQUE_GAME_ID = 6
GameStates = enum_builder(
    'Intro',
    'Play'
)
