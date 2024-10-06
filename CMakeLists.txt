cmake_minimum_required(VERSION 3.22.1)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
# add_compile_options(-Wall -Wextra -Wpedantic)

project(ci-project VERSION 1.0
                   DESCRIPTION "CI Project"
                   LANGUAGES CXX)

include(FetchContent)
FetchContent_Declare(
   googletest
   GIT_REPOSITORY https://github.com/google/googletest.git
   GIT_TAG v1.14.0
)
FetchContent_MakeAvailable(googletest)

# This block needs to be above any building lines.
if(CMAKE_SYSTEM MATCHES Windows)
   execute_process(COMMAND python ./generate.py WORKING_DIRECTORY ./script/) # WINDOWS / script is subfolder
endif()
if(CMAKE_HOST_SYSTEM MATCHES Linux)
   execute_process(COMMAND python3 ./generate.py WORKING_DIRECTORY ../script/) # LINUX / script is parallel
endif()

include_directories(./lib/signals ./lib/buffer)

add_library(signals STATIC ./lib/signals/signals.cpp ./lib/buffer/buffer.o)
target_include_directories(signals PRIVATE ./lib/signals include) # PRIVATE/PUBLIC Both work fine

add_executable(test test/test.cpp)
target_link_libraries(test PRIVATE gtest_main signals) # PRIVATE/PUBLIC Both work fine

# The script folder is parallel to current folder in both cases.
if(CMAKE_SYSTEM MATCHES Windows)
   add_custom_target(generate COMMAND python ./generate.py WORKING_DIRECTORY ../script/) # WINDOWS
endif()
if(CMAKE_HOST_SYSTEM MATCHES Linux)
   add_custom_target(generate COMMAND python3 ./generate.py WORKING_DIRECTORY ../script/) # LINUX
endif()