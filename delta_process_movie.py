
import pathlib
import delta.config as cfg
from delta.utilities import xpreader
from delta.pipeline import Pipeline
import tensorflow as tf

dev = tf.config.list_physical_devices()
print(dev)

def to_str(posixpath):
    return str(posixpath.resolve())   

#set paths
root = pathlib.Path(pathlib.Path.home(), 'home', 'delta')
data_dir = root / 'data'
file_name = 'kdb_003_snap1_4_MMStack_Pos0.ome.tif'

#create output dir
output_path = root / 'processed' / 'movie1'
(output_path).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder

#get config file
config_file = root / 'config_2D.json'
cfg.load_config(config_file)
cfg.save_format = ('pickle','movie')

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
    
#exit python
import os
os._exit(os.EX_OK)
