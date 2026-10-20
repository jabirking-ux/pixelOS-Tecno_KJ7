import struct
import os

def unpack_boot_header(path):
    with open(path, "rb") as f:
        magic = f.read(8)
        if magic != b"ANDROID!":
            print(f"{path}: Not an Android boot image (magic={magic})")
            return
        
        # Header version is at offset 40 in v0-v4
        f.seek(40)
        header_version = struct.unpack("<I", f.read(4))[0]
        print(f"=== {path} (Header version: {header_version}) ===")

        if header_version >= 3:
            f.seek(8)
            kernel_size = struct.unpack("<I", f.read(4))[0]
            ramdisk_size = struct.unpack("<I", f.read(4))[0]
            os_version = struct.unpack("<I", f.read(4))[0]
            header_size = struct.unpack("<I", f.read(4))[0]
            reserved = struct.unpack("<4I", f.read(16))
            f.seek(40)
            h_ver = struct.unpack("<I", f.read(4))[0]
            cmdline = f.read(1536).decode("utf-8", errors="replace").rstrip("\x00")
            print(f"Kernel size: {kernel_size} ({kernel_size/1024/1024:.2f} MB)")
            print(f"Ramdisk size: {ramdisk_size}")
            os_v = (os_version >> 11) & 0x7ff
            os_patch = os_version & 0x7ff
            print(f"OS version raw: {os_version} (Parsed: {os_v}, patch: {os_patch})")
            print(f"Cmdline: {cmdline}")
            if header_version == 4:
                signature_size = struct.unpack("<I", f.read(4))[0]
                print(f"Signature size: {signature_size}")

def unpack_vendor_boot_header(path):
    with open(path, "rb") as f:
        magic = f.read(8)
        if magic != b"VNDRBOOT":
            print(f"{path}: Not a VNDRBOOT image (magic={magic})")
            return
        header_version = struct.unpack("<I", f.read(4))[0]
        page_size = struct.unpack("<I", f.read(4))[0]
        kernel_addr = struct.unpack("<I", f.read(4))[0]
        ramdisk_addr = struct.unpack("<I", f.read(4))[0]
        ramdisk_size = struct.unpack("<I", f.read(4))[0]
        cmdline = f.read(2048).decode("utf-8", errors="replace").rstrip("\x00")
        tags_addr = struct.unpack("<I", f.read(4))[0]
        name = f.read(16).decode("utf-8", errors="replace").rstrip("\x00")
        header_size = struct.unpack("<I", f.read(4))[0]
        dtb_size = struct.unpack("<I", f.read(4))[0]
        dtb_addr = struct.unpack("<Q", f.read(8))[0]
        print(f"=== {path} (Header v{header_version}) ===")
        print(f"Page size: {page_size}")
        print(f"Kernel addr: {hex(kernel_addr)}")
        print(f"Ramdisk addr: {hex(ramdisk_addr)}")
        print(f"Ramdisk size: {ramdisk_size} ({ramdisk_size/1024/1024:.2f} MB)")
        print(f"Tags addr: {hex(tags_addr)}")
        print(f"Product name: {name}")
        print(f"Header size: {header_size}")
        print(f"DTB size: {dtb_size} ({dtb_size/1024:.2f} KB)")
        print(f"DTB addr: {hex(dtb_addr)}")
        print(f"Vendor Cmdline: {cmdline}")

        if header_version == 4:
            vendor_ramdisk_table_size = struct.unpack("<I", f.read(4))[0]
            vendor_ramdisk_table_entry_num = struct.unpack("<I", f.read(4))[0]
            vendor_ramdisk_table_entry_size = struct.unpack("<I", f.read(4))[0]
            bootconfig_size = struct.unpack("<I", f.read(4))[0]
            print(f"Vendor ramdisk table size: {vendor_ramdisk_table_size}")
            print(f"Vendor ramdisk table entry num: {vendor_ramdisk_table_entry_num}")
            print(f"Vendor ramdisk table entry size: {vendor_ramdisk_table_entry_size}")
            print(f"Bootconfig size: {bootconfig_size}")

if __name__ == "__main__":
    unpack_boot_header("stock_backup/boot.img")
    unpack_boot_header("stock_backup/init_boot.img")
    unpack_vendor_boot_header("stock_backup/vendor_boot.img")
