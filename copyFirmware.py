import pathlib
import os
import shutil
import time

currentPath = pathlib.Path(__file__).parent.resolve()
os.chdir(currentPath)
fileCount = 0

for file in pathlib.Path(str(currentPath)+'\\.pio\\build').rglob('*.bin'):
    shutil.copy(file, str(currentPath)+'\\Firmware\\'+file.name)
    fileCount += 1
for file in pathlib.Path(str(currentPath)+'\\.pio\\build').rglob('*.elf'):
    shutil.copy(file, str(currentPath)+'\\Firmware\\'+file.name)
    fileCount += 1
print(str(fileCount)+' files copied')
time.sleep(5)
exit(0)