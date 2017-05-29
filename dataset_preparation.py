import glob
import os
import shutil

from fire import Fire


def file_id(filepath):
    basename = os.path.basename(filepath)
    return basename[:basename.rfind('.')]


def copy_files(files, outdir):
    os.makedirs(outdir)
    for f in files:
        shutil.copy(f, outdir)


def split_dir(input_dir, outdir1, outdir2, split_ratio=0.8, file_ext=''):
    """
    Splits files from input_dir with split_ratio and copies to outdir1 and outdir2.
    """
    all_files = glob.glob(input_dir + '/*' + file_ext)
    fileset_size = int(len(all_files) * split_ratio)
    fileset1 = all_files[:fileset_size]
    fileset2 = all_files[fileset_size:]
    copy_files(fileset1, outdir1)
    copy_files(fileset2, outdir2)


def copy_intersection(input_dir1, input_dir2, outdir):
    """
    Copy all files from input_dir2 to outdir which have matching base filenames with input_dir1.
    Args:
        input_dir1: Dir against which filenames to be matched.
        input_dir2: Dir from where files to be copied.
        outdir: Target dir.

    """
    all_files1 = glob.glob(input_dir1 + '/*')
    all_files2 = glob.glob(input_dir2 + '/*')
    file_ids1 = set([file_id(f) for f in all_files1])
    os.makedirs(outdir)
    for f in all_files2:
        if file_id(f) in file_ids1:
            shutil.copy(f, outdir)


if __name__ == '__main__':
    Fire({'split-dir': split_dir, 'copy-intersection': copy_intersection})
