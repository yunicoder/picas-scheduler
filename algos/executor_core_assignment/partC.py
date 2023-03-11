from pathlib import Path
from typing import Dict, List

from algos.executor_strategy import check_satisfy_all_executor_strategies
from components.callback import CallBack
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, sort_nodes_by_highest_priority


def assign_lowest_utilization_core():
    """最も優先度の低いコアに割り当てる
    
    (利用率が1以下のコアが見つからなかった) and (ノードが一つである) 場合に呼ばれる
    """
    return


def merge_all_executors_containing_core():
    """コアに含まれる全てのエグゼキューターを一つのエグゼキューターにマージする"""
    return