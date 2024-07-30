import os
from zipfile import ZipFile

import argparse
from pathlib import Path

from tqdm import tqdm

import dask.dataframe as dd
from dask.diagnostics import ProgressBar
ProgressBar().register()

from src.read_iris_in_meta import get_omids_list


def process_index_dump(index_path):
    if not os.path.isdir('data/iris_in_meta'):
        raise FileNotFoundError(f"Folder 'data/iris_in_meta' does not exist. Please create the 'iris_in_meta' dataset first")

    # unzip the internal archives
    if index_path.endswith('.zip'):
        extraction_dir = index_path.replace('.zip', '')
        with ZipFile(index_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_dir)
        index_path = extraction_dir

    file_names = [Path(index_path) / Path(archive) for archive in os.listdir(index_path)]

    omids_list = get_omids_list()

    output_dir = Path("data/iris_in_index")

    for archive in tqdm(file_names):
        zip_file = ZipFile(archive)

        csvs = ['zip://'+n for n in zip_file.namelist() if n.endswith('.csv')]

        ddf = dd.read_csv(csvs, storage_options={'fo': zip_file.filename}, usecols=['id', 'citing', 'cited'])
        ddf = ddf[ddf['cited'].isin(omids_list) | ddf['citing'].isin(omids_list)]
        ddf.to_parquet(output_dir / archive.stem, write_index=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process zip file containing OpenCitations Index CSV files")
    parser.add_argument("-index", "--index_dump", type=str, help="Path to the OpenCitations Index dump folder")

    args = parser.parse_args()
    process_index_dump(args.index_dump)
