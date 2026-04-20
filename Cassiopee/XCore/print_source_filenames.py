"""Helper script invoked by CMake at configure time to obtain the list of C/C++
and Fortran source files for this module.

It imports ``srcs.py`` (located in the same directory) after injecting a stub
``KCore.Dist`` module so that optional-feature probes default to *disabled*.
CMake-level ``find_package`` / ``option`` calls in ``CMakeLists.txt`` are
responsible for enabling or disabling features at build time.
"""
import sys
import types
import os


def _make_stub_dist():
    """Return a minimal stub of KCore.Dist with all features disabled."""
    m = types.ModuleType("Dist")
    m.getAdditionalLibPaths = lambda: []
    m.getAdditionalIncludePaths = lambda: []
    m.getAdditionalLibs = lambda: []
    m.checkMpi = lambda: (False, "", "", [])
    m.checkMpi4py = lambda: (False, "", "")
    m.checkAdolc = lambda: (False, "", "", "")
    m.checkMpeg = lambda: (False, "", "")
    m.checkHdf = lambda: (False, "", "", [])
    m.checkNetcdf = lambda: (False, "", "", [])
    m.checkFortranLibs = lambda: (True, [], [])
    m.checkCppLibs = lambda: (True, [], [])
    m.checkPython = lambda: ("", "", "", [])
    m.checkNumpy = lambda: ("", "", "")
    m.checkModuleCassiopee = lambda name: ("", "", "")
    m.checkOCC = lambda: (False, "", "")
    m.getDistUtilsCompilers = lambda: ("", "", "", "", "", "", "")
    m.getCppArgs = lambda: []
    m.getCArgs = lambda: []
    m.getLinkArgs = lambda: []
    m.getf77Compiler = lambda: ""
    m.getCppCompiler = lambda: ""
    m.getAR = lambda: "ar"
    m.getSystem = lambda: ("linux", "")
    m.getInstallPath = lambda prefix="": prefix
    m.writeInstallPath = lambda: None
    m.writeSetupCfg = lambda: None
    m.symLinks = lambda: None
    m.isSimd = lambda f: False
    m.getEnvForScons = lambda: {}
    m.createFortranBuilder = lambda env, inc: env
    m.createFortranFiles = lambda env, srcs: []
    m.getOCCModules = lambda: []
    m.getFromConfigDict = lambda key, default=None: default
    return m


# Inject the stub before importing srcs so that any
# ``import KCore.Dist as Dist`` inside srcs.py succeeds.
_stub_dist = _make_stub_dist()
_stub_kcore = types.ModuleType("KCore")
_stub_kcore.Dist = _stub_dist
sys.modules.setdefault("KCore", _stub_kcore)
sys.modules["KCore.Dist"] = _stub_dist

# Ensure the directory containing srcs.py is on sys.path.
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

import srcs  # noqa: E402  (import must come after sys.path manipulation)

_sources = []
for _attr in ("cpp_srcs", "cpp_srcs1", "cpp_srcs2", "for_srcs", "fortran_srcs"):
    _val = getattr(srcs, _attr, None)
    if _val:
        _sources.extend(_val)

print("\n".join(s for s in _sources if s))
