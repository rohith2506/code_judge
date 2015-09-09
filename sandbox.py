import os
import sys

TIME_LIMIT = 3.00
EXTENSIONS = {'python':'.py','cpp': '.cpp','c': '.c'}
PROG_FILE_NAME = "prog"
INPUT_FILE_NAME = "in.txt"
OUTPUT_FILE_NAME = "out.txt"
ERROR_FILE_NAME = "err.txt"
EXECUTABLE_FILE_NAME = "prog"
PROG_FOLDERS = {"python": "progs/python", "cpp": "progs/cpp", "c":"progs/c"}


def copy_sandbox_executable_to_prog_folder(prog_folder):
    command = "cp sandbox/sandbox " + prog_folder
    os.system(command)


def execute_code(prog_folder, prog_lang, prog_file, input_file, output_file, error_file, executable):
    status = True
    copy_sandbox_executable_to_prog_folder(prog_folder)
    open(error_file, "w").close()

    if prog_lang == "python":
        exec_command = "#!/usr/bin/python"
        python_file = open(prog_file, "r").read()
        modified_python_file = exec_command + "\n" + python_file
        outfile = open(prog_file, "w")
        outfile.write(modified_python_file)
        outfile.close()
        command = "chmod +x " + prog_file
        os.sytem(command)
        sandbox_command = "./sandbox ./" + prog_file + " --input=" + input_file + " --output=" + \
                          output_file + " --time=" + TIME_LIMIT + "--chroot=" + prog_folder + " --debug > " \
                          + error_file + " 2>&1"
        os.system(command)
        error_string = open(error_file, "r").read()
        if len(error_string) > 0:
            status = False
    elif prog_lang == "cpp":
        command = "g++ " + prog_file + " -o " + executable + " 2> " + error_file
        os.system(command)
        error_string = open(error_file, "r").read()
        if len(error_string) > 0:
            status = False
        else:
            sandbox_command =  "./sandbox ./" + executable + " --input=" + input_file + \
                               " --output=" + output_file + " --time=" + TIME_LIMIT + \
                                "chroot=" + prog_folder + " --debug > " + error_file + " 2>&1"
            os.system(sandbox_command)
    else:
        command = "gcc " + prog_file + " -o " + executable + " 2> " + error_file
        print command
        os.system(command)
        error_string = open(error_file, "r").read()
        if len(error_string) > 0:
            status = False
        else:
            sandbox_command =  "./sandbox ./" + executable + " --input=" + input_file + \
                               " --output=" + output_file + " --time=" + TIME_LIMIT + \
                               " --chroot=" + prog_folder + " --debug > " + error_file + " 2>&1"
            os.system(sandbox_command)

    result = ""
    if status == False:
        output_file = error_file
    for line in open(output_file, "r"):
        result += line
    return (result, status)


def get_required_output(prog_id, prog_lang, code, prog_input):
    # create folder using unique id and store files
    prog_folder = PROG_FOLDERS[prog_lang] + "/" + prog_id
    command = "mkdir " + prog_folder
    os.system(command)
    prog_file   = prog_folder + "/" + PROG_FILE_NAME + EXTENSIONS[prog_lang]
    input_file  = prog_folder + "/" + INPUT_FILE_NAME
    output_file = prog_folder + "/" + OUTPUT_FILE_NAME
    error_file  = prog_folder + "/" + ERROR_FILE_NAME
    executable = prog_folder + "/" + EXECUTABLE_FILE_NAME   

    # store code
    open(prog_file, "w").close()
    ofile = open(prog_file, "w")
    ofile.write(code)
    ofile.close()

    # store input
    open(input_file, "w").close()
    ofile = open(input_file, "w")
    ofile.write(prog_input)
    ofile.close()  

    result, status = execute_code(prog_folder, prog_lang, prog_file, input_file, \
                                              output_file, error_file, executable)
    if 'TLE Time Limit exceeded (H)' in result:
        result = "TIME LIMIT EXCEEDED"
    elif 'MemoryError' in result:
        result = "MEMORY LIMIT EXCEEDED"
    elif 'RuntimeError' in result:
        result = "RUNTIME ERROR"
    else:
        result = result
    return (result, status)
