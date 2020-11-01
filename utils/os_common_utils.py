import os
import errno

def create_file_and_parent_folders():
    """
    Creates a file with desired mode and creates necessary folders if this behavior is wanted and they do not exist.
    If for example, one wants to create file foo.txt with this path: /home/user/foo.txt, the home and user folders
    will be created if they do not already exist. Otherwise, no folders will be created.

    :param create_parent_folders specifies whether folders need to be created if they do not exist
    "param file_mode file mode (a, w, r, etc.)
    
    """
    tokens = file_path.split("/")
    for idx, tok in enumerate(tokens):
        if idx > 0:
            
        if not os.path.exists(c):
            os.makedirs(config_json_content["logFolderPath"])

def create_all_folders_for_path(path):
    try:
        tokens = []
        if len(path) == 0:
            return 0
        if path[0] == "/":           
            tokens = path[1:len(path)].split("/")
        if len(tokens) == 0:
            return 0
        curr_path = tokens[0]
        for tok in tokens:
            if not os.path.exists(tok):
                os.makedirs(tok)
    except:
