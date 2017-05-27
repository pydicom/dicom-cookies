# Dicom Cookies!

- [API Human Readable Base](https://pydicom.github.io/dicom-cookies)
- [API Datasets Base](https://pydicom.github.io/dicom-cookies/datasets)
- [API Images Base](https://pydicom.github.io/dicom-cookies/images)

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
