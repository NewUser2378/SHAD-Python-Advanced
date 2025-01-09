from collections import defaultdict
from typing import List, Dict, Union, Set, Type, Any

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ValueType = Union[int, List[int], str, Dict[str, str]]


def save_rows_to_parquet(rows: List[Dict[str, ValueType]], output_filepath: str) -> None:
    """
    Save rows to parquet file.

    :param rows: list of rows containing data.
    :param output_filepath: local filepath for the resulting parquet file.
    :return: None.
    """
    field_types: Dict[str, Set[Type[Any]]] = defaultdict(set)
    all_keys: List[str] = []
    seen_keys: Set[str] = set()
    for row in rows:
        for key, value in row.items():
            if key not in seen_keys:
                all_keys.append(key)
                seen_keys.add(key)
            if isinstance(value, list):
                value_type: Type[Any] = list
            elif isinstance(value, dict):
                value_type = dict
            elif isinstance(value, int):
                value_type = int
            elif isinstance(value, str):
                value_type = str
            else:
                raise TypeError(f"Unsupported value type: {type(value)} for key: {key}")
            if value_type not in field_types[key]:
                if field_types[key]:
                    raise TypeError(f"Field {key} has different types")
                field_types[key].add(value_type)
    schema_fields: List[pa.Field] = []
    for key in all_keys:
        field_type = next(iter(field_types[key]))
        is_nullable = any(key not in row for row in rows)
        if field_type == int:
            pa_type = pa.int64()
        elif field_type == str:
            pa_type = pa.string()
        elif field_type == list:
            pa_type = pa.list_(pa.int64())
        elif field_type == dict:
            pa_type = pa.map_(pa.string(), pa.string())
        else:
            raise TypeError(f"Wrong type {field_type} for field {key}")
        schema_fields.append(pa.field(key, pa_type, nullable=is_nullable))
    schema = pa.schema(schema_fields)
    data: List[List[Any]] = []
    for row in rows:
        row_data = [row.get(key, None) for key in all_keys]
        data.append(row_data)
    df = pd.DataFrame(data, columns=all_keys)
    table = pa.Table.from_pandas(df, schema=schema)
    pq.write_table(table, output_filepath)
