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
from SoilTextureCalculator import getTexture,SWCON

# ICultivar= ["[Structure].FinalLeafNumber.FixedValue = 29",
#             "[Tuber].LiveFWt.DryMatterContent.XYPairs.Y = 0.13,0.21",
#             "[Structure].Phyllochron.Phyllochron.Phyllochron.XYPairs.X = 0,0.15,0.74,0.75,1",
#             "[Structure].Phyllochron.Phyllochron.Phyllochron.XYPairs.Y = 5,40,40,60,60",
#             "[Structure].BranchingRate.PotentialBranchingRate.XYPairs.X = 0,6,7,20,21",
#             "[Structure].BranchingRate.PotentialBranchingRate.XYPairs.Y = 0,0,0.5,0.5,0"]
# '[Potato].Structure.Phyllochron.Phyllochron.Phyllochron.XYPairs.X(1)'
VariableNames=[ '[Clock].Today.Year as Year',
                "[Clock].Today.DayOfYear as DayOfYear",
                "[Potato].Tuber.Total.Wt*10 as Yield",

                # "[Soil].Nutrient.NO3.kgha",
                # "[Soil].SoilWater.Drainage",
                # "[Soil].SoilWater.Eo",
                # "[Soil].SoilWater.Es",
                # "[Soil].SoilWater.pond",
                # "[Soil].SoilWater.Runoff",
                # "[Soil].SoilWater.SWmm",
                # "[Potato].Arbitrator.DM.Allocated",
                # "[Potato].Arbitrator.DM.TotalPlantDemand",
                # "[Potato].Arbitrator.DM.NutrientLimitation",
                # "[Potato].Arbitrator.DM.SinkLimitation",
                # "[Potato].Arbitrator.DM.TotalFixationSupply",
                # "[Potato].Arbitrator.N.TotalPlantDemand",
                # "[Potato].Arbitrator.N.TotalPlantSupply",
                # "[Potato].Arbitrator.N.Allocated",
                # "[Potato].Leaf.AppearedCohortNo",
                # "[Potato].Leaf.CohortParameters.MaximumNConc",
                # "[Potato].Leaf.CohortParameters.MinimumNConc",
                # "[Potato].Leaf.CoverDead",
                # "[Potato].Leaf.CoverGreen",
                # "[Potato].Leaf.CoverTotal",
                # "[Potato].Leaf.Dead.N",
                # "[Potato].Leaf.Dead.NConc",
                # "[Potato].Leaf.Dead.Wt",
                # "[Potato].Leaf.DeadCohortNo",
                # "[Potato].Leaf.ExpandedCohortNo",
                # "[Potato].Leaf.ExpandingCohortNo",
                # "[Potato].Leaf.Fn",
                # "[Potato].Leaf.Fw",
                # "[Potato].Leaf.LAI",
                # "[Potato].Leaf.LAIDead",
                # "[Potato].Leaf.Live.N",
                # "[Potato].Leaf.Live.NConc",
                # "[Potato].Leaf.Live.Wt",
                # "[Potato].Leaf.Photosynthesis.FT",
                # "[Potato].Leaf.Photosynthesis.FVPD",
                # "[Potato].Leaf.PlantAppearedGreenLeafNo",
                # "[Potato].Leaf.SenescingCohortNo",
                # "[Potato].Leaf.SpecificArea",
                # "[Potato].Leaf.Transpiration",
                # "[Potato].Leaf.PotentialEP",
                # "[Potato].Phenology.CurrentPhase.Name",
                # "[Potato].Phenology.Stage",
                # "[Potato].Phenology.Stage",
                # "[Potato].Root.Dead.N",
                # "[Potato].Root.Dead.NConc",
                # "[Potato].Root.Dead.Wt",
                # "[Potato].Root.Depth",
                # "[Potato].Root.Live.N",
                # "[Potato].Root.Live.NConc",
                # "[Potato].Root.Live.Wt",
                # "[Potato].Root.MaximumNConc",
                # "[Potato].Root.MinimumNConc",
                # "[Potato].Root.NUptake",
                # "[Potato].Root.WaterUptake",
                # "[Potato].Stem.Dead.N",
                # "[Potato].Stem.Dead.NConc",
                # "[Potato].Stem.Dead.Wt",
                # "[Potato].Stem.Live.N",
                # "[Potato].Stem.Live.NConc",
                # "[Potato].Stem.Live.StorageWt",
                # "[Potato].Stem.Live.StructuralWt",
                # "[Potato].Stem.Live.Wt",
                # "[Potato].Stem.MaximumNConc",
                # "[Potato].Stem.MinimumNConc",
                # "[Potato].Structure.Height",
                # "[Potato].Structure.LeafTipsAppeared",
                # "[Potato].Structure.FinalLeafNumber",
                # "[Potato].Structure.PlantTotalNodeNo",
                # "[Potato].Structure.PrimaryBudTotalNodeNo",
                # "[Potato].Structure.TotalStemPopn",
                # "[Potato].AboveGround.N",
                # "[Potato].AboveGround.Wt",
                # "[Potato].BelowGround.N",
                # "[Potato].BelowGround.Wt",
                # "[Potato].Total.N",
                # "[Potato].Total.Wt",
                # "[Potato].TotalDead.N",
                # "[Potato].TotalDead.Wt",
                # "[Potato].TotalLive.N",
                # "[Potato].TotalLive.Wt",
                # "[Potato].Tuber.Dead.N",
                # "[Potato].Tuber.Dead.NConc",
                # "[Potato].Tuber.Dead.Wt",
                # "[Potato].Tuber.LiveFWt.DryMatterContent",
                # "[Potato].Tuber.Live.N",
                # "[Potato].Tuber.Live.NConc",
                # "[Potato].Tuber.Live.Wt",
                # "[Potato].Tuber.LiveFWt",
                # "[Potato].Tuber.MaximumNConc",
                # "[Potato].Tuber.MinimumNConc",
                # "[Potato].Leaf.InitialisedCohortNo"
                ]
