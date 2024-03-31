import os
import sys
import glob

from libmol import WrongG96Mol
import psutil
import multiprocessing as mp


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
    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            f"$ python3 {os.path.basename(__file__)} mol.g96\n"
            f"$ python3 {os.path.basename(__file__)} *.g96"
        )
        exit()

    wrong_g96 = sys.argv[1]

    wrong_g96_list = sorted(glob.glob(wrong_g96))

    pool = mp.Pool(psutil.cpu_count(logical=False))

    for wrong_g96 in wrong_g96_list:
        pool.apply_async(
            func=_fix,
            args=(wrong_g96,),
        )

    pool.close()
    pool.join()
