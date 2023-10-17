import os

def get_uuids(path):
    """
    Get a list of UUIDs from the specified path.

    Args:
        path (str): The path to the directory containing the UUIDs.

    Returns:
        list: A list of UUIDs found in the directory.

    """
    uuids = os.listdir(path)
    uuids = [x for x in uuids if not x.startswith('.')]
    return uuids
