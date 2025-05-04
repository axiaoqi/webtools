import tkinter as tk
from tkinter import ttk, filedialog, messagebox
# Import TkinterDnD from tkinterdnd2 library
from tkinterdnd2 import DND_FILES, TkinterDnD
import pathlib
import threading
import platform # To potentially help with path parsing if needed
import time # For status updates during potentially long scans

# --- 中文字符串定义 ---
# (保持不变，这里省略以减少篇幅，请使用上一版本中的 STRINGS_CN 字典)
STRINGS_CN = {
    "window_title": "TXT 文件合并工具",
    "drop_label": "请拖放文件夹或 TXT 文件到此处", # 更新拖放提示
    "start_button": "开始合并",
    "clear_button": "清空列表",
    "status_ready": "准备就绪。请拖放文件夹或 TXT 文件。", # 更新准备提示
    "status_busy_add": "操作进行中，无法添加。",
    "status_scanning_folder": "正在扫描 {count} 个新文件夹...",
    "status_no_valid_items": "拖放的内容中不包含有效的文件夹或 TXT 文件。", # 更新无效提示
    "status_items_processed": "拖放的项目已处理（可能包含重复项）。", # 更新重复提示
    "status_added_files": "直接添加了 {count} 个 TXT 文件。",
    "status_added_files_and_scanning": "直接添加 {f_count} 个文件，正在扫描 {d_count} 个文件夹...",
    "status_cleared": "列表已清空。准备就绪。",
    "status_scanning": "正在扫描: {folder_name}...",
    "status_scan_error": "扫描 {folder_name} 出错: {error}",
    "status_scan_fatal_error": "扫描过程中发生严重错误。",
    "status_scan_complete": "扫描完成 ({elapsed:.2f}秒). 发现 {new_count} 个新文件。总计: {total_count} 个文件。",
    "status_scan_failed": "扫描失败！详情请查看消息框或控制台。",
    "status_merge_cancelled": "合并已取消。",
    "status_merge_starting": "开始合并...",
    "status_merging": "正在合并 {current}/{total} 个文件...",
    "status_merge_complete_errors": "合并完成，有 {error_count} 个错误。已处理 {success_count}/{total_count} 个文件。",
    "status_merge_complete_success": "合并完成！已处理 {success_count} 个文件。准备就绪。",
    "status_merge_failed": "合并失败！详情请查看消息框或控制台。",

    "msg_busy_title": "忙碌",
    "msg_busy_clear": "操作进行中，无法清空列表。",
    "msg_confirm_exit_title": "确认退出",
    "msg_confirm_exit_scan": "扫描正在进行中。确定要退出吗？",
    "msg_confirm_exit_merge": "合并正在进行中。确定要退出吗？",
    "msg_scan_error_title": "扫描错误",
    "msg_scan_error_body": "扫描过程中发生错误:\n{error_message}",
    "msg_input_error_title": "输入错误",
    "msg_input_error_body": "列表中没有 TXT 文件可供合并。", # 调整无文件提示
    "msg_merge_complete_errors_title": "合并完成（有错误）",
    "msg_merge_complete_errors_body": "合并完成，出现 {error_count} 个错误。\n成功合并 {success_count}/{total_count} 个文件到:\n{output_path}\n\n出错或跳过的文件:\n - {error_list}\n\n详情请查看控制台日志。",
    "msg_merge_success_title": "成功",
    "msg_merge_success_body": "合并完成！\n{success_count} 个文件已成功合并到:\n{output_path}",
    "msg_merge_error_title": "合并错误",
    "msg_merge_error_body": "合并过程中发生错误:\n{error_message}",
    "msg_dependency_error_title": "缺少依赖项",
    "msg_dependency_error_body": "必需的库 'tkinterdnd2' 未找到。\n\n请使用以下命令安装:\npip install tkinterdnd2",

    "file_dialog_title": "将合并文件另存为",
    "file_dialog_type_txt": "文本文件",
    "file_dialog_type_all": "所有文件",

    "console_ignore_item": "忽略无效项目: {path}", # 更新忽略提示
    "console_error_resolve": "解析或检查路径 '{path}' 时出错: {error}",
    "console_already_scanned": "文件夹已被扫描或添加: {path}",
    "console_scan_in_progress": "扫描已在进行中。",
    "console_scanning_folder": "正在扫描: {path}",
    "console_os_error": "扫描文件夹 {path} 时操作系统错误: {error}",
    "console_scan_unexpected_error": "扫描文件夹 {path} 时发生意外错误: {error}",
    "console_fatal_scan_error": "扫描过程中发生严重错误: {error}",
    "console_file_already_in_list": "文件已在列表中: {path}",
    "console_adding_file": "直接添加文件: {path}",
    "console_error_processing": "处理文件 '{filename}' 时出错: {error}",
    "console_skipping_missing": "跳过不存在的文件: {path}",
    "console_fatal_merge_error": "合并过程中发生严重错误: {error}",
    "console_dep_error_1": "错误：必需的库 'tkinterdnd2' 未找到。",
    "console_dep_error_2": "请使用以下命令安装: pip install tkinterdnd2",
}

