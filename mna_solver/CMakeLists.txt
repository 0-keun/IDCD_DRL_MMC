###########################################################################
# CMakeLists.txt generated for component mna_solver
# Product type: executable
###########################################################################
cmake_minimum_required(VERSION 3.12)
project(mna_solver)

# Propagate the CMAKE_EXPORT_COMPILE_COMMANDS variable from the 
# environment if it is defined as an environment variable, but not as a 
# CMake variable. This is to work around a bug in CMake 3.19 when the 
# "NMake Makefiles" generator is selected.
if(DEFINED ENV{CMAKE_EXPORT_COMPILE_COMMANDS} AND NOT DEFINED CMAKE_EXPORT_COMPILE_COMMANDS)
    set(CMAKE_EXPORT_COMPILE_COMMANDS $ENV{CMAKE_EXPORT_COMPILE_COMMANDS})
endif()


# Set directory properties.
set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT mna_solver)

###########################################################################
## Path variables
###########################################################################
# Derive an absolute path to the code generation anchor folder.
get_filename_component(START_DIR ../../.. ABSOLUTE)

# Special directories defined by using CACHE variables can be overridden 
# by setting the variable from the command line, e.g.,
# 
# 	cmake . -DMATLAB_ROOT=/path/to/another/matlab/root
set(MATLAB_ROOT C:/Program\ Files/MATLAB/R2024b CACHE PATH "")

###########################################################################
## System Libraries
###########################################################################
find_library(FOUND_LIBM m NO_SYSTEM_ENVIRONMENT_PATH PATHS ${CMAKE_C_IMPLICIT_LINK_DIRECTORIES} ${CMAKE_CXX_IMPLICIT_LINK_DIRECTORIES})

###########################################################################
## Target definition and commands
###########################################################################

# Definition of target "mna_solver".
add_executable(mna_solver  ${START_DIR}/codegen/exe/mna_solver/rt_nonfinite.c
    ${START_DIR}/codegen/exe/mna_solver/rtGetNaN.c
    ${START_DIR}/codegen/exe/mna_solver/rtGetInf.c
    ${START_DIR}/codegen/exe/mna_solver/mna_solver_initialize.c
    ${START_DIR}/codegen/exe/mna_solver/mna_solver_terminate.c
    ${START_DIR}/codegen/exe/mna_solver/mna_solver.c
    ${START_DIR}/codegen/exe/mna_solver/colon.c
    ${START_DIR}/codegen/exe/mna_solver/mod.c
    ${START_DIR}/codegen/exe/mna_solver/mldivide.c)

# Set properties for target "mna_solver".
set_target_properties(mna_solver PROPERTIES PREFIX ""
    POSITION_INDEPENDENT_CODE ON
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH_USE_LINK_PATH TRUE)

# Specify language features required for target "mna_solver".
target_compile_features(mna_solver PUBLIC c_std_99)

# Specify compiler preprocessor definitions for target "mna_solver".
target_compile_definitions(mna_solver PRIVATE -D__USE_MINGW_ANSI_STDIO=1
    -DMODEL=mna_solver)

# Specify include directories for target "mna_solver".
target_include_directories(mna_solver PRIVATE ${START_DIR}/codegen/exe/mna_solver
    ${START_DIR}
    ${MATLAB_ROOT}/extern/include)

# Specify library link dependencies for target "mna_solver". CMake 
# generator expressions are used to create a CMakeLists.txt file that 
# supports multiple platforms with differently named system library 
# dependencies.
target_link_libraries(mna_solver PRIVATE $<$<BOOL:${FOUND_LIBM}>:m>
    $<$<BOOL:${WIN32}>:kernel32>
    $<$<BOOL:${WIN32}>:ws2_32>
    $<$<BOOL:${WIN32}>:mswsock>
    $<$<BOOL:${WIN32}>:advapi32>)

# Extract DWARF debug symbols into a separate file when building 
# executable programs for Apple platforms.
if(APPLE AND (CMAKE_C_COMPILER_ID STREQUAL "AppleClang"))
    string(APPEND _dsymutilcmd "$<IF:$<CONFIG:DEBUG,RELWITHDEBINFO>,"
                "xcrun;dsymutil;$<TARGET_FILE:mna_solver>;--flat,"
                "true"
        >)
    add_custom_command(TARGET mna_solver
            POST_BUILD
            COMMAND "${_dsymutilcmd}"
            COMMAND_EXPAND_LISTS
            BYPRODUCTS mna_solver.dwarf)
endif()


###########################################################################
## Target install rules
###########################################################################

# Install rule for executable target "mna_solver". The "OPTIONAL" keyword 
# is required to support SIL/PIL when build of the final executable is 
# suppressed.
install(TARGETS mna_solver
    RUNTIME DESTINATION "."
    OPTIONAL)

# Install rule for Microsoft PDB debug symbols, if required.
if(CMAKE_C_LINKER_SUPPORTS_PDB)
    install(FILES $<TARGET_PDB_FILE:mna_solver>
        DESTINATION .
        OPTIONAL
        CONFIGURATIONS Debug RelWithDebInfo)
endif()

# Install rule for Apple DWARF debug symbols, if required.
if(APPLE AND (CMAKE_C_COMPILER_ID STREQUAL "AppleClang"))
    install(FILES $<TARGET_FILE_DIR:mna_solver>/mna_solver.dwarf
        DESTINATION .
        OPTIONAL
        CONFIGURATIONS Debug RelWithDebInfo)
endif()

###########################################################################
## Build success message
###########################################################################
add_custom_command(TARGET mna_solver POST_BUILD
     COMMAND ${CMAKE_COMMAND} -E cmake_echo_color --cyan "\\#\\#\\# Created executable: $<TARGET_FILE:mna_solver>")

###########################################################################
## Call toolchain hook function if defined
###########################################################################
if(COMMAND toolchain_target_hook)
    toolchain_target_hook(mna_solver)
endif()
