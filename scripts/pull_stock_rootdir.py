import os
import subprocess

ADB = r"C:\Program Files\platform-tools\adb.exe"

def pull_files():
    rootdir_etc = "device/tecno/kj7/rootdir/etc"
    os.makedirs(rootdir_etc, exist_ok=True)

    files_to_pull = [
        "/vendor/etc/fstab.mt6789",
        "/vendor/etc/fstab.emmc",
        "/vendor/etc/fstab.enableswap",
        "/vendor/etc/ueventd.rc",
        "/vendor/etc/init/hw/init.mt6789.rc",
        "/vendor/etc/init/hw/init.mt6789.usb.rc",
        "/vendor/etc/init/hw/init.project.rc",
        "/vendor/etc/init/hw/init.connectivity.rc",
        "/vendor/etc/init/hw/init.connectivity.common.rc",
        "/vendor/etc/init/hw/init.sensor_2_0.rc",
        "/vendor/etc/init/hw/init.stnfc.rc",
    ]

    for f in files_to_pull:
        fname = os.path.basename(f)
        out_path = os.path.join(rootdir_etc, fname)
        print(f"Pulling {f} -> {out_path}...")
        res = subprocess.run([ADB, "pull", f, out_path], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Successfully pulled {fname}")
        else:
            print(f"Failed to pull {f}: {res.stderr.strip()}")

if __name__ == "__main__":
    pull_files()
