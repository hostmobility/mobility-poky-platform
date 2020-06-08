# mx5-platform

Temporary manifest location for mx5

# Host Mobility Yocto/OE-core Setup

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

