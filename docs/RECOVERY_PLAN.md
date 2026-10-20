# Stock Firmware Restoration & Emergency Recovery Plan for Tecno KJ7

This document defines the exact, verified recovery procedure to return the Tecno Spark 20 Pro+ (TECNO-KJ7 / MT6789) to 100% operational stock firmware in case of bootloop, soft-brick, or rollback.

---

## 1. Stock Backup Archive Details

The following clean stock partitions were dumped directly from the active slot (`_b`) of the device and are safely archived locally on the host PC in:
`KJ7-PixelOS17/stock_backup/`

| Partition | Local File | Partition Size | Verified SHA-256 Hash |
| :--- | :--- | :--- | :--- |
| `boot_b` | `boot.img` | 67,108,864 bytes | `7E115FD96905FA5EBE390AE7ABE58C710D9ADD7A8B8131FE44924069018B8C96` |
| `vendor_boot_b` | `vendor_boot.img` | 67,108,864 bytes | `5BE03E44FFB4E8BBDA002321924E3646BC88E26BD03D32420275DD9DB872323F` |
| `dtbo_b` | `dtbo.img` | 8,388,608 bytes | `D460DE2CD7035C9890563C91FAA7E18676828E4885374E99E5E13DE11F69530C` |
| `vbmeta_b` | `vbmeta.img` | 8,388,608 bytes | `B75C6EEB23CE2EB7C1E12AE890F829FCFEBF7883D0F5BBA7F5880EA98809330C` |
| `vbmeta_system_b` | `vbmeta_system.img` | 8,388,608 bytes | `DBFE64B4A896A12A13FAFA65704389073B21BD2F126412717F813F08B8F46938` |
| `vbmeta_vendor_b` | `vbmeta_vendor.img` | 8,388,608 bytes | `73754237DF4F56551CEADEB5C8AA445B370D89A994575F24B2657DF19E971ECB` |

---

## 2. Standard Fastboot Restoration Procedure

If custom images are tested and the device fails to boot or enters a bootloop:

### Step 1: Boot into Fastboot Mode
1. Power off the device completely.
2. Hold **Volume Down + Power** until the Tecno logo and `FASTBOOT` appears on screen.
3. Connect the phone to PC via USB.
4. Verify device detection:
   ```powershell
   & "C:\Program Files\platform-tools\fastboot.exe" devices
   ```

### Step 2: Check Active Slot
Check which slot is currently active:
```powershell
& "C:\Program Files\platform-tools\fastboot.exe" getvar current-slot
```
If the slot was changed, switch it back to slot `b` (the verified stock slot):
```powershell
& "C:\Program Files\platform-tools\fastboot.exe" --set-active=b
```

### Step 3: Flash Verified Stock Partitions
Flash the stock images from `stock_backup/`:

```powershell
cd "c:\Users\User\Documents\Tecno KJ7 PixelOS\KJ7-PixelOS17\stock_backup"

& "C:\Program Files\platform-tools\fastboot.exe" flash boot_b boot.img
& "C:\Program Files\platform-tools\fastboot.exe" flash vendor_boot_b vendor_boot.img
& "C:\Program Files\platform-tools\fastboot.exe" flash dtbo_b dtbo.img
& "C:\Program Files\platform-tools\fastboot.exe" flash vbmeta_b vbmeta.img
& "C:\Program Files\platform-tools\fastboot.exe" flash vbmeta_system_b vbmeta_system.img
& "C:\Program Files\platform-tools\fastboot.exe" flash vbmeta_vendor_b vbmeta_vendor.img
```

### Step 4: Reboot to Stock System
```powershell
& "C:\Program Files\platform-tools\fastboot.exe" reboot
```

The device will reboot cleanly into the existing stock Android 14 operating system with all user data and encryption keys intact.

---

## 3. Deep Brick (BROM / Preloader) Emergency Recovery

If the bootloader itself is corrupted or fastboot cannot be reached:
1. MediaTek MT6789 contains a hardware-level Boot ROM (BROM).
2. The device can be revived via SP Flash Tool or MTKClient (open-source python tool):
   - Hold **Volume Up + Volume Down** while plugging in USB (with device powered off).
   - The device enumerates as `MediaTek USB Port (COMx)`.
   - MTKClient can dump and write any partition directly via BROM payload mode.
