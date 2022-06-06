#!/usr/bin/env python3.10

import argparse
from pyliftover import LiftOver

parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('chr', help="Chromosome column number (0 index)", type=int)
parser.add_argument('pos', help="position column number (0 index)", type=int)
parser.add_argument('build_from', help="Which build to convert from (eg b38)", type=str)
parser.add_argument('build_to', help="Which build to convert to (eg b38)",type=str)
parser.add_argument('file', help="File to Convert")
parser.add_argument("--header", help="include if file has a header (Default no-header)", action=argparse.BooleanOptionalAction)
parser.add_argument('--delim', help="Delimiter of input file")
parser.add_argument('--delim_out', help="Delimiter to use when outputting file (Default tab)")
parser.add_argument('--out', help='file output name')

args = parser.parse_args()
print(args)

# Get liftover chain
build_dictionary = {
    'b38':'hg38',
    'b37':'hg19',
    '38':'hg38',
    '37':'hg19'
}
if args.build_from in build_dictionary.keys():
    args.build_from = build_dictionary[args.build_from]
if args.build_to in build_dictionary.keys():
    args.build_to = build_dictionary[args.build_to]
lo = LiftOver(args.build_from, args.build_to)

# If out was not input, make a new output name
if args.out is None:
    args.out = args.build_to + '_converted_' + args.file
    print('No output file name given, writing to: '+args.out)
if args.delim_out is None:
    args.delim_out = '\t'

# Open files 1 and 2 and read/write them
file1 = open(args.file, 'r')
file2 = open(args.out, 'w+')

if args.header:
    file2.write(file1.readline())
    next(file1)

line_count = 0
missing_count = 0
for line in file1:
    if args.delim is None:
        out = line.split()
    else:
        out = line.split(args.delim)
    if 'chr' not in out[args.chr]:
        out[args.chr] = 'chr' + str(out[args.chr])
    new_pos = lo.convert_coordinate(out[args.chr], int(out[args.pos]))
    if len(new_pos) == 0:
        out[args.pos] = 'NA'
        missing_count +=1
    else:
        out[args.pos] = new_pos[0][1]
    out = [str(x) for x in out]
    out.append('\n')
    out = args.delim_out.join(out)
    file2.write(out)
    line_count+=1
    if line_count % 3_000_000 == 0:
        print(str(line_count)+'th snp converted')

print('Done!')
print(str(missing_count) + ' SNPs did not have a conversion build')