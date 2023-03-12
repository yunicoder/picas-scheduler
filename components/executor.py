from typing import List

from .callback import CallBack, sort_cb_by_priority


class Executor:
    def __init__(self, executor_id: int):
        self.executor_id: int = executor_id  # エグゼキューターid
        self.callbacks: List[CallBack] = []  # エグゼキューターに割り当てられたcb
        self.priority: int = self.executor_id  # 優先度
        self.utilization = 0  # 利用率

        self.assigned_core_id: int = None  # 割り当てられたコアid

    def set_assigned_core(self, assigned_core_id: int) -> None:
        """割り当てられたコアidをセットする
        基本的にcore.assign_executor()から呼ばれる
        """
        self.assigned_core_id = assigned_core_id
        
    def assign_callbacks(self, callbacks: List[CallBack]) -> None:
        """コールバックをエグゼキューターに割り当てる"""
        # 割り当てられたコールバックに追加
        self.callbacks.extend(callbacks)

        # 優先度でソート
        self.callbacks = sort_cb_by_priority(self.callbacks)

        # 利用率の更新
        self._update_utilization()

        # 各コールバックのインスタンスにエグゼキューターを登録する
        for cb in callbacks:
            cb.set_assigned_executor(self.executor_id)

    def _update_utilization(self) -> None:
        """利用率を更新"""
        utilization = 0
        for cb in self.callbacks:
            utilization += cb.wcet / cb.period
        self.utilization = utilization
    
    def reinitialization(self) -> None:
        """エグゼキューターの再初期化"""
        self.callbacks = []
        self._update_utilization()

def sort_executors_by_utilization(executors: List[Executor]) -> List[Executor]:
    """利用率でソート"""
    return sorted(executors, key=lambda exe: exe.utilization)

def sort_executors_by_priority(executors: List[Executor]) -> List[Executor]:
    """優先度でソート"""
    return sorted(executors, key=lambda exe: exe.priority)