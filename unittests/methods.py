import os
import shutil
from unittests.constants import *

def remove_output_dirs(dirs_list=[OUTPUT_JSON_PATH,WEB_DIR,WEB_DIR_ARCHIVE]):
    for this_item in dirs_list:
        if (this_item.endswith((".json",".tar.gz")) and os.path.exists(this_item)):
            os.remove(this_item)
        else:
            if os.path.exists(this_item):
                shutil.rmtree(this_item)