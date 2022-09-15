# -*- coding: utf-8 -*-
# @Time : 10/19/2021 12:03
# @Author : wxy
# @File : test.py
# @Software: PyCharm
import json
from dataclasses import dataclass, field, asdict, astuple
from collections import OrderedDict

def IOderedDict(object):
    return OrderedDict({key:value for key, value in vars(object).items()})
@dataclass(order=True)
class Simulations:

    Schema:str ='Models.Core.Simulations, Models'
    ExplorerWidth:int=259
    Version:str=100
    ApsimVersion:str='0.0.0.0'
    Name: str = 'Simulations'
    Children:list = field(default_factory=list)
    Enabled:bool=True
    ReadOnly:bool=False
    def add(self,object):
        return self.Children.append(IOderedDict(object))

    def build(self):
        return json.dumps(obj=self.__dict__,
                   default=lambda x: x.__dict__, sort_keys=False,indent=2,ensure_ascii=False).replace('Schema', '$type')

    def save(self,path):
        with open(path,'w',encoding='utf-8') as f:
            f.write(self.build())

@dataclass(order=True)
class Experiment:
     Schema:str='Models.Factorial.Experiment, Models'
     Name:str="Experiment"
     Children: list = field(default_factory=list)
     IncludeInDocumentation:bool=True
     Enabled:bool=True
     ReadOnly:bool=False
     def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Factors:
     Schema:str='Models.Factorial.Factors, Models'
     Name:str="Factors"
     Children: list = field(default_factory=list)
     IncludeInDocumentation:bool=True
     Enabled:bool=True
     ReadOnly:bool=False
     def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Permutation:
    '''
    This class permutates all child models by each other.
    '''
    Schema:str='Models.Factorial.Permutation, Models'
    Name:str="Permutation"
    Children: list = field(default_factory=list)
    IncludeInDocumentation:bool=True
    Enabled:bool=True
    ReadOnly:bool=False
    def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Simulation:
    '''
    A simulation model
    '''
    Schema: str = 'Models.Core.Simulation, Models'
    IsRunning: bool = False
    Descriptors: str =None
    Name: str = 'Simulation'
    Children: list = field(default_factory=list)
    Enabled:bool=True
    ReadOnly:bool=False
    def add(self,object):
        return self.Children.append(IOderedDict(object))


@dataclass(order=True)
class Memo:
    Schema:str = 'Models.Memo, Models'
    Text:str=""
    Name: str = 'Memo'
    Children: list = field(default_factory=list)
    Enabled:bool=True
    ReadOnly:bool=False

    def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class DataStore:
    Schema:str ='Models.Storage.DataStore, Models'
    useFirebird:bool=False
    CustomFileName:str = None
    Name:str="DataStore"
    Children: list = field(default_factory=list)
    Enabled:bool=True
    ReadOnly:bool=False

    def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Weather:
    Schema:str ='Models.Climate.Weather, Models'
    ConstantsFile:str= None
    FileName: str = ''
    ExcelWorkSheetName:str = None
    Name:str="Weather"
    Children: list = field(default_factory=list)
    Enabled:bool=True
    ReadOnly:bool=False

    def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Clock:
    Schema:str ='Models.Clock, Models'
    Start:str=None
    End:str=None
    Name:str="Clock"
    Children: list = field(default_factory=list)
    Enabled:bool=True
    ReadOnly:bool=False
    def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Summary:
    Schema:str = 'Models.Summary, Models'
    Verbosity:int=100
    Name:bool="Summary"
    Children: list = field(default_factory=list)
    Enabled:bool=True
    ReadOnly:bool=False
    def add(self,object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Replacements:
     Schema:str='Models.Core.Replacements, Models'
     Name:str="Replacements"
     Children: list = field(default_factory=list)
     IncludeInDocumentation:bool=True
     Enabled:bool=True
     ReadOnly:bool=False
     def add(self,object):
        return self.Children.append(IOderedDict(object))
@dataclass(order=True)
class Cultivar:
     Schema:str='Models.PMF.Cultivar, Models'
     Command: list = field(default_factory=list)
     Name:str="Cultivar"
     Children: list = field(default_factory=list)
     IncludeInDocumentation:bool=True
     Enabled:bool=True
     ReadOnly:bool=False
     def add(self,object):
        return self.Children.append(IOderedDict(object))
@dataclass(order=True)
class SoilArbitrator:
     Schema:str='Models.Soils.Arbitrator.SoilArbitrator, Models'
     Name:str="Soil Arbitrator"
     Children: list = field(default_factory=list)
     Enabled: bool = True
     ReadOnly: bool = False

     def add(self,object):
        return self.Children.append(IOderedDict(object))
@dataclass(order=True)
class Zone:
    Schema:str= 'Models.Core.Zone, Models'
    Area: float = 1.0
    Slope: float = 0.0
    AspectAngle: float = 0.0
    Altitude:float=0.0
    Name: str = "Field"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Soil:
    Schema:str = 'Models.Soils.Soil, Models'

    RecordNumber:int= 0
    ASCOrder:float=None
    ASCSubOrder:float=None
    SoilType: str = ''
    LocalName: str = ''
    Site: str = None
    NearestTown:str=None
    Region:str=None
    State:str=None
    Country:str=None
    NaturalVegetation:str=None
    ApsoilNumber:float=None
    Latitude:float=0.0
    Longitude:float=0.0
    LocationAccuracy:float=None
    YearOfSampling: float = None
    DataSource:str=None
    Comments:str=None
    Name:str="Soil"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class SurfaceOrganicMatter:
    Schema:str= 'Models.Surface.SurfaceOrganicMatter, Models'
    InitialResidueMass:float=0.0
    InitialStandingFraction:float=0.0
    InitialCPR:float=0.0
    InitialCNR:float=0.0
    ResourceName: str = "SurfaceOrganicMatter"
    Name:str= "SurfaceOrganicMatter"
    InitialResidueType: str= ''
    Enabled: bool = True
    ReadOnly: bool = False
    def __post_init__(self):
        self.InitialResidueName: str = self.InitialResidueType
    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class MicroClimate:
    Schema:str = 'Models.MicroClimate, Models'
    a_interception:float = 0.0
    b_interception:float = 1.0
    c_interception:float = 0.0
    d_interception:float = 0.0
    soil_albedo:float =  0.23
    SoilHeatFluxFraction:float= 0.4
    MinimumHeightDiffForNewLayer:float=  0.0
    NightInterceptionFraction:float=  0.5
    ReferenceHeight:float=  2.0
    Name:str="MicroClimate"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Irrigation:
    '''
    This model controls irrigation events.
    '''
    Schema:str='Models.Irrigation, Models'
    Name:str="Irrigation"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))
