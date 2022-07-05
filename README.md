# simple-and-kawaii
A very simple and kawaii build system focused on Android cross-compiling!

## Installation
As Kawaii is still early, you'll have to install it from Git.

```sh
git clone https://github.com/EchidnaHQ/simple-and-kawaii --filter=blob:none
cd simple-and-kawaii
pip install .
```
## Basic instructions
```
$ kawaii init # Will ask questions about your Android SDK locations and configuration and store them with the generated Meson cross-file in the .kawaii/cache folder relative to the root of the Git repository
$ kawaii build-deps # Will build all projects under the 'kawaii-deps' directory that has the 'kawaii.config.json' file. The directory path can be changed with the 'libs-folder' key in the '.kawaii/config.json' file!!!
$ kawaii build # Not yet implemented!!! Will build the current directory with automatic configurations.
# You can run the build commands directly. Use them in kawaii-build.sh scripts!
$ kawaii meson
$ kawaii cmake
$ kawaii autotools
$ kawaii cargo-apk # Runs https://crates.io/crates/cargo-apk. Please use our fork instead [here](https://github.com/EchidnaHQ/simple-and-kawaii) for the time being as Kawaii need some patches for `cargo-apk` to work property!
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

### Native library dependencies
To compile a native library for use as a dependency, add the Git repo as a submodule to the `kawaii-deps` folder on the root of your Git repository. Then create a file named `kawaii.config.json` on the root of the library that you want to be built and add the dependencies!!!

```json
{
    "deps":[]
}
```

If the project doesn't have any dependencies, please set it to an empty array, since 'deps' is a required field.

Kawaii will then detect the build system used by the project. Meson is preferred to CMake, and both of them are preferred to Autotools. 

As the project might use neither of them or need custom configurations, you can specify the build instructions in the 'kawaii-build.sh' script like this!!!
```sh
kawaii meson -Ddocumentation=false \ # Pass your Meson arguments to the script!
            -Dc_link_args="-v" # It'll pass it to Meson!
```

Kawaii will pass some environment variables to the build script! Look at [`build.py`](./simple_and_kawaii/build.py) for all the possible variables!