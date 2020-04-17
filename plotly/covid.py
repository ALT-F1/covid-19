from country_continent_codes import CountryContinentCodes
from datetime import datetime, timedelta
import inspect
import logging
import numpy as np
import pandas as pd
import urllib.error
import urllib.request

"""# Load the LATEST data from the European Center for Disease Prevention and Control (ECDC)"""


"""
    helpers
"""


class Utils:

    """
        check if an url exists
    """
    @classmethod
    def check_if_data_source_exists(cls, url):
        url_exists = False
        try:
            conn = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            # ...
            # print('HTTPError: {}, the file does not exist'.format(e.code))
            url_exists = False
        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            # ...
            print('URLError: {}'.format(e.reason))
            url_exists = False
        else:
            # 200
            # ...
            print(f'Data source is : {url}')
            url_exists = True
        return (url_exists), url


class ECDC:

    def __init__(self):
        logging.info(f"{'='*25} {inspect.currentframe().f_code.co_name}")

        # load the data
        self.df = self.extract_datasource()
        self.df = self.transform_add_columns(self.df)
        

    """
        extract transform and load the data from the country continent codes list
    """
    def load_country_continent_codes(self):
        logging.info(f"{'='*25} {inspect.currentframe().f_code.co_name}")

        return CountryContinentCodes().cleanse(), CountryContinentCodes().map()

    """
        Add a column 'continent' mapping the country with its continent
        Add columns 'cases_sum_to_date', 'deaths_sum_to_date', 'cases_growth'
    """

    def transform_add_columns(self, df):
        logging.info(f"{'='*25} {inspect.currentframe().f_code.co_name}")
        self.country_continent_codes_df, self.alpha3_region_map = self.load_country_continent_codes()
        df['continent'] = df['countryterritoryCode'].map(
            self.alpha3_region_map)
        df = self.add_columns_with_growth(df, periods=1)
        df['dateRep_str'] = df["dateRep"].astype(str)
        return df

    def add_columns_with_growth(self, df, periods=1):
        logging.info(f"{'='*25} {inspect.currentframe().f_code.co_name}")
        countries =  df['countriesAndTerritories'].unique()
        print(f"uniques countries : {len(countries)}")
        for country in countries:
            df_growth = df[
                df["countriesAndTerritories"] == country].copy(deep=True)
            df_growth = df_growth.sort_values(
                by=["dateRep"],
                ascending=True
            )
            df_growth['cases_sum_to_date'] = df_growth['cases'].cumsum()
            df_growth['deaths_sum_to_date'] = df_growth['deaths'].cumsum()
            df_growth['cases_growth'] = df_growth['cases_sum_to_date'].pct_change(
                periods=periods, fill_method='pad')
            df_growth['deaths_growth'] = df_growth['deaths_sum_to_date'].pct_change(
                periods=periods, fill_method='pad')
            df = df.append(df_growth,ignore_index=True)
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.dropna()
        return df
    """
        load the data from the ECDC
    """

    def extract_datasource(self):
        logging.info(f"{'='*25} {inspect.currentframe().f_code.co_name}")

        datasource_url_template = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-%latest_datasource_date%"

        datasource_url = self.find_latest_datasource(datasource_url_template)

        if datasource_url is None:
            raise Exception(
                f'There is no datasource on the ECDC website. is https://www.ecdc.europa.eu down?')

        # read the data from the excel sheet
        return pd.read_excel(datasource_url)

    """
        find the latest datasource starting today from the ECDC website

        format of the url: 
            https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-17.xlsx

            https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-%latest_datasource_date%.xlsx

    """

    def find_latest_datasource(self, url):
        is_found = False
        i = -1
        while is_found == False and i < 5:
            i += 1
            latest_datasource_date = (
                datetime.now() - timedelta(i)).strftime('%Y-%m-%d')
            datasource_url = url.replace(
                '%latest_datasource_date%',
                latest_datasource_date
            )
            # print(f'Search for this latest date: {latest_datasource_date}',
            #      f'datasource_url: {datasource_url}')
            is_found, existing_datasource_date = Utils.check_if_data_source_exists(
                datasource_url + ".xls"
            )
            if is_found == False:
                is_found, existing_datasource_date = Utils.check_if_data_source_exists(
                    datasource_url + ".xlsx"
                )

        if is_found == True:
            print(f'Latest date is : {latest_datasource_date}')
            return existing_datasource_date
        else:
            return None

    def data(self):
        return self.df


class DATA:
    def __init__(self):
        logging.info(f"{'='*25} {inspect.currentframe().f_code.co_name}")
        self._ecdc = ECDC()

    def ecdc(self):
        logging.info(f"{'='*25} {inspect.currentframe().f_code.co_name}")
        return self._ecdc.df


class COVID:
    def __init__(self):
        self.data = DATA()


if __name__ == "__main__":
    covid = COVID()
    print(f"ECDC DataFrame head:\n{covid.data.ecdc().head(3)}")
    print(f"ECDC DataFrame tail:\n{covid.data.ecdc().tail(3)}")
