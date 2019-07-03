#!/usr/bin/env python3
import pysam
from collections import Counter
from sys import stdin, stdout, stderr
import argparse


def main():
    ap = argparse.ArgumentParser("bamCB2RG")
    ap.add_argument("input_bam", type=str,
                    help="Input bam file with RG and CB read tags")
    ap.add_argument("output_bam", type=str,
                    help="Output bam file with RG tags set to each read's CB tag")

    args = ap.parse_args()

    newrgs = {}
    rgsmlist = set()
    print("Reading bam to generate new header", file=stderr)
    with pysam.AlignmentFile(args.input_bam) as bam:
        oldrgs = {d["ID"]: d for d in bam.header["RG"]}
        for i, aln in enumerate(bam):
            rgdata = oldrgs[aln.get_tag('RG')].copy()
            rgid = aln.get_tag('RG') + "_" + aln.get_tag('CB')
            rgsm = rgdata["SM"] + "_" + aln.get_tag('CB')
            rgdata["ID"] = rgid
            rgdata["SM"] = rgsm
            newrgs[rgid] = rgdata
            if i > 0 and i % 100000 == 0:
                print("\t{:0.0f}k reads".format(i/1000), file=stderr)
        newheader = bam.header.to_dict()
        print("\tDone making new header from", i, "reads", file=stderr)

    newheader["RG"] = [d for rid, d in sorted(newrgs.items())]

    with pysam.AlignmentFile(args.input_bam) as bam, \
        pysam.AlignmentFile(args.output_bam, "wb", header=newheader) as out:
        print("Writing new bam file with corrected read tags", file=stderr)
        for i, aln in enumerate(bam):
            rgid = aln.get_tag('RG') + "_" + aln.get_tag('CB')
            aln.set_tag("RG", rgid)
            out.write(aln)
            if i > 0 and i % 100000 == 0:
                print("\t{:0.0f}k reads".format(i/1000), file=stderr)
        print("\tDone making new bam! Total of", i, "reads", file=stderr)

if __name__ == "__main__":
    main()
