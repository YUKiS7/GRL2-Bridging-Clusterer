"""mcplayhd concept features, ported from section 03 of 02_preprocessing

one replay (dict, same json as the bulk files) in -> one feature row (dict) out, or None if not classifiable
"""
from grl.settings import CONCEPT_WINDOW_SIZE, Y_WEIGHT, MAX_CLICKS, EYE_HEIGHT


def last_block_tick(steps):
    """index of the last step that placed a non-AIR block, returns an int or None if no block was placed"""
    # TODO: copy from 02
    pass


def best_window_start(steps, last_tick):
    """finds the start of the window that covers the most distance without going down, returns an int or None"""
    # TODO: copy from 02
    pass


def blocks_before(steps, start):
    """set of (x, y, z) tuples of non-AIR blocks placed before the window"""
    # TODO: copy from 02
    pass


def concept_window_features(item, start, already_placed):
    """one feature row as dict, or None if the window has no new block"""
    # TODO: copy from 02
    pass


def replay_to_row(item):
    """NEW: the whole chain for one replay (what the loop in 02 does), returns a dict or None"""
    # TODO: last_block_tick -> best_window_start -> blocks_before -> concept_window_features
    pass
