from collections import defaultdict
import raylib as rl
import pyray

# References:
# https://en.wikipedia.org/wiki/Huffman_coding

#text = """In computer science and information theory, a Huffman code is a particular type of optimal prefix code that is commonly used for lossless data compression. The process of finding or using such a code is Huffman coding, an algorithm developed by David A. Huffman while he was a Sc.D. student at MIT, and published in the 1952 paper "A Method for the Construction of Minimum-Redundancy Codes".[1]
#
#The output from Huffman's algorithm can be viewed as a variable-length code table for encoding a source symbol (such as a character in a file). The algorithm derives this table from the estimated probability or frequency of occurrence (weight) for each possible value of the source symbol. As in other entropy encoding methods, more common symbols are generally represented using fewer bits than less common symbols. Huffman's method can be efficiently implemented, finding a code in time linear to the number of input weights if these weights are sorted.[2] However, although optimal among methods encoding symbols separately, Huffman coding is not always optimal among all compression methods - it is replaced with arithmetic coding[3] or asymmetric numeral systems[4] if a better compression ratio is required."""


text = 'A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED'
#text = "the quick brown fox jumped over the lazy dog."

freq_table = defaultdict(int)

class HTNode:

    def __init__(self, value, weight, leftNode = None, rightNode = None):
        self.value = value
        self.weight = weight
        self.leftNode = leftNode
        self.rightNode = rightNode

    def __str__(self):
        return f"<Node value={self.value}, weight={self.weight}>"

    def is_leaf(self):
        return self.leftNode is None and self.rightNode is None



def make_freq_table():
    for char in text:
        freq_table[char] += 1

def create_encoder_tree(sorted_items):
    nodeList = []
    for item in sorted_items:
        node = HTNode(value=item[0], weight=item[1])
        nodeList.append(node)

    while len(nodeList) > 1:
        n1 = nodeList.pop(0)
        n2 = nodeList.pop(0)

        newNode = HTNode( str(n1.value) + str(n2.value), n1.weight + n2.weight, n1, n2)
        nodeList.append(newNode)
        nodeList = sorted(nodeList, key=lambda node: node.weight)
    return nodeList

def print_tree(nodeList):
    if nodeList.leftNode is not None:
        print_tree(nodeList.leftNode)
    if nodeList.rightNode is not None:
        print_tree(nodeList.rightNode)
    print(nodeList)
    
def get_encoding(node, currPath, encoding_map):
    if node.is_leaf():
        #print(currPath + node.value)
        encoding_map[node.value] = currPath
        return
    else:
        get_encoding(node.rightNode, currPath + '1', encoding_map) 
        get_encoding(node.leftNode, currPath + "0", encoding_map)

def draw_node1(node:HTNode, x:int, y:int, depth, curr_level = 1, radius = 13):
    """Draw a node.

    Draw the node at position x, y
    """
    x_offset = radius+7
    font = rl.GetFontDefault()
    font_size = 20
    if node.is_leaf():
        rl.DrawCircle(x, y, radius, rl.BLACK);
        rl.DrawCircleLines(x, y, radius, rl.WHITE);
        text = node.value
        if text == '\n': text = '\\n'
        text = text.encode()
        text_dimensions = rl.MeasureTextEx(font, text, font_size, 0)
        rl.DrawText(text, x-int(text_dimensions.x/2), y - int(text_dimensions.y/2), font_size, rl.WHITE)
        
    else:
        rl.DrawCircle(x, y, 2, rl.WHITE)
   
    dx = 2**(depth - curr_level ) * x_offset

    if node.leftNode is not None:            
        rl.DrawLine(x, y, x - dx, y + 60, rl.WHITE)
        draw_node1(node.leftNode, x - dx, y+60, depth , curr_level+1)
    if node.rightNode is not None:
        rl.DrawLine(x, y, x + dx, y + 60, rl.WHITE)
        draw_node1(node.rightNode, x + dx, y+60, depth, curr_level + 1)

