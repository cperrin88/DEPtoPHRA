# Dependency structure to phrase structure converter
This software converts dependency structures to phrase structures. It follows a algorithm by Xia Fei and Martha Palmer.

## Requirements & installation
This software is written for and tested with Python3. You need `pip` to install the requirements.
To install the requirements use:

    pip install -r requirements.txt

## Running the software
To run the software you need 4 files:
 - Dependency graph: This is a file in the MALT-Tab format. It contains the dependency graph that will be converted.
 - Projection table: This table projects categories to other categories
 - Argument table: This table is needed to attach the projections of arguments to the head
 - Modification table: This table is needed to attach the projections of modifications to the head

For examples are in the `example_data` folder.

Example run:

    $ python3 DEPtoPHRA.py example_data/dependency_tree.mtab example_data/projection_table.json example_data/argument_table.json example_data/modification_table.json

This prints the tree as a string to the stdout

You can display the help with:

    $ python3 DEPtoPHRA.py -h

The output would be:

    usage: DEPtoPHRA.py [-h] [-d] [-q] [-o OUTFILE]
                        data projections arguments modifiers

    Converts a dependency structure to a phrase structure

    positional arguments:
      data                  Dependency graph in Malt-TAB format
      projections           Projections in JSON format
      arguments             Argument table in JSON format
      modifiers             Modification table in JSON format

    optional arguments:
      -h, --help            show this help message and exit
      -d, --draw            Draw the graph (windowmanager needed)
      -q, --qtree           Print latex qTree to the console
      -o OUTFILE, --outfile OUTFILE
                            Write tree to file
