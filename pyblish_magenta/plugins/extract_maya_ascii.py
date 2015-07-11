# stdlib
import os

# maya & pyblish lib
import pyblish.api
import pyblish_maya

# local lib
import pyblish_magenta.plugin


@pyblish.api.log
class ExtractMayaAscii(pyblish_magenta.plugin.Extractor):
    """Extract model as Maya Ascii"""

    label = "Maya Ascii"
    hosts = ["maya"]
    families = ["model", "rig"]
    optional = True

    def process(self, instance):
        from maya import cmds

        # Define extract output file path
        dir_path = self.temp_dir(instance)
        filename = "{0}.ma".format(instance.name)
        path = os.path.join(dir_path, filename)

        # Perform extraction
        self.log.info("Performing extraction..")
        with pyblish_maya.maintained_selection():
            cmds.select(instance, noExpand=True)
            cmds.file(path,
                      force=True,
                      typ="mayaAscii",
                      exportSelected=True,
                      constructionHistory=False)

        self.log.info("Extracted instance '{0}' to: {1}".format(
            instance.name, path))