#
# Copyright (C) 2026 The PixelOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from core targets. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/tecno/kj7/device.mk)

# Display resolution
TARGET_SCREEN_WIDTH := 1080
TARGET_SCREEN_HEIGHT := 2436

# Inherit from PixelOS common configuration
$(call inherit-product-if-exists, vendor/custom/config/common_full_phone.mk)
$(call inherit-product-if-exists, vendor/pixelos/config/common_full_phone.mk)

PRODUCT_NAME := pixelos_kj7
PRODUCT_DEVICE := kj7
PRODUCT_MANUFACTURER := TECNO
PRODUCT_BRAND := TECNO
BOARD_VENDOR := TECNO
PRODUCT_MODEL := TECNO Spark 20 Pro+
CUSTOM_BUILD := kj7
LINEAGE_BUILD := kj7
TARGET_DISABLE_EPPE := true

PRODUCT_GMS_CLIENTID_BASE := android-tecno

PRODUCT_BUILD_PROP_OVERRIDES += \
    DeviceName=KJ7 \
    BuildFingerprint=TECNO/KJ7-OP/TECNO-KJ7:14/UP1A.231005.007/260112V2294:user/release-keys
