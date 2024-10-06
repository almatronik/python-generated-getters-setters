mkdir build
echo Rename the appropriate object file for your OS to object.o in lib/buffer
ar rvs ./build/buffer.a ./lib/buffer/buffer.o

cd script && python generate.py && cd ..
g++ -c -std=c++14 ./lib/signals/signals.cpp -I./lib/buffer -I./lib/signals -o ./build/signals.o
g++ -c -std=c++14 ./test/test.cpp -I./lib/signals -lgtest_main -lgtest -o ./build/test.o
g++ -std=c++14 ./build/test.o -I./lib/signals -lgtest_main -lgtest ./build/signals.o ./build/buffer.a -I./lib/buffer -o ./build/test

./build/test
rm -rf build
rm -rf ./script/__pycache__