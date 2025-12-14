import os

def clean_folder(src_folder, target_folder):
    names = []
    for filename in os.listdir(src_folder):
        path = os.path.join(src_folder, filename)
        if os.path.isfile(path):
            name = os.path.splitext(filename)[0]
            names.append(name)

    for filename in os.listdir(target_folder):
        path = os.path.join(target_folder, filename)
        if os.path.isfile(path):
            name = os.path.splitext(filename)[0]
            if name not in names:
                os.remove(path)

clean_folder('./data/images', './data/masks')

