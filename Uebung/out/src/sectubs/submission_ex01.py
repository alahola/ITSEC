#!/usr/bin/env python3

'''
@author: Christian Wressnegger
'''

import argparse
import os
import shutil
import stat
import sys
import tarfile


MAX_STUDENTS_PER_TEAM = 2


# Simple logging functionality


def log_ex(t, s):
    ''' Print the string s with a common logging prefix and type t '''
    header = "[{}] ".format(t)
    s = s.replace("\n", "\n" + " " * len(header))
    sys.stdout.write("{}{}\n".format(header, s))


def log(m):
    ''' Log a generic message m '''
    log_ex('*', m)


def info(m):
    ''' Log an info message m '''
    log_ex('I', m)


def error(m):
    ''' Log an error message m '''
    log_ex('!', m)


def warn(m):
    ''' Log an warning message m '''
    log_ex('W', m)


# Argument parsing


def __pop_arg():
    ''' Remove and return the first argument from the list of program arguments '''
    if len(sys.argv) <= 1:
        return None

    arg = sys.argv[1]
    del(sys.argv[1])
    return arg


# I/O


def __create_dir(p, force=False):
    '''
    Create directory at path p. If force is set to True existing
    directories will be delete first.
    '''
    if not p:
        return False

    if os.path.exists(p):
        if force:
            shutil.rmtree(p)

        else:
            error("Default output directory already exists. Please delete it first.")
            return False

    os.mkdir(p)

    if not os.path.exists(p) or not os.path.isdir(p):
        error("Output directory doesn't exist or isn't a directory")
        return False

    elif force:
        shutil.rmtree(p)
        os.mkdir(p)

    return True


def __create_outputdir(p, force=True, dry_run=False):
    '''
    Create an output directory at path p. If force is set to True existing
    directories will be delete first.

    In case p is set to None a directory named 'out' will be created in the
    current directory.
    '''

    if p == None:
        p = os.path.join(os.getcwd(), "out")

    p = os.path.abspath(p)
    return (p if dry_run or __create_dir(p, force) else None)


# Data


NAME_FILE = "NAME"
SRC_DIR = "src"
DOC_DIR = "doc"
SEP = '/'  # tar archives make use of '/' only

SUBMISSION_NOTE = '''\
For submission, copy your solutions in there and make it a tar.gz
archive:
            ~$ tar czf submission.tar.gz *

Also, do not forget to 'check' and 'test' your solutions first
using this tool ;)
'''


# Program modes


def add_student(firstnames, surname, student_id, output, max_nstudents=1, errors_only=False):

    output = __create_outputdir(output, dry_run=True)

    if not firstnames:
        error("No first name specified")
        return -1

    if not surname:
        error("No surname name specified")
        return -2

    if student_id == None:
        error("No student id specified")
        return -3

    if not firstnames:
        error("No first name specified")
        return -4

    try:
        with open(os.path.join(output, NAME_FILE), 'r') as f:
            n = sum(1 for _ in f)
    except:
        n = 0

    try:
        if n >= max_nstudents:
            error("Teams may consist out of {} student(s) only".format(max_nstudents))
            return -6

        with open(os.path.join(output, NAME_FILE), 'a') as f:
            f.write("{} {} ({})\n".format(firstnames, surname, student_id))

    except IOError as e:
        error(str(e))
        return -5

    if not errors_only:
        info("Successfully added another team mate")

    return 0


def prepare_submission(firstnames, surname, student_id, output, rm_output):

    output = __create_outputdir(output, rm_output)

    if not output:
        return -1

    if not __create_dir(os.path.join(output, SRC_DIR), rm_output):
        error("Unable to create source directory")
        return -2

    if not __create_dir(os.path.join(output, DOC_DIR), rm_output):
        error("Unable to create source directory")
        return -3

    ret = add_student(firstnames, surname, student_id, output,
                      max_nstudents=MAX_STUDENTS_PER_TEAM, errors_only=True)
    if ret < 0:
        shutil.rmtree(output, ignore_errors=True)
        return ret - 3

    info("Basic folder structure successfully created at\n'{}'\n".format(output))
    info(SUBMISSION_NOTE)
    return 0


def check_submission(archive, errors_only=False):
    if not os.path.exists(archive):
        error("The specified archive does not exist :(")
        return -1

    report = SEP.join([DOC_DIR, "report.pdf"])

    try:
        with tarfile.open(archive, 'r:gz') as f:
            submission = dict([(ti.path, ti) for ti in f.getmembers()])
            submitted_folders = set(
                x.partition(SEP)[0] for x in submission.keys() if SEP in x)

            # Student ID?
            try:
                if submission[NAME_FILE].size <= 0:
                    error("Empty student identification :(")
                    return -2

            except KeyError:
                error('No student identification (file "{}") included'.format(NAME_FILE))
                return -2

            # Documentation included?
            try:
                if submission[report].size <= 0:
                    error("Zero-size documentation :(")
                    return -3

            except KeyError:
                error('No documentation (file "{}") included'.format(report))
                return -3

            # Sources included?
            if SRC_DIR not in submitted_folders:
                if not errors_only:
                    warn("No sources included. Are you sure?")

        if not errors_only:
            info("Very well, the format and structure of the submission looks good")

    except (IOError, OSError, tarfile.ReadError):
        error("Unable to process/check the archive. Is it really a tar.gz file?")
        return -4

    return 0


