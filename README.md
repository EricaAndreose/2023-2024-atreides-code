# 2023-2024-atreides-code
The repository for the team Atreides of the Open Science course a.a. 2023/2024

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11262417.svg)](https://doi.org/10.5281/zenodo.11262417)
[![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/open-sci/2023-2024-atreides-code/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/open-sci/2023-2024-atreides-code)

## Research questions:

1) What is the coverage of the publications available in IRIS, that strictly concern research conducted within the University of Bologna, in OpenCitations Meta?
2) What are the types of publications that are better covered in OpenCitations Meta?
3) What is the amount of citations (according to OpenCitations Index) the IRIS publications included in OpenCitations Meta are involved in (as citing entity and as cited entity)?
4) How many of these citations come from and go to publications not included in IRIS?
5) How many of these citations involve publications in IRIS as both citing and cited entities?

## Download data

-IRIS dump (14 March 2024): [https://doi.org/10.6092/unibo%2Famsacta%2F7608](https://doi.org/10.6092/unibo%2Famsacta%2F7608)

-OpenCitations Meta April 2024 Dump: [https://doi.org/10.6084/m9.figshare.21747461.v8](https://doi.org/10.6084/m9.figshare.21747461.v8)

-OpenCitations Index November 2023 Dump: [https://doi.org/10.6084/m9.figshare.24356626.v2](https://doi.org/10.6084/m9.figshare.24356626.v2)

## Reproduce the experiment
Clone the repository

Install the dependencies in *requirements.txt*

Create the necessary datasets (at least 'IRIS in Meta' and 'IRIS in Index') by running the following command:

```python create_datasets.py -meta <path_to_meta_zip> -iris <path_to_iris_zip> -index <path_to_index_zip> --iris_in_meta --iris_in_index```

Alternatively, download them from the links at the bottom of this page and place them in the 'data/' directory of the repository folder.

Use the following command to run the script:

```python answer_research_questions.py```

You can get the answer to a specific research question by adding to the previous commang the ```-rq``` flag followed by the number of the research question you want the answer of.

For more detailed guidelines consult the protocol for the software: [https://dx.doi.org/10.17504/protocols.io.3byl497wjgo5/v4](https://dx.doi.org/10.17504/protocols.io.3byl497wjgo5/v4)

## Result datasets

-IRIS in Meta: [https://doi.org/10.6084/m9.figshare.25879420.v1](https://doi.org/10.6084/m9.figshare.25879420.v1)

-IRIS in Index: [https://doi.org/10.6084/m9.figshare.25879441.v1](https://doi.org/10.6084/m9.figshare.25879441.v1)

-IRIS Not in Meta: [https://doi.org/10.6084/m9.figshare.25897708.v1](https://doi.org/10.6084/m9.figshare.25897708.v1)

-IRIS No ID: [https://doi.org/10.6084/m9.figshare.25897759.v1](https://doi.org/10.6084/m9.figshare.25897759.v1)



