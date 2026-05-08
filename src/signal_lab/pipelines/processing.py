def run(data_dict):
    return {k: v for k, v in data_dict.items() if v is not None and not v.empty}
