# Host Mobility platform poky

## Host Mobility Yocto/OE-core Setup

Fork of [fsl-community-bsp-platform](https://github.com/Freescale/fsl-community-bsp-platform -b dunfell/)

To simplify installation we provide a repo manifest which manages the different git repositories
and the used versions. (more on repo: http://code.google.com/p/git-repo/ )

Before proceeding take a look at [Yocto Manual - Build Host Packages](http://www.yoctoproject.org/docs/2.3/mega-manual/mega-manual.html#packages).

Install the repo bootstrap binary:

```
sudo apt-get install repo
or
mkdir ~/bin
PATH=~/bin:$PATH
curl http://commondatastorage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
```

##  Building in Docker

There is a script that uses Docker that builds this platform without needing to install Yocto building tools on the host.

Usage:
1. download [bid](scripts/bid) and [build_script_template](scripts/build_script_template) (template script that is run inside docker. copied to build-folder as ```build_script```)
2. Put these two files the same folder, the build folder or e.g. ```$HOME/.bin```

```bash
mkdir mybuild; cd mybuild; bid console-hostmobility-image 
```