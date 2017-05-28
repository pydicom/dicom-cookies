# Dicom Cookies!

- [API Human Readable Base](https://pydicom.github.io/dicom-cookies)
- [API Datasets Base](https://pydicom.github.io/dicom-cookies/datasets)
- [API Images Base](https://pydicom.github.io/dicom-cookies/images)

This is a testing dataset of dicom files, actually images of cookies (and candy tumors) provided in Dicom Format with various metadata, the intention being that you can use this dataset to test your DICOM applications. The dataset is provided in the [Experiment Factory](https://www.github.com/expfactory-data/cookies) standard, using the [JSON API](http://jsonapi.org/) specification to make it servable from this static Github folder The general goal of this simple framework is to make it possible for anyone, with little programming experience, to put images and associated in metadata, push them to Github, and have them programatically accessible. The entire thing is rendered statically using [Jekyll on Github Pages](https://help.github.com/articles/using-jekyll-as-a-static-site-generator-with-github-pages/).

## Where is the data?
The dataset can be viewed in entity on <a href="{{ site.github }}" target="_blank">Github</a>. 
Each dataset is a separate folder within `_datasets`, and this means that you can add a new dataset by simply adding a folder with the appropriate subfolders and metadata. 

## How can I share my own data?
You can easily create your own programatically accessible data by doing the following:

 1. use this repo as a template, and clear out the `_datasets` folder, replacing with your data with the structure (outlined below).
 2. push to the `gh-pages` branch of a repo. If your github username is `pydicom`, and the repo is called `dicom-cookies`, this means that the Github Pages branch is deployed at [https://pydicom.github.io/dicom-cookies].
    - The "human friendly" version of will be at [https://pydicom.github.io/dicom-cookies](https://pydicom.github.io/dicom-cookies).
    - The general datasets endpoint can be found at [https://pydicom.github.io/dicom-cookies/datasets](https://pydicom.github.io/dicom-cookies/datasets).
    - A filtered version for each of [images](https://pydicom.github.io/dicom-cookies/images) and (if defined) [texts](https://pydicom.github.io/dicom-cookies/texts) is also available.


## How do I query it?
A complete example of how you might programatically access your data is provided in [get_datasets.py](scripts/get_datasets.py), and outlined here. The general steps are as follows:

 - Give the repository unique resource identifier (uri) to the application.
 - optionally specify images, texts

In the example provided, the tool defaults to this repo, so you don't need to specify anything at all, other than your preference for downloading datasets, or images. But also for this application, the only datasets that we have are images, so the two functionalities return the same thing. Let's take a look at how this might work, [or just watch here](https://asciinema.org/a/122503?speed=3).

[![asciicast](https://asciinema.org/a/122503.png)](https://asciinema.org/a/122503?speed=3)

```bash
wget https://raw.githubusercontent.com/pydicom/dicom-cookies/master/scripts/get_datasets.py

python get_datasets.py

usage: get_datasets.py [-h] [--output OUTPUT] [--images] [--show] [--uri URI]

download and query data from your json dataset API.

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  a folder to save output files to.
  --images         download images
  --show           print the json data structure of the endpoint to the screen
  --uri URI        the github repo username/reponame

Specify to download data with --output or just print to screen with --show
```
Cool! So the tool wants an output directory, or for us to specify it to just print json to the screen. The first thing we could do is print to the screen, like this:


```
python get_datasets.py --show
```

or we could pipe it into a file:

```
python get_datasets.py --show >> dicom-cookies.json
```

But we probably want to get the data! Here is how to do that.

```
# Here is an output directory
mkdir /home/vanessa/Desktop/cookies
python get_datasets.py --output /home/vanessa/Desktop/cookies
```

And our datasets are downloaded!


## Dataset Generation
Generation of the dataset was done via the [create_dataset.py](scripts/create_dataset.py) script. The only dependency is [pydicom](https://pydicom.readthedocs.io).


### How is it structured?
A dataset folder includes top level files for metadata, images, and subfolders with the actual `images`. Texts are optional but not included in the cookies dataset. The organization might look like the following:

```
_datasets
   cookie-1
      images.txt
      images
          image1.dcm
          image2.dcm
```

In the above example, we have an entity named "cookie-1" with a metadata.txt file that will be rendered at the url `/datasets/cookie-1/metadata` as json, and this metadata file will have an `includes` section that will indicate if we have images and/or text, or neither, and then link to `/datasets/cookie-1/images` and/or `/datasets/cookie-1/texts`. Details about the metadata file, images and text files, are below. For the above, we should note that the folder name `cookie-1` is going to coincide with the `dataset-id`.


### Metadata
`metadata.txt` should be a text file located at the top level of the subject folder. Note that the `dataset-id` coincides with the folder name for the dataset. THe `metadata.txt` includes the fields specified in [meta.yml](https://www.github.com/expfactory-data/cookies/master/_data/meta.yml), organized according to being required or not. We can look at a minimal example:

```
---
type: entity
dataset-id: cookie-1

includes:
  - images
---
```

Features about the dataset can be put in the list of `attributes`, although in our case, we are including them with the dicom files:

```
attributes:
  - color: red
  - flavor: chocolate
```

The `includes` section indicates that the entity has subfolders "images"," and an images.txt is also present to describe the contents.  


### Images and Texts
Each of the images.txt and texts.txt file in a dataset folder simply need to have a list of the files that you want published, with type "images" for images, and "texts" for texts:

```
---
type: images
dataset-id: cookie-1

images:
  - image1.dcm
  - image2.dcm
---
```

As a reminder, in the example above, we have a folder that looks like this, and we are viewing the images.txt file:

```
   cookie-1
      images.txt
      images
          image1.dcm
          image2.dcm
```

#### Why do I have to list my files?
While these variables could be sniffied programmatically, it is important that you are able to include a data object in a repository, but turn it's "published" status on or off. If an image is not included in the list above, it will not be rendered in the json data structure for the API.
