from typing import Literal
from ...types.response import Params


def params_to_query_string(params: Params) -> dict:
    valid_params = params.model_dump()
    if isinstance(valid_params['include'], list):
        valid_params['include'] = ','.join(valid_params['include'])
    search_params = {}
    for key in valid_params:
        val = valid_params[key]
        if isinstance(val, dict):
            for entry in val:
                search_params[f'{key}[{entry}]'] = f'{val[entry]}'
        else:
            search_params[key] = f'{val}' if val else val
    return search_params

def include_to_query_string(include: list | None):
    if isinstance(include, list):
        return {
            "include": ','.join(include)
        }
    return {}