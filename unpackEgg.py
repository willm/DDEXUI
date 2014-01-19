import os
import pkg_resources
import sys
from setuptools.archive_util import unpack_archive

def unpackEgg(modulo):
    eggs = pkg_resources.require(modulo)
    for egg in eggs:
        if os.path.isdir(egg.location):
            sys.path.insert(0, egg.location)
            continue
        unpack_archive(egg.location, ".")
    eggpacks = set()
    eggspth = open("./eggs.pth", "w")
    for egg in eggs:
        eggspth.write(os.path.basename(egg.location))
        eggspth.write("\n")
        eggpacks.update(egg.get_metadata_lines("top_level.txt"))
    eggspth.close()

    eggpacks.clear()

if __name__ == '__main__':
    unpackEgg(sys.argv[1])

