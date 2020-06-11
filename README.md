# coloration-script

## Installation

Clone this repo
```bash
git clone https://github.com/yElSaadany/coloration-script.git
```

For now, you need *pandas*
```bash
pip install pandas
```

## Usage

First, you need a JSON file with the same structure as the ones you have
in the *json_examples* folder. Once you have one, run :
```bash
python coloration.py someSentimentFile.json -m -o output_folder
```
*Warning*: For now, you have to use the -m option.

If it works, nothing should appear on the standard output.
You now have a folder named with your -o option (defaults to *output*).

This folder contains all the HTML files generated from the JSON sentiment file.
You can open this folder with your favorite browser.

You can add some JavaScript to see the sentiment value of each sentences by
copying *coloration.js* to your output folder:
```bash
cp coloration.js output_folder
```