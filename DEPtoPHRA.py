__author__ = 'Christopher Perrin'

from nltk import parse
import argparse
import json
import converter

def main():
    parser = argparse.ArgumentParser(description="Converts a dependency structure to a phrase structure")
    parser.add_argument("data", type=str, help="Dependency graph in Malt-TAB format")
    parser.add_argument("projections", type=argparse.FileType(mode="r"), help="Projections in JSON format")
    parser.add_argument("arguments", type=argparse.FileType(mode="r"), help="Argument table in JSON format")
    parser.add_argument("modifiers", type=argparse.FileType(mode="r"), help="Modification table in JSON format")
    args = parser.parse_args()

    deps = parse.DependencyGraph.load(args.data)
    proj = json.load(args.projections)
    arg = json.load(args.arguments)
    mod = json.load(args.modifiers)
    for dep in deps:
        c = converter.Converter(dep, proj, arg, mod)
        c.convert()


if __name__ == '__main__':
    main()