from typing import List

from components.core import Core, sort_core_by_utilization
from components.executor import Executor, sort_executors_by_priority
from components.node import Node


def assign_lowest_utilization_core(selected_node: Node, cores: List[Core]):
    """最も優先度の低いコアに割り当てる
    
    (利用率が1以下のコアが見つからなかった) and (ノードが一つである) 場合に呼ばれる
    """
    lowest_utilization_core = sort_core_by_utilization(cores)[0]

    # 一時的なエグゼキューターを作成してそこにノードを割り当てる
    temp_executor = Executor(executor_id=99999)
    temp_executor.assign_callbacks(selected_node.callbacks)
    
    # 一時的なエグゼキューターを最も優先度の低いコアに割り当てる
    # NOTE: 次の関数でエグゼキューターは一つにまとめらる
    lowest_utilization_core.assign_executor(temp_executor)

    # エグゼキューターを一つにまとめる
    merge_all_executors_containing_core(lowest_utilization_core)


def merge_all_executors_containing_core(target_core: Core):
    """コアに含まれる全てのエグゼキューターを一つのエグゼキューターにマージする
    
    実行可能なコアが見つかったが、戦略を満たさなかった場合に呼ばれる
    """
    # 唯一残すエグゼキューター (最も優先度の低いエグゼキューター)
    merge_target_executor = sort_executors_by_priority(target_core.executors)[0]

    # 残すエグゼキューターに全てのコールバックを集約させる
    for exe in target_core.executors:
        if exe.executor_id == merge_target_executor.executor_id:
            continue  # 残すエグゼキューターは無視
        
        # 残すエグゼキューターにコールバックを移す
        merge_target_executor.assign_callbacks(exe.callbacks)
        exe.reinitialization()  # エグゼキューターの初期化

    # コアに再割り当てさせる
    target_core.reinitialization()  # 初期化
    target_core.assign_executor(merge_target_executor)
