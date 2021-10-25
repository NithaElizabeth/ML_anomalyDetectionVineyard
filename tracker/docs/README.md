
<br />
<p align="center">
    <!--- relative path means image/image.png instead of https://etc... -->
    <!--<img src="img/follow_leader.gif" alt="Logo" width="700" height="463"> -->                        
</a>

  <h1 align="center">Guidelines for publishing Releases</h1>

  <p align="center">
    Since the model sizes are too large to be put on the core repository, we include the model files as <a href url="https://github.com/software3daerospace/treecounter-ML/releases">releases</a>. This helps us to get to testing the application quicker. This document will present a set of guidelines and general format of publishing the models as a new release. 
  </p>
</p>

---

## Generating the model files

Take the `models` directory from the local repository and zip it into a file called `model.zip`. This directory should contain the files as per the following structure:

```bash
.                                                                                                                       └── yolov4                                                                                                                  ├── class-names.json                                                                                                    ├── classes-3.names                                                                                                     ├── yolov4-custom.cfg                                                                                                   ├── yolov4-custom_4000.weights                                                                                          ├── yolov4-custom_final.weights                                                                                         └── yolov4-custom_last.weights
```

The `.weights` file might change depending on the current model being used. 

---

## Drafting a new release

Now that you have your `models.zip` file generated, you would want to go to the [releases](https://github.com/software3daerospace/treecounter-ML/releases) section on GitHub, and select the option __Draft a New Release__. This will open up a page as shown below:

<p align="center">
    <img src="https://github.com/software3daerospace/treecounter-ML/blob/fix-tracks/docs/imgs/release-page.png" alt="GitHub Draft a New Release" width="948" height="486"> 
</p>

Add the version number of the release, following the trend of the past releases. Be sure to tag it against the branch you want to publish the release for. You can read more about semantic versioning at https://semver.org/.

Set the title as `Pre-trained Model <date> `

In the Description of the release, include information about the date the model was generated, the instructions to import the model onto the local clone, and report the validation results of the model by running the `./darknet map ... ... ...` on the local repository.

A barebones model of the Description is provided below:

```md
## Pre-trained model generated on <date>

Include general comments on the model and the dataset here *(dataset size, test/train split ratio, etc.)*

## Usage

- Download the `models.zip` file from the release.
- Extract the contents into the `models` directory
- Run the application: `python3 ./track_video.py`

## Validation Results(mAP)

Class | Average Precision 
----- | -----------------
tree  | 01.23
wooden post | 45.67
metal post | 89.10


Run the validation test on the local repository and paste the contents here.
```

## Publishing the Release

The final step is to publish the release with the model. Once you have provided the description, you can move ahead and attach the `models.zip` file along with your release by dragging and dropping the zip file in the section called **Attach binaries** and select **Publish release** as shown below:

<p align="center">
    <img src="https://github.com/software3daerospace/treecounter-ML/blob/fix-tracks/docs/imgs/release-publish.png" alt="Attach Binary and Publish" width="1034" height="480"> 
</p>