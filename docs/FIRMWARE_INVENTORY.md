# TECNO KJ7 Stock Firmware Inventory & Backup Record

**Device Identifier:** TECNO-KJ7 / KJ7-OP  
**Stock Build:** `KJ7-H895MNOAk-U-OP-260112V2294` (System Android 14)  
**Vendor Build:** `260112V2353` (Vendor Android 12 BSP)  
**Kernel:** Linux 5.10.226-android12-9-00047-g4968e29b7f92-ab12786767  
**Dump Method:** Direct block read via KernelSU root (`dd if=/dev/block/by-name/<partition>`)  
**Active Slot:** `_b`

---

## 1. Stock Boot & Firmware Partition Images

| File Name | Partition Name | Size (Bytes) | SHA-256 Hash | Partition Role | Extraction Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `boot.img` | `boot_b` | 67,108,864 | `7E115FD96905FA5EBE390AE7ABE58C710D9ADD7A8B8131FE44924069018B8C96` | GKI Linux 5.10 Kernel + Root Ramdisk | Dumped & Extracted (`Image.gz` extracted) |
| `vendor_boot.img` | `vendor_boot_b` | 67,108,864 | `5BE03E44FFB4E8BBDA002321924E3646BC88E26BD03D32420275DD9DB872323F` | Vendor ramdisk (normal + recovery) + DTB | Dumped & Extracted (`dtb.img` extracted) |
| `init_boot.img` | `init_boot_b` | 8,388,608 | `2DAEB1F36095B44B318410B3F4E8B5D989DCC7BB023D1426C492DAB0A3053E74` | Generic Boot Ramdisk (OEM left zeroed) | Dumped (Verified all zeroes in OEM BSP) |
| `dtbo.img` | `dtbo_b` | 8,388,608 | `D460DE2CD7035C9890563C91FAA7E18676828E4885374E99E5E13DE11F69530C` | Device Tree Blob Overlay Table | Dumped & Verified (`d7b7ab1e` magic) |
| `vbmeta.img` | `vbmeta_b` | 8,388,608 | `B75C6EEB23CE2EB7C1E12AE890F829FCFEBF7883D0F5BBA7F5880EA98809330C` | Android Verified Boot root descriptor | Dumped & Verified |
| `vbmeta_system.img` | `vbmeta_system_b` | 8,388,608 | `DBFE64B4A896A12A13FAFA65704389073B21BD2F126412717F813F08B8F46938` | AVB descriptor for system / product | Dumped & Verified |
| `vbmeta_vendor.img` | `vbmeta_vendor_b` | 8,388,608 | `73754237DF4F56551CEADEB5C8AA445B370D89A994575F24B2657DF19E971ECB` | AVB descriptor for vendor / odm | Dumped & Verified |

---

## 2. Dynamic Partitions (Super) Inventory

- **Total Super Partition Size:** `8,870,707,200` bytes (~8.46 GB)
- **Super Block Device:** `/dev/block/sdc61`
- **Dynamic Group Name:** `main_b`
- **Maximum Group Size:** `8,868,610,048` bytes

### Dynamic Subpartition Breakdown:
1. `system_b`: EROFS filesystem (Android 14 system base)
2. `system_ext_b`: EROFS filesystem (System extensions)
3. `product_b`: EROFS filesystem (Product apps and configs)
4. `vendor_b`: EROFS filesystem (Android 12 MediaTek MT6789 BSP HALs)
5. `vendor_dlkm_b`: EXT4 filesystem (Kernel modules for vendor hardware)
6. `odm_dlkm_b`: EXT4 filesystem (ODM kernel modules)
7. `tr_product_b`: EROFS filesystem (Transsion HiOS UI and custom apps)
8. `tr_preload_b`: EROFS filesystem (Preloaded carrier/OEM bloatware)
9. `tr_mi_b`, `tr_theme_b`, `tr_region_b`, `tr_company_b`, `tr_carrier_b`: EXT4 filesystems (Operator and localization assets)

---

## 3. Extracted Kernel & Hardware Artifacts

Located in `kernel/extracted/`:

1. `Image.gz`:
   - Size: 19,527,273 bytes
   - Format: GZIP-compressed ARM64 Linux kernel
   - Kernel Release: `5.10.226-android12-9-00047-g4968e29b7f92-ab12786767`
2. `dtb.img`:
   - Size: 205,263 bytes
   - Format: Flattened Device Tree Table (DTBO Table header `0xd7b7ab1e`)
   - Target Board: MediaTek MT6789 (`soc/11270000.ufshci`)
3. `kernel.config`:
   - Decompressed kernel build configuration directly extracted from `/proc/config.gz`
   - Clang Version: 12.0.5 (`r416183b`)
4. `bootconfig`:
   - Extracted kernel bootconfig parameters from `/proc/bootconfig`
5. `modules.load.vendor_dlkm`:
   - Complete list and load order of in-tree kernel drivers (Wi-Fi, Bluetooth, Audio, Touchscreen, Fingerprint, Cameras).
