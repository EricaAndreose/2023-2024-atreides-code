import argparse
from pathlib import Path
import glob
import os

import textwrap
import polars as pl
pl.Config.set_tbl_hide_dataframe_shape(True)
pl.Config.set_tbl_hide_column_names(True)
pl.Config.set_tbl_hide_column_data_types(True)


def answer_question_1(iim_path='data/iris_in_meta'):
    iris_in_meta_path = Path(iim_path)

    if not iris_in_meta_path.exists():
        return f"Folder '{str(iris_in_meta_path)}' does not exist. Please run the 'meta_to_parquet.py' script first."

    lf_iim = pl.scan_parquet(iris_in_meta_path / '*.parquet')
    
    result = lf_iim.select(pl.len()).collect()

    return result


def answer_question_2(iim_path='data/iris_in_meta'):
    iris_in_meta_path = Path(iim_path)

    if not iris_in_meta_path.exists():
        return f"Folder '{str(iris_in_meta_path)}' does not exist. Please run the 'meta_to_parquet.py' script first."

    lf_iim = pl.scan_parquet(iris_in_meta_path / '*.parquet')
    
    result = lf_iim.group_by('type').len().sort('len', descending=True).with_columns(pl.col('type').str.replace(r"^$", 'no type')).collect()

    return result


def answer_question_3(iii_path='data/iris_in_index'):
    iii_path = Path(iii_path)

    if not iii_path.exists():
        return f"Folder '{str(iii_path)}' does not exist. Please run the 'index_to_parquet.py' script first."

    iii_glob = glob.glob(str(iii_path / '*' / '*.parquet'))

    lf_iii = pl.scan_parquet(iii_glob)
    
    result = lf_iii.select(pl.len()).collect()

    return result


def answer_question_4(iim_path='data/iris_in_meta', iii_path='data/iris_in_index'):
    iii_path = Path(iii_path)
    iris_in_meta_path = Path(iim_path)

    if not iii_path.exists():
        return f"Folder '{str(iii_path)}' does not exist. Please run the 'index_to_parquet.py' script first."
    if not iris_in_meta_path.exists():
        return f"Folder '{str(iris_in_meta_path)}' does not exist. Please run the 'meta_to_parquet.py' script first."

    iii_glob = glob.glob(str(iii_path / '*' / '*.parquet'))
    lf_iii = pl.scan_parquet(iii_glob)

    lf_iim = pl.scan_parquet(iris_in_meta_path / '*.parquet')

    oc_omids_list = (
        lf_iim
        .select('omid')
        .collect()
    )['omid'].to_list()

    rq4a = (
        lf_iii
        .select('citing')
        .filter(
            ~pl.col('citing').is_in(oc_omids_list)
        )
        .select(pl.len())
        .collect()
    ).item()

    rq4b = (
        lf_iii
        .select('cited')
        .filter(
            ~pl.col('cited').is_in(oc_omids_list)
        )
        .select(pl.len())
        .collect()
    ).item()

    lf_iii = pl.scan_parquet(iii_glob)
    
    pl.Config.set_tbl_hide_column_names(False)
    result = pl.DataFrame({'citing': [rq4a], 'cited': [rq4b]})
    
    return result


def answer_question_5(iim_path='data/iris_in_meta', iii_path='data/iris_in_index'):
    iii_path = Path(iii_path)
    iris_in_meta_path = Path(iim_path)

    if not iii_path.exists():
        return f"Folder '{str(iii_path)}' does not exist. Please run the 'index_to_parquet.py' script first."
    if not iris_in_meta_path.exists():
        return f"Folder '{str(iris_in_meta_path)}' does not exist. Please run the 'meta_to_parquet.py' script first."

    iii_glob = glob.glob(str(iii_path / '*' / '*.parquet'))
    lf_iii = pl.scan_parquet(iii_glob)

    lf_iim = pl.scan_parquet(iris_in_meta_path / '*.parquet')

    oc_omids_list = (
        lf_iim
        .select('omid')
        .collect()
    )['omid'].to_list()

    rq5 = (
        lf_iii
        .select('citing', 'cited')
        .filter(
            pl.col('citing').is_in(oc_omids_list) & pl.col(
                'cited').is_in(oc_omids_list)
        )
    )

    lf_iii = pl.scan_parquet(iii_glob)
    
    pl.Config.set_tbl_hide_column_names(True)
    result = rq5.select(pl.len()).collect()

    return result


