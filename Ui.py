from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLabel, QPushButton, QLineEdit, QFileDialog,
                             QTableWidget, QTableWidgetItem, QListWidget, QGridLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPointF, QTimer
from PyQt6.QtGui import QPalette, QColor, QIcon, QTransform
import sys
import pdfplumber

from main import RecruitmentSystem  

class RecruitmentUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Recruitment System")
        self.setGeometry(100, 100, 1200, 800)
        
        self.dark_mode = True
        self.apply_theme()
        
        self.system = RecruitmentSystem()

        self.home_widget = self.create_home_screen()
        self.setCentralWidget(self.home_widget)

        self.tabs = None

        # Timer for real-time updates on the dashboard
        self.dashboard_timer = QTimer()
        self.dashboard_timer.timeout.connect(self.update_dashboard)
        self.dashboard_timer.start(30000)  # Update every 30 seconds

    def create_home_screen(self):
        home_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        welcome_label = QLabel("Welcome to the AI Recruitment System")
        welcome_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white; padding: 20px;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)

        subtitle_label = QLabel("Streamline your hiring process with AI-powered precision")
        subtitle_label.setStyleSheet("font-size: 18px; color: #cccccc;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

        start_button = QPushButton("Get Started")
        self.style_button(start_button)
        start_button.setFixedWidth(200)
        start_button.clicked.connect(self.show_main_interface)
        self.add_button_animation(start_button)
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        home_widget.setLayout(layout)
        return home_widget

    def show_main_interface(self):
        if not self.tabs:
            self.tabs = QTabWidget()
            self.tabs.setTabPosition(QTabWidget.TabPosition.North)
            self.tabs.setStyleSheet("QTabBar::tab { padding: 10px; font-size: 14px; }")
            self.add_tabs()
            self.add_theme_toggle()

        self.setCentralWidget(self.tabs)
        # Call update_dashboard() after the tabs are fully set up
        self.update_dashboard()
        self.update()

    def add_tabs(self):
        self.tabs.addTab(self.create_job_description_tab(), "Job Description")
        self.tabs.addTab(self.create_cv_upload_tab(), "Upload CV")
        self.tabs.addTab(self.create_match_candidates_tab(), "Match Candidates")
        self.tabs.addTab(self.create_interviews_tab(), "Interviews")
        self.tabs.addTab(self.create_dashboard_tab(), "Dashboard")

    def create_tab_layout(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        tab.setLayout(layout)
        return tab, layout

    def create_job_description_tab(self):
        tab, layout = self.create_tab_layout()

        self.jd_title_input = QLineEdit()
        self.jd_company_input = QLineEdit()
        self.jd_description_input = QLineEdit()
        form_layout = QFormLayout()
        form_layout.addRow("Job Title", self.jd_title_input)
        form_layout.addRow("Company", self.jd_company_input)
        form_layout.addRow("Description", self.jd_description_input)
        layout.addLayout(form_layout)

        upload_pdf_button = QPushButton("Upload Job Description PDF")
        self.style_button(upload_pdf_button)
        upload_pdf_button.clicked.connect(self.upload_jd_pdf)
        self.add_button_animation(upload_pdf_button)
        layout.addWidget(upload_pdf_button, alignment=Qt.AlignmentFlag.AlignCenter)

        proceed_button = QPushButton("Process Job Description")
        self.style_button(proceed_button)
        proceed_button.clicked.connect(self.process_job_description)
        self.add_button_animation(proceed_button)
        layout.addWidget(proceed_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return tab

    def create_cv_upload_tab(self):
        tab, layout = self.create_tab_layout()

        self.cv_name_input = QLineEdit()
        self.cv_email_input = QLineEdit()
        self.cv_phone_input = QLineEdit()
        self.cv_text_input = QLineEdit()
        form_layout = QFormLayout()
        form_layout.addRow("Candidate Name", self.cv_name_input)
        form_layout.addRow("Email", self.cv_email_input)
        form_layout.addRow("Phone", self.cv_phone_input)
        form_layout.addRow("CV Text", self.cv_text_input)
        layout.addLayout(form_layout)

        upload_pdf_button = QPushButton("Upload CV PDF")
        self.style_button(upload_pdf_button)
        upload_pdf_button.clicked.connect(self.upload_cv_pdf)
        self.add_button_animation(upload_pdf_button)
        layout.addWidget(upload_pdf_button, alignment=Qt.AlignmentFlag.AlignCenter)

        proceed_button = QPushButton("Upload CV")
        self.style_button(proceed_button)
        proceed_button.clicked.connect(self.process_cv)
        self.add_button_animation(proceed_button)
        layout.addWidget(proceed_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return tab

    def create_match_candidates_tab(self):
        tab, layout = self.create_tab_layout()

        self.match_job_id_input = QLineEdit()
        self.match_candidate_id_input = QLineEdit()
        self.match_threshold_input = QLineEdit(placeholderText="Default: 0.8")
        form_layout = QFormLayout()
        form_layout.addRow("Job ID", self.match_job_id_input)
        form_layout.addRow("Candidate ID", self.match_candidate_id_input)
        form_layout.addRow("Threshold", self.match_threshold_input)
        layout.addLayout(form_layout)

        proceed_button = QPushButton("Match Candidate")
        self.style_button(proceed_button)
        proceed_button.clicked.connect(self.match_candidate)
        self.add_button_animation(proceed_button)
        layout.addWidget(proceed_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return tab

    def create_interviews_tab(self):
        tab, layout = self.create_tab_layout()

        self.interview_job_id_input = QLineEdit()
        self.interview_min_score_input = QLineEdit(placeholderText="Default: 0.8")
        form_layout = QFormLayout()
        form_layout.addRow("Job ID", self.interview_job_id_input)
        form_layout.addRow("Min Match Score", self.interview_min_score_input)
        layout.addLayout(form_layout)

        proceed_button = QPushButton("Generate Interview Requests")
        self.style_button(proceed_button)
        proceed_button.clicked.connect(self.generate_interviews)
        self.add_button_animation(proceed_button)
        layout.addWidget(proceed_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return tab

    def create_dashboard_tab(self):
        tab, layout = self.create_tab_layout()

        # Section 1: Statistics Overview
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)

        self.jobs_count_label = QLabel("0")
        self.candidates_count_label = QLabel("0")
        self.matches_count_label = QLabel("0")
        self.interviews_count_label = QLabel("0")

        for label in [self.jobs_count_label, self.candidates_count_label, 
                      self.matches_count_label, self.interviews_count_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                background-color: #2e2e2e;
                color: white;
                padding: 15px;
                font-size: 18px;
                border-radius: 5px;
            """)

        stats_layout.addWidget(QLabel("Open Jobs"), 0, 0)
        stats_layout.addWidget(self.jobs_count_label, 1, 0)
        stats_layout.addWidget(QLabel("Candidates"), 0, 1)
        stats_layout.addWidget(self.candidates_count_label, 1, 1)
        stats_layout.addWidget(QLabel("Matches"), 0, 2)
        stats_layout.addWidget(self.matches_count_label, 1, 2)
        stats_layout.addWidget(QLabel("Interviews"), 0, 3)
        stats_layout.addWidget(self.interviews_count_label, 1, 3)

        layout.addLayout(stats_layout)

        # Section 2: Job Descriptions Table
        jobs_label = QLabel("Job Descriptions")
        jobs_label.setStyleSheet("font-size: 16px; padding: 10px; color: white;")
        layout.addWidget(jobs_label)

        self.jobs_table = QTableWidget()
        self.jobs_table.setColumnCount(5)  # ID, Title, Company, Description, Delete
        self.jobs_table.setHorizontalHeaderLabels(["ID", "Title", "Company", "Description", "Action"])
        self.jobs_table.setStyleSheet("""
            QTableWidget {
                background-color: #2e2e2e;
                color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #3e3e3e;
                color: white;
                padding: 5px;
            }
        """)
        self.jobs_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.jobs_table)

        # Section 3: Candidate Details Table
        candidate_label = QLabel("Recent Candidates")
        candidate_label.setStyleSheet("font-size: 16px; padding: 10px; color: white;")
        layout.addWidget(candidate_label)

        self.candidate_table = QTableWidget()
        self.candidate_table.setColumnCount(6)  # Added column for Delete button
        self.candidate_table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Match Score", "Interview Status", "Action"])
        self.candidate_table.setStyleSheet("""
            QTableWidget {
                background-color: #2e2e2e;
                color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #3e3e3e;
                color: white;
                padding: 5px;
            }
        """)
        self.candidate_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.candidate_table)

        # Section 4: Top Matches Table
        top_matches_label = QLabel("Top Candidate-Job Matches")
        top_matches_label.setStyleSheet("font-size: 16px; padding: 10px; color: white;")
        layout.addWidget(top_matches_label)

        self.top_matches_table = QTableWidget()
        self.top_matches_table.setColumnCount(5)  # Added column for Delete button
        self.top_matches_table.setHorizontalHeaderLabels(["Candidate ID", "Job ID", "Match Score", "Details", "Action"])
        self.top_matches_table.setStyleSheet("""
            QTableWidget {
                background-color: #2e2e2e;
                color: white;
                border: none;
            }
            QHeaderView::section {
                background-color: #3e3e3e;
                color: white;
                padding: 5px;
            }
        """)
        self.top_matches_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.top_matches_table)

        # Section 5: Recent Activity Log
        activity_label = QLabel("Recent Activity")
        activity_label.setStyleSheet("font-size: 16px; padding: 10px; color: white;")
        layout.addWidget(activity_label)

        self.activity_log = QListWidget()
        self.activity_log.setStyleSheet("""
            QListWidget {
                background-color: #2e2e2e;
                color: white;
                border: none;
                padding: 5px;
            }
        """)
        layout.addWidget(self.activity_log)

        # Section 6: Refresh Button
        refresh_button = QPushButton("Refresh Dashboard")
        self.style_button(refresh_button)
        refresh_button.clicked.connect(self.update_dashboard)
        self.add_button_animation(refresh_button)
        layout.addWidget(refresh_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return tab

    def update_dashboard(self):
        """Update the dashboard with real-time data."""
        try:
            # Check if required methods exist
            if not hasattr(self.system.db, 'get_all_job_descriptions'):
                raise AttributeError("RecruitmentDB missing get_all_job_descriptions method")
            if not hasattr(self.system.db, 'get_all_candidates'):
                raise AttributeError("RecruitmentDB missing get_all_candidates method")
            if not hasattr(self.system.db, 'get_all_matches'):
                raise AttributeError("RecruitmentDB missing get_all_matches method")
            if not hasattr(self.system.db, 'get_match_by_candidate'):
                raise AttributeError("RecruitmentDB missing get_match_by_candidate method")

            # Update Statistics
            jobs = self.system.db.get_all_job_descriptions() or []
            candidates = self.system.db.get_all_candidates() or []
            matches = self.system.db.get_all_matches() or []

            jobs_count = len(jobs)
            candidates_count = len(candidates)
            matches_count = len(matches)
            interviews_count = sum(1 for match in matches if match.get('interview_requested', False))

            self.jobs_count_label.setText(str(jobs_count))
            self.candidates_count_label.setText(str(candidates_count))
            self.matches_count_label.setText(str(matches_count))
            self.interviews_count_label.setText(str(interviews_count))

            # Update Job Descriptions Table if it exists
            if hasattr(self, 'jobs_table'):
                self.jobs_table.setRowCount(len(jobs))
                for row, job in enumerate(jobs):
                    self.jobs_table.setItem(row, 0, QTableWidgetItem(str(job['id'])))
                    self.jobs_table.setItem(row, 1, QTableWidgetItem(job.get('title', 'N/A')))
                    self.jobs_table.setItem(row, 2, QTableWidgetItem(job.get('company', 'N/A')))
                    self.jobs_table.setItem(row, 3, QTableWidgetItem(job.get('description', 'N/A')[:50] + "..."))

                    # Add Delete button
                    delete_button = QPushButton("Delete")
                    delete_button.setStyleSheet("""
                        QPushButton {
                            background-color: #ff4444;
                            color: white;
                            padding: 5px;
                            border-radius: 3px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #cc0000;
                        }
                    """)
                    delete_button.clicked.connect(lambda _, jid=job['id']: self.delete_job(jid))
                    self.jobs_table.setCellWidget(row, 4, delete_button)

            # Update Candidate Table if it exists
            if hasattr(self, 'candidate_table'):
                self.candidate_table.setRowCount(len(candidates))
                for row, candidate in enumerate(candidates):
                    candidate_id = str(candidate['id'])
                    match = self.system.db.get_match_by_candidate(candidate_id)
                    match_score = str(match['match_score']) if match else "N/A"
                    interview_status = "Scheduled" if match and match.get('interview_requested', False) else "Not Scheduled"

                    self.candidate_table.setItem(row, 0, QTableWidgetItem(candidate_id))
                    self.candidate_table.setItem(row, 1, QTableWidgetItem(candidate.get('name', 'N/A')))
                    self.candidate_table.setItem(row, 2, QTableWidgetItem(candidate.get('email', 'N/A')))
                    self.candidate_table.setItem(row, 3, QTableWidgetItem(match_score))
                    self.candidate_table.setItem(row, 4, QTableWidgetItem(interview_status))

                    # Add Delete button
                    delete_button = QPushButton("Delete")
                    delete_button.setStyleSheet("""
                        QPushButton {
                            background-color: #ff4444;
                            color: white;
                            padding: 5px;
                            border-radius: 3px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #cc0000;
                        }
                    """)
                    delete_button.clicked.connect(lambda _, cid=candidate['id']: self.delete_candidate(cid))
                    self.candidate_table.setCellWidget(row, 5, delete_button)

            # Update Top Matches Table if it exists
            if hasattr(self, 'top_matches_table'):
                sorted_matches = sorted(matches, key=lambda x: x['match_score'], reverse=True)[:5]  # Top 5 matches
                self.top_matches_table.setRowCount(len(sorted_matches))
                for row, match in enumerate(sorted_matches):
                    self.top_matches_table.setItem(row, 0, QTableWidgetItem(str(match['candidate_id'])))
                    self.top_matches_table.setItem(row, 1, QTableWidgetItem(str(match['job_id'])))
                    self.top_matches_table.setItem(row, 2, QTableWidgetItem(str(match['match_score'])))
                    self.top_matches_table.setItem(row, 3, QTableWidgetItem(str(match.get('match_details', 'N/A'))))

                    # Add Delete button
                    delete_button = QPushButton("Delete")
                    delete_button.setStyleSheet("""
                        QPushButton {
                            background-color: #ff4444;
                            color: white;
                            padding: 5px;
                            border-radius: 3px;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: #cc0000;
                        }
                    """)
                    delete_button.clicked.connect(lambda _, cid=match['candidate_id'], jid=match['job_id']: self.delete_match(cid, jid))
                    self.top_matches_table.setCellWidget(row, 4, delete_button)

            # Update Activity Log if it exists
            if hasattr(self, 'activity_log'):
                self.activity_log.clear()
                for candidate in candidates[:3]:
                    self.activity_log.addItem(f"Candidate {candidate.get('name', 'N/A')} (ID: {candidate['id']}) added")
                for match in matches[:3]:
                    self.activity_log.addItem(f"Candidate ID {match['candidate_id']} matched to Job ID {match['job_id']} (Score: {match['match_score']})")

        except Exception as e:
            print(f"Error updating dashboard: {e}")
            # Reset counts to 0
            self.jobs_count_label.setText("0")
            self.candidates_count_label.setText("0")
            self.matches_count_label.setText("0")
            self.interviews_count_label.setText("0")
            # Clear tables only if they exist
            if hasattr(self, 'jobs_table'):
                self.jobs_table.setRowCount(0)
            if hasattr(self, 'candidate_table'):
                self.candidate_table.setRowCount(0)
            if hasattr(self, 'top_matches_table'):
                self.top_matches_table.setRowCount(0)
            if hasattr(self, 'activity_log'):
                self.activity_log.clear()
                self.activity_log.addItem(f"Error loading dashboard data: {str(e)}. Please try again.")

    # PDF Upload Methods
    def upload_jd_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Job Description PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                self.jd_description_input.setText(text)
                print(f"Loaded Job Description PDF: {file_path}")
                self.update()
            except Exception as e:
                print(f"Error loading PDF: {e}")

    def upload_cv_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CV PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                self.cv_text_input.setText(text)
                print(f"Loaded CV PDF: {file_path}")
                self.update()
            except Exception as e:
                print(f"Error loading PDF: {e}")

    # Backend processing methods
    def process_job_description(self):
        title = self.jd_title_input.text()
        company = self.jd_company_input.text()
        description = self.jd_description_input.text()
        job_id = self.system.process_job_description(title, company, description)
        print(f"Job processed with ID: {job_id}")
        self.update()

    def process_cv(self):
        name = self.cv_name_input.text()
        email = self.cv_email_input.text()
        phone = self.cv_phone_input.text()
        cv_text = self.cv_text_input.text()
        candidate_id = self.system.process_cv(name, email, cv_text, phone)
        print(f"CV processed with ID: {candidate_id}")
        self.update()

    def match_candidate(self):
        try:
            job_id = int(self.match_job_id_input.text())
            candidate_id = int(self.match_candidate_id_input.text())
            threshold = float(self.match_threshold_input.text() or 0.8)
            match_result = self.system.match_candidate_to_job(job_id, candidate_id, threshold)
            print(f"Match result: {match_result}")
            self.update()
        except ValueError as e:
            print(f"Error: Invalid input - {e}")

    def generate_interviews(self):
        try:
            job_id = int(self.interview_job_id_input.text())
            min_score = float(self.interview_min_score_input.text() or 0.8)
            requests = self.system.generate_interview_requests(job_id, min_score)
            print(f"Generated {len(requests)} interview requests.")
            for req in requests:
                print(f"Interview request sent to {req['candidate_name']} ({req['candidate_email']})")
            self.update()
        except ValueError as e:
            print(f"Error: Invalid input - {e}")

    # Delete methods for dashboard
    def delete_job(self, job_id):
        """Delete a job description and refresh the dashboard"""
        try:
            self.system.db.delete_job_description(job_id)
            self.activity_log.addItem(f"Deleted Job ID {job_id}")
            self.update_dashboard()
        except Exception as e:
            self.activity_log.addItem(f"Error deleting Job ID {job_id}: {str(e)}")

    def delete_candidate(self, candidate_id):
        """Delete a candidate and refresh the dashboard"""
        try:
            self.system.db.delete_candidate(candidate_id)
            self.activity_log.addItem(f"Deleted Candidate ID {candidate_id}")
            self.update_dashboard()
        except Exception as e:
            self.activity_log.addItem(f"Error deleting Candidate ID {candidate_id}: {str(e)}")

    def delete_match(self, candidate_id, job_id):
        """Delete a match and refresh the dashboard"""
        try:
            # Find the match ID for the candidate-job pair
            matches = self.system.db.get_all_matches()
            match_id = None
            for match in matches:
                if match['candidate_id'] == candidate_id and match['job_id'] == job_id:
                    match_id = match['id']
                    break
            if match_id:
                self.system.db.delete_match(match_id)
                self.activity_log.addItem(f"Deleted Match (Candidate ID {candidate_id}, Job ID {job_id})")
                self.update_dashboard()
            else:
                self.activity_log.addItem(f"Match not found for Candidate ID {candidate_id} and Job ID {job_id}")
        except Exception as e:
            self.activity_log.addItem(f"Error deleting Match (Candidate ID {candidate_id}, Job ID {job_id}): {str(e)}")

    # Theme and styling
    def apply_theme(self):
        if self.dark_mode:
            self.init_dark_mode()
        else:
            self.init_light_mode()

    def init_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(100, 100, 255))
        self.setPalette(palette)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QLineEdit { 
                background-color: #2e2e2e; 
                color: white; 
                border: 1px solid #555; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QLabel { color: white; }
            QTabWidget::pane { border: none; }
        """)

    def init_light_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Button, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
        self.setPalette(palette)
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QLineEdit { 
                background-color: white; 
                color: black; 
                border: 1px solid #ccc; 
                border-radius: 5px; 
                padding: 5px; 
            }
            QLabel { color: black; }
            QTabWidget::pane { border: none; }
        """)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        icon = "dark_mode_icon.png" if self.dark_mode else "light_mode_icon.png"
        self.theme_button.setIcon(QIcon(icon))

    def add_theme_toggle(self):
        self.theme_button = QPushButton()
        self.theme_button.setIcon(QIcon("dark_mode_icon.png"))
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setStyleSheet("border: none; background: transparent;")
        self.theme_button.clicked.connect(self.toggle_theme)

        header = QWidget()
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(self.theme_button)
        header.setLayout(header_layout)
        self.tabs.setCornerWidget(header, Qt.Corner.TopRightCorner)

    def style_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 8px;
                border: none;
                min-width: 200px;
                max-width: 200px;
                min-height: 40px;
                max-height: 40px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

    def add_button_animation(self, button):
        animation = QPropertyAnimation(button, b"scale")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        animation.setStartValue(1.0)
        animation.setKeyValueAt(0.5, 1.1)
        animation.setEndValue(1.0)
        animation.setLoopCount(1)

        button.clicked.connect(animation.start)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecruitmentUI()
    window.show()
    sys.exit(app.exec())