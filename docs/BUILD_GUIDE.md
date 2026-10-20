# PixelOS Android 17 Build Guide for Tecno KJ7 (MT6789)

---

## 1. Development PC Feasibility Audit

### Current Machine Specifications:
- **Processor:** Intel Core i5-11400 (6 Cores, 12 Threads)
- **Host RAM:** 16 GB Physical RAM (Installed: ~15.8 GB, Free: ~4.5 GB)
- **Host Disk Space:**
  - Drive `C:`: 51.86 GB Free (Total: 348.97 GB)
  - Drive `D:`: 27.33 GB Free (Total: 62.70 GB)
  - Drive `G:`: 63.33 GB Free (Total: 63.33 GB)
- **Environment:** Windows 10/11 x64, WSL2 (Ubuntu instance installed but stopped)

### Critical Feasibility Assessment:
> [!WARNING]
> **Full Compilation Blocked by Storage & RAM on Current PC.**
> - **Storage Requirement:** An Android 17 (AOSP / LineageOS 24 / PixelOS seventeen) source checkout requires **~180 GB to 250 GB** of disk space for git objects alone, plus **~150 GB to 200 GB** for build outputs (`out/target/product/kj7`). The total required disk capacity is **350 GB to 450 GB** of native Linux (ext4) storage.
> - **Available Capacity:** Drive `C:` has only **51.8 GB**, and Drive `D:` has only **27.3 GB**. Attempting `repo sync` locally will completely fill the drive and crash the host operating system.
> - **RAM Requirement:** Soong / Ninja / Metalava in modern Android compiles require **at least 32 GB RAM** (or 16 GB with massive zram/swap). 16 GB with only 4.5 GB free will trigger aggressive OOM-killer during Metalava and dexpreopt phases.

### Recommended Build Infrastructure:
To build PixelOS Android 17, use a dedicated Linux build workstation or cloud build host (e.g., Hetzner, AWS c6a.4xlarge, or GCP n2-standard-8/16) with:
- **OS:** Ubuntu 22.04 LTS or 24.04 LTS x86_64
- **CPU:** 8 to 16 cores (AMD Ryzen 7/9 or Intel i7/i9 / Xeon)
- **RAM:** 32 GB to 64 GB
- **Storage:** 400 GB+ NVMe SSD formatted as ext4
- **Swap:** 16 GB to 32 GB swapfile

---

## 2. Environment Setup (Linux Host)

Install build dependencies on the Linux build host:

```bash
sudo apt update && sudo apt install -y \
    bc bison build-essential ccache curl flex g++-multilib gcc-multilib git git-lfs \
    gnupg gperf imagemagick lib32readline-dev lib32z1-dev libelf-dev liblz4-tool \
    libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils \
    lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev \
    python3 python3-pip openjdk-21-jdk libtinfo5
```

Install repo tool:
```bash
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
export PATH=~/bin:$PATH
```

Configure Git identity:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 3. Initializing PixelOS Android 17 Source Tree

Initialize the official PixelOS manifest for Android 17:

```bash
mkdir -p ~/pixelos-17
cd ~/pixelos-17

repo init -u https://github.com/PixelOS-AOSP/android_manifest.git -b seventeen --git-lfs
```

---

## 4. Local Manifest for Tecno KJ7 (`.repo/local_manifests/kj7.xml`)

Create `.repo/local_manifests/kj7.xml` to include the verified KJ7 device tree, vendor tree, and kernel prebuilts:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <!-- Device Tree -->
  <project path="device/tecno/kj7" name="RapStuff/android_device_tecno_kj7" revision="lineage-23.0" remote="github" />

  <!-- Vendor Blobs -->
  <project path="vendor/tecno/kj7" name="RapStuff/android_vendor_tecno_kj7" revision="lineage-22.1" remote="github" />

  <!-- Prebuilt GKI Kernel -->
  <project path="kernel/tecno/kj7" name="RapStuff/android_kernel_tecno_kj7" revision="lineage-23.0" remote="github" />
</manifest>
```

Sync the source code:
```bash
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags
```

---

## 5. Integrating PixelOS Product Configuration

In `device/tecno/kj7/`:

1. Create `pixelos_kj7.mk`:
```makefile
# Inherit from core targets
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit device configuration
$(call inherit-product, device/tecno/kj7/device.mk)

# Inherit PixelOS common configuration
$(call inherit-product, vendor/pixelos/config/common_full_phone.mk)

PRODUCT_NAME := pixelos_kj7
PRODUCT_DEVICE := kj7
PRODUCT_MANUFACTURER := TECNO
PRODUCT_BRAND := TECNO
BOARD_VENDOR := TECNO
PRODUCT_MODEL := TECNO Spark 20 Pro+

PRODUCT_GMS_CLIENTID_BASE := android-tecno

PRODUCT_BUILD_PROP_OVERRIDES += \
    DeviceName=KJ7 \
    BuildFingerprint=TECNO/KJ7-OP/TECNO-KJ7:14/UP1A.231005.007/260112V2294:user/release-keys
```

2. Update `AndroidProducts.mk`:
```makefile
PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/pixelos_kj7.mk

COMMON_LUNCH_CHOICES := \
    pixelos_kj7-user \
    pixelos_kj7-userdebug \
    pixelos_kj7-eng
```

3. Ensure `BoardConfig.mk` partition sizes match the verified physical hardware:
```makefile
BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864
BOARD_VENDOR_BOOTIMAGE_PARTITION_SIZE := 67108864
BOARD_DTBOIMG_PARTITION_SIZE := 8388608
BOARD_SUPER_PARTITION_SIZE := 8870707200
BOARD_MEDIATEK_DYNAMIC_PARTITIONS_SIZE := 8868610048
```

---

## 6. Build Execution

Set up environment and build:

```bash
source build/envsetup.sh
lunch pixelos_kj7-userdebug
m -j$(nproc --all) bacon
```

Outputs will be generated in `out/target/product/kj7/`:
- `boot.img`
- `vendor_boot.img`
- `dtbo.img`
- `super.img` (or OTA package: `PixelOS_kj7-17.0-*.zip`)
