from typing import List

from .executor import Executor


class Core:
    def __init__(self, core_id: int):
        self.core_id: int = core_id  # コアid
        self.executors: List[Executor] = []  # コアに割り当てられたエグゼキューター
        self.utilization: int = 0  # 利用率
            
    def assign_executor(self, executor: Executor):
        """エグゼキューターをコアに割り当てる"""
        # 割り当て
        self.executors.append(executor)

        # # 優先度でソート
        # # NOTE: 優先度順に割り当てるならこれいらないかも
        # callbacks = sort_cb_by_priority(callbacks)

        # 利用率の更新
        self._update_utilization()

        # エグゼキューターのインスタンスにコアを登録する
        executor.set_assigned_core(self.core_id)

    def _update_utilization(self) -> None:
        """利用率を更新"""
        self.utilization = sum([exe.utilization for exe in self.executors])
    

def sort_core_by_utilization(cores: List[Core]) -> List[Core]:
    """利用率でソート"""
    return sorted(cores, key=lambda core: core.utilization)