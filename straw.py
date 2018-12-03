#!/usr/bin/env python3
from argparse import ArgumentParser, FileType, ArgumentTypeError
from hicparser import HicParser, NormType, Unit, Range


def straw(norm_type, input_file, chr1loc, chr2loc, unit, bin_size):
    chr1, *loc1 = chr1loc.split(":")
    chr2, *loc2 = chr2loc.split(":")

    range1 = range2 = None

    if len(loc1) and len(loc2):
        range1 = Range(*map(int, loc1))
        range2 = Range(*map(int, loc2))

    hic = HicParser(input_file)

    norm = None

    if norm_type != 'NONE':
        norm = NormType(norm_type)

    return hic.values(chr1, chr2, bin_size, Unit(unit), norm, range1, range2)


def printme(norm_type, input_file, chr1loc, chr2loc, unit, bin_size, output_file):
    values = straw(norm_type, input_file, chr1loc, chr2loc, unit, bin_size)

    for x, y, count in values:
        output_file.write("{} {} {}\n".format(x, y, count))


def _chromosome_type(string):
    fields = string.split(":")

    if len(fields) not in (1, 3):
        raise ArgumentTypeError("one or three values excepted")

    chromosome, *locations = fields
    if len(locations):
        try:
            int(locations[0])
            int(locations[1])
        except ValueError:
            raise ArgumentTypeError("number expected")

    return string


if __name__ == "__main__":
    parser = ArgumentParser(prog="straw", description="Hic data access")
    parser.add_argument("norm_type", choices=("NONE", "VC", "VC_SQRT", "KR"), help="The norm type to use")
    parser.add_argument("hic_file", type=FileType(mode="rb"), help="The hic file")
    parser.add_argument("chr1loc", type=_chromosome_type, help="Chromosome 1 <chr1>[:x1:x2]")
    parser.add_argument("chr2loc", type=_chromosome_type, help="Chromosome 2 <chr2>[:x1:x2]")
    parser.add_argument("unit", choices=("BP", "FRAG"), help="The resolution unit")
    parser.add_argument("bin_size", type=int, help="The resolution bin size")
    parser.add_argument("output_file", type=FileType(mode="w"), nargs="?", default="-", help="Output file to write to")
    args = parser.parse_args()

    printme(args.norm_type, args.hic_file, args.chr1loc, args.chr2loc, args.unit, args.bin_size, args.output_file)
