# pymove

pmove is just a script to batch rename files using Regex.

```
usage: pmove.py [-h] [-fp [FOLDER_PATH]] [-csv [CSV_LIST_FILE]]
                        [-seq SEQUENCE [SEQUENCE ...]] [-v] [-c]

Use pmove -h for more details

For positional arguments substitution use: \number instead of $number
```

## Replacement:

```pmove "(\d{4})\-(\d{2})" "\2-\1"``` produces:

```
FILE-0001-01.txt  -> FILE-01-0001.txt
FILE-0002-01.txt  -> FILE-01-0002.txt
FILE-0003-01.txt  -> FILE-01-0003.txt
```

## Numbering Sequence:

It is also capable of using numbering sequences to rename files.

```pmove "FILE" "DOC_%#%" --sequence 222 2 7``` produces:

```
FILE-0001-01.txt  -> DOC_0000222-0001-01.txt
FILE-0002-01.txt  -> DOC_0000224-0002-01.txt
FILE-0003-01.txt  -> DOC_0000226-0003-01.txt
```

## Recursive replacement

If you specify the flag ```-r``` the cuanges will be performed to files in subfolders recursively.