# --- 尝试设置中文兼容字体 ---
DEFAULT_FONT = "Microsoft YaHei"
FALLBACK_FONT = "Arial"
APP_FONT = None
LISTBOX_FONT_CONFIG = {}
FONT_CONFIG = {}
try:
    import tkinter.font
    fonts = tkinter.font.families()
    if DEFAULT_FONT not in fonts:
        print(f"警告：字体 '{DEFAULT_FONT}' 未找到，尝试使用 '{FALLBACK_FONT}'。")
        if FALLBACK_FONT not in fonts:
             print(f"警告：备用字体 '{FALLBACK_FONT}' 也未找到，使用系统默认字体。")
             APP_FONT = None
        else: APP_FONT = FALLBACK_FONT
    else: APP_FONT = DEFAULT_FONT
except ImportError: APP_FONT = None
except Exception as e: print(f"检查字体时出错: {e}，使用系统默认字体。"); APP_FONT = None

if APP_FONT:
    FONT_CONFIG = {"font": (APP_FONT, 10)}
    LISTBOX_FONT_CONFIG = {"font": (APP_FONT, 9)}

# --- 主应用类 ---
class TextMergerApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title(STRINGS_CN["window_title"])
        self.geometry("700x550")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.scanned_folders = set()
        self.txt_file_paths = []
        self.lock = threading.Lock()

        self.scanning_in_progress = False
        self.merging_in_progress = False
        self.scan_thread = None
        self.merge_thread = None

        style = ttk.Style(self)
        style.configure('TFrame', padding=5)
        style.configure('TButton', padding=5, **FONT_CONFIG)
        style.configure('TLabel', padding=5, **FONT_CONFIG)

        # Top Frame for Drop Area
        self.drop_frame = ttk.Frame(self, relief=tk.SUNKEN, borderwidth=2, style='TFrame')
        self.drop_frame.pack(pady=10, padx=10, fill=tk.X)

        self.drop_label = ttk.Label(
            self.drop_frame,
            text=STRINGS_CN["drop_label"], # Updated text
            anchor=tk.CENTER,
            font=(APP_FONT, 12) if APP_FONT else ("Arial", 12)
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True, ipady=20)

        # Middle Frame for File Listbox and Scrollbar
        self.list_frame = ttk.Frame(self, style='TFrame')
        self.list_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.listbox_scrollbar_y = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL)
        self.listbox_scrollbar_x = ttk.Scrollbar(self.list_frame, orient=tk.HORIZONTAL)

        self.listbox = tk.Listbox(
            self.list_frame,
            yscrollcommand=self.listbox_scrollbar_y.set,
            xscrollcommand=self.listbox_scrollbar_x.set,
            selectmode=tk.EXTENDED,
            bg='white',
            relief=tk.FLAT,
            **LISTBOX_FONT_CONFIG
        )
        self.listbox_scrollbar_y.config(command=self.listbox.yview)
        self.listbox_scrollbar_x.config(command=self.listbox.xview)

        self.listbox_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bottom Frame for Buttons
        self.button_frame = ttk.Frame(self, style='TFrame')
        self.button_frame.pack(pady=5, padx=10, fill=tk.X)

        self.start_button = ttk.Button(
            self.button_frame,
            text=STRINGS_CN["start_button"],
            command=self.start_merge_thread,
            style='TButton'
        )
        self.start_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.clear_button = ttk.Button(
            self.button_frame,
            text=STRINGS_CN["clear_button"],
            command=self.clear_list,
            style='TButton'
        )
        self.clear_button.pack(side=tk.RIGHT, padx=5, expand=True, fill=tk.X)

        # Status Label
        self.status_label = ttk.Label(self, text=STRINGS_CN["status_ready"], anchor=tk.W, style='TLabel')
        self.status_label.pack(pady=(5, 10), padx=10, fill=tk.X)

        # Drag and Drop Setup
        self.drop_target_widgets = [self.drop_label, self.listbox]
        for widget in self.drop_target_widgets:
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', self.handle_drop)
            widget.dnd_bind('<<DropEnter>>', self.on_drop_enter)
            widget.dnd_bind('<<DropLeave>>', self.on_drop_leave)

        self.update_ui_state()

    # --- Drag and Drop Handlers ---
    def parse_drop_data(self, data_string):
        """
        解析拖放数据字符串。
        返回一个包含有效目录 Path 对象和有效 .txt 文件 Path 对象的列表。
        """
        # (路径解析逻辑保持不变)
        paths = []
        data_string = data_string.strip()
        current_path = ''
        in_braces = False
        for char in data_string:
            if char == '{' and not in_braces: in_braces = True; current_path = ''
            elif char == '}' and in_braces:
                in_braces = False
                if current_path: paths.append(pathlib.Path(current_path))
                current_path = ''
            elif char == ' ' and not in_braces:
                if current_path: paths.append(pathlib.Path(current_path))
                current_path = ''
            else: current_path += char
        if current_path: paths.append(pathlib.Path(current_path))

        if not paths and ' ' in data_string.strip() and '{' not in data_string:
             try: paths = [pathlib.Path(p) for p in data_string.strip().split()]
             except Exception: pass

        valid_items = []
        for p in paths:
            try:
                # 尝试解析路径，但不要求严格存在，因为文件可能临时不可访问
                # 我们将在实际添加或扫描时再次检查
                resolved_p = p.resolve() # Resolve to absolute path

                # *** 修改验证逻辑 ***
                if resolved_p.is_dir():
                    valid_items.append(resolved_p) # 是目录，有效
                elif resolved_p.is_file() and resolved_p.suffix.lower() == '.txt':
                    valid_items.append(resolved_p) # 是文件且后缀为 .txt，有效
                else:
                     print(STRINGS_CN["console_ignore_item"].format(path=resolved_p))
            except FileNotFoundError:
                 print(STRINGS_CN["console_ignore_item"].format(path=p)) # 文件或目录不存在
            except Exception as e:
                 # 捕获其他可能的解析错误，例如权限问题
                 print(STRINGS_CN["console_error_resolve"].format(path=p, error=e))

        return valid_items


    def handle_drop(self, event):
        """处理拖放事件，区分文件和文件夹"""
        self.on_drop_leave(event)
        if self.scanning_in_progress or self.merging_in_progress:
            self.status_label.config(text=STRINGS_CN["status_busy_add"])
            return

        dropped_paths_str = event.data
        potential_items = self.parse_drop_data(dropped_paths_str)

        folders_to_scan_now = []
        files_added_directly = 0

        with self.lock: # 保护对 scanned_folders 和 txt_file_paths 的访问
            for item_path in potential_items:
                try:
                    # 再次检查存在性和类型，因为 resolve() 可能没有严格检查
                    if item_path.is_dir():
                        if item_path not in self.scanned_folders:
                            folders_to_scan_now.append(item_path)
                            self.scanned_folders.add(item_path)
                            print(f"准备扫描文件夹: {item_path}")
                        else:
                            print(STRINGS_CN["console_already_scanned"].format(path=item_path))
                    elif item_path.is_file() and item_path.suffix.lower() == '.txt':
                        # 对于文件，检查是否已在最终的文件列表 txt_file_paths 中
                        if item_path not in self.txt_file_paths:
                            self.txt_file_paths.append(item_path)
                            self.listbox.insert(tk.END, str(item_path))
                            files_added_directly += 1
                            print(STRINGS_CN["console_adding_file"].format(path=item_path))
                        else:
                            print(STRINGS_CN["console_file_already_in_list"].format(path=item_path))
                    # 如果 resolve() 成功但现在 is_dir()/is_file() 失败，忽略它
                except Exception as e:
                     print(f"添加项目时出错 '{item_path}': {e}") # 例如检查时权限问题

        # 更新状态和启动扫描（如果在循环外进行可以合并状态更新）
        if folders_to_scan_now and files_added_directly > 0:
            self.status_label.config(
                text=STRINGS_CN["status_added_files_and_scanning"].format(
                    f_count=files_added_directly, d_count=len(folders_to_scan_now)
                )
            )
            self.start_scan_thread(folders_to_scan_now)
        elif folders_to_scan_now:
            self.status_label.config(
                text=STRINGS_CN["status_scanning_folder"].format(count=len(folders_to_scan_now))
            )
            self.start_scan_thread(folders_to_scan_now)
        elif files_added_directly > 0:
            self.status_label.config(
                text=STRINGS_CN["status_added_files"].format(count=files_added_directly)
            )
             # 如果只添加了文件，确保列表滚动到底部并更新UI状态
            self.listbox.see(tk.END)
            self.update_ui_state()
        elif not potential_items:
             self.status_label.config(text=STRINGS_CN["status_no_valid_items"])
        else:
             # 所有拖放的项目要么无效，要么是重复的
             self.status_label.config(text=STRINGS_CN["status_items_processed"])


    def on_drop_enter(self, event):
        if not self.scanning_in_progress and not self.merging_in_progress:
            widget = event.widget
            try: widget.config(background='lightblue')
            except tk.TclError: pass


    def on_drop_leave(self, event):
        widget = event.widget
        default_bg = 'SystemButtonFace'
        if isinstance(widget, tk.Listbox): default_bg = 'white'
        elif isinstance(widget, ttk.Label):
             try: default_bg = ttk.Style().lookup(widget.winfo_class(), 'background')
             except Exception: pass
        try: widget.config(background=default_bg)
        except tk.TclError: pass

    # --- List and UI Management ---
    def clear_list(self):
        if self.scanning_in_progress or self.merging_in_progress:
            messagebox.showwarning(STRINGS_CN["msg_busy_title"], STRINGS_CN["msg_busy_clear"])
            return
        with self.lock:
            self.scanned_folders.clear()
            self.txt_file_paths.clear()
        self.listbox.delete(0, tk.END)
        self.status_label.config(text=STRINGS_CN["status_cleared"])
        self.update_ui_state()

    def update_ui_state(self):
        scanning = self.scanning_in_progress
        merging = self.merging_in_progress
        busy = scanning or merging
        with self.lock: list_empty = not self.txt_file_paths

        start_state = tk.DISABLED if (busy or list_empty) else tk.NORMAL
        clear_state = tk.DISABLED if busy else tk.NORMAL

        self.start_button.config(state=start_state)
        self.clear_button.config(state=clear_state)
        # 拖放目标保持启用状态，在 handle_drop 中检查忙碌状态

    def on_closing(self):
        # (保持不变)
        if self.scanning_in_progress:
            if messagebox.askyesno(STRINGS_CN["msg_confirm_exit_title"], STRINGS_CN["msg_confirm_exit_scan"]): self.destroy()
        elif self.merging_in_progress:
            if messagebox.askyesno(STRINGS_CN["msg_confirm_exit_title"], STRINGS_CN["msg_confirm_exit_merge"]): self.destroy()
        else: self.destroy()

    # --- Scanning Logic (Threaded) ---
    # (start_scan_thread, _perform_scan, _scan_complete, _scan_error 保持不变)
    def start_scan_thread(self, folders_to_scan):
        if self.scan_thread and self.scan_thread.is_alive():
            print(STRINGS_CN["console_scan_in_progress"])
            return
        self.scanning_in_progress = True
        self.update_ui_state()
        self.scan_thread = threading.Thread(
            target=self._perform_scan, args=(folders_to_scan,), daemon=True
        )
        self.scan_thread.start()

    def _perform_scan(self, folders_to_scan):
        found_files_in_this_scan = []
        total_scanned_count = 0
        start_time = time.time()
        try:
            for folder_p in folders_to_scan:
                print(STRINGS_CN["console_scanning_folder"].format(path=folder_p))
                self.after(0, self.update_status, STRINGS_CN["status_scanning"].format(folder_name=folder_p.name))
                try:
                    for txt_file in folder_p.rglob('*.txt'):
                        if txt_file.is_file():
                            found_files_in_this_scan.append(txt_file)
                            total_scanned_count += 1
                except OSError as oe:
                     print(STRINGS_CN["console_os_error"].format(path=folder_p, error=oe))
                     self.after(0, self.update_status, STRINGS_CN["status_scan_error"].format(folder_name=folder_p.name, error=oe))
                except Exception as e:
                     print(STRINGS_CN["console_scan_unexpected_error"].format(path=folder_p, error=e))
                     self.after(0, self.update_status, STRINGS_CN["status_scan_error"].format(folder_name=folder_p.name, error='未知错误'))
            self.after(0, self._scan_complete, found_files_in_this_scan, total_scanned_count, start_time)
        except Exception as e:
            error_msg = STRINGS_CN["console_fatal_scan_error"].format(error=e)
            print(error_msg)
            self.after(0, self._scan_error, error_msg)

    def _scan_complete(self, newly_found_files, scanned_count, start_time):
        newly_added_to_list = 0
        current_total = 0
        with self.lock:
            for file_path in newly_found_files:
                # 检查是否已存在（可能被直接拖放或在其他扫描中找到）
                if file_path not in self.txt_file_paths:
                    self.txt_file_paths.append(file_path)
                    self.listbox.insert(tk.END, str(file_path))
                    newly_added_to_list += 1
                else:
                    print(f"扫描发现的文件已存在于列表中: {file_path}") # Debug info
            current_total = len(self.txt_file_paths)

        if newly_added_to_list > 0: self.listbox.see(tk.END)

        elapsed = time.time() - start_time
        # 更新状态，即使扫描线程结束，也报告总数
        self.status_label.config(
            text=STRINGS_CN["status_scan_complete"].format(
                elapsed=elapsed, new_count=newly_added_to_list, total_count=current_total
            )
        )
        self.scanning_in_progress = False
        self.scan_thread = None
        self.update_ui_state() # 更新按钮状态等

    def _scan_error(self, error_message):
        self.status_label.config(text=STRINGS_CN["status_scan_failed"])
        messagebox.showerror(
            STRINGS_CN["msg_scan_error_title"],
            STRINGS_CN["msg_scan_error_body"].format(error_message=error_message)
        )
        self.scanning_in_progress = False
        self.scan_thread = None
        self.update_ui_state()

    # --- Merging Logic (Threaded) ---
    # (start_merge_thread, _perform_merge, _merge_complete, _merge_error 保持不变)
    def start_merge_thread(self):
        if self.scanning_in_progress or self.merging_in_progress: return
        with self.lock:
             if not self.txt_file_paths:
                 messagebox.showerror(STRINGS_CN["msg_input_error_title"], STRINGS_CN["msg_input_error_body"])
                 return
             files_to_merge_copy = list(self.txt_file_paths)

        output_path_str = filedialog.asksaveasfilename(
            title=STRINGS_CN["file_dialog_title"],
            defaultextension=".txt",
            filetypes=[(STRINGS_CN["file_dialog_type_txt"], "*.txt"),
                       (STRINGS_CN["file_dialog_type_all"], "*.*")]
        )
        if not output_path_str:
            self.status_label.config(text=STRINGS_CN["status_merge_cancelled"])
            return
        output_path = pathlib.Path(output_path_str)
        self.merging_in_progress = True
        self.update_ui_state()
        self.status_label.config(text=STRINGS_CN["status_merge_starting"])
        self.merge_thread = threading.Thread(
            target=self._perform_merge, args=(files_to_merge_copy, output_path), daemon=True
        )
        self.merge_thread.start()

    def _perform_merge(self, txt_file_list, output_file_path):
        file_count = 0
        error_files = []
        total_files = len(txt_file_list)
        try:
            self.after(0, self.update_status, STRINGS_CN["status_merging"].format(current=0, total=total_files))
            with output_file_path.open('w', encoding='utf-8') as outfile:
                for idx, txt_file in enumerate(txt_file_list):
                    if txt_file.is_file():
                        try:
                            filename_no_ext = txt_file.stem
                            content = txt_file.read_text(encoding='utf-8', errors='ignore')
                            outfile.write(f"{filename_no_ext}\n")
                            outfile.write(content)
                            outfile.write("\n\n")
                            file_count += 1
                            if (idx + 1) % 10 == 0 or (idx + 1) == total_files:
                                self.after(0, self.update_status, STRINGS_CN["status_merging"].format(current=idx+1, total=total_files))
                        except Exception as e:
                            error_msg = STRINGS_CN["console_error_processing"].format(filename=txt_file.name, error=e)
                            print(error_msg)
                            error_files.append(str(txt_file))
                    else:
                        error_msg = STRINGS_CN["console_skipping_missing"].format(path=txt_file)
                        print(error_msg)
                        error_files.append(f"{txt_file} (不存在)")
            self.after(0, self._merge_complete, output_file_path, file_count, total_files, error_files)
        except Exception as e:
            error_msg = STRINGS_CN["console_fatal_merge_error"].format(error=e)
            print(error_msg)
            self.after(0, self._merge_error, error_msg)

    def update_status(self, message):
        is_scanning = self.scanning_in_progress and self.scan_thread and self.scan_thread.is_alive()
        is_merging = self.merging_in_progress and self.merge_thread and self.merge_thread.is_alive()
        if is_scanning or is_merging:
            self.status_label.config(text=message)

    def _merge_complete(self, output_path, count_success, count_total, errors):
        self.merging_in_progress = False
        self.merge_thread = None
        if errors:
            error_list_str = "\n - ".join(errors[:10])
            if len(errors) > 10: error_list_str += f"\n ...以及其他 {len(errors)-10} 个。"
            warning_msg = STRINGS_CN["msg_merge_complete_errors_body"].format(
                error_count=len(errors), success_count=count_success, total_count=count_total,
                output_path=output_path, error_list=error_list_str
            )
            self.status_label.config(
                text=STRINGS_CN["status_merge_complete_errors"].format(
                    error_count=len(errors), success_count=count_success, total_count=count_total
                )
            )
            messagebox.showwarning(STRINGS_CN["msg_merge_complete_errors_title"], warning_msg)
        else:
            success_msg = STRINGS_CN["msg_merge_success_body"].format(
                success_count=count_success, output_path=output_path
            )
            self.status_label.config(
                text=STRINGS_CN["status_merge_complete_success"].format(success_count=count_success)
            )
            messagebox.showinfo(STRINGS_CN["msg_merge_success_title"], success_msg)
        self.update_ui_state()

    def _merge_error(self, error_message):
        self.merging_in_progress = False
        self.merge_thread = None
        self.status_label.config(text=STRINGS_CN["status_merge_failed"])
        messagebox.showerror(
            STRINGS_CN["msg_merge_error_title"],
            STRINGS_CN["msg_merge_error_body"].format(error_message=error_message)
        )
        self.update_ui_state()


if __name__ == "__main__":
    try: from tkinterdnd2 import TkinterDnD
    except ImportError:
        try:
            root_check = tk.Tk(); root_check.withdraw()
            messagebox.showerror(STRINGS_CN["msg_dependency_error_title"], STRINGS_CN["msg_dependency_error_body"])
            root_check.destroy()
        except tk.TclError:
             print(STRINGS_CN["console_dep_error_1"]); print(STRINGS_CN["console_dep_error_2"])
        exit(1)

    app = TextMergerApp()
    app.mainloop()