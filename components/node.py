from typing import List

from .callback import CallBack, sort_cb_by_id, sort_cb_by_priority


class Node:
    def __init__(self, node_id: int, callbacks: List[CallBack]):
        self.node_id: int = node_id  # ノードid
        self.callbacks: List[CallBack] = self._cb_preprocess(callbacks)  # ノードに含まれているcb
        self.utilization: int = self._calc_utilization(callbacks)  # 利用率
        self.highest_priority: int = None  # このノードの中で最も高い優先度

    def _cb_preprocess(self, callbacks: List[CallBack]) -> List[CallBack]:
        """コールバックの前処理"""
        callbacks = sort_cb_by_id(callbacks)  # コールバックidでソート
        return callbacks
    
    def _calc_utilization(self, callbacks: List[CallBack]) -> int:
        utilization = 0
        for cb in callbacks:
            utilization += cb.wcet / cb.period
        return utilization
    
    def set_highest_priority(self) -> None:
        """このノードの中で最も高い優先度を計算してセットする
        NOTE: コールバックに優先度が割り当てられてからしか呼び出せない
        """
        self.highest_priority = max([cb.priority for cb in self.callbacks])

def set_highest_priorities(nodes: List[Node]) -> List[Node]:
    """ノードの中で最も高い優先度を計算してセットする
    NOTE: コールバックに優先度が割り当てられてからしか呼び出せない
    """
    for node in nodes:
        node.set_highest_priority()
    return nodes

def sort_nodes_by_highest_priority(nodes: List[Node]) -> List[Node]:
    """最も高い優先度でソート"""
    # 降順にしないといけない点に注意
    return sorted(nodes, key=lambda node: node.highest_priority, reverse=True)
 
def exclude_lowest_priority_in_nodes(nodes: List[Node]) -> List[Node]:
    """最も優先度の低いコールバックを含むノードを除去して返す"""
    all_callbacks = [cb for node in nodes for cb in node.callbacks]
    
    # 最も優先度の低いコールバック
    lowest_priority_callback = sort_cb_by_priority(all_callbacks)[0]

    # 最も優先度の低いコールバックを含むノードを除去
    nodes = [node for node in nodes if node.node_id != lowest_priority_callback.node_id]

    return nodes