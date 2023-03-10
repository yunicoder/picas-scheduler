from pathlib import Path
from typing import Dict, List

from algos.executor_strategy import check_satisfy_all_executor_strategies
from components.callback import CallBack
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, sort_nodes_by_highest_priority


def partB_assignment(not_assinned_nodes: List[Node], selected_nodes: List[Node], executors: List[Executor]) -> List[Node]:
    """
    選択されたノードを適切なエグゼキューターに割り当てる
    まだ割り当てられていないノードを更新して返す

    Args:
        not_assinned_nodes: まだ割り当てられていないノード
        selected_nodes: 選択されたノードのサブセット
        executors: エグゼキューターの集合

    Returns:
        not_assinned_nodes: まだ割り当てられていないノード
    """
    selected_executors = _select_executors(selected_nodes, executors)  # ノードとの利用率の合計が1以下のエグゼキューターを抽出

    # ノードをエグゼキューターに割り当てる
    is_success_assign_exe = False
    for exe in selected_executors:
        if check_satisfy_all_executor_strategies(exe, [selected_nodes]):
            # HACK: 割り当てるのnode単位でやった方がいい
            callbacks = [cb for node in selected_nodes for cb in node.callbacks]
            for cb in callbacks:
                exe.assign_callback(cb) # 割り当て
            is_success_assign_exe = True
            break
    
    if is_success_assign_exe:
        # エグゼキューターに割り当てられたので、割り当てられていないノードリストからpop
        not_assinned_nodes = [node for node in not_assinned_nodes if node not in selected_nodes]
    else:
        # どのエグゼキューターにも割り当てれれなかった場合 Part C へ
        pass

    return not_assinned_nodes

def _select_executors(selected_nodes: List[Node], executors: List[Executor]) -> List[Executor]:
    """ノードとエグゼキューターの利用率が合計1以下のエグゼキューターのみ選択"""
    selected_executors = []

    # NOTE: executorsは優先度順に並んでいる必要がある
    selected_nodes_utilization = sum([node.utilization for node in selected_nodes])
    for exe in executors:
        if (selected_nodes_utilization + exe.utilization) <= 1:  
            selected_executors.append(exe)
    
    return selected_executors


