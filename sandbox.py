import os
import pdb
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

def get_results(result):
    if 'TLE Time Limit exceeded (H)' in result:
        result = "TIME LIMIT EXCEEDED"
    elif 'MemoryError' in result:
        result = "MEMORY LIMIT EXCEEDED"
    elif 'RuntimeError' in result:
        result = "RUNTIME ERROR"
    else:
        result = result
    return result


def execute_code_for_python(prog_folder, prog_lang, prog_file, input_file, output_file, error_file):
    status = True
    copy_sandbox_executable_to_prog_folder(prog_folder)
    command = "chmod +x " + prog_folder
    os.system(command)
    open(error_file, "w").close()

    exec_command = "#!/usr/bin/python"
    python_file = open(prog_file, "r").read()
    modified_python_file = exec_command + "\n" + python_file
    
    outfile = open(prog_file, "w")
    outfile.write(modified_python_file)
    outfile.close()
    command = "chmod +x " + prog_file
    os.system(command)
    sandbox_command = "./" + prog_folder + "/sandbox ./" + prog_file + " --input=" + input_file + \
                      " --output=" + output_file + " --time=" + str(TIME_LIMIT) + " --chroot="  + \
                      prog_folder + " --debug > " + error_file + " 2>&1"
    os.system(sandbox_command)
    
    error_string = open(error_file, "r").read()
    if len(error_string) > 0:
        status = False
        result = get_results(error_string)
    else:
        result = None
        status = True
    return (result, status)
            

def execute_code_for_compiled_progs(prog_folder, prog_lang, prog_file, input_file, output_file, error_file, executable):
    status = True
    copy_sandbox_executable_to_prog_folder(prog_folder)
    command = "chmod +x " + prog_folder
    os.system(command)
    open(error_file, "w").close()

    if prog_lang == "cpp":
        command = "g++ " + prog_file + " -o " + executable + " > " + error_file + " 2>&1 "
        os.system(command)
        error_string = open(error_file, "r").read()
        if len(error_string) > 0:
            status = False
            return (error_string, status)
        else:
            sandbox_command =  "./" + prog_folder + "/sandbox ./" + executable + " --input=" + \
                                input_file + " --output=" + output_file + " --time=" + str(TIME_LIMIT) + \
                                "chroot=" + prog_folder + " > " + error_file + " 2>&1"
            os.system(sandbox_command)
    else:
        command = "gcc " + prog_file + " -o " + executable + " > " + error_file + " 2>&1"
        os.system(command)
        error_string = open(error_file, "r").read()
        if len(error_string) > 0:
            status = False
            return (error_string, status)
        else:
            sandbox_command =  "./" + prog_folder + "/sandbox ./" + executable + " --input=" + \
                               input_file + " --output=" + output_file + " --time=" + str(TIME_LIMIT) + \
                               "chroot=" + prog_folder + " > " + error_file + " 2>&1"
            os.system(sandbox_command)

    error_string = open(error_file, "r").read()
    if len(error_string) > 0:
        status = False
        result = get_results(error_string)
    else:
        status = True
        result = None
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

    if prog_lang == "python":
        result, status = execute_code_for_python(prog_folder, prog_lang, prog_file, input_file, \
                                                                        output_file, error_file)
    else:
        result, status = execute_code_for_compiled_progs(prog_folder, prog_lang, prog_file, \
                                            input_file, output_file, error_file, executable)

    if not result:
        # Without any error here.
        result = open(output_file, "r").read()
        return (result, status)
    else:
        # with compile (or) runtime errors
        return (result, status)
