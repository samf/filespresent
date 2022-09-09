#! /usr/bin/env python3

import argparse
import csv
import os.path

cli = argparse.ArgumentParser(
    description="validate files mentioned in csvs exist"
)
cli.add_argument(
    "csvfile", type=argparse.FileType("r"), help="csv file to read"
)
cli.add_argument(
    "--field", "-f", type=str, help="field that contains the file names"
)
cli.add_argument(
    "--dir", "-d", type=str, help="directory to check for files", default="."
)


def check(cli, args):
    reader = csv.DictReader(args.csvfile)
    missing = list()
    for row in reader:
        fname = row.get(args.field, None)
        if fname is None:
            cli.error(f"field {args.field} not found")
        if not fname:
            # blank rows are okay
            continue
        fpath = os.path.join(args.dir, fname)
        if not os.path.isfile(fpath):
            missing.append(fname)
    if not missing:
        cli.exit()
    print("missing files")
    for fname in missing:
        print(" " * 4, fname)


def show_fields(cli, args):
    reader = csv.DictReader(args.csvfile)
    if not reader.fieldnames:
        cli.error(f"no fields found in {args.csvfile.name}")
    print(f"Fields in {args.csvfile.name}")
    for field in reader.fieldnames:
        print(" " * 4, field)
    cli.exit()


def main():
    args = cli.parse_args()
    if not args.field:
        show_fields(cli, args)
    if not os.path.isdir(args.dir):
        cli.error(f'"{args.dir}" is not a directory')
    check(cli, args)


if __name__ == "__main__":
    main()
