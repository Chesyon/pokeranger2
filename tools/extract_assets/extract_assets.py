from sys import exit
from argparse import ArgumentParser
from ndspy.fnt import Folder
from ndspy.rom import NintendoDSRom
from pathlib import Path


def extract_folder(
    folder: Folder, files: list[bytes], output_dir: Path, local_path: Path
):
    for i, filename in enumerate(folder.files):
        file_id = folder.firstID + i
        dir_path = Path(output_dir, local_path).resolve()
        dir_path.mkdir(exist_ok=True)
        with open(Path(dir_path, filename), "wb") as f:
            f.write(files[file_id])

    for sub_name, sub_folder in folder.folders:
        extract_folder(sub_folder, files, output_dir, Path(local_path, sub_name))


def main():
    parser = ArgumentParser(
        prog="extract_assets",
        description="Extracts assets from Pokémon Ranger: Shadows of Almia (US)",
    )
    parser.add_argument("rom_path", type=Path)
    rom_path = parser.parse_args().rom_path

    if not rom_path.is_file():
        print(f"Error: ROM file not found: {rom_path}")
        exit(1)

    output_dir = Path(__file__, "..", "..", "..", "res", "prebuilt")

    print(f"Opening ROM: {rom_path}")
    rom = NintendoDSRom.fromFile(rom_path)

    print(f"Extracting filesystem to {output_dir}/")
    extract_folder(rom.filenames, rom.files, output_dir, Path(""))

    print("Done! Assets extracted successfully.")


if __name__ == "__main__":
    main()
