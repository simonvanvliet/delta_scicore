# Using Delta on SciCore

## Access Scicore

- Access is via ssh: `ssh username@login.scicore.unibas.ch`
- To copy data use scp: `scp <options> source  destination`
  - Use the transfer nodes: `username@login-transfer.scicore.unibas.ch`
  - e.g. `scp file_in_active_path username@login-transfer.scicore.unibas.ch:home/folder_in_home_dir`

## Install miniconda

Download and install miniconda:

- `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
- `bash Miniconda3-latest-Linux-x86_64.sh`

Run  `conda init [shell_name]` where `shell_name` is the type of shell used by the cluster (e.g. `bash`, see instructions at end of installation step).

## Install delta environment

enter the following commands:

```bash
module purge
conda create -n delta2_env -c conda-forge cudnn=8 cudatoolkit=11 python=3.9 jupyterlab ipykernel openjdk ffmpeg pathlib pandas
conda activate delta2_env
pip install delta2 elasticdeform  bioformats
```

Note: this works on the A100 and RTX8000 partitions, for Pascal you will need `cudatoolkit=10`

## git clone repository

```bash
cd ~/home
mkdir delta
cd delta
git clone https://github.com/simonvanvliet/delta_scicore.git
```

## download models

```bash
cd ~/home/delta
curl -o models.zip https://drive.switch.ch/index.php/s/Gv3TP8qhxvMyRfn/download
unzip -q -j models.zip
```
