import pyblish.api

from maya import cmds


def get_all_parents(long_name):
    parents = long_name.split("|")[1:-1]
    return ['|{0}'.format('|'.join(parents[0:i+1]))
            for i in xrange(len(parents))]


@pyblish.api.log
class CollectModel(pyblish.api.Collector):
    """Inject all models from the scene into the context

    .. note:: Applicable in modeling workspace

    .. note:: This skips intermediate objects.

    """

    order = pyblish.api.Collector.order + 0.2
    hosts = ["maya"]

    def process(self, context):
        self.log.info("Selecting model..")

        # Check whether to select a model
        # -------------------------------
        # Ensure we're in the modeling context
        family_id = context.data('familyId')
        if not family_id or family_id != 'model':
            return

        missing_data = []

        root = context.data('root')
        if not root:
            self.log.error("Missing `root` data for asset...")
            missing_data.append('root')

        asset = context.data('asset')
        if not asset:
            self.log.error("Missing `asset` data for asset...")
            missing_data.append('asset')

        if missing_data:
            self.log.error("Asset data incomplete. Missing: {0}".format(missing_data))
            return

        # Scene Geometry
        # --------------
        # Get the root transform
        root_transform = cmds.ls('|{asset}_GRP'.format(asset=asset),
                                 objectsOnly=True, type='transform')
        if not root_transform:
            return
        else:
            root_transform = root_transform[0]

        # Get all children shapes
        # (because we're modeling we only care about shapes)
        shapes = cmds.ls(root_transform, dag=True,
                         shapes=True, long=True,
                         noIntermediate=True)
        if not shapes:
            return

        # The nodes we want are the shape nodes including all
        # their parents. So let's get them.
        nodes = set()
        nodes.update(shapes)
        for shape in shapes:
            nodes.update(get_all_parents(shape))

        # Create Asset
        # ------------
        instance = context.create_instance(name=asset,
                                           familyId=family_id,
                                           family='model')
        for node in nodes:
            instance.add(node)

        # Set instance pipeline data
        instance.set_data("root", root)
        instance.set_data("workFile", context.data('workFile'))
        instance.set_data("asset", asset)
