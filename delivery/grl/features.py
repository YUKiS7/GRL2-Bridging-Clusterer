"""mcplayhd concept features, ported from section 03 of 02_preprocessing

one replay (dict, same json as the bulk files) in -> one feature row (dict) out, or None if not classifiable

the settings (window size, y weight, ...) are not constants here: they come from the model bundle,
so a new bundle with other settings works without touching this file
"""
import numpy as np


def last_block_tick(steps):
    """index of the last step that placed a non-AIR block, returns an int or None if no block was placed"""
    tick_block_changed = None
    for i, step in enumerate(steps):
        for block_changed in step["blocksChanged"]:
            if block_changed["material"] != "AIR":
                tick_block_changed = i

    return tick_block_changed


def best_window_start(steps, last_tick, window_size, y_weight):
    """finds the start of the window that covers the most distance without going down, returns an int or None"""
    if last_tick is None:
        return None

    best_start = None
    best_distance = -1

    for i, step in enumerate(steps):
        # exit loop if too few ticks for window size
        if last_tick - i < window_size:
            break

        player_start_position = step["playerPosition"]
        player_end_position = steps[i + window_size - 1]["playerPosition"]

        # skip window if end position below start position
        if player_start_position["y"] > player_end_position["y"]:
            continue

        dx = player_start_position["x"] - player_end_position["x"]
        dy = player_start_position["y"] - player_end_position["y"]
        dz = player_start_position["z"] - player_end_position["z"]
        weighted_distance_squared = dx ** 2 + (dy * y_weight) ** 2 + dz ** 2

        # check window and save it if it is better
        if weighted_distance_squared > best_distance:
            best_start = i
            best_distance = weighted_distance_squared

    return best_start


def blocks_before(steps, start):
    """set of (x, y, z) tuples of non-AIR blocks placed before the window"""
    block_set = set()
    for step in steps[:start]:
        for block_changed in step["blocksChanged"]:
            if block_changed["material"] != "AIR":
                location = block_changed["loc"]
                block_set.add((location["x"], location["y"], location["z"]))

    return block_set


def concept_window_features(item, start, already_placed, window_size, max_clicks, eye_height):
    """one feature row as dict, or None if the window has no new block"""
    steps = item["stepData"]
    window = steps[start: start + window_size]

    x = np.array([step["playerPosition"]["x"] for step in window])
    dx = np.diff(x)
    y = np.array([step["playerPosition"]["y"] for step in window])
    dy = np.diff(y)
    z = np.array([step["playerPosition"]["z"] for step in window])
    dz = np.diff(z)
    yaw = np.array([step["playerPosition"]["yaw"] for step in window])
    yaw_change = (np.diff(yaw) + 180) % 360 - 180
    pitch = np.array([step["playerPosition"]["pitch"] for step in window])
    pitch_change = np.diff(pitch)

    row = {
        "idAnonymous": item["idAnonymous"],
        "fastBuilderMode": item["fastBuilderMode"],
    }

    row.update({f"dx_{i}": value for i, value in enumerate(dx, start=1)})
    row.update({f"dy_{i}": value for i, value in enumerate(dy, start=1)})
    row.update({f"dz_{i}": value for i, value in enumerate(dz, start=1)})
    row.update({f"yaw_change_{i}": value for i, value in enumerate(yaw_change, start=1)})
    row.update({f"pitch_change_{i}": value for i, value in enumerate(pitch_change, start=1)})
    row.update({f"sneaking_{i}": int(step["sneaking"]) for i, step in enumerate(window)})
    row.update({f"clicks_{i}": min(step["clicks"], max_clicks) for i, step in enumerate(window)})

    # remember new blocks, but only if not on location that a block was placed in before
    for i, step in enumerate(window):
        new_blocks = []
        for block_changed in step["blocksChanged"]:
            loc = block_changed["loc"]
            position = (loc["x"], loc["y"], loc["z"])
            if (block_changed["material"] != "AIR") and (position not in already_placed):
                new_blocks.append(position)
        already_placed.update(new_blocks)

        if new_blocks:
            row[f"new_block_{i}"] = 1
            block_x, block_y, block_z = new_blocks[0]
            player = step["playerPosition"]
            row[f"block_dx_{i}"] = block_x - player["x"]
            row[f"block_dy_{i}"] = block_y - (player["y"] + eye_height)
            row[f"block_dz_{i}"] = block_z - player["z"]
        else:
            row[f"new_block_{i}"] = 0
            row[f"block_dx_{i}"] = 0
            row[f"block_dy_{i}"] = 0
            row[f"block_dz_{i}"] = 0

    # drop window without any blocks placed
    if sum(row[f"new_block_{i}"] for i in range(window_size)) == 0:
        return None

    return row


def replay_to_row(item, feature_settings):
    """chain for one replay, returns a dict or None

    feature_settings: the dict from the model bundle, e.g. {"CONCEPT_WINDOW_SIZE": 50, "Y_WEIGHT": 0.5, ...}
    """
    window_size = feature_settings["CONCEPT_WINDOW_SIZE"]
    steps = item["stepData"]
    start = best_window_start(steps, last_block_tick(steps), window_size, feature_settings["Y_WEIGHT"])

    if start is None:
        return None

    return concept_window_features(item, start, blocks_before(steps, start), window_size,
                                   feature_settings["MAX_CLICKS"], feature_settings["EYE_HEIGHT"])
