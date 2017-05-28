#!/bin/env python

'''
Runtime executable, example of how we might use our little API to get images

Copyright (c) 2017 Vanessa Sochat, Stanford University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''


import requests
from glob import glob
import argparse
import urllib
import json
import sys
import os



def get_parser():

    parser = argparse.ArgumentParser(
    description="download and query data from your json dataset API.")

    parser.add_argument("--output", 
                        dest='output', 
                        help="a folder to save output files to.", 
                        type=str, 
                        default=None)

    parser.add_argument('--images', 
                        dest='images', 
                        help="download images", 
                        default=False, 
                        action='store_true')

    parser.add_argument('--show', 
                        dest='show', 
                        help="print the json data structure of the endpoint to the screen", 
                        default=False, 
                        action='store_true')

    parser.add_argument("--uri", 
                        dest='uri', 
                        help="the github repo username/reponame", 
                        type=str, 
                        default="pydicom/dicom-cookies")

    return parser


def main():
    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if args.output is None and args.show is False:
        parser.print_help()

        print("\nSpecify to download data with --output or just print to screen with --show")
        sys.exit(0)

    username,reponame=parse_uri(args.uri)

    base = "https://%s.github.io/%s" %(username,reponame)    
    images_base = "%s/images" %(base)    
    datasets_base = "%s/datasets" %(base)    

    # Does the user want images or datasets?
    url = datasets_base
    images_only=False
    if args.images is True:
        url = images_base
        images_only=True

    # Retrieve the data structure
    if args.show is False:
        print("Retrieving %s" %(url))
    result = requests.get(url).json()

    if args.show is False:
        print("Found %s results" %(len(result['data'])))

    output = None
    if args.output is not None:
        if os.path.exists(args.output):
            output = args.output

    if output is None:
        if args.show is True:
            print_pretty(result)
    else:
        print("Saving datasets to output folder.")
        for entity in result['data']:
            save_dataset(base=output,
                         entity=entity,
                         images_only=images_only)

# Helper Functions

def parse_uri(uri):
    return uri.split('/',1)

def print_pretty(content):
    print(json.dumps(content, indent=4, separators=(',', ': ')))

def download_file(from_url,to_file):
    urllib.request.urlretrieve(from_url, to_file)

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def save_dataset(base,entity,images_only=False):
    entity_base = "%s/%s" %(base,entity['id'])    
    mkdir(entity_base) 
    if images_only:    
        gets = ['images']
    else:
        gets = ['images','texts']
    for key,url in entity['links'].items():
        if key in gets:
            entity_content = "%s/%s" %(entity_base,key)
            mkdir(entity_content) 
            content = requests.get(url).json()
            for image in content['data']:
                if key in image:
                    for k,v in image[key].items():
                        print("Downloading %s for %s" %(k,entity['id']))
                        output_file = "%s/%s" %(entity_content,k)
                        download_file(v,output_file)
          

if __name__ == '__main__':
    main()
