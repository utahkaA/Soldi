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

    def _plot(self, ax, act_df, pred_df, kind):
        colors = {"asset": "#cc2e41", "income": "#412ecc", "outgo": "#2ecc41"}
        labels = {"income": "Income", "outgo": "Outgo"}

        # check actually last value.
        act_last = act_df.asset[-1]
        act_annotation = str(act_last)
        for col in act_df.columns:
            color = colors[col]
            label = labels[col] if col in labels else kind
            act_df[col].plot(ax=ax, color=color, label=label)

        if pred_df.size > 0:
            # check predict asset's last value.
            pred_last = pred_df.asset[-1]
            pred_annotation = str(pred_last)
            for col in pred_df.columns:
                color = colors[col]
                label = labels[col] if col in labels else kind
                pred_df[col].plot(ax=ax, color=color, linestyle="dashed",
                                  label="__nolegend__")
            title = "Asset: {0} (Pred: {1})".format(act_annotation,
                                                    pred_annotation)
        else:
            title = "Asset: {0}".format(act_annotation)
        ax.set_title(title)
        ax.legend()

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

        self._plot(ax1, act_asset_df, pred_asset_df, kind="Asset")
        self._plot(ax2, act_inbank_df, pred_inbank_df, kind="in Bank")
        self._plot(ax3, act_inlocal_df, pred_inlocal_df, kind="in Local")
        self._plot(ax4, act_inwallet_df, pred_inwallet_df, kind="in Wallet")

        plt.tight_layout()
        figure_name = "{0}/{1}.png".format(self.path_to_figure, self.today)
        plt.savefig(figure_name)

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
        pred_asset_df = asset_df[asset_df.index >= today]

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
                                 columns=['income', 'outgo', 'asset'])
        today = pd.to_datetime(self.today)
        act_inbank_df = inbank_df[inbank_df.index <= today]
        pred_inbank_df = inbank_df[inbank_df.index >= today]

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
                                  columns=['income', 'outgo', 'asset'])
        today = pd.to_datetime(self.today)
        act_inlocal_df = inlocal_df[inlocal_df.index <= today]
        pred_inlocal_df = inlocal_df[inlocal_df.index >= today]

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
                                   columns=['income', 'outgo', 'asset'])
        today = pd.to_datetime(self.today)
        act_inwallet_df = inwallet_df[inwallet_df.index <= today]
        pred_inwallet_df = inwallet_df[inwallet_df.index >= today]

        return act_inwallet_df, pred_inwallet_df