def test_submission(archive, valscripts, output, rm_output, unpack_only=False):
    if not os.path.exists(archive):
        error("Input file doesn't exist")
        return -1

    if check_submission(archive, True) != 0:
        return -2

    output = __create_outputdir(output, rm_output)
    if not output:
        return -3

    def include(ti):
        path = ti.path
        if os.path.basename(path).startswith('.'):  # hidden files
            return False
        if path.startswith(DOC_DIR) and path.endswith(".pdf"):
            return True
        if path.startswith(SRC_DIR) and path.endswith(".py"):
            return True
        if path.startswith(SRC_DIR) and path.endswith(".txt"):
            return True
        if path == NAME_FILE:
            return True

        return False

    # Extract all files matching the above specification (cf. include(.))
    with tarfile.open(archive, 'r:gz') as f:
        l = list(ti for ti in f.getmembers() if include(ti))

        # Make sure we can access the files
        for x in l:
            x.mode = x.mode | stat.S_IRWXU

        f.extractall(output, l)

    student_name = os.path.join(output, NAME_FILE)
    src = os.path.join(output, SRC_DIR)

    with open(student_name, 'r') as f:
        for line in f.readlines():
            info(line.strip())
            break

    info("Copied files:")
    for filename in sorted(x.name for x in l):
        print(filename)

    valscripts = [x for x in valscripts if os.path.exists(x)]

    if valscripts:
        os.makedirs(src, exist_ok=True)

        info("Validation scripts:")
        for script in valscripts:
            shutil.copy(script, src)
            print(script)

        if not unpack_only:
            test = os.path.basename(valscripts[0])
            info("Start unit test: {}\n".format(test))

            test = os.path.join(src, test)
            os.chmod(test, stat.S_IRWXU)

            os.chdir(src)
            os.system("python3 -B " + test)

    else:
        info("Cannot run tests. No validation scripts specified.")

    return 0


MODES = ["prepare", "add-student", "check-format", "test"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", metavar="T", action="store", choices=MODES,
                        help="One of: {0}".format(', '.join(MODES)), default=None)

    mode = __pop_arg()

    if mode == MODES[0]:
        parser = argparse.ArgumentParser()
        parser.add_argument("--firstname", action="store", type=str, metavar="STR", dest="firstnames", required=True,
                            help="Your first names")
        parser.add_argument("--surname", action="store", type=str, metavar="STR", dest="surname", required=True,
                            help="Your surname")
        parser.add_argument("--student-id", action="store", type=int, metavar="INT", dest="student_id", required=True,
                            help="Your student id")
        parser.add_argument("--out", action="store", dest="output", default=None,
                            help="The output directory to write the contents to.")
        parser.add_argument("--out:force", action="store_true", dest="rm_output", default=False,
                            help="Remove the output directory first (Default: False).")

        args = parser.parse_args()
        sys.exit(prepare_submission(args.firstnames, args.surname,
                                    args.student_id, args.output, args.rm_output))

    elif mode == MODES[1]:
        parser = argparse.ArgumentParser()
        parser.add_argument("--firstname", action="store", type=str, metavar="STR", dest="firstnames", required=True,
                            help="Your first names")
        parser.add_argument("--surname", action="store", type=str, metavar="STR", dest="surname", required=True,
                            help="Your surname")
        parser.add_argument("--student-id", action="store", type=int, metavar="INT", dest="student_id", required=True,
                            help="Your student id")
        parser.add_argument("--out", action="store", dest="output", default=None,
                            help="The output directory to write the contents to.")

        args = parser.parse_args()
        sys.exit(add_student(args.firstnames, args.surname,
                             args.student_id, args.output, max_nstudents=MAX_STUDENTS_PER_TEAM))

    elif mode == MODES[2]:
        parser = argparse.ArgumentParser()
        parser.add_argument("input", action="store", type=str, metavar="{submission as TAR.GZ}",
                            help="The archive containing the files to process.")

        args = parser.parse_args()
        sys.exit(check_submission(args.input))

    elif mode == MODES[3]:
        parser = argparse.ArgumentParser()
        parser.add_argument("input", action="store", type=str, metavar="{submission as TAR.GZ}",
                            help="The archive containing the files to process.")

        parser.add_argument("--validation-scripts", action="store", nargs="+", type=str,
                            metavar="FILE", dest="validation_scripts", default=[], required=True,
                            help="One or more scripts that are copied to the 'src' folder. The first is executed as unit test.")
        parser.add_argument("--unpack-only", action="store_true", dest="unpack_only", default=False,
                            help="Skips the actual test and only unpacks and prepares the submission")
        parser.add_argument("--out", action="store", dest="output", default=None,
                            help="The output directory to write the contents to.")
        parser.add_argument("--out:force", action="store_true", dest="rm_output", default=False,
                            help="Remove the output directory first (Default: False).")

        args = parser.parse_args()
        sys.exit(test_submission(
            args.input, args.validation_scripts, args.output, args.rm_output, args.unpack_only))

    else:
        parser.print_help()
        sys.exit(1)

