import itertools
from typing import List

from components.callback import CallBack, sort_cb_by_id
from components.chain import Chain
from components.executor import Executor
from components.node import Node


def check_satisfy_all_executor_strategies(executor: Executor, assigned_nodes: List[Node], chains: List[Chain]) -> bool:
    """
    戦略 I, II, III, IV を満たすかどうか
    Args:
        core: 割り当てるエグゼキューター
        assigned_nodes: コアに割り当てられる予定のノード
    """
    res = True
    all_callbacks = [cb for cb in executor.callbacks] + [cb for node in assigned_nodes for cb in node.callbacks]
    all_callbacks = list(set(all_callbacks))

    # エグゼキューターに何個のチェインを割り当てるかによって戦略を使い分ける
    num_chains_containing_executor = len(list(set([cb.chain_id for cb in all_callbacks])))

    # タイマーコールバックが含まれているかによって戦略を使い分ける
    is_contain_timer_callback = any([cb.is_timer_callback for cb in all_callbacks])

    if num_chains_containing_executor == 1:
        if not is_contain_timer_callback:
            res = _check_strategy_one(all_callbacks)
        else:
            res = _check_strategy_two(all_callbacks)
    else:  # 複数のチェインが存在する場合
        if not is_contain_timer_callback:
            res = _check_strategy_three(all_callbacks, chains)
        else:
            res = _check_strategy_four(all_callbacks, chains)

    return res


def _check_strategy_one(all_regular_callbacks: List[CallBack]) -> bool:
    """戦略 I を満たすかどうか
    
    優先度を比較して以下だったらTrue
    レギュラーコールバックの優先度がチェイン内の順序と逆に割り当てられている
    """
    res = True
    all_regular_callbacks = sort_cb_by_id(all_regular_callbacks)
    
    # 隣同士の優先度を比較してどんどん大きくなっていっていればTrue
    for i in range(len(all_regular_callbacks) - 1):
        if all_regular_callbacks[i].priority < all_regular_callbacks[i+1].priority:
            res = False
            break  # これ以降のコールバックをチェックする必要ないのでbreak

    # この戦略を満たさないことはあり得ないので一応確認 (for debug)
    _debug_unsatisfy(res, "I")

    return res

def _check_strategy_two(all_callbacks: List[CallBack]) -> bool:
    """戦略 II を満たすかどうか
    
    優先度を比較して以下だったらTrue
    レギュラーコールバックにタイマコールバックよりも高い優先度を与える

    ※レギュラーコールバックのスケジューリングは戦略Iに従う
    """
    # チェイン内のコールバックを分類する
    # NOTE: 一つのチェインにtcbは一つしかない
    timer_callback = [cb for cb in all_callbacks if cb.is_timer_callback][0]
    regular_callbacks = [cb for cb in all_callbacks if not cb.is_timer_callback]

    # 戦略IIは以下を満たせばTrue
    # (タイマーコールバックの優先度) < (レギュラーコールバック優先度の最小値)
    priority_tcb = timer_callback.priority
    min_priority_rcb = min([cb.priority for cb in regular_callbacks])
    if priority_tcb < min_priority_rcb:
        is_satisfy_strategy_two = True
    else:
        is_satisfy_strategy_two = False

    # レギュラーコールバックについては戦略Iをチェックする
    is_satisfy_strategy_one = _check_strategy_one(regular_callbacks)

    # この戦略を満たさないことはあり得ないので一応確認 (for debug)
    _debug_unsatisfy(is_satisfy_strategy_one, "I in II")
    _debug_unsatisfy(is_satisfy_strategy_two, "II")

    return is_satisfy_strategy_one and is_satisfy_strategy_two

