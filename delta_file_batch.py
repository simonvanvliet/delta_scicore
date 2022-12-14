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
    
#set paths
root = pathlib.Path(pathlib.Path.home(), 'home', 'delta')
data_dir = root / 'data' 

#set filetype regexp
filetype = '*.dv'
short_name_regexp = '_R3D' #filenames are cutoff at this string

#create output dir
output_path = root / 'processed'
(output_path).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder

#get config file
config_file = root / 'delta_scicore' / 'config_2D.json'
cfg.load_config(config_file)

#set models
cfg.model_file_seg = to_str(root / 'models' / "unet_pads_seg.hdf5")
cfg.model_file_track = to_str(root / 'models' / "unet_pads_track.hdf5")
 
#find files
file_names = [f.name for f in sorted(data_dir.glob(filetype))]

for idx, file in enumerate(file_names):

    #make nickname of movie
    end = file.find(short_name_regexp)
    file_name_short = file[:end]
    
    #make subfolder for current position
    output_dir = output_path / file_name_short
    (output_dir).mkdir(exist_ok=True)

    try:  
        print('starting with movie %s' %file) 

        # Init reader (use bioformats=True if working with nd2, czi, ome-tiff etc):
        im_reader = xpreader(to_str(data_dir / file), use_bioformats=True)

        # Print experiment parameters to make sure it initialized properly:
        print("""Initialized experiment reader:
            - %d positions
            - %d imaging channels
            - %d timepoints"""%(im_reader.positions, im_reader.channels, im_reader.timepoints)
        )

        # Init pipeline:
        xp = Pipeline(im_reader, resfolder=to_str(output_dir))   

        # Run pipeline
        xp.process()
        
        # postprocess
        datafiles = [f.name for f in sorted((output_dir).glob('*.pkl'))]
                
        df = delta_to_df(output_dir / datafiles[0])
        df['movie_name'] = file_name_short
        df['replicate'] = idx
        
        #save data-frame
        save_name = file_name_short + '.csv'
        df.to_csv(output_dir / save_name)
        
    except:
        print('error with movie %s' %file) 

#exit python
import os
os._exit(os.EX_OK)
