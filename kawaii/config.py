import click 
from pathlib import Path
import os
from os import path


def init_config(main_config):
    
    android = main_config.get("android") or dict()
    sdk_root = os.environ.get("ANDROID_HOME") if os.environ.get("ANDROID_HOME") else os.environ.get("ANDROID_SDK_ROOT") if os.environ.get("ANDROID_SDK_ROOT") else android["sdk-root"]

    main_config["android"] = {

        **(main_config["android"] if "android" in main_config else {}),
        "sdk": os.environ.get("ANDROID_PLATFORM").removeprefix("android-") if os.environ.get("ANDROID_PLATFORM") else android["sdk"],
        "ndk": get_absolute_ndk(os.environ.get("NDK_VERSION") if os.environ.get("NDK_VERSION") else Path(os.environ.get("ANDROID_NDK_ROOT")).name if os.environ.get("ANDROID_NDK_ROOT") else android["ndk"], Path(sdk_root)),
        "sdk-root": sdk_root

    }

    return main_config


def set_environment(v, r):
    if v:
        os.environ["KAWAII_VERBOSE"] = "1"
    if r:
        os.environ["KAWAII_RECONFIGURE"] = "1"

    


def get_absolute_ndk(version: str, sdk_path: Path):
    path = sdk_path.joinpath("ndk")
    versions = list(path.glob(version))
    if len(version.split(".")) < 3:
        versions.extend(path.glob(version + ".*"))
    versions = list(set(versions))
    if len(versions) > 1:
        click.echo(f"Error: There are more than one NDK version installed that matches the {version} glob")
        exit(1)
    elif len(versions) == 0:
        click.echo(f"No versions")
        exit(1)

    return versions[0].name