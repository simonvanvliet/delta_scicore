
import pathlib
import json
import delta.config as cfg
from delta.utilities import xpreader
from delta.pipeline import Pipeline
from delta_postprocess import delta_to_df 
import tensorflow as tf

dev = tf.config.list_physical_devices()
print(dev)

def to_str(posixpath):
    return str(posixpath.resolve())   

def save_config(cfg, posixpath):
    with open(posixpath, 'w') as f:
        json.dump(cfg, f, indent=2)
    
#set paths
root = pathlib.Path(pathlib.Path.home(), 'home', 'delta')
data_dir = root / 'data'
file_name = 'kdb_003_snap1_4_MMStack_Pos0.ome.tif'
output_name = 'movie1'

#create output dir
output_path = root / 'processed' / output_name
(output_path).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder

#get config file
config_file = root / 'delta_scicore' / 'config_2D.json'
cfg.load_config(config_file)

#set models
cfg.model_file_seg = to_str(root / 'models' / "unet_pads_seg.hdf5")
cfg.model_file_track = to_str(root / 'models' / "unet_pads_track.hdf5")

#save config       
save_config(cfg, output_path / 'config.json')     
        
# Init reader (use bioformats=True if working with nd2, czi, ome-tiff etc):
im_reader = xpreader(to_str(data_dir / file_name), use_bioformats=True)

#Use for tiff files    
#im_reader = xpreader(
    # to_str(data_dir), 
    # prototype = 'pos%01i_ch%01i_frm%04i.tif',
    # fileorder = 'pct',
    # filenamesindexing=0)

# Print experiment parameters to make sure it initialized properly:
print("""Initialized experiment reader:
    - %d positions
    - %d imaging channels
    - %d timepoints"""%(im_reader.positions, im_reader.channels, im_reader.timepoints)
)

# Init pipeline:
xp = Pipeline(im_reader, resfolder=to_str(output_path))   

# Run pipeline
xp.process()

# postprocess
datafiles = [f.name for f in sorted((output_path).glob('*.pkl'))]
        
df = delta_to_df(output_path / datafiles[0])
df['movie_name'] = output_name
df['replicate'] = 0

#save data-frame
save_name = output_name + '.csv'
df.to_csv(output_path / save_name)
    
#exit python
import os
os._exit(os.EX_OK)
