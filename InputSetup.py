# -*- coding: utf-8 -*-
# @Time : 11/29/2021 9:36
# @Author : wxy
# @File : run.py
# @Software: PyCharm
import numpy as np
from ModelFactory import Simulations,Memo,Weather,Cultivar,Replacements,\
    MicroClimate,Soil,SoilArbitrator,Summary,DataStore,Simulation,Clock,Zone,SurfaceOrganicMatter,\
    Fertiliser,Irrigation,Plant,Operations,Report,Manager
from ModelFactory import Physical,SoilWater,Organic,Chemical,InitialWater,Sample,CERESSoilTemperature,Nutrient,SoilCrop
from soil import get_soil
from SoilTextureCalculator import getTexture,SWCON,get_Salb,get_CN2b,get_Diffus

# ICultivar= ["[Structure].FinalLeafNumber.FixedValue = 29",
#             "[Tuber].LiveFWt.DryMatterContent.XYPairs.Y = 0.13,0.21",
#             "[Structure].Phyllochron.Phyllochron.Phyllochron.XYPairs.X = 0,0.15,0.74,0.75,1",
#             "[Structure].Phyllochron.Phyllochron.Phyllochron.XYPairs.Y = 5,40,40,60,60",
#             "[Structure].BranchingRate.PotentialBranchingRate.XYPairs.X = 0,6,7,20,21",
#             "[Structure].BranchingRate.PotentialBranchingRate.XYPairs.Y = 0,0,0.5,0.5,0"]
# '[Potato].Structure.Phyllochron.Phyllochron.Phyllochron.XYPairs.X(1)'
ICultivar = ["[Phenology].Vegetative.Target.FixedValue = 550",#TTveg
            "[Phenology].EarlyFlowering.Target.FixedValue = 120",
            "[Phenology].EarlyGrainFilling.Target.FractionofGrainfilling.FixedValue = 0.324",
            "[Phenology].EarlyPodDevelopment.Target.FixedValue = 200",
            "[Phenology].LateGrainFilling.Target.EntireGrainfillPeriod.FixedValue = 650",
            "[Phenology].VegetativePhotoperiodModifier.XYPairs.X = 13.1, 16.49",
            "[Phenology].ReproductivePhotoperiodModifier.XYPairs.X = 13.1, 16.49",
            "[Leaf].AreaLargestLeaf.FixedValue=0.013",
            "[Grain].PotentialHarvestIndex.FixedValue=0.4"]
VariableNames=[ '[Clock].Today.Year as Year',
                "[Clock].Today.DayOfYear as DayOfYear",
                "[Soybean].Grain.Total.Wt*10 as Yield",
                "[Soybean].Phenology.Stage",
                ]
Code1 = open('D:/ApsimClient/MangerScript/SowFixDate.cs',newline='\r').read()
Code2 = open('D:/ApsimClient/MangerScript/SoybeanHarvest.cs',newline='\r').read()
Code3 = open('D:/ApsimClient/MangerScript/AutomaticFertiliser.cs',newline='\r').read()
Code4 = open('D:/ApsimClient/MangerScript/AutomaticIrrigation.cs',newline='\r').read()
Parameters1=[{
                  "Key": "Crop",
                  "Value": "Soybean"
                },
                {
                  "Key": "SowDate",
                  "Value": "05-Jun"
                },
                {
                  "Key": "CultivarName",
                  "Value": "Generic_MG4"
                },
                {
                    "Key": "SowingDepth",
                    "Value": "50"
                },
                {
                  "Key": "PlantSpacing",
                  "Value": "300"
                },
                {
                  "Key": "RowSpacing",
                  "Value": "700"
                },

                {
                  "Key": "Population",
                  "Value": "38"
                }
                # {
                #   "Key": "StemNumberPerSeedTuber",
                #   "Value": "2.2"
                # },
                # {
                #   "Key": "SetFinalLeafNumber",
                #   "Value": "40"
                # },
                # {
                #   "Key": "HarvestDate",
                #   "Value": "04/28/2017 00:00:00"
                # }
]
Parameters3=[{
                  "Key": "FertiliserType",
                  "Value": "Urea"
                },
                {
                  "Key": "Threshold",
                  "Value": "300"
                }
]
Parameters4=[{
                  "Key": "Crop",
                  "Value": "Soybean"
                },
                {
                  "Key": "AutoIrrigationOn",
                  "Value": "True"
                },
                {
                  "Key": "FASWThreshold",
                  "Value": "0.9"
                },
                {
                    "Key": "FASWDepth",
                    "Value": "600"
                },
                {
                  "Key": "weeks",
                  "Value": "3"
                },
                {
                  "Key": "afterSowing",
                  "Value": "2"
                }
]
# month="JanFebMarAprMayJunJulAugSepOctNovDec"    #将所有月份简写存到month中
# pos=(int(month)-1)*3 #输入的数字为n,将(n-1)*3,即为当前月份所在索引位置

# findmonth=month[pos:pos+3]
#创建模型节点
Simulations = Simulations()
Memo = Memo()
Zone = Zone()
#------------------------
#SOIL
lon = 117.35
lat = 30.15
BD = get_soil('BD',lon_in=lon,lat_in=lat)
pH = get_soil('PH',lon_in=lon,lat_in=lat)
CL = get_soil('CL',lon_in=lon,lat_in=lat)
SI = get_soil('SI',lon_in=lon,lat_in=lat)
SA = get_soil('SA',lon_in=lon,lat_in=lat)
TN = get_soil('TN',lon_in=lon,lat_in=lat)
SOM = get_soil('SOM',lon_in=lon,lat_in=lat)
KS = get_soil('K_SCH',lon_in=lon,lat_in=lat)
# SAT = get_soil('THSGM',lon_in=lon,lat_in=lat)
DUL = get_soil('TH33',lon_in=lon,lat_in=lat)
LL15 = get_soil('TH1500',lon_in=lon,lat_in=lat)
Carbon = [i/1.724 for i in SOM]
SoilCNRatio = [Carbon[i]/TN[i] for i in range(len(TN))]

