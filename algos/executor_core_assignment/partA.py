from pathlib import Path
from typing import Dict, List

from algos.core_strategy import check_satisfy_all_core_strategies
from components.callback import CallBack
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, sort_nodes_by_highest_priority


def partA_assignment(
    not_assinned_nodes: List[Node],
    selected_nodes: List[Node],
    executors: List[Executor],
    cores: List[Core],
    chains: List[Chain],
) -> List[Node]:
    """
    選択されたノードを適切なエグゼキューターに、そのエグゼキューターを適切なコアを割り当てる
    まだ割り当てられていないノードを更新して返す

    Args:
        not_assinned_nodes: まだ割り当てられていないノード
        selected_nodes: 選択されたノードのサブセット
        executors: エグゼキューターの集合
        cores: コアの集合

    Returns:
        not_assinned_nodes: まだ割り当てられていないノード
    """
    selected_executor = _select_executor(executors)  # 今回割り当てるエグゼキューターを決定

    # 割り当てが終了するまでループ
    is_complete_assign_exe_and_core = False
    while not is_complete_assign_exe_and_core:
        # コールバックをエグゼキューターに割り当てる
        # HACK: 割り当てるのnode単位でやった方がいい
        callbacks = [cb for node in selected_nodes for cb in node.callbacks]
        selected_executor.callbacks = []  # 空に初期化
        for cb in callbacks:
            selected_executor.assign_callback(cb)

        # 割り当て可能なCPUコアを選択する
        selected_cores = _select_cores(selected_executor, cores)
        
        # 割り当てるべきコアがない場合
        if len(selected_cores) == 0:
            if len(selected_nodes) > 1:
                # 選択するノードを減らして再挑戦
                selected_nodes = selected_nodes[:-1]
                continue
            else:
                # 一つしかノードがない場合はPart C
                break

        # エグゼキューターをコアに割り当てる
        is_success_assign_core = False
        for core in selected_cores:
            if check_satisfy_all_core_strategies(core, [selected_executor], executors, chains):
                core.assign_executor(selected_executor)  # 割り当て
                is_success_assign_core = True
                is_complete_assign_exe_and_core = True
                break
        
        # どのコアにも割り当てれれなかった場合
        if not is_success_assign_core:
            # go to Part C
            break
    
    if is_complete_assign_exe_and_core:
        # エグゼキューターに割り当てられたので、割り当てられていないノードリストからpop
        not_assinned_nodes = [node for node in not_assinned_nodes if node not in selected_nodes]
    else:
        # go to Part C
        pass

    return not_assinned_nodes


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
