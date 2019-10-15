import os
from presets import mid_preset, high_preset, low_preset
import yaml
import logging

logPath, fileName = os.getcwd(), 'interface_logger'
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s - %(threadName)s] [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logPath, fileName)),
        logging.StreamHandler()
    ])

logger = logging.getLogger()

# Initiate (Empty) Database or Load Existing One.
db_name = 'db-new.yaml'

if not os.path.exists(db_name):
    logging.info('No database found. Initializing.')
    with open(db_name, 'w') as db:
        DB = {freq: {} for freq in freq_list}  # populate outer-level keys with frequencies
        yaml.dump(DB, db)
else:
    logging.info("%s Database found, loaded."%db_name)
    with open(db_name, 'r') as db:
        DB = yaml.load(db, Loader=yaml.FullLoader)

oldDB = {}

for entry_key in DB:
    entry = DB[entry_key]
    entry_name = entry.get('freq', 1)
    if entry_name not in oldDB:
        oldDB[entry_name] = {}
        
    logging.info("converting %s-%s"%(entry_name, entry_key))
    
    shape = entry.get('shape', '(0,0)')
    shape = shape[1:-1] # strip parentheses
    shapes = shape.split(',') # break
    shape = (float(shapes[0]), float(shapes[1]))

    if shape[0] > 0:
        preset_fun = high_preset
    elif shape[0] < 0:
        preset_fun = low_preset
    else:
        preset_fun = mid_preset

    oldDB[entry_name][entry_key] = preset_fun(float(DB[entry_key]['min']),
                                              float(DB[entry_key]['max']),
                                              shape[1])
logging.info("Conversion accomplished from new to old schema.")
for d in oldDB:
    for f in oldDB[d]:
        print('%s-%s:'%(d,f), oldDB[d][f])

try:
    db_name = 'converted_' + db_name
    with open(db_name, 'w') as db:
        yaml.dump(oldDB, db)
    logging.info("Saved new yaml file %s to disc."%db_name)
except Exception as e:
    logging.info("Problem encountered! Stack trace to follow...")
    logging.info(e)