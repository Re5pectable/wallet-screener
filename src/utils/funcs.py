def get_swap_delta(swap_data: str) -> dict[str, int]:
    swap_data = swap_data[2:]
    return {
        'pool_token0_delta': int(swap_data[:64], 16) - int(swap_data[64*2:64*3], 16),
        'pool_token1_delta': int(swap_data[64:64*2], 16) - int(swap_data[-64:], 16),
    }

def exclude_none_from_dict(data: dict):
    return {
        key: value for key, value in data.items() if value is not None
    }
    
    

