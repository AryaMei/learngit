import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTableWidget, QTableWidgetItem, QGroupBox, 
                             QLineEdit, QPushButton, QTextEdit, QFormLayout, QCheckBox,
                              QHeaderView)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt

class CompositeDesignApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("复合材料铺层设计系统")
        self.setGeometry(100, 100, 1200, 800)
        
        # 主窗口部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # 主布局（水平分为左中右三部分）
        self.main_layout = QHBoxLayout(self.main_widget)
        
        # 左侧区域
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        
        # 右侧区域
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        
        # 中间区域
        self.center_panel = QWidget()
        self.center_layout = QVBoxLayout(self.center_panel)
        
        # 将三个区域添加到主布局
        self.main_layout.addWidget(self.left_panel, 40)  # 左侧占40%
        self.main_layout.addWidget(self.center_panel, 30)  # 中间占30%
        self.main_layout.addWidget(self.right_panel, 30)  # 右侧占30%
        
        # 初始化各个区域的UI
        self.init_left_panel()
        self.init_center_panel()
        self.init_right_panel()
    
    def init_left_panel(self):
        """初始化左侧面板"""
        # 上方示意图区域
        self.diagram_group = QGroupBox("三明治夹心几何示意图")
        self.diagram_layout = QVBoxLayout()
        
        # 示例图片（实际使用时替换为您的图片路径）
        self.diagram_label = QLabel()
        self.diagram_label.setAlignment(Qt.AlignCenter)
        self.diagram_label.setStyleSheet("background-color: white; border: 1px solid gray;")
        self.diagram_label.setFixedHeight(300)
        
        # 模拟一个示意图
        pixmap = QPixmap("单位制.png")
        self.diagram_label.setPixmap(pixmap.scaled(260, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # self.diagram_label.setText("铺层示意图区域")
        
        self.diagram_layout.addWidget(self.diagram_label)
        self.diagram_group.setLayout(self.diagram_layout)
        
        #------------------------------------------------------------------------------------------------
        # 下方铺层数据表格
        self.layer_data_group = QGroupBox("铺层设计数据")
        self.layer_data_layout = QVBoxLayout()
        
        #添加一个checkbox，判断三明治上下层铺层是否一致
        self.check_layout = QHBoxLayout()
        self.layer_same_chechbox = QCheckBox("如果上下铺层顺序一致，请勾选复选框")
        #设置需要输入的铺层的数量
        self.layer_number_layout = QFormLayout()
        self.layer_number_up = QLineEdit()
        self.layer_number_down = QLineEdit()
        self.layer_number_layout.addRow("上层铺层数量：", self.layer_number_up)
        self.layer_number_layout.addRow("下层铺层数量：", self.layer_number_down)
        self.check_layout.addWidget(self.layer_same_chechbox)
        self.check_layout.addLayout(self.layer_number_layout)
        
        self.layer_data_layout.addLayout(self.check_layout)

        
        self.layer_table = QTableWidget()
        self.layer_table.setColumnCount(3)
        self.layer_table.setHorizontalHeaderLabels(["LayerNumber", "PlyAngle(°)", "Thickness(mm)"])
        self.layer_table.setRowCount(10)  # 默认10行
        
        #设置表格的表头相关的样式
        self.layer_table.verticalHeader().setVisible(False)
        self.layer_table_header = self.layer_table.horizontalHeader()
        self.layer_table_header.setStyleSheet("QHeaderView::section { background-color: lightblue; Font: bold;}")
        self.layer_table_header.setDefaultAlignment(Qt.AlignCenter)
        self.layer_table_header.setSectionResizeMode(QHeaderView.Stretch)   #设置表头扩展至整个界面
        
        # 设置表格中需要显示的内容
        self.table_operator(0,"上层铺层顺序")
        self.table_operator(5,"下层铺层顺序")
        
        for row in range(1,5):
            self.layer_table.setItem(row, 0, QTableWidgetItem(str(row)))
            self.layer_table.setItem(row+5, 0, QTableWidgetItem(str(row)))


        
        self.layer_data_layout.addWidget(self.layer_table)
                
        self.layer_data_group.setLayout(self.layer_data_layout)
        
        # 将示意图和表格添加到左侧布局
        self.left_layout.addWidget(self.diagram_group)
        self.left_layout.addWidget(self.layer_data_group)

    
    def init_center_panel(self):
        """初始化中间面板"""
        # 上方几何参数区域
        self.geometry_group = QGroupBox("几何参数")
        self.geometry_layout = QFormLayout()
        
        # 几何参数输入字段
        self.length_input = QLineEdit()
        self.width_input = QLineEdit()
        self.radius_input = QLineEdit()
        self.thickness_input = QLineEdit()
        
        # 设置默认值
        self.length_input.setText("1000")
        self.width_input.setText("500")
        self.radius_input.setText("0")
        self.thickness_input.setText("2.5")
        
        # 添加到表单
        self.geometry_layout.addRow("长度(mm):", self.length_input)
        self.geometry_layout.addRow("宽度(mm):", self.width_input)
        self.geometry_layout.addRow("圆角半径(mm):", self.radius_input)
        self.geometry_layout.addRow("总厚度(mm):", self.thickness_input)
        
        self.geometry_group.setLayout(self.geometry_layout)
        
        # 下方材料参数区域
        self.material_group = QGroupBox("材料参数")
        self.material_layout = QFormLayout()
        
        # 材料参数输入字段
        self.e1_input = QLineEdit()
        self.e2_input = QLineEdit()
        self.g12_input = QLineEdit()
        self.v12_input = QLineEdit()
        self.density_input = QLineEdit()
        
        # 设置默认值（示例数据）
        self.e1_input.setText("135000")
        self.e2_input.setText("9000")
        self.g12_input.setText("4500")
        self.v12_input.setText("0.3")
        self.density_input.setText("1.6")
        
        # 添加到表单
        self.material_layout.addRow("E1(MPa):", self.e1_input)
        self.material_layout.addRow("E2(MPa):", self.e2_input)
        self.material_layout.addRow("G12(MPa):", self.g12_input)
        self.material_layout.addRow("ν12:", self.v12_input)
        self.material_layout.addRow("密度(g/cm³):", self.density_input)
        
        self.material_group.setLayout(self.material_layout)
        
        # 将几何和材料参数组添加到中间布局
        self.center_layout.addWidget(self.geometry_group)
        self.center_layout.addWidget(self.material_group)
        self.center_layout.addStretch()  # 添加伸缩项使内容靠上
    
    def init_right_panel(self):
        """初始化右侧面板"""
        # 设置区域
        self.settings_group = QGroupBox("计算设置")
        self.settings_layout = QFormLayout()
        
        # 计算设置选项
        self.analysis_type = QLineEdit("线性分析")
        self.mesh_size = QLineEdit("5")
        self.solver_type = QLineEdit("直接求解器")
        
        self.settings_layout.addRow("分析类型:", self.analysis_type)
        self.settings_layout.addRow("网格尺寸(mm):", self.mesh_size)
        self.settings_layout.addRow("求解器类型:", self.solver_type)
        
        self.settings_group.setLayout(self.settings_layout)
        
        # 按钮区域
        self.btn_group = QGroupBox("操作")
        self.btn_layout = QVBoxLayout()
        
        self.calc_btn = QPushButton("开始计算")
        self.export_btn = QPushButton("导出结果")
        self.save_btn = QPushButton("保存设计")
        self.load_btn = QPushButton("加载设计")
        
        # 设置按钮样式
        button_style = "QPushButton {padding: 8px; font-weight: bold;}"
        self.calc_btn.setStyleSheet(button_style + "background-color: #4CAF50; color: white;")
        self.export_btn.setStyleSheet(button_style)
        self.save_btn.setStyleSheet(button_style)
        self.load_btn.setStyleSheet(button_style)
        
        self.btn_layout.addWidget(self.calc_btn)
        self.btn_layout.addWidget(self.export_btn)
        self.btn_layout.addWidget(self.save_btn)
        self.btn_layout.addWidget(self.load_btn)
        self.btn_layout.addStretch()
        
        self.btn_group.setLayout(self.btn_layout)
        
        # 结果输出区域
        self.output_group = QGroupBox("计算结果")
        self.output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #f0f0f0;")
        
        # 添加一些示例输出
        self.output_text.setPlainText("计算结果将显示在这里...\n\n"
                                   "1. 最大应力: \n"
                                   "2. 最大应变: \n"
                                   "3. 安全系数: \n"
                                   "4. 重量估算: ")
        
        self.output_layout.addWidget(self.output_text)
        self.output_group.setLayout(self.output_layout)
        
        # 将设置、按钮和输出添加到右侧布局
        self.right_layout.addWidget(self.settings_group)
        self.right_layout.addWidget(self.btn_group)
        self.right_layout.addWidget(self.output_group)
        
        # 连接按钮信号
        self.calc_btn.clicked.connect(self.run_calculation)
        self.export_btn.clicked.connect(self.export_results)
        self.save_btn.clicked.connect(self.save_design)
        self.load_btn.clicked.connect(self.load_design)
    

    #设置表格合并的函数，并修改其显示的内容,输入的参数为：合并哪一行，显示的文本
    def table_operator(self,rowNumber,text):
        self.layer_table.setSpan(rowNumber,0,1,3)   #合并第一行,函数中的参数：起始行，起始列，行跨度，列跨度
        merged_item = QTableWidgetItem(text)
        merged_item.setTextAlignment(Qt.AlignCenter)  # 文字居中
        merged_item.setFlags(merged_item.flags() & ~Qt.ItemIsEditable)  #不可编辑
        merged_item.setBackground(QColor(228,228,228))            #定义背景颜色
        self.layer_table.setItem(rowNumber,0,merged_item)
    
    def run_calculation(self):
        """执行计算"""
        # 这里应该是实际的计算逻辑
        # 现在只是模拟计算结果显示
        self.output_text.clear()
        self.output_text.append("计算完成！\n")
        self.output_text.append("输入参数摘要：")
        self.output_text.append(f"- 长度: {self.length_input.text()} mm")
        self.output_text.append(f"- 宽度: {self.width_input.text()} mm")
        self.output_text.append(f"- 总厚度: {self.thickness_input.text()} mm")
        self.output_text.append("\n铺层信息：")
        
        # 显示铺层数据
        for row in range(self.layer_table.rowCount()):
            angle = self.layer_table.item(row, 1).text()
            thickness = self.layer_table.item(row, 2).text()
            material = self.layer_table.item(row, 3).text()
            self.output_text.append(f"层 {row+1}: 角度={angle}°, 厚度={thickness}mm, 材料={material}")
        
        # 模拟计算结果
        self.output_text.append("\n计算结果：")
        self.output_text.append("1. 最大应力: 256.8 MPa")
        self.output_text.append("2. 最大应变: 0.0018")
        self.output_text.append("3. 安全系数: 2.5")
        self.output_text.append("4. 重量估算: 1.2 kg")
    
    def export_results(self):
        """导出结果"""
        self.output_text.append("\n导出功能: 结果已导出到文件")
    
    def save_design(self):
        """保存设计"""
        self.output_text.append("\n保存功能: 设计已保存")
    
    def load_design(self):
        """加载设计"""
        self.output_text.append("\n加载功能: 请选择设计文件")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompositeDesignApp()
    window.show()
    sys.exit(app.exec_())