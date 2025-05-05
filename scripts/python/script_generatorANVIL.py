import sys
import os

def generate_script(script_name, command):
    script_content = f"""#!/bin/bash

#SBATCH -A bio240304
#SBATCH -p shared
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=48:00:00
#SBATCH --mem=250GB
#SBATCH --cpus-per-task=1

. ~/.bashrc
start=`date +%s`

{command}

end=`date +%s`
runtime=$((end-start))
echo "run time: $runtime"
"""

    with open(script_name, 'w') as script_file:
        script_file.write(script_content)

    os.chmod(script_name, 0o755)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 script_generator.py <script_name> <command>")
        sys.exit(1)

    script_name = sys.argv[1]
    command = sys.argv[2]
    generate_script(script_name, command)