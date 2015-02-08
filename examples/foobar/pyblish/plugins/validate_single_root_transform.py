import pyblish.api
from maya import cmds


def getRootNode(longPath):
    return '|' + longPath.lstrip('|').split("|", 1)[0]


class ValidateSingleRootTransform(pyblish.api.Validator):
    """ Validate all nodes are in a single root """
    families = ['rig', 'model']
    hosts = ['maya']
    category = 'rig'
    version = (0, 1, 0)

    def process_instance(self, instance):
        """Process all the nodes in the instance """
        # ensure long names so we can get root by strings (fastest way?)
        member_nodes_paths = cmds.ls(instance, type='dagNode', long=True)

        roots = set()
        for node in member_nodes_paths:
            root = getRootNode(node)
            roots.add(root)

        if len(roots) > 1:
            raise ValueError("Multiple root nodes found named shapes found: {0}".format(list(roots)))