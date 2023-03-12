from typing import List

from algos.core_strategy import check_satisfy_all_core_strategies
from algos.executor_core_assignment.partC import (
    assign_lowest_utilization_core, merge_all_executors_containing_core)
from components.callback import CallBack
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, exclude_lowest_priority_in_nodes


def partA_assignment(
    not_assigned_nodes: List[Node],
    selected_nodes: List[Node],
    executors: List[Executor],
    cores: List[Core],
    chains: List[Chain],
) -> List[Node]:
    """
    選択されたノードを適切なエグゼキューターに、そのエグゼキューターを適切なコアを割り当てる
    まだ割り当てられていないノードを更新して返す

    Args:
        not_assigned_nodes: まだ割り当てられていないノード
        selected_nodes: 選択されたノードのサブセット
        executors: エグゼキューターの集合
        cores: コアの集合

    Returns:
        not_assigned_nodes: まだ割り当てられていないノード
    """
    selected_executor = _select_executor(executors)  # 今回割り当てるエグゼキューターを決定

    # 割り当てが終了するまでループ
    is_complete_assign_exe_and_core = False
    while not is_complete_assign_exe_and_core:
        # エグゼキューターの初期化 (空のエグゼキューターしかここでは登場しない)
        selected_executor.reinitialization()

        # 割り当て可能なCPUコアを選択する
        selected_cores = _select_cores(selected_executor, cores)
        
        # 割り当てるべきコアがない場合
        if len(selected_cores) == 0:
            if len(selected_nodes) > 1:
                # 選択されたノードの中で最も低いコールバックを含むノードを除去して再挑戦
                selected_nodes = exclude_lowest_priority_in_nodes(selected_nodes)
                continue
            else:
                # 一つしかノードがない場合はPartCで無理やり割り当てる
                assign_lowest_utilization_core(selected_nodes[0], cores)
                is_complete_assign_exe_and_core = True
                break  # 無理やりコアに割り当てられたのでwhileループ終了
        
        # 選択されたノードを一旦エグゼキューターに割り当てる
        callbacks = [cb for node in selected_nodes for cb in node.callbacks]
        selected_executor.assign_callbacks(callbacks)

        # 利用率の小さい順に走査して、エグゼキューターをコアに割り当てる
        selected_cores = sort_core_by_utilization(selected_cores)
        for core in selected_cores:
            if check_satisfy_all_core_strategies(core, [selected_executor], executors, chains):
                core.assign_executor(selected_executor)  # 割り当て
                is_complete_assign_exe_and_core = True
                break
        
        if is_complete_assign_exe_and_core:
            break  # 割り当てられたのでwhileループ終了
        else:
            # 実行可能なコアは見つかったが戦略を満たせない場合、
            # コア内のエグゼキューターを一つに集約して戦略を必ず満たせるようにする
            target_core = selected_cores[0]  # 最も利用率の低いコア
            merge_all_executors_containing_core(target_core)

            # エグゼキューター->コアの割り当て失敗
            selected_executor.reinitialization()  # エグゼキューターの初期化
            is_complete_assign_exe_and_core = False
            break  # 失敗

    if is_complete_assign_exe_and_core:
        # エグゼキューターに割り当てられたノードを、割り当てられていないノードリストからpop
        not_assigned_nodes = [node for node in not_assigned_nodes if node not in selected_nodes]

    return not_assigned_nodes


def _select_executor(executors: List[Executor]) -> Executor:
    """今回割り当てるエグゼキューターを決定
    NOTE: partAに入る前にチェックしているので必ず空のエグゼキューターが存在する
    """
    # NOTE: executorsは優先度順に並んでいる必要がある
    for exe in executors:
        if len(exe.callbacks) == 0:  # 空のエグゼキューター
            return exe

def _select_cores(executor: Executor, cores: List[Core]) -> List[Core]:
    """エグゼキューターとコアの利用率が合計1以下のコアのみ選択"""
    selected_core: List[Core] = []
    for core in cores:
        if executor.utilization + core.utilization <= 1:
            selected_core.append(core)
    
    if len(selected_core) != 0:
        # 利用率でソート
        selected_core = sort_core_by_utilization(selected_core)

    return selected_core

