import sys
import datetime
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# ===== 导入 GunmuCore =====
import GunmuCore

# ===== 日志函数 =====
def log(msg, level='INFO'):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] [{level}] {msg}')

class GunmuDocs(QMainWindow):
    def __init__(self):
        super().__init__()
        log('🚀 GunmuDocs 初始化开始')
        
        self.setWindowTitle('🌳 Gunmu Docs')
        self.setGeometry(100, 100, 900, 700)
        self.current_mode = 'gunmu'
        self.current_file = None  # 当前打开的文件路径
        
        # ===== 堆叠布局 =====
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        
        self.home_page = self.create_home_page()
        self.editor_page = self.create_editor_page()
        
        self.stacked.addWidget(self.home_page)      # index 0
        self.stacked.addWidget(self.editor_page)    # index 1
        
        self.stacked.setCurrentIndex(0)
        log('✅ GunmuDocs 初始化完成')
    
    # ========== 主页 ==========
    def create_home_page(self):
        log('🏠 创建主页')
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        title = QLabel('🌳 Gunmu Docs')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 48px; font-weight: bold; color: #4ecdc4; padding: 40px;')
        layout.addWidget(title)
        
        subtitle = QLabel('选择你的加密模式')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet('font-size: 18px; color: #888; padding-bottom: 30px;')
        layout.addWidget(subtitle)
        
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(15)
        
        # 三种模式按钮
        modes = [
            ('🌳 新建 Gunmu 文档', 'gunmu', '#0f3460', '.gunmu'),
            ('🎯 新建 Otto 文档', 'otto', '#2d4059', '.gotto'),
            ('🌲 新建 Emoji 文档', 'emoji', '#1a5a3a', '.gemoji'),
        ]
        
        for label, mode, color, ext in modes:
            btn = QPushButton(label)
            btn.setStyleSheet(f'''
                QPushButton {{
                    font-size: 24px;
                    padding: 30px;
                    background: {color};
                    color: white;
                    border: none;
                    border-radius: 12px;
                }}
                QPushButton:hover {{
                    background: {color};
                    opacity: 0.8;
                }}
            ''')
            btn.clicked.connect(lambda checked, m=mode, e=ext: self.open_editor(m, e))
            btn_layout.addWidget(btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        return page
    
    # ========== 编辑器页面 ==========
    def create_editor_page(self):
        log('📝 创建编辑器页面')
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        
        # 顶部栏
        top_bar = QHBoxLayout()
        
        back_btn = QPushButton('← 返回主页')
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(self.go_home)
        top_bar.addWidget(back_btn)
        
        self.mode_label = QLabel('当前模式: 🌳 Gunmu')
        self.mode_label.setStyleSheet('font-size: 16px; color: #4ecdc4; font-weight: bold;')
        top_bar.addWidget(self.mode_label)
        
        top_bar.addStretch()
        layout.addLayout(top_bar)
        
        # 双栏编辑区
        splitter = QSplitter(Qt.Horizontal)
        
        # 左：输入
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        left_label = QLabel('📝 输入')
        left_label.setStyleSheet('font-weight: bold; color: #4ecdc4;')
        left_layout.addWidget(left_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('在这里输入文本...')
        left_layout.addWidget(self.text_edit)
        
        # 右：输出
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        right_label = QLabel('📄 输出')
        right_label.setStyleSheet('font-weight: bold; color: #ff6b6b;')
        right_layout.addWidget(right_label)
        
        self.output_edit = QTextEdit()
        self.output_edit.setPlaceholderText('编码/解码结果将显示在这里...')
        self.output_edit.setReadOnly(True)
        right_layout.addWidget(self.output_edit)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([450, 450])
        layout.addWidget(splitter)
        
        # 操作按钮
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        
        self.encode_btn = QPushButton('🌳 编码')
        self.encode_btn.clicked.connect(self.do_encode)
        btn_row.addWidget(self.encode_btn)
        
        self.decode_btn = QPushButton('🌿 解码')
        self.decode_btn.clicked.connect(self.do_decode)
        btn_row.addWidget(self.decode_btn)
        
        self.swap_btn = QPushButton('🔄 交换')
        self.swap_btn.clicked.connect(self.swap_texts)
        btn_row.addWidget(self.swap_btn)
        
        self.clear_btn = QPushButton('🗑️ 清空')
        self.clear_btn.clicked.connect(self.clear_all)
        btn_row.addWidget(self.clear_btn)
        
        btn_row.addStretch()
        layout.addLayout(btn_row)
        
        # ===== 文件操作按钮 =====
        file_row = QHBoxLayout()
        file_row.setSpacing(10)
        
        self.save_btn = QPushButton('💾 保存文件')
        self.save_btn.clicked.connect(self.save_file)
        file_row.addWidget(self.save_btn)
        
        self.save_as_btn = QPushButton('📂 另存为')
        self.save_as_btn.clicked.connect(self.save_as_file)
        file_row.addWidget(self.save_as_btn)
        
        self.open_btn = QPushButton('📂 打开文件')
        self.open_btn.clicked.connect(self.open_file)
        file_row.addWidget(self.open_btn)
        
        file_row.addStretch()
        layout.addLayout(file_row)
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('✅ 就绪')
        
        return page
    
    # ========== 功能函数 ==========
    def open_editor(self, mode, ext):
        log(f'📂 打开编辑器, 模式: {mode}')
        self.current_mode = mode
        self.current_ext = ext
        self.current_file = None
        
        mode_display = {
            'gunmu': '🌳 Gunmu (滚木)',
            'otto': '🎯 Otto',
            'emoji': '🌲 Emoji'
        }.get(mode, mode)
        
        self.mode_label.setText(f'当前模式: {mode_display}')
        
        placeholder = f'输入文本，点击编码转为{mode_display}...'
        self.text_edit.setPlaceholderText(placeholder)
        self.text_edit.clear()
        self.output_edit.clear()
        
        self.stacked.setCurrentIndex(1)
        self.status_bar.showMessage(f'✅ 已切换到 {mode_display} 模式')
        log(f'✅ 已切换到 {mode_display} 模式')
    
    def go_home(self):
        log('🏠 返回主页')
        self.stacked.setCurrentIndex(0)
        self.status_bar.showMessage('✅ 返回主页')
    
    def do_encode(self):
        text = self.text_edit.toPlainText()
        log(f'📝 编码请求, 输入长度: {len(text)} 字符')
        
        if not text:
            log('⚠️ 输入为空', 'WARN')
            self.status_bar.showMessage('⚠️ 请先输入文本')
            return
        
        try:
            mode_map = {
                'gunmu': '滚木',
                'otto': 'otto',
                'emoji': 'emoji'
            }
            mode_name = mode_map.get(self.current_mode, '滚木')
            
            log(f'🔧 调用 GunmuCore 编码, 模式: {mode_name}')
            binary = GunmuCore.getBinary(text)
            log(f'✅ getBinary 完成, 二进制长度: {len(binary)}')
            
            result = GunmuCore.encode(binary, mode_name)
            log(f'✅ encode 完成, 结果长度: {len(result)}')
            
            self.output_edit.setText(result)
            self.status_bar.showMessage(f'✅ 编码成功！{len(text)} 字符 → {len(result)} 字符')
            log(f'✅ 编码成功！{len(text)} 字符 → {len(result)} 字符')
        except Exception as e:
            log(f'❌ 编码失败: {str(e)}', 'ERROR')
            self.status_bar.showMessage(f'❌ 编码失败: {str(e)}')
    
    def do_decode(self):
        text = self.text_edit.toPlainText()
        log(f'📝 解码请求, 输入长度: {len(text)} 字符')
        
        if not text:
            log('⚠️ 输入为空', 'WARN')
            self.status_bar.showMessage('⚠️ 请先输入文本')
            return
        
        try:
            mode_map = {
                'gunmu': '滚木',
                'otto': 'otto',
                'emoji': 'emoji'
            }
            mode_name = mode_map.get(self.current_mode, '滚木')
            
            log(f'🔧 调用 GunmuCore 解码, 模式: {mode_name}')
            binary = GunmuCore.decode(text, mode_name)
            log(f'✅ decode 完成, 二进制长度: {len(binary)}')
            
            result = GunmuCore.notBinary(binary)
            log(f'✅ notBinary 完成, 结果长度: {len(result)}')
            
            self.output_edit.setText(result)
            self.status_bar.showMessage(f'✅ 解码成功！{len(text)} 字符 → {len(result)} 字符')
            log(f'✅ 解码成功！{len(text)} 字符 → {len(result)} 字符')
        except Exception as e:
            log(f'❌ 解码失败: {str(e)}', 'ERROR')
            self.status_bar.showMessage(f'❌ 解码失败: {str(e)}')
    
    def swap_texts(self):
        log('🔄 交换输入输出')
        input_text = self.text_edit.toPlainText()
        output_text = self.output_edit.toPlainText()
        self.text_edit.setText(output_text)
        self.output_edit.setText(input_text)
        self.status_bar.showMessage('🔄 已交换')
    
    def clear_all(self):
        log('🗑️ 清空所有内容')
        self.text_edit.clear()
        self.output_edit.clear()
        self.status_bar.showMessage('🗑️ 已清空')
    
    # ========== 文件操作 ==========
    def save_file(self):
        """保存文件（如果已有路径则直接保存，否则另存为）"""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """另存为"""
        mode_map = {
            'gunmu': ('滚木文件 (*.gunmu)', '.gunmu'),
            'otto': ('Otto文件 (*.gotto)', '.gotto'),
            'emoji': ('Emoji文件 (*.gemoji)', '.gemoji')
        }
        file_filter, default_ext = mode_map.get(self.current_mode, ('所有文件 (*.*)', ''))
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            '保存文件',
            os.path.expanduser('~'),
            file_filter
        )
        
        if file_path:
            # 如果没有扩展名，自动添加
            if not os.path.splitext(file_path)[1]:
                file_path += default_ext
            self.current_file = file_path
            self._save_to_file(file_path)
    
    def _save_to_file(self, file_path):
        """实际保存操作"""
        try:
            content = self.output_edit.toPlainText()
            if not content:
                content = self.text_edit.toPlainText()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.status_bar.showMessage(f'✅ 已保存: {os.path.basename(file_path)}')
            log(f'✅ 保存文件: {file_path}')
        except Exception as e:
            log(f'❌ 保存失败: {str(e)}', 'ERROR')
            self.status_bar.showMessage(f'❌ 保存失败: {str(e)}')
    
    def open_file(self):
        """打开文件"""
        file_filter = 'Gunmu文件 (*.gunmu *.gotto *.gemoji);;所有文件 (*.*)'
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '打开文件',
            os.path.expanduser('~'),
            file_filter
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 根据扩展名自动切换模式
                ext = os.path.splitext(file_path)[1].lower()
                mode_map = {
                    '.gunmu': 'gunmu',
                    '.gotto': 'otto',
                    '.gemoji': 'emoji'
                }
                mode = mode_map.get(ext, 'gunmu')
                
                # 自动切换到对应模式
                if mode != self.current_mode:
                    self.current_mode = mode
                    mode_display = {
                        'gunmu': '🌳 Gunmu (滚木)',
                        'otto': '🎯 Otto',
                        'emoji': '🌲 Emoji'
                    }.get(mode, mode)
                    self.mode_label.setText(f'当前模式: {mode_display}')
                
                self.text_edit.setText(content)
                self.output_edit.clear()
                self.current_file = file_path
                self.status_bar.showMessage(f'✅ 已打开: {os.path.basename(file_path)}')
                log(f'✅ 打开文件: {file_path}')
            except Exception as e:
                log(f'❌ 打开失败: {str(e)}', 'ERROR')
                self.status_bar.showMessage(f'❌ 打开失败: {str(e)}')

if __name__ == '__main__':
    log('🌟 GunmuDocs 启动')
    app = QApplication(sys.argv)
    window = GunmuDocs()
    window.show()
    log('🖥️ 窗口已显示')
    sys.exit(app.exec_())