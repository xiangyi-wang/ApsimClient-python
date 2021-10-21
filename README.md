# ApsimClient-python
[APSIM Client](https://github.com/APSIMInitiative/APSIM.Client) implemented by python which can communicate with [APSIM Server](https://github.com/APSIMInitiative/ApsimX).
<br/>It is still under development.</br>
# Usage
## Start APSIM Server
[Offical document](https://apsimnextgeneration.netlify.app/usage/server/)</br>
### Quick examples
#### Windows
`path/to/my/apsim-server.exe --file path/to/my/Wheat.apsimx --verbose --native --remote --keep-alive --address 127.0.0.1 --port 27747`
#### Linux(Not tested)
 
## Connect to APSIM Server 
```python3
# Connect to the socket.
print("Connecting to server...")
sock = connect_to_remote_server("127.0.0.1", 27747)
print("connected\n")
# change cultivar parameter you target and its parameter type 
# PROPERTY_TYPE_INT = 0
# PROPERTY_TYPE_DOUBLE = 1
# PROPERTY_TYPE_BOOL = 2
# PROPERTY_TYPE_DATE = 3
# PROPERTY_TYPE_STRING = 4
# PROPERTY_TYPE_INT_ARRAY = 5
# PROPERTY_TYPE_DOUBLE_ARRAY = 6
# PROPERTY_TYPE_BOOL_ARRAY = 7
# PROPERTY_TYPE_DATE_ARRAY = 8
# PROPERTY_TYPE_STRING_ARRAY = 9
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
# target fields
param_list=['Clock.Today.DayOfYear','Yield']#'Clock.Today',
nparams=len(param_list)
#start read,you need to define field type,such as 'yield' is double,'dayofyear' is integer
# args = {'tablename':'Report','params':{'name':['Yield'],'length':[sizeof(c_double)]}}
results=read_output(sock,tablename,param_list,param_type=[c_int32,c_double,])
print(results)

# run result
>Connecting to server...
 connected
 run finished
 {'Clock.Today.DayOfYear': [318, 319, 294, 308, 322, 311, 318, 361, 325, 325, 314, 327, 333, 319, 307, 305, 338, 328, 314, 309, 325, 330, 308, 331, 329, 306, 313, 329, 318, 336,  310, 313, 300, 322, 308, 325, 316, 332, 303, 305, 301, 312, 334, 326, 318, 322, 314, 305, 301, 305, 306, 307, 317, 322, 288, 323, 334, 311, 313, 338, 301, 316, 315, 326, 293, 326, 297, 307, 334, 297, 316, 321, 304, 324, 300, 303, 294, 331, 323], 'Yield': [4675.505002851583, 4642.251938605291, 686.2924903487012, 6844.349526495427, 5917.882404481129, 3318.8726833488977, 3528.561072906573, 4271.98687928234, 4382.335814416772, 3769.957669864337, 2998.903904867223, 373.46490358631274, 3102.359835581683, 3707.256235477268, 5146.099585554524, 4004.525563899052, 2519.513595551568, 211.62941318016397, 5580.008624757564, 2331.9813951561205, 3097.282350722976, 2248.990571929094, 6223.912088672994, 2016.4227013050117, 2749.7823667725975, 6000.524444678357, 5409.486821415956, 2022.145094269597, 4666.779961099444, 3763.471370405101, 4196.049532396217, 4091.470599154035, 5906.628016528976, 5138.624113304045, 5515.531747020991, 2567.6635951310705, 5344.559222862979, 3130.7810690401443, 3615.098657127981, 2250.1424062191627, 5012.404385192762, 5463.903436689789, 1991.801360158845, 3392.971028795228, 2521.691718805625, 4699.592908864443, 4339.995925504385, 4773.542375666551, 6170.961609996037, 6512.8397557822045, 5005.343848505993, 3215.636569096305, 1398.1631838724738, 2945.938377830589, 5643.007727698414, 6215.74473849772, 4027.609886870473, 4122.11434919744, 3368.8595339357116, 6051.798132734885, 3799.2227141144053, 2340.640407483498, 4385.648113743056, 2914.578312911737, 5497.687057040138, 5322.5373846279, 2973.343218377085, 2158.9374747963793, 4054.6797739917706, 3675.9986479713343, 4624.683367673841, 3644.728574677256, 1316.9616408080715, 3437.0481996559397, 4301.84836017624, 1719.348640360466, 6222.761812429735, 3498.152210050991, 2383.2366802504216]}

```
    
    
    
    
Future work
1. Improve the basic communicate function as a socket client.
2. Add modules to build and edit APSIMX files.
3. Integrate parameter estimation and sensitivity analysis functions.
