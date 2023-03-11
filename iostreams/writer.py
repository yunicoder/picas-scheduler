from pathlib import Path
from typing import List

from components.callback import CallBack
from components.chain import Chain
from components.core import Core
from components.executor import Executor
from components.node import Node


def write_all_info(
    output_dir: Path,
    callbacks: List[CallBack],
    chains: List[Chain],
    nodes: List[Node],
    executors: List[Executor],
    cores: List[Core],
) -> None:
    _write_callbacks_info(output_dir, callbacks)
    _write_chains_info(output_dir, chains)
    _write_nodes_info(output_dir, nodes)
    _write_executors_info(output_dir, executors)
    _write_cores_info(output_dir, cores)

def _write_callbacks_info(output_dir: Path, callbacks: List[CallBack]) -> None:
    file_path = output_dir / Path("callback_info.csv")

    # 各列のタイトル
    columns = ["callback_id", "wcet", "period", "priority", "node_id", "chain_id", "is_timer_callback", "assigned_executor_id"]
    columns_str = ",".join(columns) + "\n"

    # 情報
    callbacks_info = []
    for cb in callbacks:
        callbacks_info.append(
            f"{cb.callback_id},{cb.wcet},{cb.period},{cb.priority},{cb.node_id},{cb.chain_id},{cb.is_timer_callback},{cb.assigned_executor_id}"
        )
    callbacks_info_str = "\n".join(callbacks_info)
    
    with open(file=file_path, mode="w") as file:
        file.writelines(columns_str)  # カラムタイトル
        file.writelines(callbacks_info_str)  # コールバック情報

def _write_chains_info(output_dir: Path, chains: List[Chain]) -> None:
    file_path = output_dir / Path("chain_info.csv")

    # 各列のタイトル
    columns = ["chain_id", "contain_callback_ids", "priority", "wcet_sum"]
    columns_str = ",".join(columns) + "\n"

    # 情報
    chains_info = []
    for chain in chains:
        chains_info.append(
            f"{chain.chain_id},{[cb.callback_id for cb in chain.callbacks]},{chain.priority},{chain.wcet_sum}"
        )
    chains_info_str = "\n".join(chains_info)
    
    with open(file=file_path, mode="w") as file:
        file.writelines(columns_str)  # カラムタイトル
        file.writelines(chains_info_str)  # チェイン情報

def _write_nodes_info(output_dir: Path, nodes: List[Node]) -> None:
    file_path = output_dir / Path("node_info.csv")

    # 各列のタイトル
    columns = ["node_id", "contain_callback_ids", "utilization", "highest_priority"]
    columns_str = ",".join(columns) + "\n"

    # 情報
    nodes_info = []
    for node in nodes:
        nodes_info.append(
            f"{node.node_id},{[cb.callback_id for cb in node.callbacks]},{node.utilization},{node.highest_priority}"
        )
    nodes_info_str = "\n".join(nodes_info)
    
    with open(file=file_path, mode="w") as file:
        file.writelines(columns_str)  # カラムタイトル
        file.writelines(nodes_info_str)  # ノード情報

def _write_executors_info(output_dir: Path, executors: List[Executor]) -> None:
    file_path = output_dir / Path("executor_info.csv")

    # 各列のタイトル
    columns = ["executor_id", "contain_callback_ids", "priority", "utilization", "assigned_core_id"]
    columns_str = ",".join(columns) + "\n"

    # 情報
    executors_info = []
    for executor in executors:
        executors_info.append(
            f"{executor.executor_id},{[cb.callback_id for cb in executor.callbacks]},{executor.priority},{executor.utilization},{executor.assigned_core_id}"
        )
    executors_info_str = "\n".join(executors_info)
    
    with open(file=file_path, mode="w") as file:
        file.writelines(columns_str)  # カラムタイトル
        file.writelines(executors_info_str)  # エグゼキューター情報

def _write_cores_info(output_dir: Path, cores: List[Core]) -> None:
    file_path = output_dir / Path("core_info.csv")

    # 各列のタイトル
    columns = ["core_id", "contain_executor_ids", "utilization"]
    columns_str = ",".join(columns) + "\n"

    # 情報
    cores_info = []
    for core in cores:
        cores_info.append(
            f"{core.core_id},{[exe.executor_id for exe in core.executors]},{core.utilization}"
        )
    cores_info_str = "\n".join(cores_info)
    
    with open(file=file_path, mode="w") as file:
        file.writelines(columns_str)  # カラムタイトル
        file.writelines(cores_info_str)  # コア情報