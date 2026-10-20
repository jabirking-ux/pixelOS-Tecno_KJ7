import zipfile
import os
import shutil

def main():
    zip_path = "vendor_kj7.zip"
    dest_dir = "vendor/tecno/kj7"
    os.makedirs(dest_dir, exist_ok=True)

    print("Extracting vendor_kj7.zip...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        prefix = "android_vendor_tecno_kj7-lineage-22.1/"
        total = len(z.infolist())
        count = 0
        for member in z.infolist():
            if not member.filename.startswith(prefix):
                continue
            rel_path = member.filename[len(prefix):]
            if not rel_path:
                continue
            target_path = os.path.join(dest_dir, rel_path.replace('/', os.sep))
            if member.is_dir():
                os.makedirs(target_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with z.open(member) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)
            count += 1
            if count % 500 == 0:
                print(f"Extracted {count}/{total} files...")

    print("Extraction complete. Removing archive...")
    os.remove(zip_path)
    print(f"Successfully populated {dest_dir}")

if __name__ == "__main__":
    main()
