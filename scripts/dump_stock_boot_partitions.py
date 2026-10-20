import subprocess
import os

ADB = r"C:\Program Files\platform-tools\adb.exe"

def run_cmd(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.stdout, res.stderr

def run_su(shell_cmd):
    cmd = [ADB, "shell", f"su -c '{shell_cmd}'"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.stdout

def main():
    backup_dir = "stock_backup"
    os.makedirs(backup_dir, exist_ok=True)

    partitions = [
        ("boot_b", "boot.img", "/dev/block/by-name/boot_b"),
        ("vendor_boot_b", "vendor_boot.img", "/dev/block/by-name/vendor_boot_b"),
        ("init_boot_b", "init_boot.img", "/dev/block/by-name/init_boot_b"),
        ("dtbo_b", "dtbo.img", "/dev/block/by-name/dtbo_b"),
        ("vbmeta_b", "vbmeta.img", "/dev/block/by-name/vbmeta_b"),
        ("vbmeta_system_b", "vbmeta_system.img", "/dev/block/by-name/vbmeta_system_b"),
        ("vbmeta_vendor_b", "vbmeta_vendor.img", "/dev/block/by-name/vbmeta_vendor_b"),
    ]

    print("Dumping stock boot & meta partitions to /sdcard/stock_dump/...")
    run_su("mkdir -p /sdcard/stock_dump")

    for part_name, out_file, block_dev in partitions:
        print(f"Dumping {part_name} from {block_dev}...")
        run_su(f"dd if={block_dev} of=/sdcard/stock_dump/{out_file} bs=4096")
        local_path = os.path.join(backup_dir, out_file)
        print(f"Pulling {out_file} to {local_path}...")
        subprocess.run([ADB, "pull", f"/sdcard/stock_dump/{out_file}", local_path], check=True)

    print("Cleaning up /sdcard/stock_dump/...")
    run_su("rm -rf /sdcard/stock_dump")
    print("Partition dump complete!")

if __name__ == "__main__":
    main()