texture = getTexture(np.mean(SA),np.mean(CL), np.mean(SI))
swcon_val = SWCON(texture)
swcon_list = [swcon_val for i in range(len(SA))]
SAT = [(1-BD[i]/2.65)-swcon_list[i]/10 for i in range(len(BD))]
AirDry = [LL15[0]*0.5,LL15[1]*0.7,LL15[2]*0.8,LL15[3]*0.9,LL15[4],LL15[5]]
SoilCrop = SoilCrop(Name='SoybeanSoil',LL=[LL15[0],LL15[1],LL15[2],LL15[3],LL15[4],LL15[5]*1.3],
                    KL=[0.06,0.06,0.06,0.06,0.06,0.04],
                    XF=[1,1,1,1,1,1])
Soil = Soil(Longitude=lon,
            Latitude=lat,
            SoilType=texture,
            Site='jiagedaqi')


Physical=Physical(BD=BD,
                  ParticleSizeClay=CL,
                  ParticleSizeSand=SA,
                  ParticleSizeSilt=SI,
                  AirDry=AirDry,
                  LL15=LL15,
                  DUL=DUL,
                  SAT=SAT,
                  KS=KS,
                  )
Physical.add(SoilCrop)
Salb = get_Salb(texture)
CN2b = get_CN2b(texture)
DiffusConst,DiffusSlope = get_Diffus(texture)
SoilWater=SoilWater(SWCON=swcon_list,Salb=Salb,CN2Bare=CN2b,DiffusConst=DiffusConst,DiffusSlope=DiffusSlope)
Organic=Organic(Carbon=Carbon,
                SoilCNRatio=SoilCNRatio,
                FInert=[ 0.4,
                        0.4,
                        0.4,
                        0.6,
                        0.8,
                        0.95 ],
                FBiom=[0.035,
                        0.035,
                        0.035,
                        0.02,
                        0.015,
                        0.01],
                FOM=[1243.9310541346904,
                    833.8319214727269,
                    457.61666105087295,
                    251.1453484552152,
                    137.83148958311097,
                    75.64352530338392])
Chemical=Chemical(PH=pH)
InitialWater=InitialWater()
# Sample=Sample()
CERESSoilTemperature=CERESSoilTemperature()
Nutrient=Nutrient()

Soil.add(Physical)
Soil.add(SoilWater)
Soil.add(Organic)
Soil.add(Chemical)
Soil.add(InitialWater)
# Soil.add(Sample)
Soil.add(CERESSoilTemperature)
Soil.add(Nutrient)

#========================
Report = Report(VariableNames=VariableNames,EventNames=['[Soybean].Harvesting'])#[Clock].EndOfSimulation
Plant = Plant(ResourceName='Soybean',Name='Soybean')
Irrigation = Irrigation()
Fertiliser = Fertiliser()
DataStore = DataStore()
Summary = Summary()
MicroClimate = MicroClimate()
SurfaceOrganicMatter = SurfaceOrganicMatter(InitialResidueType='maize',
                                            InitialResidueMass=2000,
                                            InitialCNR=80)


SoilArbitrator =SoilArbitrator()
Simulation = Simulation(Name='jiagedaqi')
Clock = Clock(Start='2010-01-01T00:00:00',End='2010-12-31T00:00:00')
Weather = Weather(FileName='G:\\apsim_weather\\2010a\\CN077082.met')
# Mangement=[{'Action':'Fertiliser','Date':'2010-05-14T00:00:00','FertiliserType':'UreaN','Amount':40},
#            {'Action':'Fertiliser','Date':'2010-06-14T00:00:00','FertiliserType':'UreaN','Amount':140}]


# Operations = Operations(Operation=Mangement)
Manger1 = Manager(Name='SowFixDate',Code=Code1,Parameters=Parameters1)
Manger2 = Manager(Name='SoybeanHarvest',Code=Code2)
Manger3 = Manager(Name='AutomaticFertiliser',Code=Code3,Parameters=Parameters3)
Manger4 = Manager(Name='AutomaticIrrigation',Code=Code4,Parameters=Parameters4)
Zone.add(Soil)
Zone.add(SurfaceOrganicMatter)
Zone.add(MicroClimate)
Zone.add(Irrigation)
Zone.add(Fertiliser)
Zone.add(Plant)
# Zone.add(Operations)
Zone.add(Manger1)
Zone.add(Manger2)
Zone.add(Manger3)
Zone.add(Manger4)
Zone.add(Report)

#==================
Replacements = Replacements()
Cultivar = Cultivar(Name='Generic_MG4',Command=ICultivar)
Replacements.add(Cultivar)
Simulations.add(Replacements)
#====================
#生成节点树

Simulations.add(Memo)
Simulations.add(DataStore)
Simulations.add(Simulation)
Simulation.add(Weather)
Simulation.add(Clock)
Simulation.add(Summary)
Simulation.add(SoilArbitrator)
Simulation.add(Zone)



Simulations.save(path=r'E:\APSIM2023.5.7223.0/sss.apsimx')


