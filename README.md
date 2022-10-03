# simple-and-kawaii
A very simple and kawaii build system focused on Android cross-compiling!

Kawaii at the moment only support projects that use the Git version control!! If you want Kawaii to be VCS-agnostic, feel free to contribute ^^
## Installation
As Kawaii is still early, you'll have to install it from Git.

```sh
git clone https://github.com/EchidnaHQ/simple-and-kawaii --filter=blob:none
cd simple-and-kawaii
pip install .
```
## Basic instructions
```sh
$ kawaii init # Will ask questions about your Android SDK locations and configuration and store them with the generated Meson cross-file in the .kawaii/cache folder relative to the root of the Git repository
$ kawaii build-deps # Will build all projects under the 'kawaii-deps' directory that has the 'kawaii.config.json' file. The directory path can be changed with the 'libs-folder' key in the '.kawaii/config.json' file!!!
$ kawaii build # Not yet implemented!!! Will build the current directory with automatic configurations.
# You can run the build commands directly. Use them in kawaii-build.sh scripts!
$ kawaii meson
$ kawaii cmake
$ kawaii autotools
$ kawaii cargo-apk # Runs https://crates.io/crates/cargo-apk. Please use our fork instead [here](https://github.com/EchidnaHQ/simple-and-kawaii) for the time being as Kawaii need some patches for `cargo-apk` to work property!
```

## Creating a Kawaiibuild collection
First, create a `kawaii.toml` at the root of a Git repository.
Then add the groups that you want your collection to have:

```toml
[collection]
collections = [
    "waylovely",
    "xlovely",
    "utils"
]
```

After that, just create the folders for the groups you want to make!!

```sh
$ mkdir utils xlovely waylovely
```

To make a package, create a `package_name.kawaii` file in one of the folders of your choosing. `package_name` being the name of the package of course!! ^^

```sh
$ touch utils/glib.kawaii
```

Then add the sources for the file!

```toml
[sources.glib] # Replace glib with your package's name
url = "file://./glib" # Replace ./glib with a path towards the source code of your package 
```

Kawaiibuild will automatically run the build command based on what build system it finds!! The implementation favors Meson first, then Cmake, then Autotools..

Would you like to change the build flags? You can do that by adding your own steps:

```toml
[sources.libxml2]
url = "file://./libxml2"
steps = [
    "kawaii cmake -DLIBXML2_WITH_TESTS=OFF -DLIBXML2_WITH_LZMA=OFF -DLIBXML2_WITH_HTTP=OFF -DLIBXML2_WITH_PYTHON=OFF
]
```

In this example, we explicitly tell Kawaii to use the Cmake build command with the build arguments that we pass!!

By the wayy, 
Kawaii will pass some environment variables to the build script! Look at [`build.py`](./simple_and_kawaii/build.py) for all the possible variables!

You can try building the collection with just:
```sh
$ kawaii
```

You can then use the collection inside of another Kawaii manifest outside of the repository:

```toml
collections = [
    "https://github.com/waylovely-project/kawaii-wraps"
]

deps = [
    "glib", "libffi"
]
```

## Requirements
To get started, let's do some things first:

- You'll need to get a copy of the SDK trough either Android Studio or Sdk Manager. The minimal SDK version is API 29 ^^
- For the NDK, I use the `23.2.8568313` version of the NDK ^^
- Since Waylovely depends on many C/C++ libraries, we'll need the build systems for those libraries too!
    - They are Meson, Cmake, and Autotools/GNU Make! 
- Then install the Rust toolchain for your target platform with [Rustup](https://rustup.rs/).
```sh
rustup target add armv7-linux-androideabi   # for arm
rustup target add i686-linux-android        # for x86
rustup target add aarch64-linux-android     # for arm64
rustup target add x86_64-linux-android      # for x86_64
rustup target add x86_64-unknown-linux-gnu  # for linux-x86-64
rustup target add x86_64-apple-darwin       # for darwin x86_64 (if you have an Intel MacOS)
rustup target add aarch64-apple-darwin      # for darwin arm64 (if you have a M1 MacOS)
rustup target add x86_64-pc-windows-gnu     # for win32-x86-64-gnu
rustup target add x86_64-pc-windows-msvc    # for win32-x86-64-msvc
...
```
- Then you'll need to install the [`cargo-apk`](https://crates.io/crates/cargo-apk) utility. It'll get installed to `~/.cargo/bin`, so please make sure it's loaded in your `PATH`.
```
$ cargo install cargo-apk
```
