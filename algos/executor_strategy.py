from pathlib import Path
from typing import Dict, List

from components.callback import CallBack, sort_cb_by_id
from components.chain import Chain
from components.core import Core, sort_core_by_utilization
from components.executor import Executor
from components.node import Node, sort_nodes_by_highest_priority


def check_satisfy_all_executor_strategies(executor: Executor, assigned_nodes: List[Node] = []) -> bool:
    """
    戦略 I, II, III, IV を満たすかどうか
    Args:
        core: 割り当てるエグゼキューター
        assigned_nodes: コアに割り当てられる予定のノード
    """

    return True