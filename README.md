# PixelOS Android 17 Port for Tecno Spark 20 Pro+ (TECNO-KJ7)

Official device tree, kernel configuration, and firmware engineering repository for porting **PixelOS Android 17** (`seventeen` branch) to the **Tecno Spark 20 Pro+** (codenamed `TECNO-KJ7`, MT6789 / Helio G99 Ultimate).

---

## 1. Project Summary

| Attribute | Specification |
| :--- | :--- |
| **Target Device** | Tecno Spark 20 Pro+ (`TECNO-KJ7` / `KJ7-OP`) |
| **Chipset** | MediaTek Helio G99 Ultimate (`mt6789`) |
| **Target OS** | PixelOS Android 17 (`android-17.0.0_r1` base) |
| **Active Stock OS** | Android 14 (`KJ7-H895MNOAk-U-OP-260112V2294`) |
| **Vendor BSP** | Android 12 BSP (`260112V2353`, SDK 31) |
| **Kernel Base** | Linux 5.10.226 Android Common Kernel (ACK) |
| **Slot Architecture** | Virtual A/B with EROFS Dynamic Partitions |
| **Porting Status** | **Complete Source Stack Assembled (`device/`, `vendor/`, `kernel/`) & Stock Firmware Backed Up** |

---

## 2. Directory Structure

```
KJ7-PixelOS17/
├── README.md                           # Master project summary and guide
├── docs/
│   ├── SOURCE_AUDIT.md                 # Upstream source & repository audit
│   ├── KJ7_DEVICE_AUDIT.txt            # Real hardware audit & properties dump
│   ├── FIRMWARE_INVENTORY.md           # Stock firmware hashes and partition inventory
│   ├── BUILD_GUIDE.md                  # Host requirements and build compilation manual
│   ├── PORTING_STATUS.md               # Evidence-based hardware and port status matrix
│   ├── RECOVERY_PLAN.md                # Fastboot/BROM emergency stock restoration guide
│   ├── partitions_by_name.txt          # Verified physical partition byte sizes
│   ├── proc_mounts.txt                 # Active device filesystem mounts
│   └── lpdump.txt                      # Verified super partition geometry
├── device/
│   └── tecno/
│       └── kj7/                        # Full device tree (BoardConfig, device.mk, rootdir, vintf, etc.)
├── vendor/
│   └── tecno/
│       └── kj7/                        # Full vendor tree (1,267 proprietary HALs, libs, and configs)
├── kernel/
│   ├── extracted/                      # Stock kernel Image.gz, dtb.img, dtbo.img
│   ├── tecno/
│   │   └── kj7/                        # Prebuilt kernel, DTB table, and DTBO
│   ├── kernel.config                   # Running kernel config extracted from /proc/config.gz
│   ├── bootconfig                      # Running boot parameters extracted from /proc/bootconfig
│   └── modules.load.vendor_dlkm        # Stock kernel driver load order
├── stock_backup/                       # Verified bit-for-bit stock images (boot, vendor_boot, vbmeta)
├── patches/                            # Framework/sepolicy compatibility patches
├── scripts/                            # Automation, header inspection, and extraction tools
└── logs/                               # Device logs, VINTF manifests, and ADB dumps
```

---

## 3. Current Porting Status & Known Limitations

- **Complete Source Stack:**
  - `device/tecno/kj7`: Physical partition sizes corrected (`64MB` boot, `8.87GB` super), 40 stock VINTF manifests, stock init/fstabs, SELinux policy, libinit, sensors, and power.
  - `vendor/tecno/kj7`: All 1,267 proprietary HALs, binaries, firmware files, and makefiles integrated.
  - `kernel/tecno/kj7`: Stock ACK 5.10.226 `Image.gz`, DTB table (`205 KB`), and DTBO integrated.
- **Stock Firmware Integrity:** 100% verified against connected physical device. Active slot `_b` stock boot, vendor_boot, dtbo, and vbmeta partitions have been backed up with cryptographic SHA-256 validation.
- **Development Host Limitations:** The local Windows machine (Core i5-11400, 16 GB RAM, 98 GB free on C:) cannot host the ~400 GB Android 17 compile. A Linux build host (ext4, 32 GB+ RAM, 400 GB+ SSD) is required to run the final `m bacon` target.
- **Safe Installation Policy:** In strict adherence to safety guidelines, no experimental images have been flashed, the bootloader slot has not been tampered with, and verified recovery procedures are in place before any flashing is initiated.

---

## 4. Documentation Links

- [Hardware & Device Properties Audit](docs/KJ7_DEVICE_AUDIT.txt)
- [Source & Repository Audit](docs/SOURCE_AUDIT.md)
- [Firmware Inventory & Checksums](docs/FIRMWARE_INVENTORY.md)
- [Crave.io Free Cloud Build Guide](docs/CRAVE_BUILD_GUIDE.md)
- [Linux Build & Compilation Guide](docs/BUILD_GUIDE.md)
- [Porting Status & Hardware Matrix](docs/PORTING_STATUS.md)
- [Stock Restoration & Recovery Plan](docs/RECOVERY_PLAN.md)
