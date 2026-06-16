import hashlib
import json
import os
import shutil
import stat
import subprocess
from pathlib import Path

# aergia package manager
# by las-r

# lib directory path
LIBSDIR = Path(__file__).resolve().parent.parent / "lib"

# helpers
def init():
    if not LIBSDIR.exists():
        LIBSDIR.mkdir(parents=True)
        
def validate(manifest):
    required = ["name", "author", "version", "dependencies", "src"]
    for field in required:
        if field not in manifest:
            raise ValueError(f"Missing mandatory field in aerpkg.json: {field}")
        
def remreadonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

# user functions
def install(repourl, icache=None):
    if icache is None:
        icache = set()
    if repourl in icache:
        return
    icache.add(repourl)
    init()
    print(f"Installing {repourl}...")
    hashurl = hashlib.sha224(repourl.encode("utf-8")).hexdigest()
    temppath = LIBSDIR / f"temp_{hashurl}"
    if temppath.exists(): 
        shutil.rmtree(temppath, onerror=remreadonly)
    try:
        subprocess.check_call(["git", "clone", repourl, str(temppath)])
        manifestpath = temppath / "aerpkg.json"
        if not manifestpath.exists():
            raise Exception("No aerpkg.json found in the repository.")
        with open(manifestpath, "r") as f:
            manifest = json.load(f)
            validate(manifest)
        for url in manifest["dependencies"]:
            install(url, icache)
        finalpath = LIBSDIR / manifest["name"]
        if finalpath.exists(): 
            shutil.rmtree(finalpath, onerror=remreadonly)
        shutil.move(str(temppath), str(finalpath))
        print(f"Successfully installed {manifest['name']} v{manifest['version']}")
    except Exception as e:
        if temppath.exists(): 
            shutil.rmtree(temppath, onerror=remreadonly)
        print(f"Installation failed: {e}")
        raise e

def remove(pkgname):
    pkgpath = LIBSDIR / pkgname
    if pkgpath.exists():
        shutil.rmtree(pkgpath, onerror=remreadonly)
        print(f"Removed {pkgname}")
    else:
        print(f"Package '{pkgname}' not found.")

def listpackages():
    init()
    pkgs = [d for d in LIBSDIR.iterdir() if d.is_dir()]
    if not pkgs:
        print("No packages installed.")
        return
    print(f"{'NAME':<20} | {'AUTHOR':<15} | {'VERSION':<10}")
    print("-" * 50)
    for pkg in pkgs:
        manifestpath = pkg / "aerpkg.json"
        if manifestpath.exists():
            with open(manifestpath, "r") as f:
                data = json.load(f)
                print(f"{data['name']:<20} | {data['author']:<15} | {data['version']:<10}")