def draw_node(node, x, y, toggle):
    """Draw a node.

    Draw node at the x,y position given.
    The value of toggle is used to alternate the stroke length leading into the next nodes
    in an attempt to prevent overlap of nodes
    """
    font = rl.GetFontDefault()
    font_size = 20
    if node.is_leaf():
        rl.DrawCircle(x, y, 13, rl.BLACK);
        rl.DrawCircleLines(x, y, 13, rl.WHITE);
        text = node.value
        if text == '\n': text = '\\n'
        text = text.encode()
        text_dimensions = rl.MeasureTextEx(font, text, font_size, 0)
        rl.DrawText(text, x-int(text_dimensions.x/2), y - int(text_dimensions.y/2), font_size, rl.WHITE)
        
    else:
        rl.DrawCircle(x, y, 2, rl.WHITE);

    offsetx = 40
    offsety = 60

    if node.leftNode is not None:
        if node.leftNode.is_leaf() and toggle == 0:
            offsetx = 20
            offsety = 30
            
        rl.DrawLine(x, y, x - offsetx, y + offsety, rl.WHITE)
        draw_node(node.leftNode, x-offsetx, y+offsety, 1-toggle)
    if node.rightNode is not None:
        if node.rightNode.is_leaf() and toggle == 1:
            offsetx = 20
            offsety = 30
            

        rl.DrawLine(x, y, x+offsetx, y + offsety, rl.WHITE)
        draw_node(node.rightNode, x+offsetx, y+offsety, 1-toggle)
        

def decode_string(encoded_string, tree):
    """Decode the Huffman-encoded string using the given mapping tree."""
    output = ''
    curr_node = tree
    for c in encoded_string:
        if not curr_node.is_leaf():
            if c == '0':
                curr_node = curr_node.leftNode
                if curr_node.is_leaf():
                    output+=curr_node.value
                    curr_node = tree #reset
            else:
                curr_node = curr_node.rightNode
                if curr_node.is_leaf():
                    output+=curr_node.value
                    curr_node = tree #reset
            
    return output


def tree_depth(treenode: HTNode):
    if treenode.is_leaf():
        return 0
    else:
        return 1 +  max(tree_depth(treenode.leftNode),
                        tree_depth(treenode.rightNode))
    


    
            
def draw_tree(treeNode):
    """Draw a tree."""
    rl.SetTraceLogLevel(rl.LOG_ERROR)
    rl.SetTargetFPS(30)
    rl.InitWindow(2000, 1000, "Tree".encode())

    camera = pyray.Camera2D()
    camera.target = pyray.Vector2(1000, 500)
    camera.offset = pyray.Vector2(1000, 500)
    camera.zoom = 1.0
    camera.rotation = 0.0
    
    while (not rl.WindowShouldClose()):

        if rl.IsKeyPressed(rl.KEY_Q):
            break

        if rl.IsKeyDown(rl.KEY_F):
            camera.zoom += 0.02
        if rl.IsKeyDown(rl.KEY_V):
            camera.zoom -= 0.02

        if rl.IsKeyDown(rl.KEY_A):
            camera.target.x -= 20
            #camera.offset.y += 20

        if rl.IsKeyDown(rl.KEY_D):
            camera.target.x += 20
        if rl.IsKeyDown(rl.KEY_S):
            camera.target.y += 20
        if rl.IsKeyDown(rl.KEY_W):
            camera.target.y -= 20



            
        rl.BeginDrawing();
        rl.ClearBackground(rl.BLACK)
        rl.BeginMode2D(camera)
        draw_node1(treeNode, 1000, 100, tree_depth(treeNode))
        #draw_node(treeNode, 400, 100, 0)
        rl.EndMode2D()
        rl.EndDrawing();

    rl.CloseWindow()


if __name__ == "__main__":
    make_freq_table()
    sorted_items = sorted(freq_table.items(), key = lambda pair: pair[1])
    huffman_tree = create_encoder_tree(sorted_items)
    assert len(huffman_tree) == 1
    #print_tree(huffman_tree[0])
    encoding_map: dict[ str, str ] = {}
    get_encoding(huffman_tree[0], '', encoding_map)
    print(encoding_map)

    draw_tree(huffman_tree[0])
    encoded_string = ''
    for c in text:
        encoded_string += encoding_map[c]
    decoded_string = decode_string(encoded_string, huffman_tree[0])
    
    print(f"length of raw: {len(text)*8}; length of encoded: {len(encoded_string)}")
    #print(f"Encoded: {encoded_string}")
    print("\n\n\n")
    print(f"Decoded: {decoded_string}")

    print(f"Original text length: {len(text)} chars ({len(text)*8} bits)\n Encoded text length: "
          f"{len(encoded_string)} bits\n Decoded text length: {len(decoded_string)} chars")
    print(f"   Compression ratio: {len(encoded_string)*100 / (len(text) * 8):.2f} %")


