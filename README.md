# echo-test
Echo-test is a test script for testing communication works without lossing data.
You can easliy replace ./echo to your communication echo test program which uses stdin and stdout.

## Prerequisites
* Python 3.5 and later is required
* Install colordiff (optional)
```shell
sudo apt-get install colordiff
```

## Run echo-test
* Run `make`to build ./echo program and execute `python3 echo-test.py -h` to show usage:

```
Usage: echo-test.py [-h] [-p PROG] [-t TID] [-c]
    -h         Print this message
    -p PROG    Program to test
    -t TID     Test ID to test
    -c         Enable colored text
    --difflib  Use python difflib module
```

* Run echo-test

```
python3 echo-test.py -p ./your_echo_program -c
```

* The result shows below if your echo communication works well

```
Files ./testcase/input1.txt and ./testcase/output1.txt are idnetical
Files ./testcase/input2.txt and ./testcase/output2.txt are idnetical
Files ./testcase/input3.txt and ./testcase/output3.txt are idnetical
```
* Note that echo-test uses Linux `diff` command for comparing intput and output files, and `-c` option only support when colordiff exists.
* You can also use `--difflib` option to enable python difflib module. However, it will need more memory usage.
