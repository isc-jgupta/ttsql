#ARG IRIS_BASE_IMAGE
FROM containers.intersystems.com/iscinternal/sds/base_iris:1.20.10

ARG DEV_MODE_ARG
ENV TV_INSTALL_FILES=/intersystems/install_files
# Adding source code that will be loaded by the installer
ADD --chown=irisowner:irisuser ./${IRIS_PROJECT_FOLDER_NAME}/ $IRIS_APP_SOURCEDIR
ADD --chown=irisowner:irisowner ./data $TV_INSTALL_FILES/data
# Running the installer. This will load the source code and clean up the image
RUN /sds/iris-installer.sh "UseDevMode"

# Declare that the build process is complete (for ZSTU)
RUN touch done