# -*- coding: gbk -*-
__author__ = 'wxy'
__time__ = '10/19/2021 11:08'

import ujson as json
import jsonpath_ng as jsonpath
from jsonpath_ng.ext import  parse
from jsonpath_ng.jsonpath import Fields
from jsonpath_ng.jsonpath import Slice
import jmespath
class build_apsimx():
   def __init__(self, task='Models.Core.Simulations, Models',
                           Version='0.0.0.0',
                           ExplorerWidth='259',
                           simulation_name='Simulations',
                           Children=[],
                           IncludeInDocumentation=True,
                           Enabled=True,
                           ReadOnly=True):
     self.Models = {}
     self.Models['$type'] = task
     self.Models['ExplorerWidth'] = ExplorerWidth
     self.Models['Version'] = Version
     self.Models['Name'] = simulation_name
     self.Models['Children'] = Children
     self.Models['IncludeInDocumentation'] = IncludeInDocumentation
     self.Models['Enabled'] = Enabled
     self.Models['ReadOnly'] = ReadOnly

   def add_node(self,node_routing,node_context):
     expression = parse(node_routing)
     # print(expression)
     expression.update_or_create(self.Models,node_context)

     return  self.Models

if __name__ == '__main__':
        start="1900-01-01T00:00:00"
        end="2000-12-31T00:00:00"
        weather_path='%root%\\Examples\\WeatherFiles\\Dalby.met'
        VariableNames=[
                "[Clock].Today",
                "[Clock].Today.DayOfYear",
                "[Wheat].Phenology.Zadok.Stage",
                "[Wheat].Phenology.CurrentStageName",
                "[Wheat].AboveGround.Wt",
                "[Wheat].AboveGround.N",
                "[Wheat].Grain.Total.Wt*10 as Yield",
                "[Wheat].Grain.Protein",
                "[Wheat].Grain.Size",
                "[Wheat].Grain.Number",
                "[Wheat].Grain.Total.Wt",
                "[Wheat].Grain.Total.N",
                "[Wheat].Total.Wt"
              ]
        model = build_apsimx(simulation_name='test')
        # add Models.Core.Simulations
        # 二级节点
        model.add_node(node_routing='Children[0]."$type"',node_context='Models.Core.Simulations, Models')
        model.add_node(node_routing='Children[0].IsRunning', node_context=False)
        model.add_node(node_routing='Children[0].Name', node_context='Simulation')
        model.add_node(node_routing='Children[0].Descriptors', node_context=None)
        # add Models.Clock
        # 三级节点第一个切片
        model.add_node(node_routing='Children[0].Children[0]."$type"', node_context='Models.Clock, Models')
        model.add_node(node_routing='Children[0].Children[0].Start', node_context=start)
        model.add_node(node_routing='Children[0].Children[0].End', node_context=end)
        model.add_node(node_routing='Children[0].Children[0].Name', node_context="Clock")
        model.add_node(node_routing='Children[0].Children[0].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[0].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[0].ReadOnly', node_context=False)
        # add Models.Summary
        # 三级节点第二个切片
        model.add_node(node_routing='Children[0].Children[1]."$type"', node_context='Models.Summary, Models')
        model.add_node(node_routing='Children[0].Children[1].CaptureErrors', node_context=True)
        model.add_node(node_routing='Children[0].Children[1].CaptureWarnings', node_context=True)
        model.add_node(node_routing='Children[0].Children[1].CaptureSummaryText', node_context=True)
        model.add_node(node_routing='Children[0].Children[1].Name', node_context="SummaryFile")
        model.add_node(node_routing='Children[0].Children[1].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[1].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[1].ReadOnly', node_context=False)
        # add Models.Climate.Weather
        #三级节点第三个切片
        model.add_node(node_routing='Children[0].Children[2]."$type"', node_context='Models.Climate.Weather, Models')
        model.add_node(node_routing='Children[0].Children[2].ConstantsFile', node_context=None)
        model.add_node(node_routing='Children[0].Children[2].FileName', node_context=weather_path)
        model.add_node(node_routing='Children[0].Children[2].ExcelWorkSheetName', node_context=None)
        model.add_node(node_routing='Children[0].Children[2].Name', node_context="Weather")
        model.add_node(node_routing='Children[0].Children[2].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[2].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[2].ReadOnly', node_context=False)
        # add Models.Soils.Arbitrator.SoilArbitrator
        #三级节点第四个切片
        model.add_node(node_routing='Children[0].Children[3]."$type"', node_context='Models.Soils.Arbitrator.SoilArbitrator, Models')
        model.add_node(node_routing='Children[0].Children[3].Name', node_context="SoilArbitrator")
        model.add_node(node_routing='Children[0].Children[3].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[3].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[3].ReadOnly', node_context=False)
        # add Models.Core.Zone
        #三级节点第五个切片
        model.add_node(node_routing='Children[0].Children[4]."$type"', node_context='Models.Core.Zone, Models')
        model.add_node(node_routing='Children[0].Children[4].Area', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Slope', node_context=weather_path)
        model.add_node(node_routing='Children[0].Children[4].AspectAngle', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Altitude', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Name', node_context="Weather")
        # add Models.Report
        #四级节点第一个切片
        model.add_node(node_routing='Children[0].Children[4].Children[0]."$type"', node_context='Models.Report, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[0]."VariableNames', node_context=VariableNames)
        model.add_node(node_routing='Children[0].Children[4].Children[0].EventNames', node_context="[Wheat].Harvesting")
        model.add_node(node_routing='Children[0].Children[4].Children[0].GroupByVariableName', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[0].Name', node_context="Report")
        model.add_node(node_routing='Children[0].Children[4].Children[0].Children', node_context=[])
        model.add_node(node_routing='Children[0].Children[4].Children[0].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[0].ReadOnly', node_context=False)
        # add Models.Fertiliser
        #四级节点第二个切片
        model.add_node(node_routing='Children[0].Children[4].Children[1]."$type"', node_context='Models.Fertiliser, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[1].ResourceName', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[1].Name', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[1].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[1].ReadOnly', node_context=False)
        # add Models.Soils.Soil
        #四级节点第三个切片
        model.add_node(node_routing='Children[0].Children[4].Children[2]."$type"', node_context='Models.Soils.Soil, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].RecordNumber', node_context=0)
        model.add_node(node_routing='Children[0].Children[4].Children[2].ASCOrder', node_context='Vertosol')
        model.add_node(node_routing='Children[0].Children[4].Children[2].ASCSubOrder', node_context='Black')
        model.add_node(node_routing='Children[0].Children[4].Children[2].SoilType', node_context='Clay')
        model.add_node(node_routing='Children[0].Children[4].Children[2].LocalName', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Site', node_context='Norwin')
        model.add_node(node_routing='Children[0].Children[4].Children[2].NearestTown', node_context='Norwin')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Region', node_context='Darling Downs and Granite Belt')
        model.add_node(node_routing='Children[0].Children[4].Children[2].State', node_context='Queensland')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Country', node_context='Australia')
        model.add_node(node_routing='Children[0].Children[4].Children[2].NaturalVegetation', node_context='Qld. Bluegrass, possible Qld. Blue gum')
        model.add_node(node_routing='Children[0].Children[4].Children[2].ApsoilNumber', node_context='900')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Latitude', node_context=-27.581836)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Longitude', node_context=151.320206)
        model.add_node(node_routing='Children[0].Children[4].Children[2].LocationAccuracy', node_context=" +/- 20m")
        model.add_node(node_routing='Children[0].Children[4].Children[2].YearOfSampling', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].DataSource', node_context="CSIRO Sustainable Ecosystems, Toowoomba; Characteriesd as part of the GRDC funded project\"Doing it better, doing it smarter, managing soil water in Australian agriculture' 2011")
        model.add_node(node_routing='Children[0].Children[4].Children[2].Comments', node_context='OC, CLL for all crops estimated-based on Bongeen Mywybilla Soil No1')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Name', node_context='Soil')
        # add Models.Soils.Physical
        #五级节点第一个切片
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0]."$type"', node_context='Models.Soils.Physical, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Depth', node_context=depth)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Thickness', node_context='Thickness')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].ParticleSizeClay', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].ParticleSizeSand', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].ParticleSizeSilt', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Rocks', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Texture', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].BD', node_context=BD)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].AirDry', node_context=AirDry)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].LL15', node_context=LL15)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].DUL', node_context=DUL)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].SAT', node_context=SAT)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].KS', node_context=KS)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].BDMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].AirDryMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].LL15Metadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].DULMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].SATMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].KSMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].RocksMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].TextureMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].ParticleSizeSandMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].ParticleSizeSiltMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].ParticleSizeClayMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Name', node_context='Physical')
        # add Models.Soils.SoilCrop, Models
        # 六级节点第一个切片
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0]."$type"', node_context='Models.Soils.SoilCrop, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].LL', node_context=LL)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].KL', node_context=KL)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].XF', node_context=XF)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].LLMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].KLMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].XFMetadata', node_context=None)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].Name', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[0].Children[0].ReadOnly', node_context=False)
        # add Models.WaterModel.WaterBalance
        # 五级节点第二个切片
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1]."$type"',node_context='Models.WaterModel.WaterBalance, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].SummerDate', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].SummerU',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].SummerCona',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].WinterDate',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].WinterU',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].WinterCona', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].DiffusConst',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].DiffusSlope', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].Salb', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].CN2Bare', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].CNRed', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].CNCov', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].DischargeWidth', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].CatchmentArea',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].Thickness',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].SWCON',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].KLAT',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].ResourceName',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].Name',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].Enabled',node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[1].ReadOnly',node_context=False)
        # add Models.Soils.Organic
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2]."$type"',node_context='Models.Soils.Organic, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].Depth',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].FOMCNRatio',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].Thickness',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].Carbon',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].SoilCNRatio',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].FBiom',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].FInert', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].FOM', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].CarbonMetadata', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].FOMMetadata', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].CarbonMetadata', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].Name',node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].Children',node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].Enabled',node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[2].ReadOnly',node_context=False)
        # add Models.Soils.Chemical
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3]."$type"',node_context='Models.Soils.Chemical, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].Depth',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].Thickness',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].NO3N',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].NH4N',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].PH',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].CL',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].EC', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].ESP', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].LabileP', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].UnavailableP', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].ECMetadata', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].ESPMetadata',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].PHMetadata',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].Name',node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].Children',node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].Enabled',node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[3].ReadOnly',node_context=False)
        # add Models.Soils.InitialWater
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4]."$type"',node_context='Models.Soils.InitialWater, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].PercentMethod', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].FractionFull',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].DepthWetSoil', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].RelativeTo', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].Name', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[4].ReadOnly', node_context=False)
        # add Models.Soils.Sample
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5]."$type"',node_context='Models.Soils.Sample, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].Depth',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].Thickness',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].NO3',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].NH4',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].LabileP',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].SW',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].OC', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].EC', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].CL', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].ESP', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].PH', node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].SWUnits',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].OCUnits',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].PHUnits',node_context='Fertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].Name',node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].Children',node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].Enabled',node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[5].ReadOnly',node_context=False)
        # add Models.Soils.CERESSoilTemperature
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[6]."$type"',node_context='Models.Soils.CERESSoilTemperature, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[6].Name', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[6].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[6].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[6].ReadOnly', node_context=False)
        # add Models.Soils.Nutrients.Nutrient
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[7]."$type"',node_context='Models.Soils.Nutrients.Nutrient, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[7].ResourceName', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[7].Name', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[7].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[2].Children[7].ReadOnly', node_context=False)
        # add Models.Surface.SurfaceOrganicMatter
        model.add_node(node_routing='Children[0].Children[4].Children[3]."$type"',node_context='Models.Surface.SurfaceOrganicMatter, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[3].InitialResidueName', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].InitialResidueType', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].InitialResidueMass', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].InitialStandingFraction', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].InitialCPR', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].InitialCNR', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].ResourceName',node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].Name', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[3].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[3].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[3].ReadOnly', node_context=False)
        # add Models.PMF.Plant, Models
        model.add_node(node_routing='Children[0].Children[4].Children[4]."$type"',node_context='Models.PMF.Plant, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[4].ResourceName', node_context='WheatSoil')
        model.add_node(node_routing='Children[0].Children[4].Children[4].Name', node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[4].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[4].ReadOnly', node_context=False)
        # add Models.MicroClimate, Models
        model.add_node(node_routing='Children[0].Children[4].Children[5]."$type"',node_context='Models.MicroClimate, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[5].a_interception', node_context=0)
        model.add_node(node_routing='Children[0].Children[4].Children[5].b_interception', node_context=1)
        model.add_node(node_routing='Children[0].Children[4].Children[5].c_interception', node_context=0)
        model.add_node(node_routing='Children[0].Children[4].Children[5].d_interception', node_context=0)
        model.add_node(node_routing='Children[0].Children[4].Children[5].SoilHeatFluxFraction', node_context=0.4)
        model.add_node(node_routing='Children[0].Children[4].Children[5].MinimumHeightDiffForNewLayer', node_context=0.0)
        model.add_node(node_routing='Children[0].Children[4].Children[5].NightInterceptionFraction',node_context=0.5)
        model.add_node(node_routing='Children[0].Children[4].Children[5].ReferenceHeight',node_context=2.0)
        model.add_node(node_routing='Children[0].Children[4].Children[5].Name', node_context='MicroClimate')
        model.add_node(node_routing='Children[0].Children[4].Children[5].Children', node_context='[]')
        model.add_node(node_routing='Children[0].Children[4].Children[5].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[5].ReadOnly', node_context=False)
        # add Models.Manager, Models
        model.add_node(node_routing='Children[0].Children[4].Children[6]."$type"',node_context='Models.Manager, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[6].Code', node_context=code1)
        model.add_node(node_routing='Children[0].Children[4].Children[6].Parameters', node_context=parameter1)
        model.add_node(node_routing='Children[0].Children[4].Children[6].Name', node_context='SowingFertiliser')
        model.add_node(node_routing='Children[0].Children[4].Children[6].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[6].ReadOnly', node_context=False)
        # add Models.Manager, Models
        model.add_node(node_routing='Children[0].Children[4].Children[7]."$type"',node_context='Models.Manager, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[7].Code', node_context=code2)
        model.add_node(node_routing='Children[0].Children[4].Children[7].Parameters', node_context=parameter2)
        model.add_node(node_routing='Children[0].Children[4].Children[7].Name', node_context='Harvest')
        model.add_node(node_routing='Children[0].Children[4].Children[7].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[7].ReadOnly', node_context=False)
        # add Models.Manager, Models
        model.add_node(node_routing='Children[0].Children[4].Children[8]."$type"',node_context='Models.Manager, Models')
        model.add_node(node_routing='Children[0].Children[4].Children[8].Code', node_context=code3)
        model.add_node(node_routing='Children[0].Children[4].Children[8].Parameters', node_context=parameter3)
        model.add_node(node_routing='Children[0].Children[4].Children[8].Name', node_context='SowingRule1')
        model.add_node(node_routing='Children[0].Children[4].Children[8].Enabled', node_context=True)
        model.add_node(node_routing='Children[0].Children[4].Children[8].ReadOnly', node_context=False)
        # add Models.Storage.DataStore, Models
        model.add_node(node_routing='Children[1]."$type"', node_context='Models.Storage.DataStore, Models')
        model.add_node(node_routing='Children[1].useFirebird', node_context=False)
        model.add_node(node_routing='Children[1].CustomFileName', node_context=None)
        model.add_node(node_routing='Children[1].Name', node_context='DataStore')
        model.add_node(node_routing='Children[1].Children', node_context='[]')
        model.add_node(node_routing='Children[1].Enabled', node_context=True)
        model.add_node(node_routing='Children[1].ReadOnly', node_context=False)
        print(model.Models)
# model.add_node(node_routing)
# if __name__ == '__main__':
#     ApsimClient=ApsimClient()
# model = build_apsimx()

# print(model.add_node)
# with open('E:\APSIM\Examples/Wheat.apsimx') as f:
#     lines =f.read()
#     res=json.loads(lines)
#     type = jmespath.search('"$type"',res)
#     ExplorerWidth = jmespath.search('ExplorerWidth', res)
#     Version = jmespath.search('Version', res)
#     Name = jmespath.search('Name', res)
#     Children = jmespath.search('Children', res)
#     Enabled = jmespath.search('Enabled', res)
#     ReadOnly = jmespath.search('ReadOnly', res)
#     for k,v in res.items():
#         print(k,v)
    # for i in range(len(Children)):
    #     Children1 = jmespath.search('[%s]'%(str(i)), Children)
    #     print(Children1)