import os

def simple_hash(path):
    h = 0
    with open(path, "rb") as f:
        while True:
            chunk = f.read(32768)
            if not chunk:
                break
            for byte in chunk:
                h = (h * 31 + byte) % (10**9 + 7)
    return h


def remove_duplicates(folder):
    hashes = []
    for filename in os.listdir(folder):
        full_path = os.path.join(folder, filename)

        if os.path.isfile(full_path):
            h = simple_hash(full_path)
            if h in hashes:
                os.remove(full_path)   
            else:
                hashes.append(h)


remove_duplicates('./data/images')

