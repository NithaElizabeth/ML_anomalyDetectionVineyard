<br />
<p align="center">
    <!--- relative path means image/image.png instead of https://etc... -->
    <!--<img src="img/follow_leader.gif" alt="Logo" width="700" height="463"> -->                        
</a>

  <h2 align="center">treecounter-ML</h2>

  <p align="center">
    An application that detects and tracks the trees, wooden posts, and metal posts in a given input video. Makes use of <a href="https://github.com/AlexeyAB/darknet">darknet</a> and <a href="https://www.opencv.org">OpenCV</a>.
    <br />
    <a href="https://github.com/software3daerospace/treecounter-ML/tree/main/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/software3daerospace/treecounter-ML/blob/fix-tracks/docs/imgs/results.gif">View Demo</a>
    ·
    <a href="https://github.com/software3daerospace/treecounter-ML/issues/">Report Bug</a>
    ·
    <a href="https://github.com/software3daerospace/treecounter-ML/issues/">Request Feature</a> 
  </p>
</p>

## Table of Contents

* [Setup](#setup)
* [Run](#run)
* [Roadmap](#roadmap)
* [Maintainer Information](#maintainer)

## Setup

1. (Optional) Click on `Fork`
1. Clone the project on your local machine : `git clone https://github.com/software3daerospace/treecounter-ML.git`
3. Upgrade your installation of pip: `python3 -m pip install --upgrade pip`
4. Install dependencies: `python3 -m pip install -r requirements.txt`

## Run

 1. Store the model files in the `models` directory. You can find the Pre-trained models in the [releases](https://github.com/software3daerospace/treecounter-ML/releases) section. Be sure to use the latest release.
 1. Create a `logs` directory to store the logs for each run.
 1. The default configurations of the model are stored in the file [config.json](https://github.com/software3daerospace/treecounter-ML/blob/updated-tracks/data/config.json). You can edit the default configurations according to your requirements.
 1. You can run the tracking on an input video by using the following command:

```shell
$ python3 track_video.py
```

## Roadmap

See the [open issues](https://github.com/software3daerospace/treecounter-ML/issues) for a list of proposed features (and known issues).



[contributors-shield]: https://img.shields.io/github/contributors/master-coro/follow_leader.svg?style=flat-square
[contributors-url]: https://github.com/master-coro/follow_leader/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/master-coro/follow_leader.svg?style=flat-square
[forks-url]: https://github.com/master-coro/follow_leader/network/members
[stars-shield]: https://img.shields.io/github/stars/master-coro/follow_leader.svg?style=flat-square
[stars-url]: https://github.com/master-coro/follow_leader/stargazers
[issues-shield]: https://img.shields.io/github/issues/master-coro/follow_leader.svg?style=flat-square
[issues-url]: https://github.com/master-coro/follow_leader/issues
