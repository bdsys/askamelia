# Manual packager script
#/bin/bash
echo "Removing stale deployment assets..."
rm -r deployment-assets/central-processor
#
echo "Staging deployment package dependencies..."
cp -r lambda-assets/package deployment-assets/central-processor
#
echo "Staging deployment package source code..."
cp lambda-assets/central-processor/handler.py deployment-assets/central-processor
#
echo "Changing permissions on staged deployment packages..."
chmod -R 755 deployment-assets/central-processor
#
echo "Creating zipped deployment packages..."
echo "Creating central-processor.zip A and B packages..."
cd deployment-assets/central-processor
zip -r central-processor.zip *
cp central-processor.zip central-processor-a.zip
cp central-processor.zip central-processor-b.zip
rm central-processor.zip
cd ../..
echo "Done!"
#
echo "Packager is finished!"

# Put required packages into "package" folder
# cp -r ~/.virtualenvs/gbaas-central-service/lib/python3.8/site-packages/<package name> package
# E.g -- cp -r ~/.virtualenvs/gbaas-central-service/lib/python3.8/site-packages/pyasn1 package
