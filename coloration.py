import json
import argparse


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="JSON file on which you have the sentiment analysis")
    parser.add_argument("-o", help="Output html file, will print to standard output if not selected")
    parser.add_argument("-t", help="HTML Template")
    args = parser.parse_args()
    return args


def to_file(data, output, template=None):
    with open(output, 'w') as html:
        for document in data:
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
                if float(line['sentiment']) >= 0.75:
                    a = 1 - float(line['sentiment'])
                    a = 1 - a * float(4)
                    if a < 0.1:
                        a = 0.2
                    green = 'background-color: rgba(0, 255, 0, %f); font-weight: bold' % a
                    html.write("<span class='sen' id='%s' style='%s'>%s</span>\n" % (line['sentiment'], green, line['text']))
                elif float(line['sentiment']) <= 0.25:
                    a = 1 - float(line['sentiment']) * float(4)
                    if a < 0.1:
                        a = 0.2
                    red = 'background-color: rgba(255, 0, 0, %f); font-weight: bold' % a
                    html.write("<span class='sen' id='%s' style='%s'>%s</span>\n" % (line['sentiment'], red, line['text']))
                else:
                    html.write("<span id='%s'>%s</span>\n" % (line['id'], line['text']))
            html.write("</p></body>")
            html.write("<script src='coloration.js'></script>")
            html.write("</html>")


def only_html(data):
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


if __name__ == '__main__':
    args = init_args()
    with open(args.input, 'r+') as jdoc:
        data = json.load(jdoc)

    if args.o is not None:
        to_file(data, args.o, args.t)
    else:
        only_html(data)
