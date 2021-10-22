# ApsimClient-python
This repository contains an implementation of [APSIM Client](https://github.com/APSIMInitiative/APSIM.Client)(**[APSIM Next Generation](https://github.com/APSIMInitiative/ApsimX), a crop model**) for the Python programming language. It can easily to communicate with [APSIM server](https://apsimnextgeneration.netlify.app/usage/server/). 

The official line is that the APSIM Server holds an .apsimx file open in memory and runs it on demand, potentially with modified parameter values. Communication with the server occurs primarily via unix sockets, which results in far less overhead than repeatedly invoking Models.exe. But they have no plan to implement it under windows. The original client is implemented in a [C API](https://github.com/APSIMInitiative/APSIM.Client) under Linux, but most people may be more familiar with Python than C language. So I tried to write this Python API based on the original project. In theory, it can easily cross platform.

It is still under development.

## Start APSIM Server
**[Offical document](https://apsimnextgeneration.netlify.app/usage/server/)**</br>
### Quick examples
#### Windows
```
path/to/my/ApsimX/bin/apsim-server.exe --file path/to/my/Wheat.apsimx --verbose --native --remote --keep-alive --address 127.0.0.1 --port 27747
```
#### Linux(no tested)
 
## Connect to APSIM Server 
**Note:** The field of `Clock.Today` is still not supported. You need to use the `Clock.Today.DayOfYear` field.
### Quick examples
```python3
# Connect to the socket.
print("Connecting to server...")
sock = connect_to_remote_server("127.0.0.1", 27747)
print("connected\n")
# change cultivar parameter you target and its parameter type 
PROPERTY_TYPE_INT = 0
PROPERTY_TYPE_DOUBLE = 1
PROPERTY_TYPE_BOOL = 2
PROPERTY_TYPE_DATE = 3
PROPERTY_TYPE_STRING = 4
PROPERTY_TYPE_INT_ARRAY = 5
PROPERTY_TYPE_DOUBLE_ARRAY = 6
PROPERTY_TYPE_BOOL_ARRAY = 7
PROPERTY_TYPE_DATE_ARRAY = 8
PROPERTY_TYPE_STRING_ARRAY = 9
changes=[
    {"path":"[Phenology].Phyllochron.BasePhyllochron.FixedValue",
     "value":1.5,
     'paramtype':PROPERTY_TYPE_DOUBLE
     }]
# rerun with your change
run_with_changes(sock,changes)
# read model output
# table name
tablename='Report'
#start read output, you need to define target fields and field type,such as 'yield' is double,'dayofyear' is integer
param_list={'Clock.Today.DayOfYear':c_int32,
            'Yield':c_double}

results=read_output(sock,tablename,param_list)
print(pd.DataFrame(results))


```
Run result
```
>Connecting to server...
 connected
 run finished
      Clock.Today.DayOfYear        Yield
 0                     318  4675.505003
 1                     319  4642.251939
 2                     294   686.292490
 3                     308  6844.349526
 4                     322  5917.882404
 ..                    ...          ...
 74                    300  4301.848360
 75                    303  1719.348640
 76                    294  6222.761812
 77                    331  3498.152210
 78                    323  2383.236680

[79 rows x 2 columns]

Process finished with exit code 0
```
    
    
    
## Future work
* Improve the basic communicate function as a socket client.
* Add modules to build and edit .apsimx files.
* Integrate parameter estimation and sensitivity analysis functions.
