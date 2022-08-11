from typing import Dict, List


def combine_datasets(dataset1: List[str], dataset2: Dict[str, str]) :
    """
    :param dataset1:
    :param dataset2:
    :return: Merged Dataset
    """
    country_code = dataset1[0]
    return [dataset2[country_code], dataset1[1]]
