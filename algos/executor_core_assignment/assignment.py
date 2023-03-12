from pathlib import Path
from typing import Dict, List

from components.callback import CallBack
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, sort_nodes_by_highest_priority

from .partA import partA_assignment
from .partB import partB_assignment


def executor_core_assignment(
    nodes: List[Node],
    executors: List[Executor],
    cores: List[Core],
    chains: List[Chain],
):
    not_assigned_nodes = nodes.copy()  # まだ割り当てられていないノード
    not_assigned_nodes = sort_nodes_by_highest_priority(not_assigned_nodes, is_decending=True)  # 最も高い優先度を降順でソート

    while len(not_assigned_nodes) != 0:
        selected_nodes = _select_node(not_assigned_nodes)  # 選択されたノードのサブセット
        if _is_exist_empty_executor(executors):
            # Part A in the paper
            not_assigned_nodes = partA_assignment(not_assigned_nodes, selected_nodes, executors, cores, chains)
        else:
            # Part B in the paper
            not_assigned_nodes = partB_assignment(not_assigned_nodes, selected_nodes, executors, cores, chains)


def _select_node(not_assigned_nodes: List[Node]) -> List[Node]:
    """利用率が1を超えないようにノードを抽出"""
    utilization = 0
    selected_nodes = []
    for node in not_assigned_nodes:
        utilization += node.utilization
        if utilization > 1:
            break
        selected_nodes.append(node)
    return selected_nodes


def _is_exist_empty_executor(executors: List[Executor]) -> bool:
    # エグゼキューターごとのコールバックのリスト
    num_callbacks_each_executor = [len(executor.callbacks) for executor in executors]
    return 0 in num_callbacks_each_executor  # コールバックの数が0のエグゼキューターがあるか
