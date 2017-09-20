from datetime import datetime as dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .utils import *

plt.style.use("ggplot")
plt.rcParams["font.size"] = 13
plt.rcParams["figure.figsize"] = 16, 10

class Plotter(Config):
    def __init__(self):
        super().__init__()
        df = pd.read_csv(self.path_to_csv + "event.csv")
        self.df = self._clean(df)

        self.dtrange = self._dtrange()
        self.today = what_is_the_date_today()

    def _clean(self, df):
        df = df.sort_values(by=['_timestamp'], ascending=True)
        df._timestamp = pd.DatetimeIndex(df._timestamp)
        df = df.reset_index(drop=True)
        return df

    def _dtrange(self):
        """ make datetime range list based on Event data
        """
        start = self.df._timestamp.iloc[0]
        end = self.df._timestamp.iloc[-1]
        dtrange = pd.date_range(start=start, end=end, freq='D')
        return dtrange

    def plot(self):
        act_asset_df, pred_asset_df = self._asset()
        act_inbank_df, pred_inbank_df = self._bank()
        act_inlocal_df, pred_inlocal_df = self._local()
        act_inwallet_df, pred_inwallet_df = self._wallet()

        fig = plt.figure()
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        ax3 = fig.add_subplot(223)
        ax4 = fig.add_subplot(224)

        # --- Asset ---
        act_asset_df.asset.plot(ax=ax1, label="Asset")
        act_asset_df.income.plot(ax=ax1, label="Income")
        act_asset_df.outgo.plot(ax=ax1, label="Outgo")
        if pred_asset_df.size > 0:
            asset_last = pred_asset_df.asset[-1]
            asset_annotation = str(asset_last)
            pred_asset_df.asset.plot(ax=ax1, linestyle='dashed', label="__nolegend__")
            pred_asset_df.income.plot(ax=ax1, linestyle='dashed', label="__nolegend__")
            pred_asset_df.outgo.plot(ax=ax1, linestyle='dashed', label="__nolegend__")
        else:
            asset_last = act_asset_df.asset[-1]
            asset_annotation = str(asset_last)
        ax1.set_title("Asset: {}".format(asset_annotation))
        ax1.legend()

        # --- in Bank ---
        act_inbank_df.inbank.plot(ax=ax2, label="in Bank")
        act_inbank_df.income.plot(ax=ax2, label="Income")
        act_inbank_df.outgo.plot(ax=ax2, label="Outgo")
        if pred_inbank_df.size > 0:
            inbank_last = pred_inbank_df.inbank[-1]
            inbank_annotation = str(inbank_last)
            pred_inbank_df.inbank.plot(ax=ax2, linestyle='dashed', label="__nolegend__")
            pred_inbank_df.income.plot(ax=ax2, linestyle='dashed', label="__nolegend__")
            pred_inbank_df.outgo.plot(ax=ax2, linestyle='dashed', label="__nolegend__")
        else:
            inbank_last = act_inbank_df.inbank[-1]
            inbank_annotation = str(inbank_last)
        ax2.set_title("in Bank: {}".format(inbank_annotation))
        ax2.legend()

        # --- in Local ---
        act_inlocal_df.inlocal.plot(ax=ax3, label="in Local")
        act_inlocal_df.income.plot(ax=ax3, label="Income")
        act_inlocal_df.outgo.plot(ax=ax3, label="Outgo")
        if pred_inlocal_df.size > 0:
            inlocal_last = pred_inlocal_df.inlocal[-1]
            inlocal_annotation = str(inlocal_last)
            pred_inlocal_df.inlocal.plot(ax=ax3, linestyle='dashed', label="__nolegend__")
            pred_inlocal_df.income.plot(ax=ax3, linestyle='dashed', label="__nolegend__")
            pred_inlocal_df.outgo.plot(ax=ax3, linestyle='dashed', label="__nolegend__")
        else:
            inlocal_last = act_inlocal_df.inlocal[-1]
            inlocal_annotation = str(inlocal_last)
        ax3.set_title("in Local: {}".format(inlocal_annotation))
        ax3.legend()

        # --- in Wallet ---
        act_inwallet_df.inwallet.plot(ax=ax4, label="in Wallet")
        act_inwallet_df.income.plot(ax=ax4, label="Income")
        act_inwallet_df.outgo.plot(ax=ax4, label="Outgo")
        if pred_inwallet_df.size > 0:
            inwallet_last = pred_inwallet_df.inwallet[-1]
            inwallet_annotation = str(inwallet_last)
            pred_inwallet_df.inwallet.plot(ax=ax4, linestyle='dashed', label="__nolegend__")
            pred_inwallet_df.income.plot(ax=ax4, linestyle='dashed', label="__nolegend__")
            pred_inwallet_df.outgo.plot(ax=ax4, linestyle='dashed', label="__nolegend__")
        else:
            inwallet_last = act_inwallet_df.inwallet[-1]
            inwallet_annotation = str(inwallet_last)
        ax4.set_title("in Wallet: {}".format(inwallet_annotation))
        ax4.legend()

        plt.tight_layout()
        plt.show()

    def _asset(self):
        dtrange = self.dtrange
        asset = np.zeros((dtrange.size, 3), dtype=np.int)
        for i, date in enumerate(dtrange):
            # Extract the dataframe of target date
            spec_df = self.df[self.df._timestamp == date]

            income_series = spec_df[spec_df._kind == "income"]
            income = income_series._howmuch.sum()

            outgo_series = spec_df[spec_df._kind == "outgo"]
            outgo = outgo_series._howmuch.sum()

            asset[i, :] = [income, outgo, income-outgo]
        asset[:, 2] = np.cumsum(asset[:, 2])
        asset_df = pd.DataFrame(asset,
                                index=dtrange,
                                columns=['income', 'outgo', 'asset'])
        today = pd.to_datetime(self.today)

        act_asset_df = asset_df[asset_df.index <= today]
        pred_asset_df = asset_df[asset_df.index > today]

        return act_asset_df, pred_asset_df

    def _bank(self):
        dtrange = self.dtrange

        inbank_df = self.df[(self.df._from == "bank") | (self.df._to == "bank")]
        inbank = np.zeros((dtrange.size, 3), dtype=np.int)
        for i, date in enumerate(dtrange):
            # Extract the dataframe of target date
            spec_df = inbank_df[inbank_df._timestamp == date]

            income_series = spec_df[spec_df._to == "bank"]
            income = income_series._howmuch.sum()

            outgo_series = spec_df[spec_df._from == "bank"]
            outgo = outgo_series._howmuch.sum()

            inbank[i, :] = [income, outgo, income-outgo]
        inbank[:, 2] = np.cumsum(inbank[:, 2])
        inbank_df = pd.DataFrame(inbank,
                                 index=dtrange,
                                 columns=['income', 'outgo', 'inbank'])
        today = pd.to_datetime(self.today)
        act_inbank_df = inbank_df[inbank_df.index <= today]
        pred_inbank_df = inbank_df[inbank_df.index > today]

        return act_inbank_df, pred_inbank_df

    def _local(self):
        dtrange = self.dtrange

        inlocal_df = self.df[(self.df._from == "local") | (self.df._to == "local")]
        inlocal = np.zeros((dtrange.size, 3), dtype=np.int)
        for i, date in enumerate(dtrange):
            # Extract the dataframe of target date
            spec_df = inlocal_df[inlocal_df._timestamp == date]

            income_series = spec_df[spec_df._to == "local"]
            income = income_series._howmuch.sum()

            outgo_series = spec_df[spec_df._from == "local"]
            outgo = outgo_series._howmuch.sum()

            inlocal[i, :] = [income, outgo, income-outgo]
        inlocal[:, 2] = np.cumsum(inlocal[:, 2])
        inlocal_df = pd.DataFrame(inlocal,
                                  index=dtrange,
                                  columns=['income', 'outgo', 'inlocal'])
        today = pd.to_datetime(self.today)
        act_inlocal_df = inlocal_df[inlocal_df.index <= today]
        pred_inlocal_df = inlocal_df[inlocal_df.index > today]

        return act_inlocal_df, pred_inlocal_df

    def _wallet(self):
        dtrange = self.dtrange

        inwallet_df = self.df[(self.df._from == "wallet") | (self.df._to == "wallet")]
        inwallet = np.zeros((dtrange.size, 3), dtype=np.int)
        for i, date in enumerate(dtrange):
            # Extract the dataframe of target date
            spec_df = inwallet_df[inwallet_df._timestamp == date]

            income_series = spec_df[spec_df._to == "wallet"]
            income = income_series._howmuch.sum()

            outgo_series = spec_df[spec_df._from == "wallet"]
            outgo = outgo_series._howmuch.sum()

            inwallet[i, :] = [income, outgo, income-outgo]
        inwallet[:, 2] = np.cumsum(inwallet[:, 2])
        inwallet_df = pd.DataFrame(inwallet,
                                   index=dtrange,
                                   columns=['income', 'outgo', 'inwallet'])
        today = pd.to_datetime(self.today)
        act_inwallet_df = inwallet_df[inwallet_df.index <= today]
        pred_inwallet_df = inwallet_df[inwallet_df.index > today]

        return act_inwallet_df, pred_inwallet_df
