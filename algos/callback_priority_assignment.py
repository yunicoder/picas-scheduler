from typing import List

from components.chain import Chain


def callback_priority_assignment(chains: List[Chain]) -> List[Chain]:
    # sort chain by id
    chains = sorted(chains, key=lambda chain: chain.chain_id)

    priority = 1

    # assign priority
    for chain in chains:
        # NOTE: chain.callbacksは必ずcallback_idでソートされている必要がある
        for cb in chain.callbacks:
            cb.priority = priority
            priority += 1
    
    return chains


