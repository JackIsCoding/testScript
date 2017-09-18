SERVER_NAME				= uploaderClient
TIME					= $(shell date +"%Y%m%d")
PROGRAM					= $(SERVER_NAME).$(TIME)

all:
	go build -gcflags "-N -l" -x -o $(PROGRAM) ./*.go

this: all

rebuild: clean all

clean:
	rm bin log -fr
	cd $(DIR_PRO_SCHEDULER) && make clean
	