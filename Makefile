TARGET = echo
VERBOSE = TRUE

SRCS := $(wildcard *.c)
OBJS := $(SRCS:.c=.o)

TESTDIR := testcase

CFLAGS = -g -Wall
LFLAGS = 

ifeq ($(VERBOSE), TRUE)
	HIDE = 
else
	HIDE = @
endif

.PHONY: all clean test

all: $(TARGET)

$(TARGET): $(OBJS)
	$(HIDE)$(CC) $(CFLAGS) $(OBJS) -o $@ $(LFLAGS)

%.o: %.c
	$(HIDE)$(CC) -c $(CFLAGS) $< -o $@

clean:
	$(HIDE)rm -f $(TARGET) $(OBJS)
	$(HIDE)rm -f $(TESTDIR)/output*

test: $(TARGET)
	$(HIDE)python3 echo-test.py -p ./$(TARGET) -c -t1
