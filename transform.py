import os
import transform_headings

for subdir, dirs, files in os.walk("./out"):
    for file in files:
        path = os.path.join(subdir, file)
        transform_headings.main(path)
