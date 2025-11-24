class AVLNode:
    def __init__(self, key, row):
        self.key = key
        self.row = row
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, node, key, row):
        # 1. BST insert
        if not node:
            return AVLNode(key, row)
        if key < node.key:
            node.left = self.insert(node.left, key, row)
        elif key > node.key:
            node.right = self.insert(node.right, key, row)
        else:
            # key đã tồn tại -> không chèn nữa
            return node

        # 2. cập nhật height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # 3. kiểm tra balance
        balance = self.get_balance(node)

        # 4. cân bằng (4 trường hợp)
        # LL
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        # RR
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        # LR
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # RL
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, root, key):
        # 1. BST delete
        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # node có 1 hoặc 0 con
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            # node có 2 con
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.row = temp.row
            root.right = self.delete(root.right, temp.key)

        if not root:
            return root

        # 2. cập nhật height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. kiểm tra balance
        balance = self.get_balance(root)

        # 4. cân bằng
        # LL
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        # LR
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        # RR
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        # RL
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def inorder(self, node, res):
        if node:
            self.inorder(node.left, res)
            res.append(str(node.key))
            self.inorder(node.right, res)

    def preorder(node, self, res):
        if node:
            res.append(str(node.key))
            self.preorder(node.left, res)
            self.preorder(node.right, res)

    def postorder(self, node, res):
        if node:
            self.postorder(node.left, res)
            self.postorder(node.right, res)
            res.append(str(node.key))

    def count_leaves(self, node):
        if not node:
            return 0
        if not node.left and not node.right:
            return 1
        return self.count_leaves(node.left) + self.count_leaves(node.right)

    def count_left_leaves(self, root):
        if not root or not root.left:
            return 0
        return self.count_leaves(root.left)

def count_right_leaves(self, root):
    if not root or not root.right:
        return 0
    return self.count_leaves(root.right)


