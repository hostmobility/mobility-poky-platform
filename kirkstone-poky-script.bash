#!/bin/bash -x -e

export PLATFORM_BRANCH="hmx-mickledore"
export MANIFEST_BASE=kirkstone
export DISTRO=poky
export MACHINES="\
  imx8mp-var-dart-hmx1 \
  mx4-c61 \
"
export IMAGES=meta-hostmobility-image
export TARGET_IMAGE="console-hostmobility-image"
export DL_DIR=/media/storage_hdd/YOCTO_DOWNLOADS
export DIR_WORK=${PWD}/${MANIFEST_BASE}

git checkout ${PLATFORM_BRANCH}

# BITBAKE! TODO If manifest name is changed from kirkstone.xml, change it below too TODO
# TEMPORARY CHANGE remote -s , TODO: CHANGE BACK
for MACHINE in $MACHINES; do
  bygg_args="\
    --delete-conf \
    --build-tag $BUILD_TAG \
    --manifest-file ${MANIFEST_BASE}.xml \
    --distro ${DISTRO} \
    --machine $MACHINE"
  
  scripts/bygg $bygg_args --repo-sync -- echo 'Repo sync done'
  ## START AFTER SYNC SPECIAL BUILD INSTRUCTIONS TESTING ONLY
  # (HEAD -> remove-meta-varscite-sdk)
  # commit b33c5864626b1eae7ff89f135281143024e88e45
  git -C $MANIFEST_BASE/sources/meta-mobility-poky-distro checkout b33c5864626b1eae7ff89f135281143024e88e45
  
  ## END   AFTER SYNC SPECIAL BUILD INSTRUCTIONS TESTING ONLY
  
  scripts/bygg $bygg_args -- bitbake console-hostmobility-image
  
  # If machine does not start with mx4, we skip the deploy script 
  if [[ ! $MACHINE =~ ^mx4- ]]; then
    continue
  fi

# SCRIPT RUN INSIDE DEPLOY DOCKER BELOW

cat >${DIR_WORK}/build_mx4-v2.sh <<'EOF'
#!/bin/bash -e
echo "Start build make_system.sh deploy only!"

cd mx4-deploy
# Clean up old directories. make_system.sh requires it!
sudo rm -rf deploy-*

DEPLOY_DIR=../build/tmp/deploy/images/$MACHINE

# Strip mx4- to get short machine
# Special case for c61-rio where we want to present machine as a c61 in u-boot
# script to be able to change between the machines on the same hardware.
if [[ "$MACHINE" == "mx4-c61-rio" ]]; then 
  SHORT_MACHINE="c61"; 
else 
  SHORT_MACHINE="${MACHINE:4}"
fi
./make_system.sh \
  -t $SHORT_MACHINE \
  -r $DEPLOY_DIR/${TARGET_IMAGE}-$MACHINE.tar.xz \
  -k $DEPLOY_DIR/uImage \

EOF

chmod +x ${DIR_WORK}/build_mx4-v2.sh

docker run --name docker_$JOB_BASE_NAME --rm --privileged \
    --workdir="${DIR_WORK}" \
    -v $DIR_WORK:$DIR_WORK \
    -e MACHINE \
    -e TARGET_IMAGE \
    -e BUILD_TAG \
    hostmobility/buildplatform-mx4:2.0 \
    ${DIR_WORK}/build_mx4-v2.sh
# Next machine
done
