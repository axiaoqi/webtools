"""
计算方法：
1、提取出我的所有订单，my_all_df
2、提取付款日期的订单，fukuan_df = my_all_df
3、提取退款付款日期内退款订单，tuikuan_df = fukuan_df
4、提取付款日期之前的退款订单forward_tuikuan_df = my_all_df，订单日之前的

总结：len(fukuan_df - tuikuan_df - forward_tuikuan_df)
"""
from pathlib import Path
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def run(laiyuan, start, end, file_csv):

    # csv文件或者excel文件
    if file_csv.suffix == '.csv':
        df = pd.read_csv(file_csv)
    elif file_csv.suffix == '.xlsx':
        df = pd.read_excel(file_csv)

    df['发货日期'] = pd.to_datetime(df['发货日期'])
    df['退货日期'] = pd.to_datetime(df['退货日期'])

    my_all_df = df[df['订单来源'] == laiyuan]

    ########## 计算本期所有付款的订单 ##########################
    condition1 = my_all_df['发货日期'] >= start
    condition2 = my_all_df['发货日期'] <= end
    fukuan_df = my_all_df[condition1 & condition2]
    fukuan_count = fukuan_df['数量'].sum()

    ########## 计算本期已经填单号的退款数量 ##########################
    tuikuan_df = fukuan_df[fukuan_df['退货日期'].notnull()]  # 因为结款日期会晚几天，得算退货日期在结款日期之间的单子
    tuikuan_df = tuikuan_df[(tuikuan_df['退货日期'] >= start) & (tuikuan_df['退货日期'] <= end)]  # 退货日期在结款日期中间的
    tuikuan_count = tuikuan_df['数量'].sum()

    ########### 计算上一期退款的，还没有减掉的 ##################
    _forward_all_df = my_all_df[my_all_df['发货日期'] < start]  # 取出这一期开始时间之前的订单
    forward_all_df = _forward_all_df[(_forward_all_df['退货日期'] >= start) & (_forward_all_df['退货日期'] <= end)]  # 退货日期是这一期的订单
    forward_tuikuan_count = forward_all_df['数量'].sum()

    fukuan_df = fukuan_df.reset_index()
    print(fukuan_df)

    print('本期退款的：')
    print(tuikuan_df)
    print("上期退款的还没有减去的：")
    print(forward_all_df)

    # 导出到桌面
    tuikuan_df.to_csv(Path.home().joinpath("Desktop", f"{laiyuan}_本期退款的.csv"), encoding='utf-8-sig')
    forward_all_df.to_csv(Path.home().joinpath("Desktop", f"{laiyuan}_上期退款的还没有减去的.csv"), encoding='utf-8-sig')

    print('\n')
    print(f'{laiyuan}: {start} - {end}：本期付款订单数量：{fukuan_count}')
    print(f'本期已经填了快递单号退款的数量：{tuikuan_count}')
    print(f'上一期退款还没减掉的数量：{forward_tuikuan_count}')
    print('\n')

    jiesuan_num = fukuan_count - tuikuan_count - forward_tuikuan_count
    print(f'需要结算单子：{jiesuan_num}。需要结算金额：{345.0 * jiesuan_num}')
    print('\n')


if __name__ == '__main__':
    # 订单日期
    start = '2025-2-21'
    end = '2025-3-20'

    file_csv = Path.home().joinpath("Desktop", "工作簿1.xlsx")

    laiyuans = ['阮总', '王总', '曹总']
    # laiyuans = ['阮总']
    for laiyuan in laiyuans:
        run(laiyuan, start, end, file_csv)






