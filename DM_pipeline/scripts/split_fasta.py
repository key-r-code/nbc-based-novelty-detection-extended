# This script splits a FASTA file into multiple chunks
from Bio import SeqIO
import os
import math

# Get input/output information from Snakemake
input_file = snakemake.input.fasta
output_dir = snakemake.params.outdir
num_chunks = snakemake.params.num_chunks

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Count sequences in the input file
with open(input_file) as f:
    seq_count = sum(1 for _ in SeqIO.parse(f, "fasta"))

# Calculate sequences per chunk (at least 1)
seqs_per_chunk = max(1, math.ceil(seq_count / num_chunks))

# Split the file
with open(input_file) as f:
    sequences = SeqIO.parse(f, "fasta")
    
    for i in range(num_chunks):
        chunk_seqs = []
        for _ in range(seqs_per_chunk):  # Fixed the * and seqs*per_chunk syntax error
            try:
                chunk_seqs.append(next(sequences))
            except StopIteration:
                break
        
        if chunk_seqs:  # Only write if we have sequences
            output_file = os.path.join(output_dir, f"chunk_{i+1}.fasta")
            SeqIO.write(chunk_seqs, output_file, "fasta")
        else:
            # Create empty file to maintain chunk count
            open(os.path.join(output_dir, f"chunk_{i+1}.fasta"), 'w').close()