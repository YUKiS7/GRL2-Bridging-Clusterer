"""cluster descriptions for GET /clusters, built from cluster_labels_<method>.csv (output of 04)"""
import ast

from grl.model_store import get_clusters_voted_labels
from grl.settings import SUSPICIOUS_LEVELS


def parse_votes(text):
    """technique_votes / suspicious_votes are saved as str of a dict in the csv -> back to a dict"""
    return ast.literal_eval(text)


def describe_clusters():
    """list of dicts {id, cluster_labels: [{label, share}], suspicious_levels: [{level, count}]}, all 4 levels always present"""
    result = []
    for row in get_clusters_voted_labels().to_dict("records"):
        cluster_votes = parse_votes(row["technique_votes"])
        cluster_votes_list = []

        suspicious_votes = parse_votes(row["suspicious_votes"])
        suspicious_votes_list = []

        for label, share in cluster_votes.items():
            cluster_votes_list.append({"label": label, "share": share})

        cluster_votes_list.sort(key=lambda vote: vote["share"], reverse=True)

        for number, text in SUSPICIOUS_LEVELS.items():
            count = suspicious_votes.get(number, 0)
            suspicious_votes_list.append({"level": text, "count": count})

        cluster_id = f"{row['mode']}_{row['cluster']}"

        result.append({
            "id": cluster_id,
            "cluster_labels": cluster_votes_list,
            "suspicious_levels": suspicious_votes_list,
        })

    return result



def technique_names():
    """all technique labels that appear in the votes"""
    result = []
    for cluster in describe_clusters(): # we get {id, cluster_labels, suspicious_levels}
        for cluster_labels in cluster["cluster_labels"]: # we get {label, share}
            technique = cluster_labels["label"] # we get e.g. ninja
            if technique not in result:
                result.append(technique)

    return result