@dataclass(order=True)
class Fertiliser:
    '''
    This model is responsible for applying fertiliser.
    '''
    Schema:str='Models.Fertiliser, Models'
    ResourceName:str="Fertiliser"
    Name:str="Fertiliser"
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True)
class Plant:
    Schema:str = 'Models.PMF.Plant, Models'
    ResourceName : str = None
    Name: str = None
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

# @dataclass
#     class ManageMent(object):
#     Operations:list=field(default_factory=list)
#     # def __post_init__(self):


@dataclass(order=True,repr=True)
class Operations:
    Schema:str ='Models.Operations, Models'
    Name: str = "Operations"
    Operation:list=field(default_factory=list)
    Children:list=field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False
    def __post_init__(self):
        for i in range (len(self.Operation)):
            Operation = self.Operation[i]

            if Operation['Action'] == 'Fertiliser':
                self.Operation[i] = {"Schema": "Models.Operation, Models",
                             "Date": Operation['Date'],
                             "Action": f"[Fertiliser].Apply({Operation['Amount']}, Fertiliser.Types.{Operation['FertiliserType']},0);",
                             "Enabled": True
                             }
            elif Operation['Action'] == 'Irrigation':
                self.Operation[i] = {"Schema": "Models.Operation, Models",
                             "Date": Operation['Date'],
                             "Action": f"[Irrigation].Apply({Operation['Amount']};",
                             "Enabled": True
                             }

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class Report:
    Schema:str ='Models.Report, Models'
    VariableNames: list = field(default_factory=list)
    EventNames:list = field(default_factory=list)
    GroupByVariableName: str = None
    Name: str = "Report"
    Children:list=field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class Manager:
    Schema:str ='Models.Manager, Models'
    Code: str = None
    Parameters:list = field(default_factory=list)
    Name: str = "PotatoPlantAndHarvest"
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))
IDepth=["0-4.5",
       "4.5-9.1",
       "9.1-16.6",
       "16.6-28.9",
       "28.9-49.3",
       "49.3-82.9"]#"82.9-138.3"
IThickness = [45,
              46,
              75,
              123,
              204,
              336]#554
