# directory structure

DM_pipeline/
├── pipeline.yaml      # Pipeline definition
├── factory.py         # Dynamic task generator
├── params.yaml        # Configuration parameters
├── tasks/             # Task scripts
│   ├── gunzip.py
│   ├── create_fna.py
│   ├── create_directory.py
│   ├── split_fna.py
│   └── create_bash.py
├── run_pipeline.slurm  # Slurm job script
└── products/          # Output directory
└── README.md  