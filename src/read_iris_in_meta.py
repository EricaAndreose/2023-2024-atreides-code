from pathlib import Path

import polars as pl


def read_iris_in_meta():
    iim_path = Path('data/iris_in_meta')
    if not iim_path.exists():
        raise FileNotFoundError(f"Folder '{str(iim_path)}' does not exist. Please create the 'iris_in_meta' dataset first")

    metaparquet_files = Path(iim_path) / '*.parquet'
    lf_iim = pl.scan_parquet(metaparquet_files)

    return lf_iim


def get_omids_list():
    omids_list = (
        read_iris_in_meta()
        .select('omid')
        .collect()
    )['omid'].to_list()

    return omids_list
