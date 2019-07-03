#!/usr/bin/env python3
import pysam
from collections import Counter
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
    with pysam.AlignmentFile(args.input_bam) as bam:
        oldrgs = {d["ID"]: d for d in bam.header["RG"]}
        for aln in bam:
            rgdata = oldrgs[aln.get_tag('RG')].copy()
            rgid = aln.get_tag('RG') + "_" + aln.get_tag('CB')
            rgsm = rgdata["SM"] + "_" + aln.get_tag('CB')
            rgdata["ID"] = rgid
            rgdata["SM"] = rgsm
            newrgs[rgid] = rgdata
        newheader = bam.header.to_dict()

    newheader["RG"] = [d for rid, d in sorted(newrgs.items())]

    with pysam.AlignmentFile(args.input_bam) as bam, \
        pysam.AlignmentFile(args.output_bam, "wb", header=newheader) as out:
        for aln in bam:
            rgid = aln.get_tag('RG') + "_" + aln.get_tag('CB')
            aln.set_tag("RG", rgid)
            out.write(aln)

if __name__ == "__main__":
    main()
