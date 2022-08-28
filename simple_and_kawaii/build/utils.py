from os import path
import os
from pathlib import Path
import click
from .project import packages_folder
from simple_and_kawaii.utils import get_config_key, get_cpu_info, get_host_arch, get_host_os, show_top_level
def get_envvars(command: str, **kwargs):
    cwd = kwargs.get("cwd") or os.getcwd()
    missing_config = False
    for required_config in [
    "android-abi",
    "android-sdk-root",
    "android-ndk-version",
    "android-platform",
    ]:
        if not get_config_key(required_config):
            click.echo(
                f"{required_config} is not present in the cache_config file! Please run kawaii init ^^",
                    err=True,
            )
            missing_config = True

    if missing_config:
        exit(1)
    packages_folder_dir = packages_folder()

    prefix = path.join(packages_folder_dir, path.basename(cwd))

    pkgconfig_path = ":".join(
        map(lambda path: str(path), Path(packages_folder_dir).glob("**/pkgconfig"))
    )
    android_ndk_root = path.join(
        get_config_key("android-sdk-root"), "ndk", get_config_key("android-ndk-version")
    )

    android_toolchain = path.join(
        android_ndk_root,
        "toolchains",
        "llvm",
        "prebuilt",
        f"{get_host_os()}-{get_host_arch()}",
    )

    def toolchain_arch_script(script: str):
        return path.join(
            android_toolchain,
            "bin",
            f"{get_cpu_info(get_config_key('android-abi'))['triple']}{get_config_key('android-platform')}-{script}",
        )

    def toolchain_script(script: str):
        return path.join(android_toolchain, "bin", script)

    
    args = list(kwargs.get("args") or "")
    args.insert(0, command)
    env = {
        "ANDROID_ABI": get_config_key("android-abi"),
        "ANDROID_SDK_ROOT": get_config_key("android-sdk-root"),
        "ANDROID_NDK_ROOT": android_ndk_root,
        "ANDROID_PLATFORM": "android-" + get_config_key("android-platform"),
        "PATH": os.environ.get("PATH"),
        "PREFIX": prefix,
        "TOOLCHAIN": android_toolchain,
        "PACKAGES_FOLDER": packages_folder_dir,
        "PKG_CONFIG_PATH": pkgconfig_path,
        "PKG_CONFIG_SYSROOT_DIR": path.join(android_toolchain, "sysroot"),
        "ABI_TRIPLE": get_cpu_info(get_config_key("android-abi"))["triple"],
        "MESON_CROSSFILE": path.join(
                show_top_level(),
            "kawaii",
            "cache",
                f"meson-{get_config_key('android-abi')}.ini",
            ),
            # Cross-compiling configuration for Autoconf based buildsystems
        "CC": toolchain_arch_script("clang"),
        "AR": toolchain_script("llvm-ar"),
        "AS": toolchain_arch_script("clang"),
        "CXX": toolchain_arch_script("clang++"),
        "LD": toolchain_script("ld"),
        "RANLIB": toolchain_script("llvm-ranlib"),
        "STRIP": toolchain_script("llvm-strip"),
    }

    return (env, cwd, args)
