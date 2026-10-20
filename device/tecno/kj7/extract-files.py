#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/tecno/kj7',
    'hardware/google/interfaces',
    'hardware/google/pixel',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/shadowbyte',
    'hardware/shadowbyte/libtranlog',
    'vendor/mediatek/ims',
]


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    ('libc++_shared',): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/bin/hw/android.hardware.lights-service.mediatek': blob_fixup()
        .replace_needed('android.hardware.light-V1-ndk_platform.so', 'android.hardware.light-V1-ndk.so'),
    'vendor/lib64/libeffect_hal.so': blob_fixup()
        .replace_needed('libc++_shared.so', 'libc++.so'),
    'vendor/lib64/libkeystore-engine-wifi-hidl.so': blob_fixup()
        .replace_needed('android.system.keystore2-V1-ndk_platform.so', 'android.system.keystore2-V1-ndk.so'),
    (
        'vendor/lib64/hw/android.hardware.graphics.mapper@4.0-impl-mediatek.so',
        'vendor/lib64/egl/libGLES_mali.so',
        'vendor/lib64/arm.graphics-V1-ndk_platform.so',
    ): blob_fixup()
        .replace_needed('arm.graphics-V1-ndk_platform.so', 'arm.graphics-V1-ndk.so'),
    (
        'vendor/bin/hw/android.hardware.gnss-service.mediatek',
        'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    'vendor/bin/hw/mtkfusionrild': blob_fixup()
        .add_needed('libutils-v32.so'),
    'vendor/lib64/libnvram.so': blob_fixup()
        .add_needed('libbase-v33.so'),
    (
        'vendor/bin/hw/vendor.mediatek.hardware.mtkpower@1.0-service',
        'vendor/lib64/android.hardware.power-service-mediatek.so',
    ): blob_fixup()
        .replace_needed('android.hardware.power-V2-ndk_platform.so', 'android.hardware.power-V2-ndk.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib/libaalservice.so',
        'vendor/lib64/libaalservice.so',
        'vendor/lib64/libcam.utils.sensorprovider.so',
    ): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so'),
    (
        'vendor/lib64/libmtkcam_stdutils.so',
        'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/hw/hwcomposer.mt6768.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'KJ7',
    'tecno',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
