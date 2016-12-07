#!/usr/bin/env python3

import os
import sys
import re
import subprocess as sub

XC_ROOT = os.environ.get('XC_ROOT', '')
xc_path = lambda x : os.path.join(XC_ROOT, x)

XC_ENC = xc_path('xc-enc')
XC_FRAMESIZE = xc_path('xc-framesize')
XC_SSIM = xc_path('xc-ssim')

def get_frame_sizes(y4m, targets_file):
    # first, run xc-enc in 'target frame size mode'
    try:
        enc_output = sub.check_output(
            '{xc_enc} -i y4m -F {targets_file} -q rt -o temp.ivf {y4m}'.format(
                xc_enc=XC_ENC,
                targets_file=targets_file,
                y4m=y4m), shell=True, stdin=sub.DEVNULL, stderr=sub.STDOUT)

        if not enc_output:
            raise Exception("xc-enc failed.")

        size_estimates = []

        for line in enc_output.decode('utf-8').strip().split('\n'):
            size_estimates += [int(re.findall("estimated size=(\d+)", line)[0])]

        output = sub.check_output(
            '{xc_framesize} temp.ivf'.format(xc_framesize=XC_FRAMESIZE),
            shell=True, universal_newlines=True)

        output = output.strip("\n").split("\n")
        frame_sizes = []

        for line in output[:-1]:
            frame_sizes += [int(line.split(" ")[1])]

        return (frame_sizes, size_estimates)

    finally:
        os.system('rm -f temp.ivf')

def get_target_sizes(targets_file, frame_count):
    target_sizes = []

    with open(targets_file) as fin:
        for line in fin:
            line = line.strip()
            if len(line) == 0: break
            target_sizes += [int(line)]

    if len(target_sizes) >= frame_count:
        return target_sizes[:frame_count]
    else:
        target_sizes += [target_sizes[-1]] * (frame_count - len(target_sizes))

    return target_sizes

def create_data_file(frame_sizes, size_estimates, target_sizes, output_file):
    i = 0

    with open(output_file, "w") as fout:
        for fs, es, ts in zip(frame_sizes, size_estimates, target_sizes):
            fout.write('{} {} {} {}\n'.format(i, fs, es, ts))
            i += 1

def run_test(y4m, targets_file, output_file):
    frame_sizes, size_estimates = get_frame_sizes(y4m, targets_file)
    target_sizes = get_target_sizes(targets_file, len(frame_sizes))
    create_data_file(frame_sizes, size_estimates, target_sizes, output_file)

    #print(sum([abs(x - y) for x, y in zip(frame_sizes, target_sizes)]) / len(frame_sizes))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: run_test.py <y4m> <targets_file> <output_file>")
        sys.exit(1)

    run_test(sys.argv[1], sys.argv[2], sys.argv[3])
