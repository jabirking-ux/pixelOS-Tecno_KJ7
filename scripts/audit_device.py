import subprocess
import os

ADB = r"C:\Program Files\platform-tools\adb.exe"

def run_adb(args):
    cmd = [ADB] + args
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.stdout, res.stderr

def run_su(shell_cmd):
    # Escape quotes
    cmd = [ADB, "shell", f"su -c '{shell_cmd}'"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.stdout

def main():
    print("Fetching partitions and sizes...")
    script = """
    for p in /dev/block/by-name/*; do
        name=$(basename "$p")
        sz=$(blockdev --getsize64 "$p" 2>/dev/null || echo 0)
        target=$(readlink -f "$p")
        echo "$name | $sz | $target"
    done
    """
    out = run_su(script)
    with open("docs/partitions_by_name.txt", "w", encoding="utf-8") as f:
        f.write(out)
    print("Partitions written to docs/partitions_by_name.txt")

    print("Fetching /proc/partitions...")
    out_part = run_su("cat /proc/partitions")
    with open("docs/proc_partitions.txt", "w", encoding="utf-8") as f:
        f.write(out_part)

    print("Fetching dynamic partition / super information...")
    out_lpdump = run_su("lpdump 2>/dev/null || echo 'lpdump not available'")
    with open("docs/lpdump.txt", "w", encoding="utf-8") as f:
        f.write(out_lpdump)

    print("Fetching mounts...")
    out_mount = run_su("cat /proc/mounts")
    with open("docs/proc_mounts.txt", "w", encoding="utf-8") as f:
        f.write(out_mount)

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    main()
