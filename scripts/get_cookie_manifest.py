#!/bin/env python

# get_cookie_names is an example of how to get all the patient names (and other fun metadata to search)
# of our downloaded dicom cookies. The main purpose of this is to generate a simple datastructure
# that will drive (give suggestions) for a user to search the same dataset via a Find Service User and
# Provider We are going to use the files provided in the repo, but we just as easily could have downloaded he datasets with get_datasets.py, and pointed to that base.

# We are going to use a function from node_dcm.utils to get the list of files. and another
# from node_dcn.validate to validate them. These functions are also provided here.

from pydicom import read_file
import json
import fnmatch
import sys
import os

############################################################################
# from node_dcm.utils import get_dicom_files
############################################################################

def print_pretty(content,output_file=None):
    if output_file is None:
        print(json.dumps(content, indent=4, separators=(',', ': ')))
    else:
        with open(output_file,'w') as filey:
            filey.write(json.dumps(content, indent=4, separators=(',', ': '))) 
    return output_file


def recursive_find_dicoms(base):
    '''recursive find dicoms will search for dicom files in all directory levels
    below a base. It uses get_dcm_files to find the files in the bases.
    '''
    dicoms = []
    for root, dirnames, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, '*.dcm'):
            dicoms.append(os.path.join(root, filename))

    return dicoms


def get_dicom_files(contenders,check=True):
    '''get_dcm_files will take a list of single dicom files or directories,
    and return a single list of complete paths to all files
    '''
    if not isinstance(contenders,list):
        contenders = [contenders]

    dcm_files = []
    for contender in contenders:
        if os.path.isdir(contender):
            dicom_dir = recursive_find_dicoms(contender)
            dcm_files.extend(dicom_dir)
        else:
            if contender.endswith('.dcm'):
                bot.debug("Adding single file %s" %(contender))
                dcm_files.append(contender)

    dcm_files = validate_dicoms(dcm_files)
    return dcm_files


############################################################################
# from node_dcm.validate import validate_dicoms
############################################################################


def validate_dicoms(dcm_files):
    '''validate dicoms will test opening one or more dicom files, and return a list
    of valid files.
    :param dcm_files: one or more dicom files to test'''
    if not isinstance(dcm_files,list):
        dcm_files = [dcm_files]

    valids = []

    for dcm_file in dcm_files:

        try:
            with open(dcm_file, 'rb') as filey:
                dataset = read_file(filey, force=True)
            valids.append(dcm_file)
             
        except IOError:
            print('Cannot read input file {0!s}'.format(dcm_file))
            sys.exit(1)

    print("Found %s valid dicom files" %(len(valids)))
    return valids



here = os.path.dirname(__file__)
base = os.path.join(here,'..','_datasets')
dicom_files = get_dicom_files(base)

cookies = dict()
for dicom_file in dicom_files:
    ds = read_file(dicom_file) 
    pid = str(ds.PatientID)
    cookie = {'patient_id':pid,
              'patient_name':str(ds.PatientName),
              'operator_name':str(ds.OperatorsName),
              'physician_referring':str(ds.ReferringPhysicianName),
              'physician_reading':str(ds.NameOfPhysiciansReadingStudy),
              'patient_gender':str(ds.PatientSex)}
    if pid not in cookies:
        cookies[pid] = [cookie]
    else:
        cookies[pid].append(cookie)

# Print cookie manifest to file
manifest="%s/cookie_manifest.json" %here
print("Saving cookie manifest to %s" %manifest)
print_pretty(cookies,output_file=manifest)
