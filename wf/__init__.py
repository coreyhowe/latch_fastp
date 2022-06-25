#"""
#Pre-QC,Assemble,Post-QC,Annotate RNA reads
#"""

import subprocess
from pathlib import Path
import os

from latch import small_task, large_task, workflow
from latch.types import LatchFile, LatchDir



@small_task
def preqc_task(read1: LatchFile, read2: LatchFile, output_dir: LatchDir) -> (LatchFile, LatchFile):
	out_basename = str(output_dir.remote_path)
	read1_basname = str(os.path.basename(read1.local_path))
	read2_basename =  str(os.path.basename(read2.local_path))
	qc_read1 = Path("qc_read1.fq.gz").resolve()
	qc_read2 = Path("qc_read2.fq.gz").resolve()
	_fastp_cmd = [
    "fastp",
    "--in1",
    read1.local_path,
    "--in2",
    read2.local_path,
    "--out1",
    str(qc_read1),
    "--out2",
    str(qc_read2)]
	
	subprocess.run(_fastp_cmd)
	
	return (LatchFile(str(qc_read1),
	f"{out_basename}/{read1_basname}.fastp_qc.fq.gz"),
	LatchFile(str(qc_read2),
	f"{out_basename}/{read2_basename}.fastp_qc.fq.gz"))
	
@workflow
def fastp(read1: LatchFile, read2: LatchFile, output_dir: LatchDir) -> (LatchFile, LatchFile):
#def Fastp_Trinity(read1: LatchFile, read2: LatchFile, output_dir: LatchDir) -> (LatchFile, LatchDir):
    """

    # RNA De Novo Assembly
    
    A tool designed to provide fast all-in-one preprocessing for FastQ files. Read the documentation [here](https://github.com/OpenGene/fastp). 
    
    __metadata__:
        display_name: All-in-one preprocessing for FastQ files
        author:
            name: Corey Howe
            email: 	
            github: 
        repository: test
        license:
            id: MIT

    Args:

        read1:
          Paired-end read 1 file to be QC'd.

          __metadata__:
            display_name: Read1

        read2:
          Paired-end read 2 file to be QC'd.

          __metadata__:
            display_name: Read2
            
        output_dir:
          The directory where results will go.
          
          __metadata__:
            display_name: Output Directory
    """
    return preqc_task(read1=read1, read2=read2, output_dir=output_dir)
    
