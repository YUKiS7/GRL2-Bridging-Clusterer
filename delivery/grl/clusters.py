"""cluster descriptions for GET /clusters, built from cluster_labels_<method>.csv (output of 04)"""


def parse_votes(text):
    """technique_votes / suspicious_votes are saved as str of a dict in the csv -> back to a dict"""
    # TODO: hint: ast.literal_eval
    pass


def describe_clusters():
    """list of dicts {id, cluster_labels: [{label, share}], suspicious: [{level, count}]}, all 4 levels always present"""
    # TODO
    pass


def technique_names():
    """all technique labels that appear in the votes (the enum for GET /techniques)"""
    # TODO
    pass
