import hashlib
import os

def main():
    filepath = os.getenv("FILEPATH")

    hash_md5 = hashlib.md5()

    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    os.makedirs('tmp')
    text_file = open("/tmp/hash.txt", "w+")
    n = text_file.write(hash_md5.hexdigest())
    text_file.close()

    print(hash_md5.hexdigest())

