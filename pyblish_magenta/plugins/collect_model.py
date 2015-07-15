import os
import pyblish.api
import pyblish_maya


@pyblish.api.log
class CollectModel(pyblish.api.Collector):
    """Inject all models from the scene into the context"""

    def process(self, context):
        from maya import cmds

        if not os.environ["TASK"] == "modeling":
            return self.log.info("No model found")

        name = os.environ["ITEM"]

        # Get the root transform
        self.log.info("Model found: %s" % name)
        assembly = "|%s_GRP" % name

        assert cmds.objExists(assembly), (
            "Model did not have an appropriate assembly: %s" % assembly)

        self.log.info("Capturing instance contents: %s" % assembly)
        nodes = self.ls(assembly)

        self.log.info("Reducing nodes to shapes only")
        shapes = cmds.ls(nodes,
                         noIntermediate=True,
                         exactType="mesh",
                         long=True,
                         dag=True)

        assert shapes, "Model did not have any shapes"

        instance = context.create_instance(name=name, family="model")
        instance[:] = self.ls(shapes)

        self.log.info("Successfully collected %s" % name)

    def ls(self, objects):
        from maya import cmds
        with pyblish_maya.maintained_selection():
            cmds.select(objects)
            nodes = cmds.file(exportSelected=True,
                              preview=True,
                              constructionHistory=True,
                              force=True)
            return cmds.ls(nodes, long=True)
