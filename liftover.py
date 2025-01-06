#!/usr/bin/env python3.10

import argparse
from pyliftover import LiftOver

parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('chr', help="Chromosome column number (0 index)", type=int)
parser.add_argument('pos', help="Position column number (0 index)", type=int)
parser.add_argument('build_from', help="Which build to convert from (eg b38)", type=str)
parser.add_argument('build_to', help="Which build to convert to (eg b38)",type=str)
parser.add_argument('file', help="File to Convert")
parser.add_argument("--header", help="include if file has a header (Default no-header)", action=argparse.BooleanOptionalAction)
parser.add_argument('--delim', default="\t", help="Delimiter of input file")
parser.add_argument('--delim_out', help="Delimiter to use when outputting file (Default: same as delim)")
parser.add_argument('--out', help='file output name')

args = parser.parse_args()
print(args)

def build_dictionary(build_identifier):
    # Get liftover chain
    known_builds = {
        'b38':'hg38',
        'b37':'hg19',
        '38':'hg38',
        '37':'hg19'
    }
    if build_identifier in known_builds.keys():
        return known_builds[build_identifier]
    else:
        return build_identifier

def format_chromosome(chromosome: str):
    chromosome = chromosome.replace('23', 'X').replace('24','Y')
    if chromosome.startswith('chr'):
        return chromosome
    else:
        return f"chr{chromosome}"
    
def unformat_chromosome(original_chrom: str, new_chrom: str):
    out = new_chrom
    if not original_chrom.startswith('chr'):
        out = new_chrom.removeprefix('chr')
    if 'X' in new_chrom and '23' in original_chrom:
        out = out.replace('X', '23')
    if 'Y' in new_chrom and '24' in original_chrom:
        out = out.replace('Y', '24')
    return out

# Update build numbers
args.build_from = build_dictionary(args.build_from)
args.build_to = build_dictionary(args.build_to)

# Update output file name if necessary
if args.out is None:
    args.out = f"{args.file}.{args.build_to}"
    print(f"No output file name given, writing to: {args.out}")

# Update output delimiter if necessary
if args.delim_out is None:
    args.delim_out = args.delim

# Construct the liftover chain object
lo = LiftOver(args.build_from, args.build_to)

# Open files 1 and 2 and read/write them
file1 = open(args.file, 'r')
file2 = open(args.out, 'w+')

# Add the header back in if necessary
if args.header:
    file2.write(file1.readline().replace(args.delim, args.delim_out))

line_count = 0
missing_count = 0
for line in file1:
    out = line.strip().split(args.delim)
        
    #if 'chr' not in out[args.chr]:
    #    out[args.chr] = 'chr' + str(out[args.chr])
    #    chr_replace = ''
    #else:
    #    chr_replace = 'chr'
    new_pos = lo.convert_coordinate(format_chromosome(out[args.chr]), int(out[args.pos]))
    
    if new_pos is None:
        out[args.pos] = 'LIFTOVER_ERROR'
    elif len(new_pos) == 0:
        out[args.pos] = 'NA'
        missing_count += 1
    else:
        out[args.chr] = unformat_chromosome(out[args.chr], new_pos[0][0])
        out[args.pos] = new_pos[0][1]
        
    out = [str(x) for x in out]
    out = args.delim_out.join(out)
    out = out + '\n'
    file2.write(out)
    line_count+=1
    if line_count % 3_000_000 == 0:
        print(str(line_count)+'th snp converted')

print('Done!')
print(str(missing_count) + ' SNPs did not have a conversion build')
