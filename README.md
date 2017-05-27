# Dicom Cookies!

[API Human Readable Base](https://pydicom.github.io/dicom-cookies)
[API Datasets Base](https://pydicom.github.io/dicom-cookies/datasets)
[API Images Base](https://pydicom.github.io/dicom-cookies/images)

This is a testing dataset of dicom files, actually images of cookies (and candy tumors) provided in Dicom Format with various metadata, the intention being that you can use this dataset to test your DICOM applications. The dataset is provided in the [Experiment Factory](https://www.github.com/expfactory-data/cookies) (static JSON API) standard, to make it servable from this static Github folder

## Dataset Generation
Generation of the dataset was done via the [create_dataset.py](scripts/create_dataset.py) script. The only dependency is [pydicom](https://pydicom.readthedocs.io).

## Cookies Dataset

This is an example dicom dataset that is being distributed by using the [JSON API](http://jsonapi.org/) specification. The entire thing is rendered statically using [Jekyll on Github Pages](https://help.github.com/articles/using-jekyll-as-a-static-site-generator-with-github-pages/).

## Where is the data?
The dataset can be viewed in entity on <a href="{{ site.github }}" target="_blank">Github</a>. 
Each dataset is a separate folder within `_datasets`, and this means that you can add a new dataset by simply adding a folder with the appropriate subfolders and metadata. 


### Dataset
A dataset folder includes top level files for metadata, images, and subfolders with the actual `images`. Texts are optional but not included in the cookies dataset. The organization might look like the following:

```
_datasets
   cookie-1
      images.txt
      images
          image1.txt
          image1/image1.jpg
```

In the above example, we have an entity named "cookie-1" with a metadata.txt file that will be rendered at the url `/datasets/cookie-1/metadata` as json, and this metadata file will have an `includes` section that will indicate if we have images and/or text, or neither, and then link to `/datasets/cookie-1/images` and/or `/datasets/cookie-1/texts`. Details about the metadata file, images and text files, are below. For the above, we should note that the folder name `cookie-1` is going to coincide with the `dataset-id`.


### Metadata
`metadata.txt` should be a text file located at the top level of the subject folder. Note that the `dataset-id` coincides with the folder name for the dataset. THe `metadata.txt` includes the fields specified in [meta.yml](https://www.github.com/expfactory-data/cookies/master/_data/meta.yml), organized according to being required or not. We can look at an example:

```
---
title: Cookie Tumor 1
type: entity
dataset-id: cookie-1
hidden: false

description: This is a cookie tumor. I am describing the cookie tumor!

license: This is a license for this dataset.

attributes:
  - cookie_type: sugar
  - cookie_age: 2
  - cookie_candy: m&ms

includes:
  - images
  - texts
---
```

Any features about the dataset should be put in the list of `attributes`. The `includes` section indicates that the entity has subfolders "images" and "texts," and an images.txt and texts.txt file to describe the contents.  This file could be very minimumal, and perhaps only have the following:

```
---
type: entity
dataset-id: cookie-1

includes:
  - images
---
```


### Images and Texts
Each of the images.txt and texts.txt file in a dataset folder simply need to have a list of the files that you want published, with type "images" for images, and "texts" for texts:

```
---
type: images
dataset-id: cookie-1

images:
  - image1
---
```

As a reminder, in the example above, we have a folder that looks like this, and we are viewing the images.txt file:

```
      images.txt
      images
          image1.txt
          image1/image1.jpg

```

Within the images folder, we should have an image1.txt file for each image that we want to serve, and include with this text file metadata (features or attributes) specified to the image:

```
---
type: image
dataset-id: image1

files:
  - image1.jpg

attributes:
  - EXIF SubjectDistance": 0
  - EXIF SceneType: 0
  - Image Resolution: 768/17
  - EXIF FlashEnergy: 1800
---
```

We also have added a list of files that are expected to be located within a subdirectory named by the image id, followed by the filename. In the example above, `image1.jpg` described in the file `images/image1.txt` would be located in `images/image1/image1.jpeg`.

#### Why do I have to list my files?
While these variables could be sniffied programmatically, it is important that you are able to include a data object in a repository, but turn it's "published" status on or off. If an image is not included in the list above, it will not be rendered in the json data structure for the API.

#### Why does each image need it's own text file?
The richness for data comes with it's metadata, meaning labels and attributes about the image. Thus, we want to represent this data on the same level as the image.
