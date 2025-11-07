# papersummary
Lightweight pipeline for summarizing documents.

Supported Document Types:
- `.pdf`
- `.pptx`
- `.docx`

## Set Up
Be sure [Python 3](https://www.python.org/downloads/) is installed.

```
git clone https://github.com/ereoh/papersummary.git
cd papersummary/

# (optional, highly reccomended)
# Use a virtual environment
python -m venv venv

# activate on Linux
source venv/bin/activate
# activate on Windows
venv\Scripts\Activate.ps1

# install library dependencies
pip install -e .

# to leave virtual environment:
deactivate
```

## Usage
0. If you used a virtual environment, activate it:
```bash
# activate on Linux
source venv/bin/activate
# activate on Windows
venv\Scripts\Activate.ps1
```
### GUI
```bash
papersummary
```

### Compile to .exe
```bash
pyside6-deploy --name="papersummary" papersummary/gui.py
```

## FAQ
- Why convert PDFs to txt?
    - Many AI agents have a hard time parsing PDF files, but can easily read txt files.
- Why no automatic prompting?
    - To keep this library as flexible and lightweight as possible, users can add their own code/workflows/pipeline to query the AI of their choice.