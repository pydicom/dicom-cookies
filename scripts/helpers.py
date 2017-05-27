from pydicom.dataset import Dataset
from pydicom import read_file
from PIL import Image
from random import choice
from haikunator import Haikunator
import datetime
import numpy
import json
import os

haikunator = Haikunator()
here = os.path.dirname(os.path.abspath(__file__))

def read_json(filename,mode='r'):
    '''read_json reads in a json file and returns
    the data structure as dict.
    '''
    with open(filename,mode) as filey:
        data = json.load(filey)
    return data

def write_file(filename,content,mode="w"):
    with open(filename,mode) as filey:
        filey.writelines(content)
    return filename


def get_name():
    return haikunator.haikunate(token_length=0,delimiter=' ')


def cookie2dicom(image,metadata):

    im = Image.open(image)
    now = datetime.datetime.now()
    width, height = im.size
    monochrome = im.convert('1')

    pixels = list(monochrome.getdata())    

    metadata = read_json(metadata)
    if isinstance(metadata,list):
        data = dict()
        for item in metadata:
            data[item['key']] = item['value']
        metadata = data

    ds = read_file("%s/dummy.dcm" %here)

    # (0008, 0008) Image Type                          CS: ['DERIVED', 'SECONDARY', 'OTHER']
    ds.ImageType = 'OTHER'

    # (0008, 0012) Instance Creation Date              DA: '20040826'
    ds.InstanceCreationDate = '%s%s%s' %(now.year,now.month,now.day)

    # (0008, 0013) Instance Creation Time              TM: '185434'
    ds.InstanceCreationTime = '%s%s%s' %(now.hour,now.minute,now.second)

    # (0008, 0014) Instance Creator UID                UI: 1.3.6.1.4.1.5962.3
    ds.InstanceCreatorUID = ''

    # (0008, 0016) SOP Class UID                       UI: MR Image Storage
    ds.SOPClassUID = 'Stanford Cookie Database'

    # (0008, 0018) SOP Instance UID                    UI: 1.3.6.1.4.1.5962.1.1.4.1.1.20040826185059.5457
    ds.SOPInstanceUID = ''

    # (0008, 0020) Study Date                          DA: '20040826'        
    ds.StudyDate = '20131210'

    # (0008, 0021) Series Date                         DA: ''
    ds.SeriesDate = ''

    # (0008, 0022) Acquisition Date                    DA: ''
    ds.AcquisitionDate = ''

    # (0008, 0030) Study Time                          TM: '185059'
    ds.StudyTime = '%s%s%s' %(now.hour,now.minute,now.second)

    # (0008, 0031) Series Time                         TM: ''
    ds.SeriesTime = ''

    # (0008, 0032) Acquisition Time                    TM: ''
    ds.AcquisitionTime = ''

    # (0008, 0050) Accession Number                    SH: ''
    ds.AccessionNumber = ''

    # (0008, 0060) Modality                            CS: 'MR'
    ds.Modality = metadata.get('EXIF FileSource','CAMERA')

    # (0008, 0070) Manufacturer                        LO: 'TOSHIBA_MEC'
    ds.Manufacturer = metadata.get('Image Make','')

    # (0008, 0080) Institution Name                    LO: 'TOSHIBA'
    ds.InstitutionName = 'Stanford University'

    # (0008, 0090) Referring Physician's Name          PN: ''
    ds.ReferringPhysicianName = 'Dr. %s' %(get_name())

    # (0008, 0201) Timezone Offset From UTC            SH: '-0400'
    ds.TimezoneOffsetFromUTC = '-0400'

    # (0008, 1010) Station Name                        SH: '000000000'
    ds.StationName = '000000000'

    # (0008, 1060) Name of Physician(s) Reading Study  PN: '----'
    ds.NameOfPhysiciansReadingStudy = 'Dr. %s' %(get_name())

    # (0008, 1070) Operators' Name                     PN: '----'
    ds.OperatorsName = get_name()

    # (0008, 1090) Manufacturer's Model Name           LO: 'MRT50H1'
    ds.ManufacturerModelName = metadata.get('Image Model','')

    # (0010, 0010) Patient's Name                      PN: 'CompressedSamples^MR1'
    ds.PatientName = get_name()

    # (0010, 0020) Patient ID                          LO: '4MR1'
    ds.PatientID = metadata.get('Id','Cookie')

    # (0010, 0030) Patient's Birth Date                DA: ''
    ds.PatientBirthDate = ''

    # (0010, 0040) Patient's Sex                       CS: 'F'
    ds.PatientSex = choice(['M','F'])

    # (0010, 1020) Patient's Size                      DS: ''
    ds.PatientSize = ''

    # (0010, 1030) Patient's Weight                    DS: "80.0000"
    ds.PatientWeight = ''

    # (0018, 0010) Contrast/Bolus Agent                LO: ''
    ds.ContrastBolusAgent = metadata.get('EXIF Contrast','')

    # (0018, 0020) Scanning Sequence                   CS: 'SE'
    ds.ScanningSequence = 'SE'

    # (0018, 0021) Sequence Variant                    CS: 'NONE'
    ds.SequenceVariant = 'NONE'

    # (0018, 0022) Scan Options                        CS: ''
    ds.ScanOptions = ''

    # (0018, 0023) MR Acquisition Type                 CS: '3D'
    ds.MRAcquisitionType = '2D'

    # (0018, 0050) Slice Thickness                     DS: "0.8000"
    ds.SliceThickness = ''

    # (0018, 0080) Repetition Time                     DS: "4000.0000"
    ds.RepetitionTime = ''

    # (0018, 0081) Echo Time                           DS: "240.0000"
    ds.EchoTime = ''

    # (0018, 0083) Number of Averages                  DS: "1.0000"
    ds.NumberOfAverages = 1.000

    # (0018, 0084) Imaging Frequency                   DS: "63.92433900"
    ds.ImagingFrequency = ''

    # (0018, 0085) Imaged Nu\cleus                      SH: 'H'
    ds.ImagedNucleus = 'H'

    # (0018, 0086) Echo Number(s)                      IS: '1'
    ds.EchoNumbers = '1'

    # (0018, 0091) Echo Train Length                   IS: ''
    ds.EchoTrainLength = ''

    # (0018, 1000) Device Serial Number                LO: '-0000200'
    ds.DeviceSerialNumber = ''

    # (0018, 1020) Software Version(s)                 LO: 'V3.51*P25'
    ds.SoftwareVersions = "*".join([metadata.get('EXIF ExifVersion',''),
                                    metadata.get('EXIF FlashPixVersion','')])

    # (0018, 1314) Flip Angle                          DS: "90"
    ds.FlipAngle = '90'

    # (0018, 5100) Patient Position                    CS: 'HFS'
    ds.PatientPosition = 'HFS'

    # (0020, 000d) Study Instance UID                  UI: 1.3.6.1.4.1.5962.1.2.4.20040826185059.5457
    ds.StudyInstanceUID = ''

    # (0020, 000e) Series Instance UID                 UI: 1.3.6.1.4.1.5962.1.3.4.1.20040826185059.5457
    ds.SeriesInstanceUID = ''

    # (0020, 0010) Study ID                            SH: '4MR1'
    ds.StudyId = 'cookietumors'

    # (0020, 0011) Series Number                       IS: '1'
    ds.SeriesNumber = 1

    # (0020, 0012) Acquisition Number                  IS: '0'
    ds.AcquisitionNumber = 0 

    # (0020, 0013) Instance Number                     IS: '1'
    ds.InstanceNumber = 1

    # (0020, 0032) Image Position (Patient)            DS: ['-83.9063', '-91.2000', '6.6406']
    ds.ImagePositionPatient = ''

    # (0020, 0037) Image Orientation (Patient)         DS: 
    ds.ImageOrientationPatient = ['1.0000', '0.0000', '0.0000', '0.0000', '1.0000', '0.0000']

    # (0020, 0052) Frame of Reference UID              UI: 1.3.6.1.4.1.5962.1.4.4.1.20040826185059.5457
    ds.FrameOfReferenceUID = ''

    # (0020, 0060) Laterality                          CS: ''
    ds.Laterality = ''

    # (0020, 1040) Position Reference Indicator        LO: ''
    ds.PositionReferenceIndicator = ''

    # (0020, 1041) Slice Location                      DS: "0.0000"
    ds.SliceLocation = 0

    # (0020, 4000) Image Comments                      LT: 'Uncompressed'
    ds.ImageComments = 'cookie'

    # (0028, 0002) Samples per Pixel                   US: 1
    ds.SamplesPerPixel = 1

    # (0028, 0004) Photometric Interpretation          CS: 'MONOCHROME2'
    ds.PhotometricInterpretation = 'MONOCHROME2'

    # (0028, 0010) Rows                                US: 64
    ds.Rows = int(metadata.get('EXIF ExifImageLength',0))

    # (0028, 0011) Columns                             US: 64
    ds.Columns = int(metadata.get('EXIF ExifImageWidth',0))

    # (0028, 0030) Pixel Spacing                       DS: ['0.3125', '0.3125']
    ds.PixelSpacing = ''

    # (0028, 0100) Bits Allocated                      US: 16
    try:
        ds.BitsAllocated = int(metadata.get('EXIF CompressedBitsPerPixel',0))
    except:
        pass

    # (0028, 0101) Bits Stored                         US: 16
    try:
        ds.BitsStored = int(metadata.get('EXIF CompressedBitsPerPixel',0))
    except:
        pass

    # (0028, 0102) High Bit                            US: 15
    try:
        ds.HighBit = int(metadata.get('Image XResolution',0))
    except:
        pass

    # (0028, 0103) Pixel Representation                US: 1
    ds.PixelRepresentation = 1

    # (0028, 0106) Smallest Image Pixel Value          SS: 0
    ds.SmallestImagePixelValue = 0

    # (0028, 0107) Largest Image Pixel Value           SS: 4000
    ds.LargestImagePixelValue = 255

    # (0028, 1050) Window Center                       DS: "600"
    try:
        ds.WindowCenter = int(metadata.get('Image ExifOffset',0))
    except:
        pass

    # (0028, 1051) Window Width                        DS: "1600"
    try:
        ds.WindowWidth = int(metadata.get('EXIF ExifImageWidth',0))
    except:
        pass

    # (7fe0, 0010) Pixel Data                          OW: Array of 4330 bytes
    ds.PixelData = bytes(pixels)

    # (fffc, fffc) Data Set Trailing Padding           OB: Array of 126 bytes
    ds.DataSetTrailingPadding = trailing_padding()

    return ds 


def trailing_padding():
    return b'\n\x00\xfe\x00\x04\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x01\x00\x00\x00\x00\x02\x00\x00\x01\x01\x04\x00\x01\x00\x00\x00\x00\x02\x00\x00\x02\x01\x03\x00\x01\x00\x00\x00\x10\x00\x00\x00\x03\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x06\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x11\x01\x04\x00\x01\x00\x00\x00\xdc\x05\x00\x00\x15\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x16\x01\x04\x00\x01\x00\x00\x00\x00\x02\x00\x00\x17\x01\x04\x00\x01\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00'

