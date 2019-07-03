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
    with pysam.AlignmentFile(args.input_bam) as bam:
        for aln in bam:
            rgid = aln.get_tag('RG') + "_" + aln.get_tag('CB')
            newrgs[rgid] = aln.get_tag('RG')
        oldrgs = {d["ID"]: d for d in bam.header["RG"]}

        newheader = bam.header.to_dict()

    rgsmlist = []
    for newrg, oldrg in sorted(newrgs.items()):
        rgdata = oldrgs[oldrg].copy()
        rgdata.update({"ID":newrg, "SM":newrg})
        rgsmlist.append(rgdata)
    newheader["RG"] = rgsmlist

    with pysam.AlignmentFile(args.input_bam) as bam, \
        pysam.AlignmentFile(args.output_bam, "wb", header=newheader) as out:
        for aln in bam:
            rgid = aln.get_tag('RG') + "_" + aln.get_tag('CB')
            aln.set_tag("RG", rgid)
            out.write(aln)

if __name__ == "__main__":
    main()
