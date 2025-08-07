import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTableWidget, QTableWidgetItem, QGroupBox, 
                             QLineEdit, QPushButton, QTextEdit, QFormLayout, QCheckBox,
                              QHeaderView, QFrame)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

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
        self.main_layout.addWidget(self.center_panel, 20)  # 中间占20%
        self.main_layout.addWidget(self.right_panel, 40)  # 右侧占40%
        
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
        self.length = QLineEdit()
        self.width = QLineEdit()
        self.hf_up = QLineEdit()        #上面板厚度
        self.hf_down = QLineEdit()
        self.hc = QLineEdit()
        
        '''
        # 设置默认值
        self.length_input.setText("1000")
        self.width_input.setText("500")
        self.radius_input.setText("0")
        self.thickness_input.setText("2.5")
        '''
        
        # 添加到表单
        self.geometry_layout.addRow("长度b(mm):", self.length)
        self.geometry_layout.addRow("宽度a(mm):", self.width)
        self.geometry_layout.addRow("上面板厚度hf1(mm):", self.hf_up)
        self.geometry_layout.addRow("下面板厚度hf2(mm):", self.hf_down)
        self.geometry_layout.addRow("芯层厚度hc(mm):", self.hc)
        
        
        self.geometry_group.setLayout(self.geometry_layout)
        
        #--------------------------------------------------------------------------
        # 中间材料参数区域
        self.material_group = QGroupBox("材料参数")
        self.material_layout = QFormLayout()        
        
        
        # 定义等效密度计算所需材料参数
        self.density_label = QLabel("输入计算等效密度(g/mm³)所需参数：")
        self.density_label.setStyleSheet("Font: bold")
        self.material_layout.addRow(self.density_label)
        self.composite_density = QLineEdit()
        self.foam_density = QLineEdit()
        density_hbox = QHBoxLayout()
        density_hbox.addWidget(QLabel("面板的密度："))
        density_hbox.addWidget(self.composite_density)
        density_hbox.addSpacing(10)  # 添加间距
        density_hbox.addWidget(QLabel("芯材的密度："))
        density_hbox.addWidget(self.foam_density)
        self.material_layout.addRow(density_hbox)
        
        #添加水平分割线
        self.add_VLine(self.material_layout)
        
        
        #定义计算层合板弯曲和挠度性能所需材料
        self.delf_para_label = QLabel("输入计算层合板弯曲挠度所需参数：")
        self.delf_para_label.setStyleSheet("Font: bold")
        self.material_layout.addRow(self.delf_para_label)
        self.composite_E1 = QLineEdit()
        self.composite_E2 = QLineEdit()
        self.composite_G = QLineEdit()
        self.composite_V12 = QLineEdit()
        self.material_layout.addRow("单层板轴向模量E1(GPa)：",self.composite_E1)
        self.material_layout.addRow("单层板横向模量E2(GPa)：",self.composite_E2)
        self.material_layout.addRow("单层板剪切模量G(GPa)：",self.composite_G)
        self.material_layout.addRow("单层板泊松比V12：",self.composite_V12)
        
        '''
        #这是将参数每一行定义有两个输入参数的代码
        modulus_hbox = QHBoxLayout()
        modulus_hbox.addWidget(QLabel("单层板轴向模量E1(GPa)："))
        modulus_hbox.addWidget(self.composite_E1)
        modulus_hbox.addSpacing(10)  # 添加间距
        modulus_hbox.addWidget(QLabel("单层板横向模量E2(GPa)："))
        modulus_hbox.addWidget(self.composite_E2)
        self.material_layout.addRow(modulus_hbox)
        
        

        modulus_hbox2 = QHBoxLayout()
        modulus_hbox2.addWidget(QLabel("单层板剪切模量G(GPa)："))
        modulus_hbox2.addWidget(self.composite_G)
        modulus_hbox2.addSpacing(10)  # 添加间距
        modulus_hbox2.addWidget(QLabel("单层板泊松比V12："))
        modulus_hbox2.addWidget(self.composite_V12)
        self.material_layout.addRow(modulus_hbox2)
        
        #添加水平分割线
        self.add_VLine(self.material_layout)
        self.core_E = QLineEdit()
        self.core_G = QLineEdit()
        core_hbox = QHBoxLayout()
        core_hbox.addWidget(QLabel("芯材的杨氏模量Ec(GPa)："))
        core_hbox.addWidget(self.core_E)
        core_hbox.addSpacing(10)  # 添加间距
        core_hbox.addWidget(QLabel("芯材的剪切模量Gc(GPa)："))
        core_hbox.addWidget(self.core_G)
        self.material_layout.addRow(core_hbox)
        '''
        self.add_VLine(self.material_layout)
        self.core_E = QLineEdit()
        self.core_G = QLineEdit()
        self.material_layout.addRow("芯材的杨氏模量Ec(GPa)：",self.core_E)
        self.material_layout.addRow("芯材的剪切模量Gc(GPa)：",self.core_G)
        
        
        self.material_group.setLayout(self.material_layout)


        #---------------------------------------------------------------------------------
        # 设置区域
        self.settings_group = QGroupBox("计算设置")
        self.settings_layout = QFormLayout()
        self.settings_layout.setVerticalSpacing(10) #增加表单布局之间的行间距
        
        # 计算设置选项
        self.coor_start = QLabel("请输入载荷加载点坐标值：")
        self.coor_start.setStyleSheet("Font: bold")
        self.coor_end= QLabel("请输入载荷终点坐标值：")
        self.coor_end.setStyleSheet("Font: bold")
        self.load_value= QLineEdit()
        
        self.settings_layout.addRow(self.coor_start)
        
        #设置起始的坐标输入为一列
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("X1:"))
        self.x1_start = QLineEdit()
        hbox1.addWidget(self.x1_start)
        hbox1.addSpacing(10)  # 添加间距
        hbox1.addWidget(QLabel("Y1:"))
        self.y1_start = QLineEdit()
        hbox1.addWidget(self.y1_start)
        self.settings_layout.addRow(hbox1)
        
        '''
        #设置载荷输入的终点坐标值的输入框
        self.settings_layout.addRow(self.coor_end)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("X2:"))
        self.x2_start = QLineEdit()
        hbox2.addWidget(self.x2_start)
        hbox2.addSpacing(10)  # 添加间距
        hbox2.addWidget(QLabel("Y2:"))
        self.y2_start = QLineEdit()
        hbox2.addWidget(self.y2_start)
        self.settings_layout.addRow(hbox2)
        '''
        
        #设置输入均布载荷的值
        # self.settings_layout.addRow("请输入集中载荷值(N)：",self.load_value)
        hbox3 = QHBoxLayout()
        self.load_label = QLabel("请输入均布均布载荷值(N/mm2)：")
        self.load_label.setStyleSheet("Font: bold")
        hbox3.addWidget(self.load_label)
        hbox3.addWidget(self.load_value)
        self.settings_layout.addRow(hbox3)
        
        
        #添加水平分割线
        self.add_VLine(self.settings_layout)
        
        #设置计算指定位置挠度的坐标值
        self.delf_label = QLabel("请输入计算指定位置挠度的坐标值：")
        self.delf_label.setStyleSheet("Font: bold")
        self.settings_layout.addRow(self.delf_label)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(QLabel("X:"))
        self.x_position = QLineEdit()
        hbox4.addWidget(self.x_position)
        hbox4.addSpacing(10)  # 添加间距
        hbox4.addWidget(QLabel("Y:"))
        self.y_position = QLineEdit()
        hbox4.addWidget(self.y_position)
        self.settings_layout.addRow(hbox4)


        
        self.settings_group.setLayout(self.settings_layout)        

        
        #需要计算的操作按钮
        # 按钮区域
        self.btn_group = QGroupBox("计算操作")
        self.btn_layout = QVBoxLayout()
        
        self.densityCal_btn = QPushButton("等效密度计算")
        self.stiffnessCal_btn = QPushButton("弯曲刚度计算")
        self.deflection_btn = QPushButton("指定位置挠度计算")
        self.curveDraw_btn = QPushButton("挠度曲线绘制")

        
        # 设置按钮样式
        button_style = "QPushButton {padding: 8px; font-weight: bold;}"
        self.densityCal_btn.setStyleSheet(button_style + "background-color: #4CAF50; color: white;")
        self.stiffnessCal_btn.setStyleSheet(button_style)
        self.deflection_btn.setStyleSheet(button_style)
        self.curveDraw_btn.setStyleSheet(button_style)
        
        self.btn_layout.addWidget(self.densityCal_btn)
        self.btn_layout.addWidget(self.stiffnessCal_btn)        
        self.btn_layout.addWidget(self.deflection_btn)
        self.btn_layout.addWidget(self.curveDraw_btn)
        self.btn_layout.addStretch()
        
        self.btn_group.setLayout(self.btn_layout)
        
        # 将几何和材料参数组添加到中间布局
        self.center_layout.addWidget(self.geometry_group)
        self.center_layout.addWidget(self.material_group)
        self.center_layout.addWidget(self.settings_group)
        self.center_layout.addWidget(self.btn_group)
        # self.center_layout.addStretch()  # 添加伸缩项使内容靠上
    
    def init_right_panel(self):
        """初始化右侧面板"""
       
        
        # 结果输出区域
        self.output_group = QGroupBox("计算结果显示")
        self.output_layout = QVBoxLayout()
        
        self.density_output_text = QTextEdit()
        self.density_output_text.setReadOnly(True)
        self.density_output_text.setStyleSheet("background-color: #f0f0f0;")
        
        self.stiffness_output_text = QTextEdit()
        self.stiffness_output_text.setReadOnly(True)
        self.stiffness_output_text.setStyleSheet("background-color: #f0f0f0;")
        
        # 添加一些示例输出
        self.density_output_text.setPlainText("计算结果将显示在这里...\n\n"
                                   "1. 最大应力: \n"
                                   "2. 最大应变: \n"
                                   "3. 安全系数: \n"
                                   "4. 重量估算: ")
        self.stiffness_output_text.setPlainText("夹层板的弯曲刚度为\n")
        
        self.output_layout.addWidget(self.density_output_text)
        self.output_layout.addWidget(self.stiffness_output_text)
        self.output_group.setLayout(self.output_layout)
        
        
        #绘制图片
        self.figure = Figure(figsize = (5,4),dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.output_layout.addWidget(self.canvas)
        self.plot()
        # 将设置、按钮和输出添加到右侧布局
        # self.output_layout.setContentsMargins(20, 40, 20, 40)   #定义布局到边缘的距离
        self.right_layout.addWidget(self.output_group)

    

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
    
    def plot(self):
        # 清除之前的图形
        self.figure.clear()
        
        # 创建坐标轴
        ax = self.figure.add_subplot(111)
        
        # 生成数据
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        # 绘制曲线
        ax.plot(x, y, 'b-', linewidth=2)
        
        # 设置标题和标签
        ax.set_title('正弦曲线', fontsize=12)
        ax.set_xlabel('X轴', fontsize=10)
        ax.set_ylabel('Y轴', fontsize=10)
        
        self.figure.subplots_adjust(left=0.2, right=0.9, bottom=0.2, top=0.9)
        
        # 刷新画布
        self.canvas.draw()
        
    def add_VLine(self,layout):
        #添加水平分割线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Raised)  #Raised是凸起，Sunken是凹陷
        line.setStyleSheet("background-color: #ccc; height: 5px;")
        layout.addRow(line)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CompositeDesignApp()
    window.show()
    sys.exit(app.exec_())
    
    
'''
需要解决的问题：
1. 层合板的材料需要输入什么样的参数（Ex,Ey G ?)
2. 材料q(x)是否有位置，还是默认是施加在结构的正中心在？

'''