def _check_strategy_three(all_callbacks: List[CallBack], chains: List[Chain]) -> bool:
    """戦略 III を満たすかどうか
    
    任意の二つのチェーンについて、優先度を比較して以下だったらTrue
    (低優先度のチェイン内の全てのコールバック優先度) < (高優先度のチェイン内の全てのコールバック優先度)
    つまり、
    (低優先度のチェイン内のコールバック優先度の最大値) < (高優先度のチェイン内のコールバック優先度の最小値)
    
    ※各チェーンのコールバックの優先度の割り当ては戦略Iに従う
    """
    res = True
    chains_id_containing_executor = list(set([cb.chain_id for cb in all_callbacks]))
    chains_containing_executor = [chain for chain in chains if chain.chain_id in chains_id_containing_executor]
    num_chains_containing_executor = len(chains_containing_executor)

    # チェインの全ての組み合わせ
    patterns = list(itertools.combinations(range(num_chains_containing_executor), r=2))
    for chain_id_i, chain_id_j in patterns:
        chain_i = chains_containing_executor[chain_id_i]
        chain_j = chains_containing_executor[chain_id_j]

        # 優先度の高低
        low_priority_chain = chain_i if chain_i.priority < chain_j.priority else chain_j
        high_priority_chain = chain_i if chain_i.priority >= chain_j.priority else chain_j

        # 低優先度のチェイン(lpchain)内のコールバック優先度の最大値
        max_cb_priority_containing_lpchain = max([cb.priority for cb in low_priority_chain.callbacks])
        # 高優先度のチェイン(hpchain)内のコールバック優先度の最小値
        min_cb_priority_containing_hpchain = min([cb.priority for cb in high_priority_chain.callbacks])

        # 戦略IIIのチェック
        if max_cb_priority_containing_lpchain < min_cb_priority_containing_hpchain:
            is_satisfy_strategy_three = True
        else:
            is_satisfy_strategy_three = False


        # 各チェインのレギュラーコールバックについては戦略Iをチェックする
        is_satisfy_strategy_one = (
            _check_strategy_one([cb for cb in low_priority_chain.callbacks])  # rcb in lpchain
            and _check_strategy_one([cb for cb in high_priority_chain.callbacks])  # rcb in hpchain
        )

        res = res and is_satisfy_strategy_one and is_satisfy_strategy_three
        if not res:
            # この戦略を満たさないことはあり得ないので一応確認 (for debug)
            _debug_unsatisfy(is_satisfy_strategy_one, "I in III")
            _debug_unsatisfy(is_satisfy_strategy_three, "III")    
            break  # これ以降のチェインをチェックする必要ないのでbreak

    return res

def _check_strategy_four(all_callbacks: List[CallBack], chains: List[Chain]) -> bool:
    """戦略 IV を満たすかどうか
    
    任意の二つのチェーンについて、優先度を比較して以下だったらTrue
    (低優先度のチェイン内のタイマーコールバック優先度) < (高優先度のチェイン内のタイマーコールバック優先度)
    
    ※各チェーンは個別に戦略IIに従う
    """
    chains_id_containing_executor = list(set([cb.chain_id for cb in all_callbacks]))
    chains_containing_executor = [chain for chain in chains if chain.chain_id in chains_id_containing_executor]
    num_chains_containing_executor = len(chains_containing_executor)

    # チェインの全ての組み合わせ
    patterns = list(itertools.combinations(range(num_chains_containing_executor), r=2))
    for chain_id_i, chain_id_j in patterns:
        chain_i = chains_containing_executor[chain_id_i]
        chain_j = chains_containing_executor[chain_id_j]

        # 優先度の高低
        low_priority_chain = chain_i if chain_i.priority < chain_j.priority else chain_j
        high_priority_chain = chain_i if chain_i.priority >= chain_j.priority else chain_j

        # 各チェイン内のタイマーコールバック
        # NOTE: タイマーコールバックは各チェインに一つしかない
        tcb_containing_lpchain = [cb for cb in low_priority_chain.callbacks if cb.is_timer_callback][0]
        tcb_containing_hpchain = [cb for cb in high_priority_chain.callbacks if cb.is_timer_callback][0]
        
        # 戦略IVのチェック
        if tcb_containing_lpchain.priority < tcb_containing_hpchain.priority:
            is_satisfy_strategy_four = True
        else:
            is_satisfy_strategy_four = False


        # 各チェインのチェックは戦略IIをチェックする
        is_satisfy_strategy_two = (
            _check_strategy_two([cb for cb in low_priority_chain.callbacks])  # lpchain
            and _check_strategy_two([cb for cb in high_priority_chain.callbacks])  # hpchain
        )
        
        
        res = res and is_satisfy_strategy_two and is_satisfy_strategy_four
        if not res:
            # この戦略を満たさないことはあり得ないので一応確認 (for debug)
            _debug_unsatisfy(is_satisfy_strategy_two, "II in IV")
            _debug_unsatisfy(is_satisfy_strategy_four, "IV")    
            break  # これ以降のチェインをチェックする必要ないのでbreak

    return res


def _debug_unsatisfy(flag: bool, strategy_number: int) -> None:
    """この戦略を満たさないことはあり得ないのでfalseになったら例外投げる"""
    if not flag:
        raise Exception(f"not satisfy strategy {strategy_number}. どこかにバグあるよ")