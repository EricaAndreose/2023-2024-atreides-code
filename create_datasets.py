import argparse


from src.meta_to_parquet import process_meta_zip, search_for_titles, create_iris_not_in_meta
from src.index_to_parquet import process_index_dump
from src.read_iris import read_iris

def main(args):

    if args.iris_in_meta:
        process_meta_zip(args.meta_path, args.iris_path)
    
    if args.iris_not_in_meta:
        create_iris_not_in_meta(args.iris_path)

    if args.iris_no_id:
        read_iris(args.iris_path, no_id=True)

    if args.search_for_titles:
        search_for_titles(args.iris_path)

    if args.iris_in_index:
        if args.index_path is None:
            print("Please provide the path to the OpenCitations Index dump folder by specifying the -index argument.")
            exit(1)
        process_index_dump(args.index_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process zip file containing OpenCitations Meta CSV files")
    parser.add_argument("-meta", "--meta_path", type=str, required=True, help="Path to the zip file of the OpenCitations Meta dump")
    parser.add_argument("-index", "--index_path", type=str, help="Path to the OpenCitations Index dump folder")
    parser.add_argument("-iris", "--iris_path", type=str, required=True, help="Path to the folder containing the IRIS CSV files")
    parser.add_argument("--iris_in_index", action="store_true", default=False, help="Create the Iris In Index dataset containing all the entities with external IDs in IRIS that are in the OpenCitations Index.")
    parser.add_argument("--iris_in_meta", action="store_true", default=False, help="Create the Iris In Meta dataset containing all the entities with external IDs IRIS that are in Meta.")
    parser.add_argument("--iris_not_in_meta", action="store_true", default=False, help="Create the Iris Not In Meta dataset containing all the entities with external IDs IRIS that are not in Meta.")
    parser.add_argument("--iris_no_id", action="store_true", default=False, help="Create the Iris No ID dataset containing all the entities with no external IDs in IRIS.")
    parser.add_argument("--search_for_titles", action="store_true", default=False, help="Search for the entities without an id in IRIS by their title in Meta. WARNING: this will take ~3 hours to complete.")

    args = parser.parse_args()


    if not any([args.iris_in_meta, args.iris_not_in_meta, args.iris_no_id, args.search_for_titles, args.iris_in_index]):
        print("Please pass a dataset specific argument to create a dataset. Use the -h flag for help.")
        exit(1)
    else:
        main(args)
