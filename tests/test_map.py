from map import Map
import tempfile
import os

def test_read_map_file() -> None:
    test_map = Map()
    test_file_name : str
    read_ok:bool
    
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as test_file:
        test_file.writelines([
            "width: 5\r", 
            "height: 4\r",
            "next-map: testmap.txt\r"  
            "---\r",
            "---------------\r",
            "=======\r",
            "ooooooo\r",
            "S------\r",
            "-------------\r",
            "Should not be in file\r"
        ])
        test_file_name = test_file.name
        
    try:
        with open(test_file_name, mode="r") as file:
            read_ok = test_map.ReadFile(file)
    finally:
        os.remove(test_file_name)

    assert(read_ok)
    assert(test_map.config["width"]==5)
    assert(test_map.config["height"]==4)
    assert(test_map.config["next-map"]=="testmap.txt")
    assert(test_map.MapString==["-----","=====","ooooo","S----"])

def test_read_weird_map_files() -> None:
    test_map = Map()
    test_file_name : str
    read_ok:bool
    
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as test_file:
        test_file.writelines([
            "width: 10\r", 
            "height: 0\r",  
            "---\r",
            "Should not be in file\r"
        ])
        test_file_name = test_file.name
        
    try:
        with open(test_file_name, mode="r") as file:
            read_ok = test_map.ReadFile(file)
    finally:
        os.remove(test_file_name)
    
    assert(len(test_map.MapString)==0)
    assert(read_ok)

    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as test_file:
        test_file.writelines([
            "width: 0\r", 
            "height: 1\r",  
            "---\r",
            "------\r"
        ])
        test_file_name = test_file.name
        
    try:
        with open(test_file_name, mode="r") as file:
            read_ok = test_map.ReadFile(file)
    finally:
        os.remove(test_file_name)

    assert(len(test_map.MapString[0])==0)
    assert(read_ok)

def test_read_wrong_file_format() -> None:
    test_map = Map()
    test_file_name : str
    read_ok:bool
    
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as test_file:
        test_file.writelines([
            "width: a\r", 
            "height: 1\r", 
            "---\r",
            "-------\r"
        ])
        test_file_name = test_file.name
        
    try:
        with open(test_file_name, mode="r") as file:
            read_ok = test_map.ReadFile(file)
    finally:
        os.remove(test_file_name)

    assert(read_ok==False)

    test_map=Map()
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as test_file:
        test_file.writelines([
            "witdh: 1\r", # dyslexia warning : "dt" is swapped (as a test)
            "height: 1\r", 
            "---\r",
            "-------\r"
        ])
        test_file_name = test_file.name
        
    try:
        with open(test_file_name, mode="r") as file:
            read_ok = test_map.ReadFile(file)
    finally:
        os.remove(test_file_name)

    assert(read_ok==False)

    test_map = Map()
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as test_file:
        test_file.writelines([
            "width: a\r", 
            "height: 1\r", 
            "---\r", 
            "-------\r"
        ])
        test_file_name = test_file.name
        
    try:
        with open(test_file_name, mode="r") as file:
            read_ok = test_map.ReadFile(file)
    finally:
        os.remove(test_file_name)

    assert(read_ok==False)

def test_find_element() -> None:
    test_map = Map()
    test_file_name : str
    
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as test_file:
        test_file.writelines([
            "width: 10\r", 
            "height: 10\r",
            "next-map: testmap.txt\r"  
            "---\r",
            "----------\r",
            "----------\r",
            "----------\r",
            "----------\r",
            "----------\r",
            "----v-----\r",
            "----S-----\r",
            "x---x-----\r",
            "=---=----o\r",
            "=---=----o\r"
        ])
        test_file_name = test_file.name
        
    try:
        with open(test_file_name, mode="r") as file:
            test_map.ReadFile(file)
    finally:
        os.remove(test_file_name)

    assert(test_map.FindElement("=")==[(1,0),(1,4),(0,0),(0,4)])
    assert(test_map.FindElement("x")==[(2,0),(2,4)])
    assert(test_map.FindElement("o")==[(1,9),(0,9)])
    assert(test_map.FindElement("S")==[(3,4)])
    assert(test_map.FindElement("v")==[(4,4)])
