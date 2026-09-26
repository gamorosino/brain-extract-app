#!/usr/bin/env python3
"""Skull-strip a T1w volume with FSL's bet.

Quick script for the T1w skull-stripping comparison -- just wraps `bet`
so I can sweep -f and -R on our cohort without retyping the command
every time.
"""
import argparse
import shutil
import subprocess
import sys


def run_bet(t1, out, frac=0.5, robust=False, bias_neck_cleanup=False):
    if shutil.which("bet") is None:
        sys.exit("FSL's `bet` not found on PATH -- source FSL's setup script first")

    cmd = ["bet", t1, out, "-f", str(frac)]
    if robust:
        cmd.append("-R")
    if bias_neck_cleanup:
        cmd.append("-B")

    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description="Skull-strip a T1w NIfTI with FSL BET")
    ap.add_argument("--t1", required=True, help="input T1w NIfTI (.nii or .nii.gz)")
    ap.add_argument("--out", required=True, help="output prefix for the brain-extracted volume")
    ap.add_argument("--frac", type=float, default=0.5, help="BET fractional intensity threshold (0-1, default 0.5)")
    ap.add_argument("--robust", action="store_true", help="use BET's robust brain center estimation (-R)")
    ap.add_argument("--bias-neck-cleanup", action="store_true", help="bias field + neck cleanup (-B)")
    args = ap.parse_args()

    run_bet(args.t1, args.out, frac=args.frac, robust=args.robust, bias_neck_cleanup=args.bias_neck_cleanup)


if __name__ == "__main__":
    main()
