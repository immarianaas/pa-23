import glob
import os
from pathlib import Path
import subprocess

dir = Path("project/pa-app/")

for file in (dir).glob("target/**/*.class"):
    print(file)
    temp = file.relative_to(dir / "target")
    decompiled = dir / "decompiled" / temp.with_suffix("").with_suffix(".json")
    decompiled.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["jvm2json", "-s", file, "-t", decompiled])
