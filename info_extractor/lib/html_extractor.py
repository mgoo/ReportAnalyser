import os
import subprocess

import xml.etree.ElementTree as ET
from pdftotree.TreeExtract import TreeExtractor
from lxml.html.clean import Cleaner


def html_to_text(filename, company, year):
    html_tree = ET.ElementTree(file="static/file_store/html/%s/%s/%s.html" % (company, year, filename))
    html_content = ET.tostring(html_tree.getroot(), encoding='unicode', method='text')
    return html_content


def pdf_to_html_text(filename, company):
    """
    This will convert a pdf into html format. In the process it will lose the
    formatting however it will identify the tables and convert them to html.

    :param filename: filename of the pdf file
    :return: html string
    """
    tree = TreeExtractor("static/file_store/pdf/%s/%s.pdf" % (company, filename))
    tree.parse()
    tree.get_tree_structure(None, None, True)
    cleaner = Cleaner(kill_tags=['figure'])
    return cleaner.clean_html(tree.get_html_tree())


def pdf_to_htmlfile_formatted(filename, company, year):
    """
    Requires the pdftohtml tool to be installed. This seems to be installed by default on
    Linux but I dont know about windows.
    This will maintain the formatting of the pdf but the tables are not identified

    :param filename: name of the pdf file to create
    :param company: code of the company that the pdf is for
    :param year: the year that the report is from
    :return: True if succeeded
    """

    return_code = subprocess.call([
        'pdftohtml',
        '-s',
        "static/file_store/pdf/%s/%s.pdf" % (company, filename),
        "static/file_store/html/%s/%s/%s_formatted.html" % (company, year, filename)
    ])
    html = read_htmlfile("%s_formatted-html" % (filename), company, year)
    # Make all the urls relative to the root rather than local
    html = html.replace('src="', 'src="/static/file_store/html/%s/%s/' % (company, year))
    with open("static/file_store/html/%s/%s/%s_formatted-html.html" % (company, year, filename), 'w') as html_file:
        html_file.write(html)
    return return_code == 0


def pdf_to_htmlfile_tables(filename, company, year):
    """
    Gets the just the tables from the pdf file and saves them to
    an html file

    :param filename: name of the pdf to read from
    :param company: code of the company that the report was from
    :param year: the year that the report was from
    """
    html = pdf_to_html_text(filename, company)

    report = ET.ElementTree(ET.fromstring(html))
    tables = ET.ElementTree(ET.fromstring('<html><head></head><body></body></html>'))

    tables_body = tables.find('body')

    for div_elem in report.findall('body/div'):
        for elem in div_elem.findall('table'):
            div_elem.remove(elem)
            tables_body.append(elem)

    tables.write("static/file_store/html/%s/%s/%s_tables.html" % (company, year, filename))
    report.write("static/file_store/html/%s/%s/%s.html" % (company, year, filename))


def pdf_to_htmlfile(filename, company, year):
    """
    This function will create a formatted html representation and a text based
    representation with bettor formatting

    :param filename: file name of the pdf file and the base for the filename
                        for the html function
    :param company:
    :param year:
    """
    if not os.path.exists("static/file_store/html/%s/%s/" % (company, year)):
        os.makedirs("static/file_store/html/%s/%s/" % (company, year))

    pdf_to_htmlfile_tables(filename, company, year)
    pdf_to_htmlfile_formatted(filename, company, year)


def save_pdf_file(pdf_file, filename, company):
    if not os.path.exists("static/file_store/pdf/%s/" % (company)):
        os.makedirs("static/file_store/pdf/%s/" % (company))

    with open("static/file_store/pdf/%s/%s.pdf" % (company, filename), 'wb+') as destination:
        for chunk in pdf_file.chunks():
            destination.write(chunk)


def read_htmlfile(filename, company, year):
    contents = ""
    with open("static/file_store/html/%s/%s/%s.html" % (company, year, filename), 'r') as html_file:
        for line in html_file.readlines():
            contents += line
    return contents
