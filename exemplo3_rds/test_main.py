import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from pytest_examples.exemplo3_rds.main import MyRDSManager


@pytest.fixture(scope="function")
def prepare_mock():
    with patch("main.boto3.client") as mock_boto_client:
        # the first thing to do is to set the return_value attribute as itself
        # this will return the mock itself when the code runs `boto3.client("rds")`
        mock_boto_client.return_value = mock_boto_client

        def mock_paginate_describe_db_cluster_snapshots(*args, **kwargs):
            snapshot_type = kwargs.get(
                "SnapshotType"
            )  # get all the parameter passed to the call

            return [{
                "DBClusterSnapshots": [
                {
                    "DBClusterSnapshotIdentifier": "ABC",
                    "SnapshotCreationTime": "2024-01-01",
                    "SnapshotType": "manual",
                }
            ]}]

        mock_boto_client.get_paginator = Mock()
        mock_paginator = Mock(return_value=None)
        mock_paginator.paginate = Mock(return_value=None)
        mock_paginator.paginate.side_effect = mock_paginate_describe_db_cluster_snapshots

        mock_boto_client.get_paginator.return_value = mock_paginator

        mock_boto_client.delete_db_cluster_snapshot = Mock(return_value=None)

        my_rds = MyRDSManager()

        yield my_rds, mock_boto_client


def test_one(prepare_mock):
    mock_my_rds, mock_boto_client = prepare_mock

    mock_my_rds.delete_db_cluster_snapshot()

    mock_boto_client.delete_db_cluster_snapshot.assert_called_once_with(DBClusterSnapshotIdentifier="ABC")

    result = mock_my_rds.get_snapshots()

    assert result == [{
        "DBClusterSnapshotIdentifier": "ABC",
        "SnapshotCreationTime": "2024-01-01",
        "SnapshotType": "manual",
    }]
