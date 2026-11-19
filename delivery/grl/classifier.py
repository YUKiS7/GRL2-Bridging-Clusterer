"""new replays -> (cluster, confidence)"""


def cluster_id(mode, cluster):
    """global cluster id for the api, e.g. ("EXTRASHORT", 1) -> "EXTRASHORT_1" """
    # TODO
    pass


def transform_new(result, df_new_mode):
    """puts new replays of one mode into the same space as the training points (copied from 05)"""
    # TODO: copy from 05
    pass


def classify(replays):
    """list of replay dicts -> list of dicts {id, cluster, confidence}, cluster/confidence None if not classifiable

    keeps the input order, and every input id appears in the output
    """
    # TODO:
    # 1. replay_to_row for each replay (None -> not classifiable)
    # 2. group the rows by mode
    # 3. per mode: transform_new, get_knn(mode), predict + predict_proba
    # 4. build the results, including the None ones
    pass
