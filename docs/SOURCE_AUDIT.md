# Upstream & Hardware Source Audit for Tecno KJ7 (MT6789) -> PixelOS Android 17

This audit evaluates all identified repositories, their default branches, commit hashes, target Android versions, licenses, and verified compatibility with the Tecno Spark 20 Pro+ (KJ7 / MT6789).

---

## 1. Source Repository Matrix

| Repository Name / URL | Branch / Ref | Commit Hash | Target Android / Framework | Suitability / Role | Missing Components / Blockers | Confidence Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PixelOS-AOSP/android_manifest**<br>`https://github.com/PixelOS-AOSP/android_manifest` | `seventeen` | `c16cfd0c95c5c3d7f5f2ef85b5b3140787db2035` | Android 17.0.0_r1 (LineageOS 24.0 base) | Official upstream OS base manifest | Does not contain Tecno device or MT6789 SoC trees; must be integrated via local manifest. | **High (Upstream)** |
| **RapStuff/android_device_tecno_kj7**<br>`https://github.com/RapStuff/android_device_tecno_kj7` | `lineage-23.0` | `caa1e099ea81b16ef035c542209db03e3ceef797` | Android 16 QPR / LineageOS 23.0 | Complete device tree (`device/tecno/kj7`) with BoardConfig, device.mk, sepolicy, sensors, libinit, extract-files. | Needs adaptation for PixelOS branding (`pixelos_kj7.mk`), partition size alignment to real UFS geometry, and Android 17 sepolicy updates. | **High (Device Tree)** |
| **RapStuff/android_vendor_tecno_kj7**<br>`https://github.com/RapStuff/android_vendor_tecno_kj7` | `lineage-22.1` | `6dec8341545495cf0c7cb69071d00675519335af` | Android 15 / LineageOS 22.1 | Proprietary vendor blobs and makefiles (`vendor/tecno/kj7`) | Contains Android 12 BSP vendor blobs extracted for LineageOS. Requires checking compatibility with Android 17 HIDL/AIDL deprecation. | **Medium-High (Vendor Tree)** |
| **RapStuff/android_kernel_tecno_kj7**<br>`https://github.com/RapStuff/android_kernel_tecno_kj7` | `lineage-23.0` | `92abecf26c08b20e17b40cb20983a13da52c9ed4` | Android 16 / LineageOS 23.0 (ACK 5.10) | Prebuilt GKI 5.10 Image.gz, vendor modules, dtb, dtbo.img | Prebuilt binary; stock kernel extracted directly from the user's running device (`5.10.226`) is more current and exact. | **Medium (Alternative Prebuilt)** |
| **kaminarich/device_tecno_KJ7**<br>`https://github.com/kaminarich/device_tecno_KJ7` | `lineage-22.1` | `b95a76a8f9d2dd880c4e1526349f3ee69ac77ad7` | Android 15 / LineageOS 22.1 | Device tree alternative | Predecessor to the `lineage-23.0` tree; useful for historical diffs and missing overlays. | **Medium** |
| **transsion-mt6789-recovery/twrp-device_tecno_TECNO-KJ7**<br>`https://github.com/transsion-mt6789-recovery/twrp-device_tecno_TECNO-KJ7` | `fox_12.1` | `bce94f8bfca9c6858d02a9a22b7e7a81f134ca51` | Android 12.1 (OrangeFox / TWRP) | Custom recovery configuration | Recovery-only; cannot build a full Android OS, but verifies MTK recovery flags and fstab. | **Reference Only** |
| **transsion-mt6789-recovery/twrp-device_transsion_mt6789-common**<br>`https://github.com/transsion-mt6789-recovery/twrp-device_transsion_mt6789-common` | `fox_12.1` | `2266cf92b0d3c92712de1dcba5c0a60be90278c3` | Android 12.1 (TWRP) | Common recovery configuration | Recovery-only; common definitions for Transsion MT6789. | **Reference Only** |
| **Transsion-MT6789-Resources/device_transsion_mt6789-common**<br>`https://github.com/Transsion-MT6789-Resources/device_transsion_mt6789-common` | `staging/lineage-20` | `5c6617367652ef6efb0f7f644a3275834817f681` | Android 13 / LineageOS 20 | Deprecated common Android tree | Marked by maintainers as "DEPRECATED, BACK TO DECOMMON". Models maintain distinct standalone trees. | **Deprecated** |

---

## 2. In-Depth Analysis of Discovered Repositories

### PixelOS Android 17 Manifest (`seventeen`)
- **Remote:** `https://github.com/PixelOS-AOSP`
- **Default Tag:** `android-17.0.0_r1`
- **LineageOS Revision:** `lineage-24.0`
- **Status:** PixelOS has opened its Android 17 manifest branch tracking the latest AOSP 17 preview and early LineageOS 24.0 base.
- **Architectural Requirement:** PixelOS expects device products in `device/<oem>/<device>/` inheriting `vendor/pixelos/config/common_full_phone.mk` with product definition `pixelos_<device>.mk`.

### Device Tree Architecture (`RapStuff/android_device_tecno_kj7`)
- Provides a clean, standalone device tree for `kj7` targeting LineageOS 23.0 (Android 16).
- Includes:
  - `BoardConfig.mk`: Sets GKI 5.10 boot header version 4, prebuilt DTB and DTBO, EROFS dynamic partitions, and AVB testkeys.
  - `device.mk`: Full configuration for MediaTek telephony, audio, sensors, GPS, and Wi-Fi.
  - `proprietary-files.txt`: 1,200+ proprietary library and HAL entries extracted from Transsion stock firmware.
  - `sepolicy/`: MediaTek-specific SELinux policies bridging AOSP framework to MTK proprietary daemons.

### Stock Discrepancies vs. Discovered Device Trees
1. **Partition Sizes:**
   - RapStuff `BoardConfig.mk`: `BOARD_BOOTIMAGE_PARTITION_SIZE := 33554432` (32MB)
   - **Real Device Hardware:** `boot_a`/`boot_b` is **`67108864` bytes (64MB)**. Flashing a 32MB assumption causes bootloader reject or mkbootimg alignment issues.
   - RapStuff `BoardConfig.mk`: `BOARD_SUPER_PARTITION_SIZE := 8616214528` (8217MB)
   - **Real Device Hardware:** `super` is **`8870707200` bytes (8459MB)** with group max `8868610048` bytes.
2. **Kernel Version & Sources:**
   - The device runs Linux `5.10.226-android12-9-00047-g4968e29b7f92-ab12786767`.
   - Transsion OEM has not published full public standalone kernel source tree for KJ7. MediaTek MT6789 utilizes GKI (Generic Kernel Image) with proprietary out-of-tree kernel modules loaded from `vendor_dlkm` and `vendor_boot`.
   - Therefore, the proven, stable path for custom Android on this device is **GKI Prebuilt Integration** using the stock verified kernel and modules extracted directly from the device.

---

## 3. License & Compliance Review
- Upstream PixelOS: Apache 2.0 / GPLv2.
- Device Tree (`RapStuff/android_device_tecno_kj7`): Apache 2.0.
- Stock Kernel: Linux GPLv2 (GKI ACK binaries freely redistributable).
- Proprietary Blobs: MediaTek / Transsion proprietary; must be extracted from authorized stock firmware or active device under fair-use interoperability principles.
