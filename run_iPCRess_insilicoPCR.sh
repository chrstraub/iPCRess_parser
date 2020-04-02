#!/bin/bash
#
#SBATCH --job-name=iPCRess
#SBATCH --mail-type=FAIL,END
#SBATCH -o %j.out      # STDOUT
#SBATCH -e %j.err      # STDERR
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=04:00:00
#SBATCH -p prod                # partition(queue)

/home/software/exonerate-2.2.0-x86_64/bin/ipcress --products --mismatch 1 /test/input/primers.txt /test/input/db.fasta



