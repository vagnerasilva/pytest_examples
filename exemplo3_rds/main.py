import boto3


class MyRDSManager:
    def __init__(self) -> None:
        self._rds_client = boto3.client("rds")

    def delete_db_cluster_snapshot(self) -> None:
        self._rds_client.delete_db_cluster_snapshot(DBClusterSnapshotIdentifier="ABC")

    def get_snapshots(self) -> list[dict]:
        snapshots = []

        paginator = self._rds_client.get_paginator("describe_db_cluster_snapshots")
        pages = paginator.paginate(DBClusterIdentifier="MyCluster")

        for page in pages:
            page_snapshots = page.get("DBClusterSnapshots")
            for snapshot in page_snapshots:
                snapshots.append(snapshot)

        return snapshots