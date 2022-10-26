#!/usr/bin/env python
import re
import logging
import subprocess
import os

logger = logging.getLogger(__name__)

ing_package = "pl.ing.mojeing"
google_installer = "com.android.vending"

mode_standalone = os.getenv("ING_STANDALONE") is not None

def shell(*args) -> str:
    prefix = ["adb", "shell"]
    if mode_standalone:
        prefix = []
    return subprocess.check_output(prefix + list(args)).decode()

def pm(*args) -> str:
    return shell("pm", *args)

def adb_devices() -> None:
    if not mode_standalone:
        logging.warning("Initializing connection with device via ADB")
        subprocess.check_output("adb devices".split())

def get_size(file_path) -> str:
    return str(int(shell("stat", "-c", "%s", file_path)))

def main() -> None:
    adb_devices()

    out = pm("path", ing_package)
    apks = [x.split(":")[1] for x in out.splitlines()]
    logger.warning(f"Found APKs {apks=}")

    copied_names = [f"ing_{i}.apk" for i in range(len(apks))]

    for name, apk in zip(copied_names, apks):
        shell("cp", apk, f"/data/local/tmp/{name}")

    pm('uninstall', ing_package)

    out = pm("install-create", "-S", str(len(apks)), "-i", google_installer)
    installation_id = re.findall(r"\[(\d+)\]", out)[0]

    for i, name in enumerate(copied_names):
        name = f"/data/local/tmp/{name}"
        pm("install-write", "-S", get_size(name), str(installation_id), str(i), name)
    logger.warning("Finished, status = " + pm('install-commit', str(installation_id)))


if __name__ == '__main__':
    main()
