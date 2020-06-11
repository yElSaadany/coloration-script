import json
import argparse
import os
import math
# Pandas until something better
from pandas.io.excel import ExcelWriter
import pandas as pd


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file on which you have the sentiment analysis")
    parser.add_argument("-o", help="Output html file, will print to standard output if not selected", default="output")
    parser.add_argument("-t", help="HTML Template")
    parser.add_argument("-m", help="Split documents into multiple HTMLs each named their document's id",
                        action="store_true", default=False)
    args = parser.parse_args()
    return args


def coloring(x):
    """Nice smooth coloring"""
    return 1 - math.cos(math.pi * (x - 0.5))**2


def to_file(data, output="id", template=None):
    """Creates an HTML file with the colored sentences.

    TODO: Templates.

    Args:
        data (dict): JSON doc with (see an .json exemple to have the structure)
        template (str): Future feature, not in use right now.
                        The idea is to have multiple HTML/CSS templates
                        to choose from.
    """
    if output == "id":
        output = data['id'] + ".html"
    with open(output, 'w') as html:
        document = data
        html.write("<!DOCTYPE html>")
        html.write("<html>")
        if template is None:
            html.write("<head></head>")
        else:
            html.write("<head>")
            html.write("<link rel='stylesheet' type='text/css' href='templates/%s.css'>" % template)
            html.write("<link rel='stylesheet' type='text/css' href='style.css'>")
            html.write("</head>")
        html.write("<body><p><div id='info'></div>")

        for line in document['sentences']:
            # Gradation
            a = coloring(line['sentiment'])
            if line['sentiment'] > 0.50:
                green = 'background-color: rgba(0, 255, 0, %f); font-weight: bold' % a
            else:
                green = 'background-color: rgba(255, 0, 0, %f); font-weight: bold' % a
            html.write("<span class='sen' id='%s' style='%s'>%s</span>\n" % (line['sentiment'], green, line['text']))
        html.write("</p></body>")
        html.write("<script src='coloration.js'></script>")
        html.write("</html>")


def only_html(data):
    """Outputs HTML directly on standard output

    Note:
        Does not use coloring().

    TODO: Use coloring().

    Args:
        data (dict): JSON doc with (see an .json exemple to have the structure)

    """
    for document in data:
        print('<p>')
        for line in document['sentences']:
            if float(line['sentiment']) >= 0.75:
                a = 1 - float(line['sentiment'])
                a = 1 - a * float(4)
                if a < 0.1:
                    a = 0.2
                green = 'background-color: rgba(0, 255, 0, %f); font-weight: bold' % a
                print("<span style='%s'>%s</span>\n" % (green, line['text']))
            elif float(line['sentiment']) <= 0.25:
                a = 1 - float(line['sentiment']) * float(4)
                if a < 0.1:
                    a = 0.2
                red = 'background-color: rgba(255, 0, 0, %f); font-weight: bold' % a
                print("<span style='%s'>%s</span>\n" % (red, line['text']))
            else:
                print("<span>%s</span>\n" % line['text'])
        print('</p>')


def get_news_data(news_json):
    """Makes a dict out of a JSON file"""
    with open(news_json, 'r+') as jdoc:
        return json.load(jdoc)


def generate_multiple_html(folder, output_folder):
    """Makes as many HTML files as there are JSON files

    Args:
        folder (str): Folder containing the JSON files
        output_folder (str): Folder to put the HTML files
    
    """
    news_json = os.listdir(folder)
    # TODO: prob need to check file names for json and also to store id
    # TODO: something better than a for loop
    for news_name in news_json:
        news = get_news_data(folder + '/' + news_name)
        name = "%s/%s.html" % (output_folder, news_name.split('.')[0])
        to_file(news, name, "default")


def multiple_html_json(documents, output_folder="results"):
    """Same as generate_multiple_html() but with one JSON file

    Args:
        documents (dict): Dict made from get_news_data()
        output_folder (str): Folder to put the HTML files

    """
    for doc in documents:
        to_file(doc, "%s/%s.html" % (output_folder, doc["id"]), "default")


def from_csv_to_excel(csv, id):
    """Makes an excel stylesheet out of a CSV (For user tests)."""
    try:
        with ExcelWriter(id+'.xlsx') as ew:
            pd.read_csv(csv).to_excel(ew, sheet_name="sheet", index=None)
    except:
        pass


def to_csv(json, output_folder='results_csv', excel=False):
    """WIP. Makes CSVs out of the sentiments. (For user tests)"""
    documents = get_news_data(json)
    for document in documents:
        output_file = output_folder + '/' + document['id'] + '.csv'
        with open(output_file, 'w+') as csv:
            for sentence in document['sentences']:
                line = '%s,%s,%f,0\n' % (sentence['id'],
                                         sentence['text'],
                                         sentence['sentiment'])
                csv.write(line)
        from_csv_to_excel(output_file, 'results_excel' + '/' + document['id'])


def load_dataframe(json):
    """Helper function of store_to_file()."""
    documents = get_news_data(json)
    frames = []
    id = []
    for document in documents:
        df = {'id': [], 'sentence': [], 'pred': [], 'human': []}
        for sentence in document['sentences']:
            df['id'].append(sentence['id'])
            df['sentence'].append(sentence['text'])
            df['pred'].append(sentence['sentiment'])
            df['human'].append(0)
        id.append(document['id'])
        frames.append(pd.DataFrame(df))
    return id, frames


def store_to_file(json, csv=False, excel=False):
    """Better than to_csv() and from_csv_to_excel() but needs Pandas
    
    Note:
        Prefer this function to have a CSV/Excel file from the
        JSON sentiments file.
    
    """
    id, frames = load_dataframe(json)

    i = 0
    if excel:
        for frame in frames:
            frame.to_excel('results_excel/'+id[i]+'.xlsx', index=False)
            i += 1

    i = 0
    if csv:
        for frame in frames:
            frame.to_csv('results_csv/'+id[i]+'.csv', index=False)
            i += 1


if __name__ == '__main__':
    args = init_args()

    # If the input arg is a folder (that means we want a compute
    # the JSON file in that folder).
    if os.path.isdir(args.input):
        if not os.path.isdir(args.o):
            os.mkdir(args.o)
        generate_multiple_html(args.input, args.o)
    else:
        # Else means that the sentiments are in a single JSON file.
        data = get_news_data(args.input)
        if args.m:
            if not os.path.isdir(args.o):
                os.mkdir(args.o)
            multiple_html_json(data, args.o)
        elif args.o is not None:
            to_file(data, args.o, args.t)
        else:
            only_html(data)
