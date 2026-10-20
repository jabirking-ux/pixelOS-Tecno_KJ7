#!/usr/bin/env bash
set -e

echo "=== Crave Cloud Build: PixelOS Android 17 for Tecno KJ7 (MT6789) ==="

# 1. Clean previous build outputs if requested
rm -rf out/target/product/kj7/*.img out/target/product/kj7/*.zip

# 2. Initialize official PixelOS Android 17 manifest
repo init -u https://github.com/PixelOS-AOSP/android_manifest.git -b seventeen --git-lfs < /dev/null || true

# 3. Setup local manifest directory
mkdir -p .repo/local_manifests
cat << 'EOF' > .repo/local_manifests/kj7.xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <project path="device/tecno/kj7" name="RapStuff/android_device_tecno_kj7" revision="lineage-23.0" remote="github" />
  <project path="vendor/tecno/kj7" name="RapStuff/android_vendor_tecno_kj7" revision="lineage-22.1" remote="github" />
  <project path="kernel/tecno/kj7" name="RapStuff/android_kernel_tecno_kj7" revision="lineage-23.0" remote="github" />
</manifest>
EOF

# 4. Sync required device repositories
echo "=== Syncing source repositories ==="
repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags

# 5. Inject verified PixelOS product configurations
cat << 'EOF' > device/tecno/kj7/AndroidProducts.mk
PRODUCT_MAKEFILES := \
    $(LOCAL_DIR)/pixelos_kj7.mk

COMMON_LUNCH_CHOICES := \
    pixelos_kj7-user \
    pixelos_kj7-userdebug \
    pixelos_kj7-eng
EOF

cat << 'EOF' > device/tecno/kj7/pixelos_kj7.mk
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, device/tecno/kj7/device.mk)
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
EOF

# 6. Apply verified physical partition sizing to BoardConfig.mk
sed -i 's/BOARD_BOOTIMAGE_PARTITION_SIZE := .*/BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864/g' device/tecno/kj7/BoardConfig.mk
sed -i 's/BOARD_SUPER_PARTITION_SIZE := .*/BOARD_SUPER_PARTITION_SIZE := 8870707200/g' device/tecno/kj7/BoardConfig.mk
sed -i 's/BOARD_MEDIATEK_DYNAMIC_PARTITIONS_SIZE := .*/BOARD_MEDIATEK_DYNAMIC_PARTITIONS_SIZE := 8868610048/g' device/tecno/kj7/BoardConfig.mk

# 7. Build Environment Setup
echo "=== Initializing build environment ==="
source build/envsetup.sh
lunch pixelos_kj7-userdebug

# 8. Start Compilation
echo "=== Starting compilation (m bacon) ==="
m bacon -j$(nproc --all)

echo "=== Build finished successfully! ==="
ls -lh out/target/product/kj7/*.zip || true