Code = open('D:/ApsimClient/MangerScript/PotatoPlantAndHarvest.cs',newline='\r').read()


Parameters=[{
                  "Key": "PlantingDate",
                  "Value": "12/16/2016 00:00:00"
                },
                {
                  "Key": "CultivarName",
                  "Value": "Rua"
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
                  "Key": "PlantingDepth",
                  "Value": "120"
                },
                {
                  "Key": "StemNumberPerSeedTuber",
                  "Value": "2.2"
                },
                {
                  "Key": "SetFinalLeafNumber",
                  "Value": "40"
                },
                {
                  "Key": "HarvestDate",
                  "Value": "04/28/2017 00:00:00"
                }]
# month="JanFebMarAprMayJunJulAugSepOctNovDec"    #将所有月份简写存到month中
# pos=(int(month)-1)*3 #输入的数字为n,将(n-1)*3,即为当前月份所在索引位置

# findmonth=month[pos:pos+3]
#创建模型节点
Simulations = Simulations()
Memo = Memo()
Zone = Zone()
#------------------------
#SOIL
lon = 111.70
lat = 29.03
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
SoilCrop = SoilCrop(LL=[LL15[0],LL15[1],LL15[2],LL15[3],LL15[4],LL15[5]*1.3],
                    KL=[0.1,0.1,0.06,0.06,0.04,0.01],
                    XF=[1,1,1,1,1,1])
Soil = Soil(Longitude=lon,
            Latitude=lat,
            SoilType=texture,
            Site='Changde')
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
SoilWater=SoilWater(SWCON=swcon_list)
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
Report = Report(VariableNames=VariableNames,EventNames=['[Potato].Harvesting'])
Plant = Plant(ResourceName='Potato',Name='Potato')
Irrigation = Irrigation()
Fertiliser = Fertiliser()
DataStore = DataStore()
Summary = Summary()
MicroClimate = MicroClimate()
SurfaceOrganicMatter = SurfaceOrganicMatter(InitialResidueType='Rice',
                                            InitialResidueMass=2000,
                                            InitialCNR=80)


SoilArbitrator =SoilArbitrator()
Simulation = Simulation(Name='Changde')
Clock = Clock(Start='2016-10-01T00:00:00',End='2017-04-28T00:00:00')
Weather = Weather(FileName='%root%\\Examples\\WeatherFiles\\CN000176.met')
Mangement=[{'Action':'Fertiliser','Date':'2017-01-14T00:00:00','FertiliserType':'UreaN','Amount':40}]


Operations = Operations(Operation=Mangement)
Manger = Manager(Code=Code,Parameters=Parameters)

Zone.add(Soil)
Zone.add(SurfaceOrganicMatter)
Zone.add(MicroClimate)
Zone.add(Irrigation)
Zone.add(Fertiliser)
Zone.add(Plant)
Zone.add(Operations)
Zone.add(Manger)
Zone.add(Report)

#==================
# Replacements = Replacements()
# Cultivar = Cultivar(Name='Rua',Command=ICultivar)
# Replacements.add(Cultivar)
# Simulations.add(Replacements)
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



Simulations.save(path='E:/APSIM/Examples/aaa.apsimx')


