import os
import struct
import math

def extract_artifacts():
    out_dir = "kernel/extracted"
    os.makedirs(out_dir, exist_ok=True)

    # 1. Extract Kernel from boot.img
    with open("stock_backup/boot.img", "rb") as f:
        f.seek(8)
        kernel_sz = struct.unpack("<I", f.read(4))[0]
        ramdisk_sz = struct.unpack("<I", f.read(4))[0]
        # v4 boot header: 4096 bytes
        f.seek(4096)
        kernel_bytes = f.read(kernel_sz)
        kernel_path = os.path.join(out_dir, "Image.gz")
        with open(kernel_path, "wb") as kf:
            kf.write(kernel_bytes)
        print(f"Extracted kernel Image.gz ({len(kernel_bytes)} bytes) to {kernel_path}")

        # Check if gzip or raw Image
        if kernel_bytes[:2] == b"\x1f\x8b":
            print("Kernel is GZIP compressed!")
        elif kernel_bytes[0x38:0x3c] == b"ARM\x64":
            print("Kernel is uncompressed ARM64 Image (magic ARMd)!")
        else:
            print(f"Kernel magic bytes: {kernel_bytes[:8].hex()}")

    # 2. Extract DTB from vendor_boot.img
    with open("stock_backup/vendor_boot.img", "rb") as f:
        f.seek(12)
        page_size = struct.unpack("<I", f.read(4))[0]
        f.seek(24)
        ramdisk_sz = struct.unpack("<I", f.read(4))[0]
        f.seek(2100) # dtb size in v4
        dtb_sz = struct.unpack("<I", f.read(4))[0]

        # Calculate offsets
        ramdisk_pages = math.ceil(ramdisk_sz / page_size)
        dtb_offset = page_size + (ramdisk_pages * page_size)
        f.seek(dtb_offset)
        dtb_bytes = f.read(dtb_sz)
        dtb_path = os.path.join(out_dir, "dtb.img")
        with open(dtb_path, "wb") as df:
            df.write(dtb_bytes)
        print(f"Extracted DTB ({len(dtb_bytes)} bytes) at offset {dtb_offset} to {dtb_path}")
        if dtb_bytes[:4] == b"\xd0\x0d\xfe\xed":
            print("Valid Device Tree Blob (0xd00dfeed) confirmed!")

    # 3. Copy dtbo.img
    with open("stock_backup/dtbo.img", "rb") as f:
        dtbo_magic = f.read(4)
        if dtbo_magic == b"\xd7\xb7\xab\x1e":
            print(f"Valid DTBO image confirmed (magic: {dtbo_magic.hex()})")

if __name__ == "__main__":
    extract_artifacts()
