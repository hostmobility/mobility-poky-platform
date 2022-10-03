# Host Mobility platform poky

# Host Mobility Yocto/OE-core Setup
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

Create a directory for your `mobility-bsp-platform` setup to live in and clone the meta information.
```
mkdir mobility-bsp-platform
cd mobility-bsp-platform
repo init -u https://github.com/hostmobility/mobility-poky-platform -b master
repo init -m kirkstone-next.xml
repo sync --force-sync
```

Setup build environment.
```
export DIR_WORK=$PWD/../
export BUILD_TAG=*yourTag*
export PLATFORM_VERSION="$(git -C $DIR_WORK.repo/manifests rev-parse --short HEAD)"
export PLATFORM_VERSION_DETAILS="$(repo forall -c 'echo $REPO_PATH\nLREV: $REPO_LREV\nRREV: $REPO_RREV; git diff --stat -b $REPO_LREV..HEAD ; echo -n "Commit: " ; git rev-parse HEAD ; echo -n "Uncommited changes: " ; git status -b -s ; git diff --stat -b ; echo ')"
echo "building with repo versions: $PLATFORM_VERSION"
export BB_ENV_PASSTHROUGH_ADDITIONS="$BB_ENV_PASSTHROUGH_ADDITIONS BUILD_TAG PLATFORM_VERSION PLATFORM_VERSION_DETAILS" 
export TEMPLATECONF=$PWD/../sources/meta-mobility-poky-distro/conf
```
**NOTE!** You need to run the above command on each new session. If you all ready have an build directory it will be un-touched and only environment will be setup.

Start baking!
```
$ source sources/poky/oe-init-build-env build;
$ bitbake console-mobility-image
or
$ bitbake mobility-image
or
$ bitbake mobility-image-chromium
```

Build result will end up in `mobility-bsp-platform/build/tmp/deploy/images/` directory.

Flash MxV with USB memory stick
```
copy and rename 'mobility-image-***.wic.gz' to mx5-image.wic.gz.
copy flashmx5.scr to USB memory.
plug in to USB port.
push reset button for 1 sec.
wait(1-2min)
when finished func led will blink green.
##  Building in Docker

There is a script that uses Docker that builds this platform without needing to install Yocto building tools on the host.

Usage:
1. download [bid](scripts/bid) and [build_script_template](scripts/build_script_template) (template script that is run inside docker. copied to build-folder as ```build_script```)
2. Put these two files the same folder, the build folder or e.g. ```$HOME/.bin```

```bash
mkdir mybuild; cd mybuild; bid console-hostmobility-image 
```