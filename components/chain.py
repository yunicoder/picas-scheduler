from typing import List

from .callback import CallBack, sort_cb_by_id


class Chain:
    def __init__(self, chain_id: int, callbacks: List[CallBack]):
        self.chain_id: int = chain_id  # チェインid
        self.callbacks: List[CallBack] = self._cb_preprocess(callbacks)  # チェインに含まれているcb
        self.wcet_sum: int = sum([cb.wcet for cb in callbacks]) # 最悪実行の合計
        self.priority: int = None  # 優先度 TODO:これ自分で勝手に決めていいっけ？


    def _cb_preprocess(self, callbacks: List[CallBack]) -> List[CallBack]:
        """コールバックの前処理"""
        callbacks = sort_cb_by_id(callbacks)  # コールバックidでソート
        
        # TODO: 最初のコールバックだけがタイマーコールバックかどうかチェックしたい
        # check_first_cb_is_tcb()
        
        return callbacks
    
    def set_priority(self) -> None:
        """コールバックの優先度を元にチェインの優先度をセットする
        NOTE: コールバックに優先度が割り当てられてからしか呼び出せない
        """
        # 一番初めのタイマーコールバックの優先度と同じ
        self.priority: int = self.callbacks[0].priority

def set_chains_priority(chains: List[Chain]) -> List[Chain]:
    """コールバックの優先度を元にチェインの優先度をセットする
    NOTE: コールバックに優先度が割り当てられてからしか呼び出せない
    """
    for chain in chains:
        chain.set_priority()
    return chains