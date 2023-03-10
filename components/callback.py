from dataclasses import dataclass
from typing import List


class CallBack:
    def __init__(self, callback_id: int, wcet: int, period: int, node_id: int, chain_id: int):
        self.callback_id: int = callback_id  # コールバックid
        self.wcet: int = wcet # 最悪実行時間
        self.period: int = period  # 周期 (相対デッドライン)
        self.priority: int = None  # 優先度
        self.node_id: int = node_id  # ノードid
        self.chain_id: int = chain_id  # チェインid

        self.assigned_executor_id: int = None  # 割り当てられたエグゼキューターid

    def set_assigned_executor(self, assigned_executor_id: int):
        """割り当てられたエグゼキューターidをセットする
        基本的にexecutor.assign_callback()から呼ばれる
        """
        self.assigned_executor = assigned_executor_id

def assign_period(callbacks: List[CallBack]) -> List[CallBack]:
    """各コールバックの周期を決定する
    (レギュラーコールバックの周期) = (同チェイン内のタイマーコールバックの周期)
    """
    # チェインごとの周期を抽出
    chain_id_to_period = dict()
    for cb in callbacks:
        if cb.period != 0:  # タイマーコールバック
            chain_id_to_period[cb.chain_id] = cb.period
    
    # レギュラーコールバックにも周期を割り当てる
    for cb in callbacks:
        if cb.period == 0:  # レギュラーコールバック
            cb.period = chain_id_to_period[cb.chain_id]
    return callbacks

def sort_cb_by_id(callbacks: List[CallBack]) -> List[CallBack]:
    """コールバックidでソート"""
    return sorted(callbacks, key=lambda cb: cb.callback_id)

def sort_cb_by_priority(callbacks: List[CallBack]) -> List[CallBack]:
    """優先度でソート"""
    return sorted(callbacks, key=lambda cb: cb.priority)