@dataclass(order=True,repr=True)
class Physical:
    Schema:str ='Models.Soils.Physical, Models'
    Depth:list = field(default_factory=lambda: IDepth)
    Thickness:list = field(default_factory=lambda: IThickness)
    ParticleSizeClay: float=None
    ParticleSizeSand: float=None
    ParticleSizeSilt: float=None
    BD: list = field(default_factory=list)
    AirDry: list = field(default_factory=list)
    LL15: list = field(default_factory=list)
    DUL: list = field(default_factory=list)
    SAT: list = field(default_factory=list)
    KS: float =None
    BDMetadata: str = None
    AirDryMetadata:str = None
    LL15Metadata:str = None
    DULMetadata: str = None
    SATMetadata:str = None
    KSMetadata: str = None
    Name: str = "Physical"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class SoilCrop:
    Schema:str ='Models.Soils.SoilCrop, Models'
    LL: list = field(default_factory=list)
    KL:list = field(default_factory=list)
    XF: list = field(default_factory=list)

    LLMetadata: str = None
    KLMetadata:str = None
    XFMetadata:str = None
    Name: str = "PotatoSoil"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class SoilWater:
    Schema:str ='Models.WaterModel.WaterBalance, Models'
    SummerDate: str = "1-Apr"
    SummerU: float= 9.0
    SummerCona: float=4.4
    WinterDate: str="1-Nov"
    WinterU: float=9.0
    WinterCona: float=4.4
    DiffusConst: float=88.0
    DiffusSlope: float=35.4
    Salb: float=0.18
    CN2Bare: float=0.0
    CNRed: float=-9E-05
    CNCov: float=0.0
    DischargeWidth: float=0.0
    CatchmentArea: float=0.0
    Thickness: list = field(default_factory=lambda: IThickness)
    SWCON: list = field(default_factory=list)
    KLAT: str = None
    ResourceName: str="WaterBalance"
    Name: str = "SoilWater"
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class Organic:
    Schema:str ='Models.Soils.Organic, Models'
    Depth: list = field(default_factory=lambda: IDepth)
    Thickness: list = field(default_factory=lambda: IThickness)
    FOMCNRatio:float= 30.0
    Carbon: list = field(default_factory=list)
    SoilCNRatio: list = field(default_factory=list)
    FBiom: str = None
    FInert: str = None
    FOM: str = None
    CarbonMetadata:str =None
    FOMMetadata:str =None
    Name: str = "Organic"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class Chemical:
    Schema:str ='Models.Soils.Chemical, Models'
    Depth: list = field(default_factory=lambda: IDepth)
    Thickness: list = field(default_factory=lambda: IThickness)
    NO3N: str = None
    NH4N: str = None
    PH: list = field(default_factory=list)
    CL: str = None
    EC: str = None
    ESP: str = None
    LabileP:str = None
    UnavailableP: str = None
    ECMetadata: str = None
    CLMetadata: str = None
    ESPMetadata: str = None
    PHMetadata: str = None
    Name: str = "Chemical"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class InitialWater:
    Schema:str ='Models.Soils.InitialWater, Models'
    PercentMethod: int= 0
    FractionFull:float= 1.0
    DepthWetSoil:str= "NaN"
    RelativeTo:str= None
    Name: str = "Initial water"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class Sample:
    Schema:str ='Models.Soils.Sample, Models'
    Depth: list = field(default_factory=lambda: IDepth)
    Thickness: list = field(default_factory=lambda: IThickness)
    NO3N:str=None
    NH4N: str=None
    SW: str=None
    OC: str=None
    EC:str=None
    CL: str=None
    ESP: str=None
    PH: str=None
    SWUnits: int=0
    OCUnits: int=0
    PHUnits: int=0
    Name: str = "Sample"
    Children: list = field(default_factory=list)
    IncludeInDocumentation: bool = True
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class CERESSoilTemperature:
    Schema:str ='Models.Soils.CERESSoilTemperature, Models'
    Name: str = "Temperature"
    Children: list = field(default_factory=list)
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))

@dataclass(order=True,repr=True)
class Nutrient:
    Schema:str ='Models.Soils.Nutrients.Nutrient, Models'
    ResourceName: str = "Nutrient"
    Name: str = "Nutrient"
    Enabled: bool = True
    ReadOnly: bool = False

    def add(self, object):
        return self.Children.append(IOderedDict(object))


if __name__ == '__main__':
    Simulations = Simulations()
    # Model.add('Simulations')
    # Model.add('Memo')
    # print(Model.__dict__)
    # Mangement = [{'Action': 'Fertiliser', 'Date': '1992-06-14T00:00:00', 'FertiliserType': 'NO3N', 'Amount': 40}]
    # a =ManageMent(Operations=Mangement)
    #
    # print( a)

