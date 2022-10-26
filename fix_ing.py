#!/usr/bin/env python
import re
import pathlib
import logging
import subprocess

logger = logging.getLogger(__name__)

ing_package = "pl.ing.mojeing"
google_installer = "com.android.vending"

def adb(args: list[str]) -> str:
    return subprocess.check_output(["adb"] + args)

def adb_pm(args: list[str]) -> str:
    return adb(["shell", "pm"] + args)

def get_size(name: str) -> int:
    return pathlib.Path(name).stat().st_size

def main() -> None:
    adb(["devices"])

    out = adb_pm(["path", ing_package]).decode()
    apks = [x.split(":")[1] for x in out.splitlines()]
    pulled_names = [f"ing_{i}.apk" for i in range(len(apks))]

    logger.warning(f"Found APKs {apks=}")

    for name, apk in zip(pulled_names, apks):
        adb(["pull", apk, name])

    for name in pulled_names:
        adb(["push", name, f"/data/local/tmp/"])

    logger.warning(f"{adb_pm(['uninstall', ing_package])=}")

    out = adb_pm(["install-create", "-S", str(len(apks)), "-i", google_installer]).decode()
    installation_id = re.findall(r"\[(\d+)\]", out)[0]

    for i, name in enumerate(pulled_names):
        adb_pm(["install-write", "-S", str(get_size(name)), str(installation_id), str(i), f"/data/local/tmp/{name}"])
    logger.warning(f"Finished, status = {adb_pm(['install-commit', str(installation_id)])}")


if __name__ == '__main__':
    main()
