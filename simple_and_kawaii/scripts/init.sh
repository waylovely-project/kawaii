#/bin/sh
echo "Hii! Welcome to Waylovely's init scripts 😊"
if [ -z $ANDROID_SDK_ROOT ]; then
    
    read -p "Where is your lovely Android Sdk folder?" $ANDROID_SDK_ROOT

fi

if [ -z $ANDROID_NDK_ROOT ]; then
    read -p "What NDK version would you like to use?" ndkver

    export ANDROID_NDK_ROOT=$ANDROID_SDK_ROOT/ndk/$ndkver
fi

python3 <<EOF

EOF


curdir=$(dirname "$0")
cd $curdir/meson-crossfiles


cp crossfile.ini.in $ANDROID_ABI.ini
sed $ANDROID_ABI.ini "s/@target_arch@/$ABI_FULL"

