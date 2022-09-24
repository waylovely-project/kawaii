from os import path
import os
from pathlib import Path
import click
from .project import packages_folder
from simple_and_kawaii.utils import get_cpu_info, get_host_arch, get_host_os, show_top_level
def get_envvars(command, arch, app_id, main_config, **kwargs):

    cwd = kwargs.get("cwd") or os.getcwd()
    missing_config = False
    android_config = main_config.get("android")
    if not android_config:
        click.echo(f"Non Android builds are not supported at the moment!!", err=True)
        exit(1)

    for required_config in [
        "ndk",
        "sdk",
    ]:
        if not android_config.get(required_config):
            click.echo(
                f"{required_config} is not present in the cache_config file! Please run kawaii init ^^",
                    err=True,
            )
            missing_config = True

    if missing_config:
        print("Config is missing!")
        exit(1)

    packages_folder_dir = packages_folder(arch, main_config)
    
    prefix = path.join(packages_folder_dir, path.basename(cwd))

    pkgconfig_path = ":".join(
        map(lambda path: str(path), Path(packages_folder_dir).glob("**/pkgconfig"))
    )    
    try:
        android_ndk_root = path.join(
        main_config["android"]["sdk-root"], "ndk", str(main_config["android"]["ndk"])
        )
    except:

        print(main_config["android"]["sdk-root"])
        exit(1)

    android_toolchain = path.join(
        android_ndk_root,
        "toolchains",
        "llvm",
        "prebuilt",
        f"{get_host_os()}-{get_host_arch()}",
    )

    def toolchain_arch_script(script: str, arch):
        return path.join(
            android_toolchain,
            "bin",
            f"{get_cpu_info(arch)['triple']}{main_config['android']['sdk']}-{script}",
        )

    def toolchain_script(script: str):
        return path.join(android_toolchain, "bin", script)


    env = {
        "ANDROID_ABI": arch,
        "ANDROID_SDK_ROOT": main_config["android"]["sdk-root"],
        "ANDROID_NDK_ROOT": android_ndk_root,
        "ANDROID_PLATFORM": "android-" + str(main_config["android"]["sdk"]),
        "PATH": os.environ.get("PATH"),
        "PREFIX": prefix,
        "TOOLCHAIN": android_toolchain,
        "PACKAGES_FOLDER": packages_folder_dir,
        "PKG_CONFIG_PATH": pkgconfig_path,
        "PKG_CONFIG_SYSROOT_DIR": path.join(android_toolchain, "sysroot"),
        "ABI_TRIPLE": get_cpu_info(arch)["triple"],
        "MESON_CROSSFILE": path.join(
                show_top_level(),
            "kawaii",
            "cache",
                f"meson-{arch}.ini",
            ),
            # Cross-compiling configuration for Autoconf based buildsystems
        "CC": toolchain_arch_script("clang", arch),
        "AR": toolchain_script("llvm-ar"),
        "AS": toolchain_arch_script("clang", arch),
        "CXX": toolchain_arch_script("clang++", arch),
        "LD": toolchain_script("ld"),
        "RANLIB": toolchain_script("llvm-ranlib"),
        "STRIP": toolchain_script("llvm-strip"),
    }
    env = {
        "abi": arch,
        "android": main_config["android"],
        "prefix": prefix,
        "toolchain": android_toolchain,
        "packages_folder": packages_folder_dir,
        "abi_triple": env["ABI_TRIPLE"],
        "env": env,
        "app_id": app_id
    }
    return (env, cwd )

