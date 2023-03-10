from typing import Dict, List, Tuple

from .callback import CallBack, assign_period
from .chain import Chain
from .core import Core
from .executor import Executor
from .node import Node


def initial_components(
    input_cbs: Dict[str, Dict[str, int]],
    num_executors: int,
    num_cores: int,
) -> Tuple[int, List[CallBack], int, List[Chain], int, List[Node], List[Executor], List[Core]]:
    """コンポーネント(コールバック, チェイン)の初期化"""
    num_callbacks, callbacks = _initial_callback(input_cbs)
    num_chains, chains = _initial_chain(callbacks)
    num_nodes, nodes = _initial_node(callbacks)
    executors = _initial_executor(num_executors)
    cores = _initial_core(num_cores)

    return (
        num_callbacks,
        callbacks,
        num_chains,
        chains,
        num_nodes,
        nodes,
        executors,
        cores
    )

def _initial_callback(input_cbs: Dict[str, Dict[str, int]]) -> Tuple[int, List[CallBack]]:
    """コールバックの初期化"""
    num_callbacks = len(list(input_cbs.keys()))
    callbacks: List[CallBack] = []

    # create callback instance
    for id in range(num_callbacks):
        cur_input_cb = input_cbs[f"cb{id}"]
        callback = CallBack(
            callback_id=id,
            wcet=cur_input_cb["exec"],
            period=cur_input_cb["period"],
            node_id=cur_input_cb["node_id"],
            chain_id=cur_input_cb["chain_id"],
        )
        callbacks.append(callback)

    # チェインidを元に周期を割り当てる
    assign_period(callbacks)

    return num_callbacks, callbacks

def _initial_chain(callbacks: List[CallBack]) -> Tuple[int, List[Chain]]:
    """チェインの初期化"""
    num_chains = len(set([cb.chain_id for cb in callbacks]))
    chains: List[Chain] = []

    # grouping callbacks by chain
    callbacks_groupby_chain: List[List[CallBack]] = [[] for _ in range(num_chains)]
    for cb in callbacks:
        callbacks_groupby_chain[cb.chain_id].append(cb)

    # create chain instance
    for cur_chain_callbacks in callbacks_groupby_chain:
        cur_chain_id = cur_chain_callbacks[0].chain_id  # どれも同じchain_idだから0番目使う
        chain = Chain(
            chain_id=cur_chain_id,
            callbacks=cur_chain_callbacks,
        )
        chains.append(chain)

    return num_chains, chains

def _initial_node(callbacks: List[CallBack]) -> Tuple[int, List[Node]]:
    """ノードの初期化"""
    num_nodes = len(set([cb.node_id for cb in callbacks]))
    nodes: List[Node] = []

    # grouping callbacks by node
    callbacks_groupby_node: List[List[CallBack]] = [[] for _ in range(num_nodes)]
    for cb in callbacks:
        callbacks_groupby_node[cb.node_id].append(cb)

    # create node instance
    for cur_node_callbacks in callbacks_groupby_node:
        cur_node_id = cur_node_callbacks[0].node_id  # どれも同じnode_idだから0番目使う
        node = Node(
            node_id=cur_node_id,
            callbacks=cur_node_callbacks,
        )
        nodes.append(node)

    return num_nodes, nodes


def _initial_executor(num_executors) -> List[Executor]:
    """エグゼキューターの初期化"""
    executors: List[Executor] = []
    for id in range(num_executors):
        exe = Executor(id)
        executors.append(exe)
    return executors

def _initial_core(num_cores) -> List[Core]:
    """エグゼキューターの初期化"""
    cores: List[Core] = []
    for id in range(num_cores):
        exe = Core(id)
        cores.append(exe)
    return cores