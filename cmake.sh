cmake -G "Unix Makefiles" -B build
cd build && make
./test
cd ..
rm -rf build
rm -rf ./test
rm -rf ./lib/signals
