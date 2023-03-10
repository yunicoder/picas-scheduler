from pathlib import Path
from typing import Dict, List

from components.callback import CallBack, sort_cb_by_id
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, sort_nodes_by_highest_priority


def check_satisfy_all_core_strategies(core: Core, assigned_executors: List[Executor] = []) -> bool:
    """
    戦略 V と VI を満たすかどうか
    Args:
        core: 割り当てるコア
        assigned_executors: コアに割り当てられる予定のエグゼキューター
    """
    res = False
    all_executors = list(set(core.executors + assigned_executors))
    all_callbacks = [cb for exe in all_executors for cb in exe.callbacks]
    all_callbacks = sort_cb_by_id(all_callbacks)  # indexでソートしておく
    num_callbacks = len(all_callbacks)

    # 何個のチェインのコールバックを持っているかによって戦略を使い分ける
    num_chains_containing_callbacks = list(set([cb.chain_id for cb in all_callbacks]))
    if num_chains_containing_callbacks == 1:
        res = _check_strategy_five(num_callbacks, all_callbacks)
    else:
        res = _check_strategy_six()
    return res

def _check_strategy_five(num_callbacks: int, all_callbacks: List[CallBack]) -> bool:
    """戦略 V を満たすかどうか
    
    優先度を比較して以下だったらTrue
    (低インデックスコールバックを含むエグゼキュータ) < (高インデックスコールバックを実行するエグゼキュータ)
    """
    res = False
    for i in range(num_callbacks-1):
        low_cb = all_callbacks[i]
        high_cb = all_callbacks[i+1]
    return True

def _check_strategy_six():
    res = False
    return True