# picas-scheduler

## Environment
- Windows
- python 3.9

## Install
Clone this repository
```
$ git clone https://github.com/yunicoder/picas-scheduler
```

Install python library
```
$ pip install -r requirements.txt
```

## Usage
```
$ python main.py
```

## Output Sample
### Callback
`callback_info.csv`
```
- "callback_id": コールバックid
- "wcet": 最悪実行時間
- "period": 周期 (相対デッドライン)
- "priority": 優先度
- "node_id": ノードid
- "chain_id": チェインid
- "is_timer_callback": タイマーコールバックかどうか
- "assigned_executor_id": # 割り当てたエグゼキューターid
```
### Chain
`chain_info.csv`
```
- "chain_id": チェインid
- "contain_callback_ids": チェインに含まれているコールバックのid
- "priority": 優先度
- "wcet_sum": 最悪実行の合計
```

### Executor
`executor_info.csv`
```
- "executor_id": エグゼキューターid
- "contain_callback_ids": エグゼキューターに割り当てられたコールバックのid
- "priority": 優先度
- "utilization": 利用率
- "assigned_core_id": 割り当てたコアid
```

### Core
`core_info.csv`
```
- "core_id": コアid
- "contain_executor_ids": コアに割り当てられたエグゼキューターid
- "utilization": 利用率
```
