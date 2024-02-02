import os
import sys
from pathlib import Path

# 修改当前目录到上层目录，方便跨不同IDE中使用
pwd = str(Path(__file__).parents[1])
os.chdir(pwd)
sys.path.append(pwd)
print("pwd:", os.getcwd())
# ====================
import inspect

from expr_codegen.codes import sources_to_exprs
from expr_codegen.tool import ExprTool

# 导入OPEN等特征
from sympy_define import *  # noqa

(OPEN, HIGH, LOW, CLOSE, VOLUME, AMOUNT,
 RETURNS, VWAP, CAP,
 ADV5, ADV10, ADV15, ADV20, ADV30, ADV40, ADV50, ADV60, ADV81, ADV120, ADV150, ADV180,
 SECTOR, INDUSTRY, SUBINDUSTRY,) = symbols("""OPEN, HIGH, LOW, CLOSE, VOLUME, AMOUNT,
RETURNS, VWAP, CAP,
ADV5, ADV10, ADV15, ADV20, ADV30, ADV40, ADV50, ADV60, ADV81, ADV120, ADV150, ADV180,
SECTOR, INDUSTRY, SUBINDUSTRY, """, cls=Symbol)


def _code_block_():
    # 因子编辑区，可利用IDE的智能提示在此区域编辑因子

    # adv{d} = average daily dollar volume for the past d days
    ADV5 = ts_mean(AMOUNT, 5)
    ADV10 = ts_mean(AMOUNT, 10)
    ADV15 = ts_mean(AMOUNT, 15)
    ADV20 = ts_mean(AMOUNT, 20)
    ADV30 = ts_mean(AMOUNT, 30)
    ADV40 = ts_mean(AMOUNT, 40)
    ADV50 = ts_mean(AMOUNT, 50)
    ADV60 = ts_mean(AMOUNT, 60)
    ADV81 = ts_mean(AMOUNT, 81)
    ADV120 = ts_mean(AMOUNT, 120)
    ADV150 = ts_mean(AMOUNT, 150)
    ADV180 = ts_mean(AMOUNT, 180)

    alpha_001 = (cs_rank(ts_arg_max(signed_power(if_else((RETURNS < 0), ts_std_dev(RETURNS, 20), CLOSE), 2.), 5)) - 0.5)
    alpha_002 = (-1 * ts_corr(cs_rank(ts_delta(log(VOLUME), 2)), cs_rank(((CLOSE - OPEN) / OPEN)), 6))
    alpha_003 = (-1 * ts_corr(cs_rank(OPEN), cs_rank(VOLUME), 10))
    alpha_004 = (-1 * ts_rank(cs_rank(LOW), 9))
    alpha_005 = (cs_rank((OPEN - (ts_sum(VWAP, 10) / 10))) * (-1 * abs_(cs_rank((CLOSE - VWAP)))))
    alpha_006 = -1 * ts_corr(OPEN, VOLUME, 10)
    alpha_007 = if_else((ADV20 < VOLUME), ((-1 * ts_rank(abs_(ts_delta(CLOSE, 7)), 60)) * sign(ts_delta(CLOSE, 7))), (-1 * 1))
    alpha_008 = (-1 * cs_rank(((ts_sum(OPEN, 5) * ts_sum(RETURNS, 5)) - ts_delay((ts_sum(OPEN, 5) * ts_sum(RETURNS, 5)), 10))))
    alpha_009 = if_else((0 < ts_min(ts_delta(CLOSE, 1), 5)), ts_delta(CLOSE, 1), if_else((ts_max(ts_delta(CLOSE, 1), 5) < 0), ts_delta(CLOSE, 1), (-1 * ts_delta(CLOSE, 1))))
    alpha_010 = cs_rank(if_else((0 < ts_min(ts_delta(CLOSE, 1), 4)), ts_delta(CLOSE, 1), if_else((ts_max(ts_delta(CLOSE, 1), 4) < 0), ts_delta(CLOSE, 1), (-1 * ts_delta(CLOSE, 1)))))
    alpha_011 = ((cs_rank(ts_max((VWAP - CLOSE), 3)) + cs_rank(ts_min((VWAP - CLOSE), 3))) * cs_rank(ts_delta(VOLUME, 3)))
    alpha_012 = (sign(ts_delta(VOLUME, 1)) * (-1 * ts_delta(CLOSE, 1)))
    alpha_013 = (-1 * cs_rank(ts_covariance(cs_rank(CLOSE), cs_rank(VOLUME), 5)))
    alpha_014 = ((-1 * cs_rank(ts_delta(RETURNS, 3))) * ts_corr(OPEN, VOLUME, 10))
    alpha_015 = (-1 * ts_sum(cs_rank(ts_corr(cs_rank(HIGH), cs_rank(VOLUME), 3)), 3))
    alpha_016 = (-1 * cs_rank(ts_covariance(cs_rank(HIGH), cs_rank(VOLUME), 5)))
    alpha_017 = (((-1 * cs_rank(ts_rank(CLOSE, 10))) * cs_rank(ts_delta(ts_delta(CLOSE, 1), 1))) * cs_rank(ts_rank((VOLUME / ADV20), 5)))
    alpha_018 = (-1 * cs_rank(((ts_std_dev(abs_((CLOSE - OPEN)), 5) + (CLOSE - OPEN)) + ts_corr(CLOSE, OPEN, 10))))
    alpha_019 = ((-1 * sign(((CLOSE - ts_delay(CLOSE, 7)) + ts_delta(CLOSE, 7)))) * (1 + cs_rank((1 + ts_sum(RETURNS, 250)))))
    alpha_020 = (((-1 * cs_rank((OPEN - ts_delay(HIGH, 1)))) * cs_rank((OPEN - ts_delay(CLOSE, 1)))) * cs_rank((OPEN - ts_delay(LOW, 1))))
    alpha_021 = if_else((((ts_sum(CLOSE, 8) / 8) + ts_std_dev(CLOSE, 8)) < (ts_sum(CLOSE, 2) / 2)), (-1 * 1), if_else(((ts_sum(CLOSE, 2) / 2) < ((ts_sum(CLOSE, 8) / 8) - ts_std_dev(CLOSE, 8))), 1, if_else(((1 < (VOLUME / ADV20)) | Eq((VOLUME / ADV20), 1)), 1, (-1 * 1))))
    alpha_022 = (-1 * (ts_delta(ts_corr(HIGH, VOLUME, 5), 5) * cs_rank(ts_std_dev(CLOSE, 20))))
    alpha_023 = if_else(((ts_sum(HIGH, 20) / 20) < HIGH), (-1 * ts_delta(HIGH, 2)), 0)
    alpha_024 = if_else((((ts_delta((ts_sum(CLOSE, 100) / 100), 100) / ts_delay(CLOSE, 100)) < 0.05) | Eq((ts_delta((ts_sum(CLOSE, 100) / 100), 100) / ts_delay(CLOSE, 100)), 0.05)), (-1 * (CLOSE - ts_min(CLOSE, 100))), (-1 * ts_delta(CLOSE, 3)))
    alpha_025 = cs_rank(((((-1 * RETURNS) * ADV20) * VWAP) * (HIGH - CLOSE)))
    alpha_026 = (-1 * ts_max(ts_corr(ts_rank(VOLUME, 5), ts_rank(HIGH, 5), 5), 3))
    alpha_027 = if_else((0.5 < cs_rank((ts_sum(ts_corr(cs_rank(VOLUME), cs_rank(VWAP), 6), 2) / 2.0))), (-1 * 1), 1)
    alpha_028 = cs_scale(((ts_corr(ADV20, LOW, 5) + ((HIGH + LOW) / 2)) - CLOSE))
    alpha_029 = (min_(ts_product(cs_rank(cs_rank(cs_scale(log(ts_sum(ts_min(cs_rank(cs_rank((-1 * cs_rank(ts_delta((CLOSE - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(ts_delay((-1 * RETURNS), 6), 5))
    alpha_030 = (((1.0 - cs_rank(((sign((CLOSE - ts_delay(CLOSE, 1))) + sign((ts_delay(CLOSE, 1) - ts_delay(CLOSE, 2)))) + sign((ts_delay(CLOSE, 2) - ts_delay(CLOSE, 3)))))) * ts_sum(VOLUME, 5)) / ts_sum(VOLUME, 20))
    alpha_031 = ((cs_rank(cs_rank(cs_rank(ts_decay_linear((-1 * cs_rank(cs_rank(ts_delta(CLOSE, 10)))), 10)))) + cs_rank((-1 * ts_delta(CLOSE, 3)))) + sign(cs_scale(ts_corr(ADV20, LOW, 12))))
    alpha_032 = (cs_scale(((ts_sum(CLOSE, 7) / 7) - CLOSE)) + (20 * cs_scale(ts_corr(VWAP, ts_delay(CLOSE, 5), 230))))
    alpha_033 = cs_rank((-1 * ((1 - (OPEN / CLOSE)) ** 1)))
    alpha_034 = cs_rank(((1 - cs_rank((ts_std_dev(RETURNS, 2) / ts_std_dev(RETURNS, 5)))) + (1 - cs_rank(ts_delta(CLOSE, 1)))))
    alpha_035 = ((ts_rank(VOLUME, 32) * (1 - ts_rank(((CLOSE + HIGH) - LOW), 16))) * (1 - ts_rank(RETURNS, 32)))
    alpha_036 = (((((2.21 * cs_rank(ts_corr((CLOSE - OPEN), ts_delay(VOLUME, 1), 15))) + (0.7 * cs_rank((OPEN - CLOSE)))) + (0.73 * cs_rank(ts_rank(ts_delay((-1 * RETURNS), 6), 5)))) + cs_rank(abs_(ts_corr(VWAP, ADV20, 6)))) + (0.6 * cs_rank((((ts_sum(CLOSE, 200) / 200) - OPEN) * (CLOSE - OPEN)))))
    alpha_037 = (cs_rank(ts_corr(ts_delay((OPEN - CLOSE), 1), CLOSE, 200)) + cs_rank((OPEN - CLOSE)))
    alpha_038 = ((-1 * cs_rank(ts_rank(CLOSE, 10))) * cs_rank((CLOSE / OPEN)))
    alpha_039 = ((-1 * cs_rank((ts_delta(CLOSE, 7) * (1 - cs_rank(ts_decay_linear((VOLUME / ADV20), 9)))))) * (1 + cs_rank(ts_sum(RETURNS, 250))))
    alpha_040 = ((-1 * cs_rank(ts_std_dev(HIGH, 10))) * ts_corr(HIGH, VOLUME, 10))
    alpha_041 = (((HIGH * LOW) ** 0.5) - VWAP)
    alpha_042 = (cs_rank((VWAP - CLOSE)) / cs_rank((VWAP + CLOSE)))
    alpha_043 = (ts_rank((VOLUME / ADV20), 20) * ts_rank((-1 * ts_delta(CLOSE, 7)), 8))
    alpha_044 = (-1 * ts_corr(HIGH, cs_rank(VOLUME), 5))
    alpha_045 = (-1 * ((cs_rank((ts_sum(ts_delay(CLOSE, 5), 20) / 20)) * ts_corr(CLOSE, VOLUME, 2)) * cs_rank(ts_corr(ts_sum(CLOSE, 5), ts_sum(CLOSE, 20), 2))))
    alpha_046 = if_else((0.25 < (((ts_delay(CLOSE, 20) - ts_delay(CLOSE, 10)) / 10) - ((ts_delay(CLOSE, 10) - CLOSE) / 10))), (-1 * 1), if_else(((((ts_delay(CLOSE, 20) - ts_delay(CLOSE, 10)) / 10) - ((ts_delay(CLOSE, 10) - CLOSE) / 10)) < 0), 1, ((-1 * 1) * (CLOSE - ts_delay(CLOSE, 1)))))
    alpha_047 = ((((cs_rank((1 / CLOSE)) * VOLUME) / ADV20) * ((HIGH * cs_rank((HIGH - CLOSE))) / (ts_sum(HIGH, 5) / 5))) - cs_rank((VWAP - ts_delay(VWAP, 5))))
    alpha_048 = (gp_demean(SUBINDUSTRY, ((ts_corr(ts_delta(CLOSE, 1), ts_delta(ts_delay(CLOSE, 1), 1), 250) * ts_delta(CLOSE, 1)) / CLOSE)) / ts_sum(((ts_delta(CLOSE, 1) / ts_delay(CLOSE, 1)) ** 2), 250))
    alpha_049 = if_else(((((ts_delay(CLOSE, 20) - ts_delay(CLOSE, 10)) / 10) - ((ts_delay(CLOSE, 10) - CLOSE) / 10)) < (-1 * 0.1)), 1, ((-1 * 1) * (CLOSE - ts_delay(CLOSE, 1))))
    alpha_050 = (-1 * ts_max(cs_rank(ts_corr(cs_rank(VOLUME), cs_rank(VWAP), 5)), 5))
    alpha_051 = if_else(((((ts_delay(CLOSE, 20) - ts_delay(CLOSE, 10)) / 10) - ((ts_delay(CLOSE, 10) - CLOSE) / 10)) < (-1 * 0.05)), 1, ((-1 * 1) * (CLOSE - ts_delay(CLOSE, 1))))
    alpha_052 = ((((-1 * ts_min(LOW, 5)) + ts_delay(ts_min(LOW, 5), 5)) * cs_rank(((ts_sum(RETURNS, 240) - ts_sum(RETURNS, 20)) / 220))) * ts_rank(VOLUME, 5))
    alpha_053 = (-1 * ts_delta((((CLOSE - LOW) - (HIGH - CLOSE)) / (CLOSE - LOW)), 9))
    alpha_054 = ((-1 * ((LOW - CLOSE) * (OPEN ** 5))) / ((LOW - HIGH) * (CLOSE ** 5)))
    alpha_055 = (-1 * ts_corr(cs_rank(((CLOSE - ts_min(LOW, 12)) / (ts_max(HIGH, 12) - ts_min(LOW, 12)))), cs_rank(VOLUME), 6))
    alpha_056 = (0 - (1 * (cs_rank((ts_sum(RETURNS, 10) / ts_sum(ts_sum(RETURNS, 2), 3))) * cs_rank((RETURNS * CAP)))))
    alpha_057 = (0 - (1 * ((CLOSE - VWAP) / ts_decay_linear(cs_rank(ts_arg_max(CLOSE, 30)), 2))))
    alpha_058 = (-1 * ts_rank(ts_decay_linear(ts_corr(gp_demean(SECTOR, VWAP), VOLUME, 4), 8), 6))
    alpha_059 = (-1 * ts_rank(ts_decay_linear(ts_corr(gp_demean(INDUSTRY, ((VWAP * 0.728317) + (VWAP * (1 - 0.728317)))), VOLUME, 4), 16), 8))
    alpha_060 = (0 - (1 * ((2 * cs_scale(cs_rank(((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME)), 1)) - cs_scale(cs_rank(ts_arg_max(CLOSE, 10)), 1))))
    alpha_061 = (cs_rank((VWAP - ts_min(VWAP, 16))) < cs_rank(ts_corr(VWAP, ADV180, 18)))
    # alpha_062 = if_else((cs_rank(ts_corr(VWAP, ts_sum(ADV20, 22), 10)) < cs_rank(((cs_rank(OPEN) + cs_rank(OPEN)) < (cs_rank(((HIGH + LOW) / 2)) + cs_rank(HIGH))))), -1, 0)
    alpha_063 = ((cs_rank(ts_decay_linear(ts_delta(gp_demean(INDUSTRY, CLOSE), 2), 8)) - cs_rank(ts_decay_linear(ts_corr(((VWAP * 0.318108) + (OPEN * (1 - 0.318108))), ts_sum(ADV180, 37), 14), 12))) * -1)
    alpha_064 = if_else((cs_rank(ts_corr(ts_sum(((OPEN * 0.178404) + (LOW * (1 - 0.178404))), 13), ts_sum(ADV120, 13), 17)) < cs_rank(ts_delta(((((HIGH + LOW) / 2) * 0.178404) + (VWAP * (1 - 0.178404))), 4))), -1, 0)
    alpha_065 = if_else((cs_rank(ts_corr(((OPEN * 0.00817205) + (VWAP * (1 - 0.00817205))), ts_sum(ADV60, 7), 6)) < cs_rank((OPEN - ts_min(OPEN, 14)))), -1, 0)
    alpha_066 = ((cs_rank(ts_decay_linear(ts_delta(VWAP, 4), 7)) + ts_rank(ts_decay_linear(((((LOW * 0.96633) + (LOW * (1 - 0.96633))) - VWAP) / (OPEN - ((HIGH + LOW) / 2))), 11), 7)) * -1)
    alpha_067 = ((cs_rank((HIGH - ts_min(HIGH, 2))) ** cs_rank(ts_corr(gp_demean(SECTOR, VWAP), gp_demean(SUBINDUSTRY, ADV20), 6))) * -1)
    alpha_068 = if_else((ts_rank(ts_corr(cs_rank(HIGH), cs_rank(ADV15), 9), 14) < cs_rank(ts_delta(((CLOSE * 0.518371) + (LOW * (1 - 0.518371))), 1))), -1, 0)
    alpha_069 = ((cs_rank(ts_max(ts_delta(gp_demean(INDUSTRY, VWAP), 3), 5)) ** ts_rank(ts_corr(((CLOSE * 0.490655) + (VWAP * (1 - 0.490655))), ADV20, 5), 9)) * -1)
    alpha_070 = ((cs_rank(ts_delta(VWAP, 1)) ** ts_rank(ts_corr(gp_demean(INDUSTRY, CLOSE), ADV50, 18), 18)) * -1)
    alpha_071 = max_(ts_rank(ts_decay_linear(ts_corr(ts_rank(CLOSE, 3), ts_rank(ADV180, 12), 18), 4), 16), ts_rank(ts_decay_linear((cs_rank(((LOW + OPEN) - (VWAP + VWAP))) ** 2), 16), 4))
    alpha_072 = (cs_rank(ts_decay_linear(ts_corr(((HIGH + LOW) / 2), ADV40, 9), 10)) / cs_rank(ts_decay_linear(ts_corr(ts_rank(VWAP, 4), ts_rank(VOLUME, 19), 7), 3)))
    alpha_073 = (max_(cs_rank(ts_decay_linear(ts_delta(VWAP, 5), 3)), ts_rank(ts_decay_linear(((ts_delta(((OPEN * 0.147155) + (LOW * (1 - 0.147155))), 2) / ((OPEN * 0.147155) + (LOW * (1 - 0.147155)))) * -1), 3), 17)) * -1)
    alpha_074 = if_else((cs_rank(ts_corr(CLOSE, ts_sum(ADV30, 37), 15)) < cs_rank(ts_corr(cs_rank(((HIGH * 0.0261661) + (VWAP * (1 - 0.0261661)))), cs_rank(VOLUME), 11))), -1, 0)
    alpha_075 = (cs_rank(ts_corr(VWAP, VOLUME, 4)) < cs_rank(ts_corr(cs_rank(LOW), cs_rank(ADV50), 12)))
    alpha_076 = (max_(cs_rank(ts_decay_linear(ts_delta(VWAP, 1), 12)), ts_rank(ts_decay_linear(ts_rank(ts_corr(gp_demean(SECTOR, LOW), ADV81, 8), 20), 17), 19)) * -1)
    alpha_077 = min_(cs_rank(ts_decay_linear(((((HIGH + LOW) / 2) + HIGH) - (VWAP + HIGH)), 20)), cs_rank(ts_decay_linear(ts_corr(((HIGH + LOW) / 2), ADV40, 3), 6)))
    alpha_078 = (cs_rank(ts_corr(ts_sum(((LOW * 0.352233) + (VWAP * (1 - 0.352233))), 20), ts_sum(ADV40, 20), 7)) ** cs_rank(ts_corr(cs_rank(VWAP), cs_rank(VOLUME), 6)))
    alpha_079 = (cs_rank(ts_delta(gp_demean(SECTOR, ((CLOSE * 0.60733) + (OPEN * (1 - 0.60733)))), 1)) < cs_rank(ts_corr(ts_rank(VWAP, 4), ts_rank(ADV150, 9), 15)))
    alpha_080 = ((cs_rank(sign(ts_delta(gp_demean(INDUSTRY, ((OPEN * 0.868128) + (HIGH * (1 - 0.868128)))), 4))) ** ts_rank(ts_corr(HIGH, ADV10, 5), 6)) * -1)
    alpha_081 = if_else((cs_rank(log(ts_product(cs_rank((cs_rank(ts_corr(VWAP, ts_sum(ADV10, 50), 8)) ** 4)), 15))) < cs_rank(ts_corr(cs_rank(VWAP), cs_rank(VOLUME), 5))), -1, 0)
    alpha_082 = (min_(cs_rank(ts_decay_linear(ts_delta(OPEN, 1), 15)), ts_rank(ts_decay_linear(ts_corr(gp_demean(SECTOR, VOLUME), ((OPEN * 0.634196) + (OPEN * (1 - 0.634196))), 17), 7), 13)) * -1)
    alpha_083 = ((cs_rank(ts_delay(((HIGH - LOW) / (ts_sum(CLOSE, 5) / 5)), 2)) * cs_rank(cs_rank(VOLUME))) / (((HIGH - LOW) / (ts_sum(CLOSE, 5) / 5)) / (VWAP - CLOSE)))
    alpha_084 = signed_power(ts_rank((VWAP - ts_max(VWAP, 15)), 21), ts_delta(CLOSE, 5))
    alpha_085 = (cs_rank(ts_corr(((HIGH * 0.876703) + (CLOSE * (1 - 0.876703))), ADV30, 10)) ** cs_rank(ts_corr(ts_rank(((HIGH + LOW) / 2), 4), ts_rank(VOLUME, 10), 7)))
    alpha_086 = if_else((ts_rank(ts_corr(CLOSE, ts_sum(ADV20, 15), 6), 20) < cs_rank(((OPEN + CLOSE) - (VWAP + OPEN)))), -1, 0)
    alpha_087 = (max_(cs_rank(ts_decay_linear(ts_delta(((CLOSE * 0.369701) + (VWAP * (1 - 0.369701))), 2), 3)), ts_rank(ts_decay_linear(abs_(ts_corr(gp_demean(INDUSTRY, ADV81), CLOSE, 13)), 5), 14)) * -1)
    alpha_088 = min_(cs_rank(ts_decay_linear(((cs_rank(OPEN) + cs_rank(LOW)) - (cs_rank(HIGH) + cs_rank(CLOSE))), 8)), ts_rank(ts_decay_linear(ts_corr(ts_rank(CLOSE, 8), ts_rank(ADV60, 21), 8), 7), 3))
    alpha_089 = (ts_rank(ts_decay_linear(ts_corr(((LOW * 0.967285) + (LOW * (1 - 0.967285))), ADV10, 7), 6), 4) - ts_rank(ts_decay_linear(ts_delta(gp_demean(INDUSTRY, VWAP), 3), 10), 15))
    alpha_090 = ((cs_rank((CLOSE - ts_max(CLOSE, 5))) ** ts_rank(ts_corr(gp_demean(SUBINDUSTRY, ADV40), LOW, 5), 3)) * -1)
    alpha_091 = ((ts_rank(ts_decay_linear(ts_decay_linear(ts_corr(gp_demean(INDUSTRY, CLOSE), VOLUME, 10), 16), 4), 5) - cs_rank(ts_decay_linear(ts_corr(VWAP, ADV30, 4), 3))) * -1)
    alpha_092 = min_(ts_rank(ts_decay_linear(((((HIGH + LOW) / 2) + CLOSE) < (LOW + OPEN)), 15), 19), ts_rank(ts_decay_linear(ts_corr(cs_rank(LOW), cs_rank(ADV30), 8), 7), 7))
    alpha_094 = ((cs_rank((VWAP - ts_min(VWAP, 12))) ** ts_rank(ts_corr(ts_rank(VWAP, 20), ts_rank(ADV60, 4), 18), 3)) * -1)
    alpha_095 = (cs_rank((OPEN - ts_min(OPEN, 12))) < ts_rank((cs_rank(ts_corr(ts_sum(((HIGH + LOW) / 2), 20), ts_sum(ADV40, 19), 13)) ** 5), 12))
    alpha_096 = (max_(ts_rank(ts_decay_linear(ts_corr(cs_rank(VWAP), cs_rank(VOLUME), 4), 4), 8), ts_rank(ts_decay_linear(ts_arg_max(ts_corr(ts_rank(CLOSE, 7), ts_rank(ADV60, 4), 4), 13), 14), 13)) * -1)
    alpha_097 = ((cs_rank(ts_decay_linear(ts_delta(gp_demean(INDUSTRY, ((LOW * 0.721001) + (VWAP * (1 - 0.721001)))), 3), 20)) - ts_rank(ts_decay_linear(ts_rank(ts_corr(ts_rank(LOW, 8), ts_rank(ADV60, 17), 5), 19), 16), 7)) * -1)
    alpha_098 = (cs_rank(ts_decay_linear(ts_corr(VWAP, ts_sum(ADV5, 26), 5), 7)) - cs_rank(ts_decay_linear(ts_rank(ts_arg_min(ts_corr(cs_rank(OPEN), cs_rank(ADV15), 21), 9), 7), 8)))
    alpha_099 = if_else((cs_rank(ts_corr(ts_sum(((HIGH + LOW) / 2), 20), ts_sum(ADV60, 20), 9)) < cs_rank(ts_corr(LOW, VOLUME, 6))), -1, 0)
    alpha_100 = (0 - (1 * (((1.5 * cs_scale(gp_demean(SUBINDUSTRY, gp_demean(SUBINDUSTRY, cs_rank(((((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME)))))) - cs_scale(gp_demean(SUBINDUSTRY, (ts_corr(CLOSE, cs_rank(ADV20), 5) - cs_rank(ts_arg_min(CLOSE, 30)))))) * (VOLUME / ADV20))))
    alpha_101 = ((CLOSE - OPEN) / ((HIGH - LOW) + 0.001))


# 读取源代码，转成字符串
source = inspect.getsource(_code_block_)
raw, exprs_dict = sources_to_exprs(globals().copy(), source)

# 生成代码
tool = ExprTool()
codes, G = tool.all(exprs_dict, style='polars', template_file='template.py.j2',
                    replace=True, regroup=True, format=True,
                    date='date', asset='asset',
                    # 还复制了最原始的表达式
                    extra_codes=())

print(codes)
#
# 保存代码到指定文件
output_file = 'codes/alpha101.py'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(codes)
