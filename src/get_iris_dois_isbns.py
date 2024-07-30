import polars as pl

from src.read_iris import read_iris


def get_iris_dois_pmids_isbns(iris_path) -> pl.DataFrame:
    df_filtered = read_iris(iris_path)

    #filter and normalize the dois
    dois = df_filtered.select('ITEM_ID', 'IDE_DOI').drop_nulls('IDE_DOI').unique()

    filtered_dois = (
        dois
        .with_columns(('doi:'+pl.col('IDE_DOI').str.extract(r'(10\.\d{4,}\/[^,\s;]*)').str.to_lowercase()).alias('id'))
        .drop_nulls('id')
        .drop('IDE_DOI')
        .rename({'ITEM_ID': 'iris_id'})
    )

    #filter and normalize the pmids
    pmids = df_filtered.select('ITEM_ID', 'IDE_PMID').drop_nulls('IDE_PMID').unique()

    filtered_pmids = (
        pmids
        .filter(
            ~pl.col('IDE_PMID').str.contains('PMC')
            )
        .with_columns(('pmid:'+pl.col('IDE_PMID').str.extract(r'0*([1-9][0-9]{1,8})', 1).str.to_lowercase()).alias('id'))
        .drop('IDE_PMID')
        .rename({'ITEM_ID': 'iris_id'})
    )

    #filter and normalize the isbns
    isbns = df_filtered.select('ITEM_ID', 'IDE_ISBN').drop_nulls('IDE_ISBN').unique()

    filtered_isbns = (
        isbns
        .with_columns(
            ('isbn:'+pl.col('IDE_ISBN').str.extract_all(r'(ISBN[-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})').list.first().str.replace_all(r'[- ]', '').str.to_lowercase()).alias('id')
        )
        .drop_nulls('id')
        .drop('IDE_ISBN')
        .rename({'ITEM_ID': 'iris_id'})
    )

    dois_isbns_pmids_df = pl.concat([filtered_dois, filtered_isbns, filtered_pmids])

    return dois_isbns_pmids_df