from typing import List

from .callback import CallBack, sort_cb_by_id


class Chain:
    def __init__(self, chain_id: int, callbacks: List[CallBack]):
        self.chain_id: int = chain_id  # チェインid
        self.callbacks: List[CallBack] = self._cb_preprocess(callbacks)  # チェインに含まれているcb
        self.priority: int = callbacks[0].priority  # 優先度 (一番初めのタイマーコールバックの優先度と同じ)
        self.wcet_sum: int = sum([cb.wcet for cb in callbacks]) # 最悪実行の合計


    def _cb_preprocess(self, callbacks: List[CallBack]) -> List[CallBack]:
        """コールバックの前処理"""
        callbacks = sort_cb_by_id(callbacks)  # コールバックidでソート
        
        # TODO: 最初のコールバックだけがタイマーコールバックかどうかチェックしたい
        # check_first_cb_is_tcb()
        
        return callbacks