#!/usr/bin/env python
import re
import logging
import subprocess

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ing_package = "pl.ing.mojeing"
google_installer = "com.android.vending"

def shell(*args) -> str:
    prefix = ["adb", "shell"]
    return subprocess.check_output(prefix + list(args)).decode()

def pm(*args) -> str:
    return shell("pm", *args)

def adb_devices() -> None:
    logging.info("Initializing connection with device via ADB")
    logging.info("You may need to accept connection on a dialog in your phone.")
    subprocess.check_("adb devices".split())

def get_size(file_path) -> str:
    return str(int(shell("stat", "-c", "%s", file_path)))

def main() -> None:
    adb_devices()

    out = pm("path", ing_package)
    apks = [x.split(":")[1] for x in out.splitlines()]
    logger.info(f"Found APKs {apks=}")

    copied_paths = [f"/data/local/tmp/ing_{i}.apk" for i in range(len(apks))]

    for name, apk in zip(copied_paths, apks):
        shell("cp", apk, name)
    logger.info("Copied split apk files to /data/local/tmp/")

    pm('uninstall', ing_package)
    logger.info("Uninstalled old version.")

    out = pm("install-create", "-S", str(len(apks)), "-i", google_installer)
    installation_id = re.findall(r"\[(\d+)\]", out)[0]
    logger.info(f"Current {installation_id=}.")

    for i, name in enumerate(copied_paths):
        pm("install-write", "-S", get_size(name), str(installation_id), str(i), name)
    logger.info("Finished, status = " + pm('install-commit', str(installation_id)))


if __name__ == '__main__':
    main()
