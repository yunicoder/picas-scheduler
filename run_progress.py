from pathlib import Path
from typing import Dict, List

from algos.callback_priority_assignment import callback_priority_assignment
from algos.executor_core_assignment.assignment import executor_core_assignment
from components.callback import CallBack
from components.chain import set_chains_priority
from components.initial_components import initial_components
from components.node import set_highest_priorities
from iostreams.reader import read_input
from iostreams.writer import write_all_info


class RunProgress():

    def __init__(self, input_path: Path, output_dir: Path) -> None:
        input = read_input(input_path)

        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)

        self.num_cpus: int = input["num_cpus"]
        self.num_executors: int = input["num_executors"]

        (
            self.num_callbacks,
            self.callbacks,
            self.num_chains,
            self.chains,
            self.num_nodes,
            self.nodes,
            self.executors,
            self.cores,
        ) = initial_components(input["callbacks"], self.num_executors, self.num_cpus)

    
    def main_process(self):
        # コールバックの優先度を割り当てる
        self.chains = callback_priority_assignment(self.chains)
        
        # 各ノードの中で最も高い優先度をノードのインスタンス変数にセット
        self.nodes = set_highest_priorities(self.nodes)

        # チェインの優先度を決定
        self.chains = set_chains_priority(self.chains)

        # エグゼキューターとコアの割り当て
        executor_core_assignment(self.nodes, self.executors, self.cores, self.chains)

        # csvに情報を出力
        write_all_info(
            self.output_dir,
            self.callbacks,
            self.chains,
            self.nodes,
            self.executors,
            self.cores,
        )
