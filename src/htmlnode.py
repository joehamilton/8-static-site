from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None,children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("TBC")
    def props_to_html(self):    
        if self.props is None:
            return ""
        # functional programming version
        return reduce(lambda acc, kv: acc + f' {kv[0]}="{kv[1]}"', self.props.items(),"")
        # more readible version
        # props_html = ""
        # for prop in self.props:
        #     props_html += f' {prop}="{self.props[prop]}"'
        # return props_html
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        self.tag = tag
        self.value = value
        self.props = props
        super().__init__(self.tag,self.value,None,self.props)
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props
    def to_html(self):
        if not self.tag:
            raise ValueError("Needs tag")
        if not self.children:
            raise ValueError("Needs children")
        leaves = reduce(lambda acc,child_leaf: acc + child_leaf.to_html(), self.children,"")
        return f'<{self.tag}{self.props_to_html()}>{leaves}</{self.tag}>'
        
