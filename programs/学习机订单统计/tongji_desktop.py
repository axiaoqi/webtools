import sys
from pathlib import Path
import pandas as pd
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QDateEdit, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit, QSpacerItem, QSizePolicy


class OrderCalculationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("订单计算工具")
        self.setGeometry(100, 100, 1400, 900)  # 增加窗口宽度

        # 初始化布局
        layout = QVBoxLayout()

        # 上面部分：文件选择、日期选择、订单来源选择
        upper_layout = QVBoxLayout()

        # 文件选择区域
        file_layout = QHBoxLayout()
        self.file_button = QPushButton("选择文件")
        self.file_button.clicked.connect(self.select_file)
        file_layout.addWidget(self.file_button)

        self.file_label = QLabel("文件路径：")
        file_layout.addWidget(self.file_label)

        upper_layout.addLayout(file_layout)
        upper_layout.addSpacing(20)

        # 日期选择区域
        date_layout = QHBoxLayout()
        self.start_date_label = QLabel("开始日期：")
        date_layout.addWidget(self.start_date_label)
        self.start_date_edit = QDateEdit(self)
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)  # 显示日历
        date_layout.addWidget(self.start_date_edit)

        self.end_date_label = QLabel("结束日期：")
        date_layout.addWidget(self.end_date_label)
        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)  # 显示日历
        date_layout.addWidget(self.end_date_edit)

        upper_layout.addLayout(date_layout)
        upper_layout.addSpacing(20)

        # 订单来源选择
        self.laiyuan_label = QLabel("选择订单来源：")
        upper_layout.addWidget(self.laiyuan_label)
        self.laiyuan_combobox = QComboBox(self)
        self.laiyuan_combobox.addItems(["阮总", "王总", "曹总"])  # 可以根据需要扩展更多的选择项
        upper_layout.addWidget(self.laiyuan_combobox)
        upper_layout.addSpacing(20)

        # 计算按钮
        self.calculate_button = QPushButton("开始计算")
        self.calculate_button.clicked.connect(self.calculate)
        upper_layout.addWidget(self.calculate_button)
        upper_layout.addSpacing(20)

        # 在右侧显示总结果
        self.result_textbox = QTextEdit()
        self.result_textbox.setReadOnly(True)
        upper_layout.addWidget(self.result_textbox)

        # 通过水平布局将左侧和右侧内容排列
        main_layout = QHBoxLayout()
        main_layout.addLayout(upper_layout)

        # 下半部分：显示计算结果和表格
        lower_layout = QVBoxLayout()

        # 用于显示表格的区域
        self.fukuan_table = self.create_table("本期付款订单")
        self.tuikuan_table = self.create_table("本期退款订单")
        self.forward_table = self.create_table("上一期未减退款")

        # 表格区块，分四列
        grid_layout = QHBoxLayout()
        grid_layout.addWidget(self.fukuan_table["widget"])
        grid_layout.addWidget(self.tuikuan_table["widget"])
        grid_layout.addWidget(self.forward_table["widget"])

        lower_layout.addLayout(grid_layout)

        # 保存为CSV按钮
        self.save_fukuan_button = QPushButton("保存本期付款订单为CSV")
        self.save_fukuan_button.clicked.connect(lambda: self.save_as_csv(self.fukuan_table["table"], "本期付款订单"))
        lower_layout.addWidget(self.save_fukuan_button)

        self.save_tuikuan_button = QPushButton("保存本期退款订单为CSV")
        self.save_tuikuan_button.clicked.connect(lambda: self.save_as_csv(self.tuikuan_table["table"], "本期退款订单"))
        lower_layout.addWidget(self.save_tuikuan_button)

        self.save_forward_button = QPushButton("保存上一期未减退款为CSV")
        self.save_forward_button.clicked.connect(lambda: self.save_as_csv(self.forward_table["table"], "上一期未减退款"))
        lower_layout.addWidget(self.save_forward_button)

        # 总结果标签和显示
        self.total_label = QLabel("计算结果：")
        lower_layout.addWidget(self.total_label)

        main_layout.addLayout(lower_layout)

        self.setLayout(main_layout)

    def create_table(self, label_text):
        """创建带标签和表格控件的函数"""
        widget = QWidget()
        widget_layout = QVBoxLayout()

        label = QLabel(label_text)
        table = QTableWidget()
        table.setColumnCount(0)
        table.setRowCount(0)

        widget_layout.addWidget(label)
        widget_layout.addWidget(table)
        widget.setLayout(widget_layout)

        return {"widget": widget, "label": label, "table": table}

    def select_file(self):
        # 打开文件选择对话框，默认选择.xlsx文件
        file, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Excel Files (*.xlsx);;CSV Files (*.csv)")
        if file:
            self.file_label.setText(f"文件路径：{file}")
            self.file_path = Path(file)

    def calculate(self):
        # 获取日期范围
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
        laiyuan = self.laiyuan_combobox.currentText()  # 获取用户选择的订单来源

        # 调用原来的计算逻辑
        if hasattr(self, 'file_path'):
            self.run(laiyuan, start_date, end_date, self.file_path)  # 将选中的订单来源传入计算函数

    def run(self, laiyuan, start, end, file_csv):
        # 读取文件
        if file_csv.suffix == '.csv':
            df = pd.read_csv(file_csv)
        elif file_csv.suffix == '.xlsx':
            df = pd.read_excel(file_csv)

        df['发货日期'] = pd.to_datetime(df['发货日期'])
        df['退货日期'] = pd.to_datetime(df['退货日期'])

        # 过滤订单来源
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

        # 输出到文本框
        result_text = (
            f'{laiyuan}: {start} - {end}：本期付款订单数量：{fukuan_count}\n'
            f'本期已经填了快递单号退款的数量：{tuikuan_count}\n'
            f'上一期退款还没减掉的数量：{forward_tuikuan_count}\n\n'
            f'需要结算单子：{fukuan_count - tuikuan_count - forward_tuikuan_count}。需要结算金额：{345.0 * (fukuan_count - tuikuan_count - forward_tuikuan_count)}\n\n'
        )
        self.result_textbox.setText(result_text)

        # 更新表格数据
        self.update_table(self.fukuan_table["table"], fukuan_df)
        self.update_table(self.tuikuan_table["table"], tuikuan_df)
        self.update_table(self.forward_table["table"], forward_all_df)

    def update_table(self, table, df):
        """更新表格数据"""
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df))

        # 设置列标题
        table.setHorizontalHeaderLabels(df.columns)

        # 填充数据
        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iloc[row, col]))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, col, item)

    def save_as_csv(self, table, label_text):
        """保存为CSV"""
        # 将表格数据转为DataFrame并保存为CSV
        row_count = table.rowCount()
        column_count = table.columnCount()

        data = []
        for row in range(row_count):
            row_data = []
            for col in range(column_count):
                row_data.append(table.item(row, col).text() if table.item(row, col) else "")
            data.append(row_data)

        df = pd.DataFrame(data, columns=[table.horizontalHeaderItem(i).text() for i in range(column_count)])

        # 文件保存对话框
        file, _ = QFileDialog.getSaveFileName(self, f"保存{label_text}为CSV", "", "CSV Files (*.csv)")
        if file:
            df.to_csv(file, index=False, encoding='utf-8-sig')
            print(f"{label_text} 已保存为 CSV 文件：{file}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrderCalculationApp()
    window.show()
    sys.exit(app.exec())
