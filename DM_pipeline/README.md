# snakemake pipeline
├── Snakefile           # Main workflow definition
├── config.yaml         # Configuration parameters (chunk size, etc.)
├── scripts/            # Helper scripts
│   ├── fastq_to_fasta.py
│   └── generate_job_scripts.py
└── input/              # Your gzipped FASTQ files