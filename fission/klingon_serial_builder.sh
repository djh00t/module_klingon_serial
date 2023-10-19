#!/bin/bash
###
### Build Klingon Serial Package
###
# Set APP_NAME
APP_NAME="klingon_serial"

# Set APP_NAME_DASH with $APP_NAME, but replace underscores with dashes
APP_NAME_DASH=$(echo $APP_NAME | sed 's/_/-/g')

# Set Fission Environment Type
export FISSION_ENV="python"
export FISSION_ENV_POOL_SIZE=1
export FISSION_NAMESPACE="default"
export FISSION_ENV_IMAGE="fission/python-env"
export FISSION_ENV_BUILDER="fission/python-builder"

# Set kubeconfig
export KUBECONFIG=~/.kube/config

# Check if environment exists containing $FISSION_ENV_IMAGE and
# $FISSION_ENV_BUILDER if not, create it
if [[ $(fission env list --namespace="$FISSION_NAMESPACE"| grep $FISSION_ENV) ]]; then
    echo "Environment $FISSION_ENV already exists, skipping creation..."
else
    echo "Environment $FISSION_ENV does not exist, creating it..."
    fission env create --name="$FISSION_ENV" --image="$FISSION_ENV_IMAGE" --builder="$FISSION_ENV_BUILDER" --version 3 --poolsize="$FISSION_ENV_POOL_SIZE" --namespace="$FISSION_NAMESPACE"
fi

# Remove Old Package
rm -f $APP_NAME.zip

# Create New Package
zip -jr $APP_NAME.zip $APP_NAME

# Check if package already exists, if it does, update it otherwise create
if [[ $(fission package list | grep $APP_NAME_DASH) ]]; then
    echo "Package $APP_NAME_DASH already exists, updating it..."
    fission package update --name=$APP_NAME_DASH --sourcearchive=$APP_NAME.zip --env=$FISSION_ENV --namespace=$FISSION_NAMESPACE --buildcmd="./build.sh"
else
    # Publish Package
    echo "Package $APP_NAME_DASH does not exist, creating it..."
    fission package create --name=$APP_NAME_DASH --sourcearchive=$APP_NAME.zip --env=$FISSION_ENV --namespace=$FISSION_NAMESPACE --buildcmd="./build.sh"
fi

# Announce Package Name
echo "Package: $APP_NAME_DASH"

# Wait for Package to Build
# Run "fission pkg info --name $APP_NAME_DASH | grep Status | awk '{ print $2 }'"
# until it returns "succeeded" or "failed"
while :; do  # This creates an infinite loop
    STATUS=$(fission pkg info --name=$APP_NAME_DASH --namespace=$FISSION_NAMESPACE | grep Status | awk '{ print $2 }')
    
    if [[ $STATUS == "succeeded" ]]; then
        echo "Package build for $APP_NAME_DASH succeeded!"
        break  # Exit the loop if status is "succeeded"
    elif [[ $STATUS == "failed" ]]; then
        echo "Package build for $APP_NAME_DASH failed."

        # Remove the package
        fission package delete --name="$APP_NAME_DASH" --namespace=$FISSION_NAMESPACE

        # Exit the script with an error code if status is "failed"
        exit 1
    else
        echo "Waiting for package $APP_NAME_DASH to succeed... Current status: $STATUS"
        sleep 1  # Wait for 5 seconds before checking again
    fi
done

# Check if function already exists, if it does, update it otherwise create it
if [[ $(fission function list | grep $APP_NAME_DASH) ]]; then
    echo "Function $APP_NAME_DASH already exists, updating it..."
    fission function update --name="$APP_NAME_DASH" --pkg="$APP_NAME_DASH"  --namespace=$FISSION_NAMESPACE --concurrency=$FISSION_ENV_POOL_SIZE --env=python --entrypoint="app.main" # --executortype="poolmgr"
else
    echo "Function $APP_NAME_DASH does not exist, creating it..."
    # Create Function
    fission function create --name="$APP_NAME_DASH" --pkg="$APP_NAME_DASH"  --namespace=$FISSION_NAMESPACE --concurrency=$FISSION_ENV_POOL_SIZE --env=python --entrypoint="app.main" # --executortype="poolmgr"
fi

# Check if route exists, if not create it otherwise create it
if [[ $(fission route list | grep $APP_NAME_DASH) ]]; then
    echo "Route $APP_NAME_DASH already exists, updating it..."
    fission route update --name="$APP_NAME_DASH" --function="$APP_NAME_DASH" --url="/$APP_NAME_DASH" --method="GET" --createingress="true"
else
    # Create Route
    echo "Route $APP_NAME_DASH does not exist, creating it..."
    fission route create --name="$APP_NAME_DASH" --function="$APP_NAME_DASH" --url="/$APP_NAME_DASH" --method="GET" --createingress="true"
fi
