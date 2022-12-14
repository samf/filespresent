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
    "--field",
    "-f",
    type=str,
    action="append",
    help="field that contains the file names; may use multiple times",
)
cli.add_argument(
    "--dir", "-d", type=str, help="directory to check for files", default="."
)


def check(cli, args):
    reader = csv.DictReader(args.csvfile)
    missing = set()
    extra = set()
    for finfo in os.scandir(args.dir):
        if not finfo.is_file():
            continue
        extra.add(finfo.name)
    for row in reader:
        for field in args.field:
            fnames = row.get(field, None)
            if fnames is None:
                cli.error(f"field {field} not found")
            if not fnames:
                # blank cells are okay
                continue
            for fname in fnames.split():
                extra.discard(fname)
                fpath = os.path.join(args.dir, fname)
                if not os.path.isfile(fpath):
                    missing.add(fname)
    if missing:
        print("missing files")
        for fname in missing:
            print(" " * 4, fname)
    if extra:
        print("extraneous files")
        for fname in extra:
            print(" " * 4, fname)


def show_fields(cli, args):
    reader = csv.DictReader(args.csvfile)
    if not reader.fieldnames:
        cli.error(f"no fields found in {args.csvfile.name}")
    print(f"Fields in {args.csvfile.name}")
    for field in reader.fieldnames:
        print(" " * 4, field)


def main():
    args = cli.parse_args()
    if not args.field:
        show_fields(cli, args)
        cli.exit()
    if not os.path.isdir(args.dir):
        cli.error(f'"{args.dir}" is not a directory')
    check(cli, args)


if __name__ == "__main__":
    main()
