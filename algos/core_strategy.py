import itertools
from pathlib import Path
from typing import Dict, List

from components.callback import CallBack, sort_cb_by_id
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, sort_nodes_by_highest_priority


def check_satisfy_all_core_strategies(core: Core, assigned_executors: List[Executor], executors: List[Executor], chains: List[Chain]) -> bool:
    """
    戦略 V と VI を満たすかどうか
    Args:
        core: 割り当てるコア
        assigned_executors: コアに割り当てられる予定のエグゼキューター
    """
    res = True
    all_executors = list(set(core.executors + assigned_executors))
    all_callbacks = [cb for exe in all_executors for cb in exe.callbacks]
    all_callbacks = sort_cb_by_id(all_callbacks)  # indexでソートしておく
    num_callbacks = len(all_callbacks)

    # 一つのコアに何個のチェインを割り当てるかによって戦略を使い分ける
    num_chains_containing_core = len(list(set([cb.chain_id for cb in all_callbacks])))
    if num_chains_containing_core == 1:
        res = _check_strategy_five(num_callbacks, all_callbacks, executors)
    else:
        res = _check_strategy_six(all_callbacks, executors, chains)
    return res

def _check_strategy_five(num_callbacks: int, all_callbacks: List[CallBack], executors: List[Executor]) -> bool:
    """戦略 V を満たすかどうか
    
    優先度を比較して以下だったらTrue
    (低インデックスコールバックを含むエグゼキュータ) < (高インデックスコールバックを実行するエグゼキュータ)
    """
    res = True
    for i in range(num_callbacks-1):
        low_cb = all_callbacks[i]
        high_cb = all_callbacks[i+1]

        # コールバックを含むエグゼキューターを抽出
        exe_containing_low_cb = [exe for exe in executors if exe.executor_id == low_cb.assigned_executor_id][0]
        exe_containing_high_cb = [exe for exe in executors if exe.executor_id == high_cb.assigned_executor_id][0]

        # 一つでも違反があればFalse
        # NOTE: exe_containing_low_cb.priority <= exe_containing_high_cb.priority を満たしたい
        if exe_containing_low_cb.priority > exe_containing_high_cb.priority:
            res = False
            break  # これ以降のコールバックをチェックする必要ないのでbreak
    return res

def _check_strategy_six(all_callbacks: List[CallBack], executors: List[Executor], chains: List[Chain]) -> bool:
    """戦略 VI を満たすかどうか
    
    任意の二つのチェーンlow_priority_chain, high_priority_chainについて、優先度を比較して以下だったらTrue
    (低優先度のチェイン内のコールバックを含むエグゼキュータ) < (高優先度のチェイン内のコールバックを含むエグゼキュータ)
    つまり、
    (低優先度のチェイン内のエグゼキュータの優先度の最大値) < (高優先度のチェイン内のエグゼキュータの優先度の最小値)
    """
    res = True

    chains_id_containing_core = list(set([cb.chain_id for cb in all_callbacks]))
    chains_containing_core = [chain for chain in chains if chain.chain_id in chains_id_containing_core]
    num_chains_containing_core = len(chains_containing_core)

    # チェインの全ての組み合わせ
    patterns = list(itertools.combinations(range(num_chains_containing_core), r=2))
    for chain_id_i, chain_id_j in patterns:
        chain_i = chains_containing_core[chain_id_i]
        chain_j = chains_containing_core[chain_id_j]

        # 優先度の高低
        low_priority_chain = chain_i if chain_i.priority < chain_j.priority else chain_j
        high_priority_chain = chain_i if chain_i.priority >= chain_j.priority else chain_j

        # チェインに含まれているコールバックが割り当てられているエグゼキューター一覧
        exe_id_containing_lpchain: List[int] = [cb.assigned_executor_id for cb in low_priority_chain.callbacks]
        exe_containing_lpchain: List[Executor] = [exe for exe in executors if exe.executor_id in exe_id_containing_lpchain]

        exe_id_containing_hpchain: List[int] = [cb.assigned_executor_id for cb in high_priority_chain.callbacks]
        exe_containing_hpchain: List[Executor] = [exe for exe in executors if exe.executor_id in exe_id_containing_hpchain]

        # 低優先度のチェイン(lpchain)内 の エグゼキュータの優先度の最大値
        max_exe_priority_containing_lpchain = max([exe.priority for exe in exe_containing_lpchain])
        # 高優先度のチェイン(hpchain)内 の エグゼキュータの優先度の最小値
        min_exe_priority_containing_hpchain = min([exe.priority for exe in exe_containing_hpchain])

        # 一つでも違反があればFalse
        # NOTE: max_exe_priority_containing_lpchain <= min_exe_priority_containing_hpchain を満たしたい
        if max_exe_priority_containing_lpchain > min_exe_priority_containing_hpchain:
            res = False
            break  # これ以降のコールバックをチェックする必要ないのでbreak
    return res
