# Installation on windows (using msys2)

## Install msys2
Download msys2 (https://www.msys2.org)
and install it.

## Install dependencies
In an msys2 mingw64 terminal:
```shell
pacman -S mingw64/mingw-w64-x86_64-gcc
pacman -S mingw64/mingw-w64-x86_64-gcc-fortran
pacman -S mingw64/mingw-w64-x86_64-python
pacman -S mingw64/mingw-w64-x86_64-python-numpy
pacman -S mingw64/mingw-w64-x86_64-cmake        # CMake build system (recommended)
pacman -S mingw64/mingw-w64-x86_64-ninja        # optional: faster generator for CMake
pacman -S mingw64/mingw-w64-x86_64-python-pip
pacman -S mingw64/mingw-w64-x86_64-python-pip-tools
pacman -S mingw64/mingw-w64-x86_64-hdf5
pacman -S mingw64/mingw-w64-x86_64-opencascade
```

> **Note:** `scons` (`mingw64/mingw-w64-x86_64-scons`) is no longer required
> when using the CMake build path.  Install it only if you intend to use the
> legacy SCons build (`PRODMODE` 0–3).

For parallel:
First install Microsoft mpi redistribution. Then:
```shell
pacman -S mingw64/mingw-w64-x86_64-msmpi
pacman -S mingw-w64-x86_64-python-mpi4py
```

<!-- For optional tigl:
```shell
pacman -S mingw64/mingw-w64-x86_64-libxml2
pacman -S mingw-w64-x86_64-python-libxstl
pacman -S mingw64/mingw-w64-x86_64-boost
pacman -S mingw64/mingw-w64-x86_64-sympy
``` -->

and export system paths (if not already done):
```shell
export PATH=/mingw64/bin:$PATH
export LD_LIBRARY_PATH=/mingw64/lib:$LD_LIBRARY_PATH
```

## Install Cassiopee (CMake – recommended)

```shell
export CASSIOPEE=<your_path>/Cassiopee
export MACHINE=msys2
    
source $CASSIOPEE/Cassiopee/Envs/sh_Cassiopee_r8
cd $CASSIOPEE/Cassiopee

# Configure, build, and install with CMake:
cmake -S Cassiopee -B build -G Ninja \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX="$CASSIOPEE/Dist/bin/msys2_r8"
cmake --build build -j$(nproc)
cmake --install build
```

Or using the helper install script with `PRODMODE=4`:

```shell
export PRODMODE=4
./Cassiopee/install
```

## Install Cassiopee (legacy SCons – still supported)

```shell
export CASSIOPEE=<your_path>/Cassiopee
export MACHINE=msys2
    
source $CASSIOPEE/Cassiopee/Envs/sh_Cassiopee_r8
cd $CASSIOPEE/Cassiopee
./install
```

## Some usefull pacman commands

Update system:
```shell
pacman -Syu
```

Find package matching keyword:
```shell
pacman -Ss <keyword>
```

Install package:
```shell
pacman -S <package>
```

List installed packages:
```shell
pacman -Q
```

Remove package:
```shell
pacman -Rs <package>
```