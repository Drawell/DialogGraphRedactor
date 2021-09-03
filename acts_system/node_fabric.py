from acts_system import Act
from node_system.node import Node


class NodeFabric:
    @staticmethod
    def add_node_to_scene(scene, class_name, x, y):
        act = scene.act
        for node_class_ in act.get_node_class_list():
            if node_class_.__name__ == class_name:
                node = Node(scene)
                node_content = node_class_(node)
                act.add_node(node_content)

                pos = scene.mouse_pos_to_view_pos(x, y)
                node.set_pos(pos.x(), pos.y())


