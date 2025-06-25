import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QLabel, QLineEdit, QFormLayout, QGridLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("平纹织物参数计算")
        self.setGeometry(100, 100, 1000, 600)

        
        # 主布局
        main_layout = QHBoxLayout()
        
        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)
        
        # 结构参数输入 - 使用两列布局
        structure_group = QGroupBox("结构参数输入")
        structure_layout = QGridLayout()
        
        # 第一列参数
        structure_layout.addWidget(QLabel("经纱宽度 aw (mm):"), 0, 0)
        self.aw_edit = QLineEdit()
        structure_layout.addWidget(self.aw_edit, 0, 1)
        
        structure_layout.addWidget(QLabel("经纱厚度 hw (mm):"), 1, 0)
        self.hw_edit = QLineEdit()
        structure_layout.addWidget(self.hw_edit, 1, 1)
        
        structure_layout.addWidget(QLabel("经纱间距 gw (mm):"), 2, 0)
        self.gw_edit = QLineEdit()
        structure_layout.addWidget(self.gw_edit, 2, 1)
        
        structure_layout.addWidget(QLabel("经纱弯曲长度 uw (mm):"), 3, 0)
        self.uw_edit = QLineEdit()
        structure_layout.addWidget(self.uw_edit, 3, 1)
        
        structure_layout.addWidget(QLabel("经纱体积分数 Vfw:"), 4, 0)
        self.Vfw_edit = QLineEdit()
        structure_layout.addWidget(self.Vfw_edit, 4, 1)
        
        # 第二列参数
        structure_layout.addWidget(QLabel("纬纱宽度 af (mm):"), 0, 2)
        self.af_edit = QLineEdit()
        structure_layout.addWidget(self.af_edit, 0, 3)
        
        structure_layout.addWidget(QLabel("纬纱厚度 hf (mm):"), 1, 2)
        self.hf_edit = QLineEdit()
        structure_layout.addWidget(self.hf_edit, 1, 3)
        
        structure_layout.addWidget(QLabel("纬纱间距 gf (mm):"), 2, 2)
        self.gf_edit = QLineEdit()
        structure_layout.addWidget(self.gf_edit, 2, 3)
        
        structure_layout.addWidget(QLabel("纬纱弯曲长度 uf (mm):"), 3, 2)
        self.h_unit_edit = QLineEdit()
        structure_layout.addWidget(self.h_unit_edit, 3, 3)
        
        structure_layout.addWidget(QLabel("纬纱体积分数 Vff:"), 4, 2)
        self.Vff_edit = QLineEdit()
        structure_layout.addWidget(self.Vff_edit, 4, 3)
        
        structure_layout.addWidget(QLabel("单晶胞厚度 h (mm):"), 5, 0, 1, 2, alignment=Qt.AlignRight)
        self.uf_edit = QLineEdit()
        structure_layout.addWidget(self.uf_edit, 5, 2, 1, 1)#从5行3列开始占两行1列
        
        structure_group.setLayout(structure_layout)
        left_layout.addWidget(structure_group)
        
        # 材料参数输入 - 使用两列布局
        material_group = QGroupBox("材料参数输入")
        material_layout = QGridLayout()
        
        # 第一列参数 - 纤维参数
        material_layout.addWidget(QLabel("纤维模量 E1 (MPa):"), 0, 0)
        self.fiber_E1_edit = QLineEdit()
        material_layout.addWidget(self.fiber_E1_edit, 0, 1)
        
        material_layout.addWidget(QLabel("纤维模量 E2 (MPa):"), 1, 0)
        self.fiber_E2_edit = QLineEdit()
        material_layout.addWidget(self.fiber_E2_edit, 1, 1)
        
        material_layout.addWidget(QLabel("纤维模量 E3 (MPa):"), 2, 0)
        self.fiber_E3_edit = QLineEdit()
        material_layout.addWidget(self.fiber_E3_edit, 2, 1)
        
        material_layout.addWidget(QLabel("纤维模量 G12 (MPa):"), 3, 0)
        self.fiber_G12_edit = QLineEdit()
        material_layout.addWidget(self.fiber_G12_edit, 3, 1)
        
        material_layout.addWidget(QLabel("纤维模量G13 (MPa):"), 4, 0)
        self.fiber_G13_edit = QLineEdit()
        material_layout.addWidget(self.fiber_G13_edit, 4, 1)
        
        material_layout.addWidget(QLabel("纤维模量G23 (MPa):"), 5, 0)
        self.fiber_G23_edit = QLineEdit()
        material_layout.addWidget(self.fiber_G23_edit, 5, 1)
        
        
        # 第二列参数 - 树脂参数
        material_layout.addWidget(QLabel("纤维泊松比 v12:"), 0, 2)
        self.fiber_v12_edit = QLineEdit()
        material_layout.addWidget(self.fiber_v12_edit, 0, 3)
        
        material_layout.addWidget(QLabel("纤维泊松比 v13:"), 1, 2)
        self.fiber_v13_edit = QLineEdit()
        material_layout.addWidget(self.fiber_v13_edit, 1, 3)
        
        material_layout.addWidget(QLabel("纤维泊松比 v23:"), 2, 2)
        self.fiber_v23_edit = QLineEdit()
        material_layout.addWidget(self.fiber_v23_edit, 2, 3)
        
        material_layout.addWidget(QLabel("树脂模量 Em (MPa):"), 3, 2)
        self.resin_Em_edit = QLineEdit()
        material_layout.addWidget(self.resin_Em_edit, 3, 3)
        
        material_layout.addWidget(QLabel("树脂模量 Gm (MPa):"), 4, 2)
        self.resin_Gm_edit = QLineEdit()
        material_layout.addWidget(self.resin_Gm_edit, 4, 3)
        
        material_layout.addWidget(QLabel("树脂泊松比 vm:"), 5, 2)
        self.resin_vm_edit = QLineEdit()
        material_layout.addWidget(self.resin_vm_edit, 5, 3)
        
        material_group.setLayout(material_layout)
        left_layout.addWidget(material_group)
        
        # 计算结果输出 - 使用QLineEdit以两列形式显示
        result_group = QGroupBox("计算结果显示")
        result_layout = QGridLayout()
        
        # 创建结果输出框
        self.result_Ex_edit = QLineEdit()
        self.result_Ex_edit.setReadOnly(True)
        self.result_Ey_edit = QLineEdit()
        self.result_Ey_edit.setReadOnly(True)
        self.result_Ez_edit = QLineEdit()
        self.result_Ez_edit.setReadOnly(True)
        self.result_Gxy_edit = QLineEdit()
        self.result_Gxy_edit.setReadOnly(True)
        self.result_Gxz_edit = QLineEdit()
        self.result_Gxz_edit.setReadOnly(True)
        self.result_Gyz_edit = QLineEdit()
        self.result_Gyz_edit.setReadOnly(True)
        self.result_vxy_edit = QLineEdit()
        self.result_vxy_edit.setReadOnly(True)
        self.result_vxz_edit = QLineEdit()
        self.result_vxz_edit.setReadOnly(True)
        self.result_vyz_edit = QLineEdit()
        self.result_vyz_edit.setReadOnly(True)
        self.result_Vf_edit = QLineEdit()
        self.result_Vf_edit.setReadOnly(True)
        
        # 第一列结果
        result_layout.addWidget(QLabel("层合板模量 Ex (MPa):"), 0, 0)
        result_layout.addWidget(self.result_Ex_edit, 0, 1)
        
        result_layout.addWidget(QLabel("层合板模量 Ey (MPa):"), 1, 0)
        result_layout.addWidget(self.result_Ey_edit, 1, 1)
        
        result_layout.addWidget(QLabel("层合板模量 Ez (MPa):"), 2, 0)
        result_layout.addWidget(self.result_Ez_edit, 2, 1)
        
        result_layout.addWidget(QLabel("层合板模量 Gxy (MPa):"), 3, 0)
        result_layout.addWidget(self.result_Gxy_edit, 3, 1)
        
        result_layout.addWidget(QLabel("层合板模量 Gxz (MPa):"), 4, 0)
        result_layout.addWidget(self.result_Gxz_edit, 4, 1)
        
        # 第二列结果
        result_layout.addWidget(QLabel("层合板模量 Gyz (MPa):"), 0, 2)
        result_layout.addWidget(self.result_Gyz_edit, 0, 3)
        
        result_layout.addWidget(QLabel("层合板泊松比 vxy:"), 1, 2)
        result_layout.addWidget(self.result_vxy_edit, 1, 3)
        
        result_layout.addWidget(QLabel("层合板泊松比vxz:"), 2, 2)
        result_layout.addWidget(self.result_vxz_edit, 2, 3)
        
        result_layout.addWidget(QLabel("层合板泊松比vyz:"), 3, 2)
        result_layout.addWidget(self.result_vyz_edit, 3, 3)
        
        result_layout.addWidget(QLabel("纤维体积分数 Vf:"), 4, 2)
        result_layout.addWidget(self.result_Vf_edit, 4, 3)
        
        result_group.setLayout(result_layout)
        left_layout.addWidget(result_group)
        
        # 右侧织物示意图
        image_label = QLabel()
        pixmap = QPixmap("单位制.png")  # 替换为您的图片路径
        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            image_label.setText("图片加载失败")
            print("错误: 无法加载图片，请检查图片路径")
        
        image_label.setAlignment(Qt.AlignCenter)
        
        # 添加到主布局
        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(image_label, 1)
        
        # 设置中心窗口
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # 连接材料参数信号
        for edit in [self.fiber_E1_edit, self.fiber_E2_edit, self.fiber_E3_edit,
                    self.fiber_G12_edit, self.fiber_v12_edit, self.resin_Em_edit, self.resin_vm_edit]:
            edit.textChanged.connect(self.calculate_results)
            
        # 初始计算
        self.calculate_results()
        
        self.setStyleSheet("""            
            QLineEdit {
                background: white;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                
                /* 模拟内阴影 */
                border-top: 1px solid #f0f0f0;
                border-left: 1px solid #f0f0f0;
                border-right: 1px solid #a0a0a0;
                border-bottom: 1px solid #a0a0a0;
            }
            /* 只读输入框样式 */
            QLineEdit[readOnly="true"] {
                background: #f8f8f8;
                color: #333;
                font-weight: bold;
                
                /* 凸起效果 */
                border-top: 1px solid #e0e0e0;
                border-left: 1px solid #e0e0e0;
                border-right: 1px solid #a0a0a0;
                border-bottom: 1px solid #a0a0a0;
            }
            
            /* 标签样式 */
            QLabel {
                font-size: 13px;
                color: #555;
            }
        """)        
    def calculate_results(self):
        try:
            # 获取输入参数
            fiber_E1 = float(self.fiber_E1_edit.text())
            fiber_E2 = float(self.fiber_E2_edit.text())
            fiber_E3 = float(self.fiber_E3_edit.text())
            fiber_G12 = float(self.fiber_G12_edit.text())
            fiber_v12 = float(self.fiber_v12_edit.text())
            
            resin_E = float(self.resin_E_edit.text())
            resin_v = float(self.resin_v_edit.text())
            
            # 这里应该是实际的计算过程
            # 由于这是一个示例，我们只做简单的模拟计算
            
            # 模拟计算结果
            E1 = fiber_E1 * 0.6 + resin_E * 0.4
            E2 = fiber_E2 * 0.5 + resin_E * 0.5
            E3 = fiber_E3 * 0.5 + resin_E * 0.5
            G12 = fiber_G12 * 0.55 + resin_E/(2*(1+resin_v)) * 0.45
            v12 = fiber_v12 * 0.6 + resin_v * 0.4
            
            # 更新结果输出框
            self.result_E1_edit.setText(f"{E1:.2f}")
            self.result_E2_edit.setText(f"{E2:.2f}")
            self.result_E3_edit.setText(f"{E3:.2f}")
            self.result_G12_edit.setText(f"{G12:.2f}")
            self.result_v12_edit.setText(f"{v12:.4f}")
            
        except ValueError:
            # 清空结果框
            self.result_Ex_edit.clear()
            self.result_Ey_edit.clear()
            self.result_Ez_edit.clear()
            self.result_Gxy_edit.clear()
            self.result_vxy_edit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())