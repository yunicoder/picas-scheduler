from pathlib import Path
from typing import Dict, List

from algos.executor_core_assignment.partC import (
    assign_lowest_utilization_core, merge_all_executors_containing_core)
from algos.executor_strategy import check_satisfy_all_executor_strategies
from components.callback import CallBack
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor, sort_executors_by_utilization
from components.node import Node, sort_nodes_by_highest_priority


def partB_assignment(not_assigned_nodes: List[Node], selected_nodes: List[Node], executors: List[Executor], cores: List[Core]) -> List[Node]:
    """
    選択されたノードを適切なエグゼキューターに割り当てる
    まだ割り当てられていないノードを更新して返す

    Args:
        not_assigned_nodes: まだ割り当てられていないノード
        selected_nodes: 選択されたノードのサブセット
        executors: エグゼキューターの集合
        cores: コアの集合

    Returns:
        not_assigned_nodes: まだ割り当てられていないノード
    """
    # 割り当てが終了するまでループ
    is_complete_assign_exe = False
    while not is_complete_assign_exe:
        # ノードとの利用率の合計が1以下のコア に含まれているエグゼキューターを抽出
        selected_executors = _select_executors(selected_nodes, cores)

        # 割り当てるべきコアがない場合
        if len(selected_executors) == 0:
            if len(selected_nodes) > 1:
                # 選択するノードを減らして再挑戦
                selected_nodes = selected_nodes[:-1]
                continue
            else:
                # 一つしかノードがない場合はPart Cで無理やり割り当てる
                assign_lowest_utilization_core()
                is_complete_assign_exe = True  # 無理やりコアに割り当てられたのでwhileループ終了
                break

        # エグゼキューターを利用率が小さい順に走査して、ノードをエグゼキューターに割り当てる
        is_success_assign_exe = False
        selected_executors = sort_executors_by_utilization(selected_executors)
        for exe in selected_executors:
            if check_satisfy_all_executor_strategies(exe, [selected_nodes]):
                # HACK: 割り当てるのnode単位でやった方がいい
                callbacks = [cb for node in selected_nodes for cb in node.callbacks]
                for cb in callbacks:
                    exe.assign_callback(cb) # 割り当て
                is_success_assign_exe = True
                break  # 割り当て完了
        
        if is_success_assign_exe:
            # エグゼキューターに割り当てられたノードは割り当てられていないノードリストからpop
            not_assigned_nodes = [node for node in not_assigned_nodes if node not in selected_nodes]
            is_complete_assign_exe = True  # エグゼキューターに割り当てられたのでwhileループ終了
        else:
            # どのエグゼキューターにも割り当てれれなかった場合 Part C へ
            merge_all_executors_containing_core()
            is_complete_assign_exe = True  # 無理やりエグゼキューターに割り当てられたのでwhileループ終了

    return not_assigned_nodes

def _select_executors(selected_nodes: List[Node], cores: List[Core]) -> List[Executor]:
    """ノードとの利用率の合計が1以下のコア に含まれているエグゼキューターを抽出"""
    selected_executors = []

    selected_nodes_utilization = sum([node.utilization for node in selected_nodes])
    for core in cores:
        if (selected_nodes_utilization + core.utilization) <= 1:  
            selected_executors.extend(core.executors)  # コアに割り当てられているエグゼキューターを追加
 
    return selected_executors