def main():
    parser = argparse.ArgumentParser(description="Answer research questions.")
    parser.add_argument(
        '-rq',
        '--research_question', 
        type=int, 
        choices=range(1, 6), 
        help="The research question number to answer (1-5). If omitted, all questions will be answered."
    )
    
    args = parser.parse_args()
    term_size = os.get_terminal_size()
    
    if args.research_question:
        result = None
        if args.research_question == 1:
            print('{:*^{}}'.format(' Research question n. 1 ', os.get_terminal_size().columns))
            print(textwrap.fill("What is the coverage of the publications available in IRIS (strictly concerning research conducted within the University of Bologna) in OpenCitations Meta?", width=os.get_terminal_size().columns) )
            result = answer_question_1()
            print(result)
            print("")
        elif args.research_question == 2:
            print('{:*^{}}'.format(' Research question n. 2 ', os.get_terminal_size().columns))
            print(textwrap.fill("Which are the types of publications that are better covered in OpenCitations Meta?", width=os.get_terminal_size().columns) )
            result = answer_question_2()
            print(result)
            print("")
        elif args.research_question == 3:
            print('{:*^{}}'.format(' Research question n. 3 ', os.get_terminal_size().columns))
            print(textwrap.fill("Research question n. 3: What is the amount of citations (according to OpenCitations Index) included in the IRIS publications that are involved in OpenCitations Meta (as citing entity and as cited entity)?", width=os.get_terminal_size().columns) )
            result = answer_question_3()
            print(result)
            print("")
        elif args.research_question == 4:
            print('{:*^{}}'.format(' Research question n. 4 ', os.get_terminal_size().columns))
            print(textwrap.fill("Research question n. 4: How many of these citations come from and go to publications that are not included in IRIS?", width=os.get_terminal_size().columns) )
            result = answer_question_4()
            print(result)
            print("")
        elif args.research_question == 5:
            print('{:*^{}}'.format(' Research question n. 5 ', os.get_terminal_size().columns))
            print(textwrap.fill("Research question n. 5: How many of these citations involve publications in IRIS as both citing and cited entities?", width=os.get_terminal_size().columns) )
            result = answer_question_5()
            print(result)
            print("")
    else:
        term_size = os.get_terminal_size()

        print('\n' + '=' * term_size.columns)
        print('{:*^{}}'.format(' Research question n. 1 ', os.get_terminal_size().columns))
        print(textwrap.fill("What is the coverage of the publications available in IRIS (strictly concerning research conducted within the University of Bologna) in OpenCitations Meta?", width=os.get_terminal_size().columns) )
        print("")
        print(answer_question_1())
        print('\n' + '=' * term_size.columns)
        print('{:*^{}}'.format(' Research question n. 2 ', os.get_terminal_size().columns))
        print(textwrap.fill("Which are the types of publications that are better covered in OpenCitations Meta?", width=os.get_terminal_size().columns) )
        print("")
        print(answer_question_2())
        print('\n' + '=' * term_size.columns)
        print('{:*^{}}'.format(' Research question n. 3 ', os.get_terminal_size().columns))
        print(textwrap.fill("Research question n. 3: What is the amount of citations (according to OpenCitations Index) included in the IRIS publications that are involved in OpenCitations Meta (as citing entity and as cited entity)?", width=os.get_terminal_size().columns) )
        print("")
        print(answer_question_3())
        print('\n' + '=' * term_size.columns)
        print('{:*^{}}'.format(' Research question n. 4 ', os.get_terminal_size().columns))
        print(textwrap.fill("Research question n. 4: How many of these citations come from and go to publications that are not included in IRIS?", width=os.get_terminal_size().columns) )
        print("")
        print(answer_question_4())
        print('\n' + '=' * term_size.columns)
        print('{:*^{}}'.format(' Research question n. 5 ', os.get_terminal_size().columns))
        print(textwrap.fill("Research question n. 5: How many of these citations involve publications in IRIS as both citing and cited entities?", width=os.get_terminal_size().columns) )
        print("")
        print(answer_question_5())
        print("")


if __name__ == "__main__":
    main()