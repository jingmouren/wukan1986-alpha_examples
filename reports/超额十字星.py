"""
2016.05.12 方正证券 夜空中最亮的星：十字星形态的选股研究

（1）实体柱长度<h;
（2）上影线长度>(a*实体柱长度);
（3）下影线长度>(b*实体柱长度)。

"""
import multiprocessing
import pathlib

import pandas as pd
import polars as pl
from loguru import logger

INPUT1_PATH = pathlib.Path(r"D:\data\jqresearch\get_price_stock_minute")
INPUT2_PATH = pathlib.Path(r"D:\data\jqresearch\get_price_index_minute")


def path_groupby_date(input_path: pathlib.Path) -> pd.DataFrame:
    """将文件名中的时间提取出来"""
    files = list(input_path.glob(f'*'))

    # 提取文件名中的时间
    df = pd.DataFrame([f.name.split('.')[0].split("__") for f in files], columns=['start', 'end'])
    df['path'] = files
    df['key1'] = pd.to_datetime(df['start'])
    df['key2'] = df['key1']
    df.index = df['key1'].copy()
    df.index.name = 'date'  # 防止无法groupby
    return df


_ = (r"close",)
(close,) = (pl.col(i) for i in _)

_ = (r"R",)
(R,) = (pl.col(i) for i in _)

_DATE_ = "date"
_ASSET_ = "asset"


def func_0_ts__asset(df: pl.DataFrame) -> pl.DataFrame:
    df = df.sort(by=[_DATE_])
    # ========================================
    df = df.with_columns(
        # TODO 偷懒了，没有用昨收价，因为还要复权
        R=pl.col("close") / pl.col("open").first() - 1,
    )
    return df


def func_1_ts__asset(df: pl.DataFrame) -> pl.DataFrame:
    df = df.select(
        pl.col('date'),
        pl.col("asset"),
        excess=pl.col("R") - pl.col("R_index")
    )
    df = df.select(
        pl.col('date').first(),
        pl.col("asset").first(),
        open=pl.col("excess").first(),
        high=pl.col("excess").max(),
        low=pl.col("excess").min(),
        close=pl.col("excess").last(),
    )
    return df


def get_returns(df: pl.DataFrame) -> pl.DataFrame:
    df = df.group_by(_ASSET_).map_groups(func_0_ts__asset)
    return df


def get_excess(df: pl.DataFrame) -> pl.DataFrame:
    df = df.group_by(_ASSET_).map_groups(func_1_ts__asset)
    return df


def get_doji(df: pl.DataFrame) -> pl.DataFrame:
    df = df.with_columns(
        real_body=(pl.col("close") - pl.col("open")).abs(),
        up_shadow=pl.col("high") - pl.max_horizontal(pl.col("open"), pl.col("close")),
        down_shadow=pl.min_horizontal(pl.col("open"), pl.col("close")) - pl.col("low"),
    )
    return df


def func_2files(idx_row):
    idx, row = idx_row
    logger.info(idx)
    df1 = pl.read_parquet(row['path_x']).rename({"code": "asset", "time": "date", "money": "amount"})
    df2 = pl.read_parquet(row['path_y']).rename({"code": "asset", "time": "date", "money": "amount"})
    df1 = get_returns(df1)
    df2 = get_returns(df2.filter(pl.col("asset") == "000001.XSHG"))
    dd = df1.join(df2, on="date", suffix='_index')
    d1 = get_excess(dd)
    return d1


if __name__ == '__main__':
    f1 = path_groupby_date(INPUT1_PATH)
    f2 = path_groupby_date(INPUT2_PATH)
    ff = pd.merge(f1, f2, left_index=True, right_index=True, how='left')
    # 过滤日期
    ff = ff["2023-01":]

    logger.info("start")

    with multiprocessing.Pool(4) as pool:
        # pandas按月分组
        output = list(pool.map(func_2files, list(ff.iterrows())))
        # polars合并
        output = pl.concat(output)
        output = output.with_columns(pl.col("date").dt.truncate("1d"))
        output = get_doji(output)
        output.write_parquet("超额十字星.parquet")
        print(output.tail())

    logger.info("done")
