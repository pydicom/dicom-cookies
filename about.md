---
layout: default
permalink: /about/
title: "About this dataset"
---

This is an example dicom dataset that is being distributed by using the [JSON API](http://jsonapi.org/) specification. The entire thing is rendered statically using [Jekyll on Github Pages](https://help.github.com/articles/using-jekyll-as-a-static-site-generator-with-github-pages/).

## How do I use this?
You can parse the entire dataset programatically by starting at the base [datasets json]({{ site.url }}/datasets). If the dataset had text objects (which it doesn't, the metadata about images is stored in the dicom headers) you could filter to just images by going to the [images json]({{ site.url }}/images). If you go to the [texts json]({{ site.url }}/texts) you will see that it is empty. Sorry, we don't have any!

## Where is the data?
The dataset can be viewed in entirety on [Github]({{ site.repo }}). 
Each dataset is a separate folder within `_datasets`, and this means that you can add a new dataset by simply adding a folder with the appropriate subfolders and metadata. 

### Dataset
A dataset folder includes top level files for metadata, and images. The organization might look like the following:

```
_datasets
   cookie-1
      metadata.txt
      images.txt
      images
          image1.dcm
          image2.dcm
```

In the above example, we have an entity named "cookie-1" with a metadata.txt file that will be rendered at the url `/datasets/cookie-1/metadata` as json, and this metadata file will have an `includes` section that will indicate if we have images and/or text, or neither, and then link to `/datasets/cookie-1/images` and/or `/datasets/cookie-1/texts`. Details about the metadata file, images and text files, are below. For the above, we should note that the folder name `cookie-1` is going to coincide with the `dataset-id`. This is whatever standard unique ID schema you are using for your dataset.

### Metadata
`metadata.txt` should be a text file located at the top level of the subject folder. Note that the `dataset-id` coincides with the folder name for the dataset. The `metadata.txt` includes the fields specified in [meta.yml](https://github.com/expfactory-data/cookies/blob/master/_data/meta.yml), organized according to being required or not. The minimal requirements are the following:

```
---
type: entity
dataset-id: "cookie-2"
hidden: false

includes:
  - images
---
```

Any features about the dataset can be put in the list of `attributes`:

```
attributes:
  - color: red
  - flavor: chocolate
```

But we haven't done that here, because most that is needed is in the dicom headers. The `includes` section indicates that the entity has subfolders "images" and if you had texts, you would add "texts." There should be an images.txt and texts.txt file to describe the contents for each that you've decided to include.


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
images.txt
images
     image1.dcm
     image2.dcm
```


#### Why do I have to list my files?
While these variables could be sniffied programmatically, it is important that you are able to include a data object in a repository, but turn it's "published" status on or off. If an image is not included in the list above, it will not be rendered in the json data structure for the API.
