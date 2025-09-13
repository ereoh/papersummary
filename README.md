# papersummary
Lightweight pipeline for summarizing PDFs

## Set Up
Be sure [Python 3](https://www.python.org/downloads/) is installed.

```
git clone https://github.com/ereoh/papersummary.git
cd papersummary/

# (optional, highly reccomended)
# Use a virtual environment
python -m venv papersummary_venv

# activate on Linux
source papersummary_venv/bin/activate
# activate on Windows
papersummary_venv\Scripts\Activate.ps1

# install library dependencies
pip install -r requirements.txt

# to leave virtual environment:
deactivate
```

## Usage
0. If you used a virtual environment, activate it:
```
# activate on Linux
source papersummary_venv/bin/activate
# activate on Windows
papersummary_venv\Scripts\Activate.ps1
```
1. Pass any number of PDFs to script:

```
python papersummary.py <path to pdf> <path to pdf 2> ...
```

Each PDF will be converted to a `.txt` file in the same location as the original PDF file.

2. Copy everything in converted `.txt` file, and paste into any AI agent.

Each file already includes a summarizing prompt: `summarize the following document:` at the top.

3. When done using the tool, leave the virtual environment:
```
deactivate
```

## FAQ
- Why convert PDFs to txt?
    - Many AI agents have a hard time parsing PDF files, but can easily read txt files.
- Why no automatic prompting?
    - To keep this library as flexible and lightweight as possible, users can add their own code/workflows/pipeline to query the AI of their choice.

## Developer Notes
- install python3-tk