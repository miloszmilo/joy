class NodeAbstractSyntax:
    def __init__(
        self,
        value: str = "",
    ):
        self.value = value
        self.left_child = None
        self.right_child = None

    def insert_left_child(self, left_child):
        self.left_child: NodeAbstractSyntax | None = left_child

    def insert_right_child(self, right_child):
        self.right_child: NodeAbstractSyntax | None = right_child
