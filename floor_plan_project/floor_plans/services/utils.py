import csv
import os
import re


def get_image_record_id_from_url(url):
    if url[-1] == "/":
        return os.path.basename(url[:-1])
    else:
        return os.path.basename(url)


def extract_urls_from_csv(file_path, start, limit):
    """
    Get urls from second column of given csv file.
    Because csv.reader is a generator we need to specify processing start and limit.
    :param file_path: string path to csv file
    :param start: starting row
    :param limit: ending row
    :return: list of urls
    """
    url_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in zip(range(limit), reader):
            if i > start:
                url_list.append(row[1])
    return url_list[1:]


def extract_urls_from_file(file_path):
    url_list = []
    with open(file_path, "r") as f:
        for line in f:
            url_list.append(line.strip())
    return url_list


def get_url_list_from_file(file_name):
    with open(file_name, "r") as f:
        s = f.read()
        return re.split("<br>", s)[1:-1]
