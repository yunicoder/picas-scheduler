from typing import List

from algos.core_strategy import check_satisfy_all_core_strategies
from algos.executor_core_assignment.partC import (
    assign_lowest_utilization_core, merge_all_executors_containing_core)
from algos.executor_strategy import check_satisfy_all_executor_strategies
from components.chain import Chain
from components.core import Core
from components.executor import Executor, sort_executors_by_utilization
from components.node import Node, sort_nodes_by_highest_priority


def partB_assignment(not_assigned_nodes: List[Node], selected_nodes: List[Node], executors: List[Executor], cores: List[Core], chains: List[Chain]) -> List[Node]:
    """
    選択されたノードを適切なエグゼキューターに割り当てる
    まだ割り当てられていないノードを更新して返す

    Args:
        not_assigned_nodes: まだ割り当てられていないノード
        selected_nodes: 選択されたノードのサブセット
        executors: エグゼキューターの集合
        cores: コアの集合
        chain: チェインの集合

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
                selected_nodes = sort_nodes_by_highest_priority(selected_nodes, is_decending=True)  # 最も高い優先度を降順でソート
                selected_nodes = selected_nodes[:-1]
                continue
            else:
                # 一つしかノードがない場合はPart Cで無理やり割り当てる
                assign_lowest_utilization_core(selected_nodes[0], cores)
                is_complete_assign_exe = True  # 無理やりコアに割り当てられたのでwhileループ終了
                break

        # 利用率が小さい順に走査して、ノードをエグゼキューターに割り当てる
        selected_executors = sort_executors_by_utilization(selected_executors)
        for exe in selected_executors:
            # exeが割り当てられているコア
            core_assigned_exe = [core for core in cores if core.core_id == exe.assigned_core_id][0]
            if (
                check_satisfy_all_executor_strategies(exe, [selected_nodes], chains)
                and check_satisfy_all_core_strategies(core_assigned_exe, [exe], executors, chains)
            ):
                callbacks = [cb for node in selected_nodes for cb in node.callbacks]
                exe.assign_callbacks(callbacks) # 割り当て
                is_complete_assign_exe = True
                break  # 割り当て完了
        
        if is_complete_assign_exe:
            break  # 割り当てられたのでwhileループ終了
        else:
            # どのエグゼキューターにも割り当てれれなかった場合、PartCで無理やり割り当てる
            # 最も利用率の低いエグゼキューターを含むコア
            target_core = [core for core in cores if core.core_id == selected_executors[0].assigned_core_id][0]
            merge_all_executors_containing_core(target_core)
            is_complete_assign_exe = True
            break  # 無理やりコアに割り当てられたのでwhileループ終了

    # エグゼキューターに割り当てられたノードは割り当てられていないノードリストからpop
    not_assigned_nodes = [node for node in not_assigned_nodes if node not in selected_nodes]

    return not_assigned_nodes

def _select_executors(selected_nodes: List[Node], cores: List[Core]) -> List[Executor]:
    """ノードとの利用率の合計が1以下のコア に含まれているエグゼキューターを抽出"""
    selected_executors = []

    selected_nodes_utilization = sum([node.utilization for node in selected_nodes])
    for core in cores:
        if (selected_nodes_utilization + core.utilization) <= 1:  
            selected_executors.extend(core.executors)  # コアに割り当てられているエグゼキューターを追加
 
    return selected_executors
