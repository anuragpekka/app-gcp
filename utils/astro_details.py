from .vedicastro.VedicAstro import VedicHoroscopeData
import polars as pl
import json


class AstroDetails:
    def __init__(self,year,month,day,hour,minute,second,lat,lon):
        self.vhd = VedicHoroscopeData(year = year, month = month, day = day, hour = hour, minute = minute, second = second, 
                        latitude = lat, longitude = lon, ayanamsa = "Krishnamurti_Senthilathiban", house_system = "Placidus")
        self.chart = self.vhd.generate_chart()
        self.planets_data = self.vhd.get_planets_data_from_chart(self.chart)
        self.houses_data = self.vhd.get_houses_data_from_chart(self.chart)
        
    def planet_details(self):
        planets_df = pl.DataFrame(self.planets_data)
        planets_df = planets_df.rename({"Object":"Planet"})
        return json.dumps(planets_df.to_dicts())
        
    def house_details(self):
        houses_df = pl.DataFrame(self.houses_data)
        return json.dumps(houses_df.drop("Object").to_dicts())
    
    def planet_signifactors(self):
        planets_significators_table = self.vhd.get_planet_wise_significators(self.planets_data, self.houses_data)
        planets_significators_df = pl.DataFrame(planets_significators_table)
        return json.dumps(planets_significators_df.to_dicts())
    
    def house_signifactors(self):
        house_significators_table = self.vhd.get_house_wise_significators(self.planets_data, self.houses_data)
        house_significators_df = pl.DataFrame(house_significators_table)
        return json.dumps(house_significators_df.to_dicts())

    def dashas(self):
        vimshottari_dasa = self.vhd.compute_vimshottari_dasa(self.chart)
        return json.dumps(vimshottari_dasa)
    
    def planetory_aspect(self):
        planetary_aspects = self.vhd.get_planetary_aspects(self.chart)
        planetary_aspects_df = pl.DataFrame(planetary_aspects)
        return json.dumps(planetary_aspects_df.to_dicts())
    
    def planet_transit(self):
        transit_details = self.vhd.get_transit_details()
        transit_df = pl.DataFrame(transit_details)
        return json.dumps(transit_df.to_dicts())

    def astrology_chart_details(self):
        chart_details = '{'
        chart_details += f'"planet_data": {self.planet_details()},'
        chart_details += f'"planet_signifactors": {self.planet_signifactors()},'
        chart_details += f'"planetary_aspects": {self.planetory_aspect()},'
        chart_details += f'"planet_transits": {self.planet_transit()},'
        chart_details += f'"house_data": {self.house_details()},'
        chart_details += f'"house_signifactors": {self.house_signifactors()},'
        chart_details += f'"vimshottari_dasa": {self.dashas()}'
        chart_details += '}'

        return chart_details
