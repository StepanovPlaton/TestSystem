from typing import Any, Union

def DictToTree(SetOfObjects: Union[list[Any], dict[str, Any]], Indent: int =0, NewLine: bool =True) -> str:
    Tree: str = ""
    if(NewLine): Tree += "\n"
    if(type(SetOfObjects) is dict):
        for key in SetOfObjects.keys():
            Tree += (" "*Indent if NewLine else "") + key + ": "
            if(type(SetOfObjects[key]) is dict or type(SetOfObjects[key]) is list): 
                Tree += DictToTree(SetOfObjects[key], Indent+2)
            else:
                Tree += str(SetOfObjects[key]) + "\n"
    elif(type(SetOfObjects) is list):
        for Item in SetOfObjects:
            Tree += " "*Indent + "- "
            if(type(Item) is dict or type(Item) is list):
                Tree += DictToTree(Item, Indent, False)
            else:
                Tree += str(Item) + "\n"
    else: raise ValueError()
    return Tree