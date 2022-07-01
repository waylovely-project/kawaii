#/bin/sh

export PACKAGES_FOLDER=$(readlink -f "$(dirname $0)/../libs/$ANDROID_ABI/")
# Don't mix up .pc files from your host and build target
export PKGCONFIG_DIRS=$(find $PACKAGES_FOLDER -wholename "**/pkgconfig" -print0 | xargs -0)
export PKG_CONFIG_PATH=${PKGCONFIG_DIRS// /:}
export PROJECT_NAME=${PWD##*/}
export PREFIX=$PACKAGES_FOLDER/$PROJECT_NAME
#export INCLUDE_DIRS=$(find $PACKAGES_FOLDER -wholename "**/include" -print0 | xargs -0)
#export INCLUDE_FLAGS=-I${INCLUDE_DIRS// / -I}
export ANDROID_PREFIX="$ANDROID_NDK_ROOT/toolchains/llvm/prebuilt/linux-x86_64"
export PKG_CONFIG_SYSROOT_DIR="${ANDROID_PREFIX}/sysroot"

# use the clang compiler
export PATH=$ANDROID_PREFIX/bin:$PATH