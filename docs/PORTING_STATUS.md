# PixelOS Android 17 Porting Status for Tecno KJ7

This document tracks the verified engineering state of the Tecno KJ7 (Spark 20 Pro+) PixelOS Android 17 porting effort. Every status claim is backed by physical evidence or verified upstream artifacts.

---

## 1. Status Overview Matrix

| Category | Component / Milestone | Status | Verified Evidence / Notes |
| :--- | :--- | :--- | :--- |
| **Hardware Audit** | Device Identification | **VERIFIED** | `ro.product.model=TECNO KJ7`, `ro.product.device=TECNO-KJ7`, SoC: MT6789 (Helio G99 Ultimate). |
| **Hardware Audit** | Partition Geometry & Sizes | **VERIFIED** | Verified exact byte sizes from `/dev/block/by-name/`: `boot_b` (64MB), `vendor_boot_b` (64MB), `dtbo_b` (8MB), `super` (8870707200 bytes). |
| **Hardware Audit** | Dynamic Partitions (Super) | **VERIFIED** | `lpdump` verified: Group `main_b` (max 8868610048 bytes), containing `system_b`, `system_ext_b`, `product_b`, `vendor_b`, `vendor_dlkm_b`, `odm_dlkm_b`, and Transsion carrier partitions. |
| **Hardware Audit** | Filesystem Types | **VERIFIED** | Verified via `/proc/mounts`: `system`, `vendor`, `product` use `erofs`; `vendor_dlkm` and `metadata` use `ext4`; `/data` uses `f2fs` with `inlinecrypt`. |
| **Stock Firmware** | Boot Partitions Backup | **VERIFIED** | Extracted and verified on disk in `stock_backup/`: `boot.img`, `vendor_boot.img`, `init_boot.img`, `dtbo.img`, `vbmeta.img`, `vbmeta_system.img`, `vbmeta_vendor.img`. Full SHA-256 hashes recorded. |
| **Stock Firmware** | Kernel Artifacts Extraction | **VERIFIED** | Extracted in `kernel/extracted/` and installed in `kernel/tecno/kj7/`: GKI `Image.gz` (19.5MB, ACK 5.10.226), `dtb.img` (DTBO table format, 205KB), `kernel.config` (from `/proc/config.gz`), and `bootconfig`. |
| **Stock Rootdir** | Stock Fstabs & Inits | **VERIFIED & INTEGRATED** | Pulled directly from running device into `device/tecno/kj7/rootdir/etc/`: `fstab.mt6789`, `fstab.emmc`, `fstab.enableswap`, `ueventd.rc`, `init.mt6789.rc`, `init.project.rc`, etc. |
| **VINTF Manifests** | 40 Stock VINTF Manifests | **VERIFIED & INTEGRATED** | Pulled directly from `/vendor/etc/vintf/` into `device/tecno/kj7/configs/vintf/`: Biometrics/Fingerprint, CameraProvider, HWComposer, Power, Light, Vibrator, Keymint, etc. |
| **Device Tree** | Complete KJ7 Device Tree | **VERIFIED & INTEGRATED** | Device tree completely assembled in `device/tecno/kj7/`: `AndroidProducts.mk`, `pixelos_kj7.mk`, `BoardConfig.mk` (physical sizes corrected), `device.mk`, `libinit`, `power`, `sensors`, `DSPVolumeSynchronizer`, `sepolicy`, `overlay-pixelos`, `Android.bp`, `Android.mk`, `setup-makefiles.py`, `proprietary-files.txt`. |
| **Vendor Blobs** | Stock Vendor Tree | **VERIFIED & INTEGRATED** | Vendor tree extracted into `vendor/tecno/kj7/` (1,267 files): `BoardConfigVendor.mk`, `kj7-vendor.mk`, `Android.bp`, `proprietary/` (all proprietary HALs, firmware, blobs), and `radio/`. |
| **Build Host** | Local Windows Compilation | **CONSTRAINED / BLOCKED** | PC has only 98 GB free on C: and 16 GB RAM. Full Android 17 compile requires 350-450 GB ext4 disk space and 32 GB RAM. Cloud/dedicated Linux build host required. |
| **Build Result** | Full ROM Image Compilation | **READY FOR LINUX HOST** | Complete source stack (`device/tecno/kj7`, `vendor/tecno/kj7`, `kernel/tecno/kj7`) is prepared and ready for build execution on Linux host. |
| **Validation** | Device Boot Testing | **NOT PERFORMED** | Boot testing will only occur once a verified image is compiled and user explicitly approves flashing. |

---

## 2. Hardware Subsystems Compatibility Assessment

1. **Kernel & Bootloader Interface:**
   - **GKI 5.10:** MediaTek MT6789 on Android 14 uses Android Common Kernel 5.10 with boot header v4.
   - **Bootloader (LK):** Does not load ramdisk from `init_boot` despite partition existence; boots ramdisk from `vendor_boot.img` and `boot.img`.
   - **SELinux:** Enforcing in stock; initial custom builds must handle MTK vendor sepolicy bridging to Android 17 framework.
2. **Graphics & Display:**
   - GPU: ARM Mali-G57 MC2. Driver modules in `vendor_dlkm` (`ged.ko`, `mali_kbase.ko` / `mtk_gpu_hal.ko`).
   - Panel: AMOLED 1080x2436 @ 120Hz.
3. **Telephony & RIL:**
   - MediaTek MT6789 modem daemon (`ccci_md_all.ko`, `ccci_ccif.ko`).
   - Dual SIM VoLTE / ViLTE requires MTK RIL stack (`librilmtk.so`).
4. **Camera & Imaging:**
   - 108 MP main + 32 MP selfie.
   - MediaTek ISP 6.0 stack (`camera_isp.ko`, `imgsensor_isp6s.ko`).
5. **Fingerprint:**
   - In-display optical fingerprint (`tran_fp.ko`). Requires Goodix/Silead vendor biometric HAL.
