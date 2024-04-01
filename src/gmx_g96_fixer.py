import glob
import multiprocessing as mp
import os
import sys

from libmol import WrongG96Mol


def _auto_backup(
    file: str,
) -> None:
    if not os.path.exists(file):
        return

    file_dir = os.path.dirname(file)
    file_name = os.path.basename(file)

    old_file_pattern = f"#{file_name}.*#"
    old_files = sorted(glob.glob(os.path.join(
        file_dir,
        old_file_pattern,
    )))

    num_old_files = len(old_files)

    new_backup_file_name = f"#{file_name}.{num_old_files + 1}#"
    new_backup_file = os.path.join(file_dir, new_backup_file_name)

    os.rename(file, new_backup_file)


def _fix(
    file: str,
) -> None:
    wrong_g96_mol = WrongG96Mol.from_file(file)
    _auto_backup(file)
    with open(file, "w") as f:
        print(wrong_g96_mol, file=f, flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(
            "Usage:\n"
            f"$ python3 {os.path.basename(__file__)} mol.g96  "
            "# single wrong g96 file\n"
            f"$ python3 {os.path.basename(__file__)} mol1.g96 mol2.g96 ...  "
            "# a list of wrong g96 files\n"
            f"$ python3 {os.path.basename(__file__)} *.g96  "
            "# match by pattern"
        )
        exit()

    wrong_g96_list = sys.argv[1:]

    pool = mp.Pool()

    for wrong_g96 in wrong_g96_list:
        pool.apply_async(
            func=_fix,
            args=(wrong_g96,),
        )

    pool.close()
    pool.join()
