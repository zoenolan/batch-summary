#!/usr/bin/python

import os
import sys
import time
import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('OPENAI_MODEL')


def usage():
    print("Usage: python summary.py <input_dir> <output_dir> <instruction_dir>")
    print("Example: python summary.py input output instructions")


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def list_subdirectories(directory):
    subdirectories = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            subdirectories.append(item)
    return subdirectories


def get_last_modified_timestamp(file_path):
    try:
        timestamp = os.path.getmtime(file_path)
        return timestamp
    except FileNotFoundError:
        return 0
    except Exception as e:
        return 0


def get_latest_modified_file(files):
    latest_time = 0

    for file in files:
        last_modified_time = get_last_modified_timestamp(file)

        if (last_modified_time > latest_time):
            latest_time = last_modified_time

    return latest_time


def get_instruction_files(directory):
    if (os.path.exists(directory) is not True):
        print("Base directory does not exist: " + directory)
        sys.exit(1)

    files = os.listdir(directory)

    if (len(files) < 1):
        print("Empty list of instructions: " + directory)
        sys.exit(1)

    paths = [directory + file for file in files]

    return paths

def load_transscripts(files):
    transscripts = ""

    for file in files:
        input_file = open(file, "r")
        transscript = input_file.read()
        input_file.close()

        transscripts = transscripts + transscript

    return transscripts


def generate_plan(transscripts, instructions, output_path):
    docuument_prompt = "docuument\n" + transscripts

    prompt_file = open(instructions, "r")
    prompt = prompt_file.read()
    prompt_file.close()

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": docuument_prompt}
    ]

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )

    result = response['choices'][0]['message']['content']

    print("Saving file: " + output_path + " ...")

    output_file = open(output_path, "w")
    output_file.write(result)
    output_file.close()


if len(sys.argv) < 4:
    usage()
    sys.exit(1)

INPUT_DIRECTORY = sys.argv[1] + "/"
OUTPUT_DIRECTORY = sys.argv[2] + "/"
INSTRUCTIONS_DIRECTORY = "./" + sys.argv[3] + "/"

instructions = get_instruction_files(INSTRUCTIONS_DIRECTORY)

if (os.path.exists(INPUT_DIRECTORY) is not True):
    print("Base directory does not exist: " + INPUT_DIRECTORY)
    sys.exit(1)

create_directory(OUTPUT_DIRECTORY)

files = os.listdir(INPUT_DIRECTORY)
if (len(files) > 0):
    print("Processing input directory ...")

    file_paths = [INPUT_DIRECTORY + "/" + path for path in files]
    transscripts = load_transscripts(file_paths)
    youngest_input = get_latest_modified_file(file_paths)

    output_subdirectory = OUTPUT_DIRECTORY
    create_directory(output_subdirectory)

    for plan in instructions:
        print("Processing plan: " + plan + " ...")

        plan_age = get_last_modified_timestamp(plan)
        if (plan_age < youngest_input):
            cutoff = youngest_input
        else:    
            cutoff = plan_age

        output_path = output_subdirectory + "/" + \
            os.path.basename(os.path.normpath(plan))
        
        output_age = get_last_modified_timestamp(output_path)

        if output_age < cutoff:
            generate_plan(transscripts, plan, output_path)
