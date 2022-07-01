#/bin/bash

. "$(dirname $0)/shared.sh"

cmake -DCMAKE_TOOLCHAIN_FILE=$(readlink -f $ANDROID_NDK_PATH/build/cmake/android.toolchain.cmake) \
-DANDROID_ABI=$ANDROID_ABI -DANDROID_PLATFORM=$ANDROID_PLATFORM \
--install-prefix=$PREFIX -G ninja "$@"

ninja install