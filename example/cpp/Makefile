app := auth
compiler := g++
opt := -std=c++11
flags := -W -Wall -g -Wpedantic
sources := auth.cpp
libs := -lcurl -ljsoncpp

all: $(app)

$(app):
	$(compiler) $(opt) $(flags) $(sources) $(libs) -o $(app)
