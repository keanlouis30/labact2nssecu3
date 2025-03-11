import subprocess
import os
import time


kape_path = r"KAPE/kape.exe"  
output_dir = r"K:\Regfile output"  
recmd_path = r"RECmd/RECmd.exe"  

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Command to extract registry hives using KAPE
kape_command = [
    kape_path,
    '--tsource', 'C:',
    '--tdest', output_dir,
    '--target', 'RegistryHives', 
    '--vhdx',  
    '--flush',  
    '--debug'  
]

print("Starting registry hive extraction with KAPE...")
subprocess.run(kape_command, check=True)
print("Extraction completed.")

for root, dirs, files in os.walk(output_dir):
    for file in files:
        if file.endswith('.hive') or file.endswith('.dat'):
            hive_path = os.path.join(root, file)
            recmd_command = [
                recmd_path,
                '-f', hive_path,
                '--bn', 'RECmd/BatchExamples/DFIRBatch.reb',
                '--csv', os.path.join(output_dir, f"{file}_parsed.csv")
            ]
            print(f"Parsing {hive_path} with RECmd...")
            subprocess.run(recmd_command, check=True)
            print(f"Parsing completed for {hive_path}.")

print("All registry hives have been processed.")