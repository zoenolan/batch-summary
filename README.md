# LLM-based Batch Summary Generator

## Setup 
- Create an venv `python3 -m venv .`
- Activate a venv `source ./bin/activate`
- Deactivate a venv `deactivate`
- Install the requirements `pip install -r requirements.txt`

## Usage
- Create an `input` directory
- Add a file with `title: "Artcile title"`
- Run `python summary.py <input_dir> <output_dir> <instruction_dir>` will take each subdirectory of `input_dir` and transform them based on each file in `instructions`. Saving a file for each prompt in a subdirectory of `output_dir`

## limitations
- Limited to 16K tokens