import os
import uuid
from datetime import datetime
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ----------------------------------------------------------------------
# 0. Dynamic LOT Number Generator (PDF와 동일 규격)
# ----------------------------------------------------------------------
def generate_lot_id():
    date_str = datetime.now().strftime("%Y%m%d")
    unique_hash = uuid.uuid4().hex[:8].upper()
    return f"HM-{date_str}-B2B-{unique_hash}"

# ----------------------------------------------------------------------
# 1. Master Excel Dataset Generator
# ----------------------------------------------------------------------
def generate_master_excel(input_path=None, output_path=None, custom_lot_id=None, license_tier="enterprise"):
    """
    license_tier 옵션:
      - "professional": 59만 원 (1인 연구원 전용)
      - "enterprise": 450만 원 (기업/연구소 팀 전체 사이트 라이선스)
    """
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    if os.path.basename(current_dir) == "public":
        public_dir = current_dir
    else:
        public_dir = os.path.join(current_dir, "public")
        os.makedirs(public_dir, exist_ok=True)

    if input_path is None:
        input_path = os.path.join(public_dir, "solid_state_battery_350.xlsx")
        if not os.path.exists(input_path):
            input_path = "solid_state_battery_350.xlsx"

    if output_path is None:
        output_path = os.path.join(public_dir, "solid_state_battery_350.xlsx")

    active_lot_id = custom_lot_id if custom_lot_id else generate_lot_id()

    # 💡 100% 영문 라이선스 문구 설정 (한글 완전 제거)
    if license_tier.lower() == "professional":
        permitted_scope = "Single Named Researcher License"
        cert_title = "OFFICIAL PROFESSIONAL RESEARCHER LICENSE & ASSET CERTIFICATE"
        cert_body = (
            f"This Master Intelligence Dataset (Tracking LOT ID: {active_lot_id}) is licensed exclusively to the designated individual researcher. "
            "Sharing across institutional teams, public redistribution, or central database indexing is strictly prohibited under single-user terms."
        )
    else:  # enterprise (기본값)
        permitted_scope = "Single Institution Site License"
        cert_title = "OFFICIAL ENTERPRISE SITE LICENSE & ASSET CERTIFICATE"
        cert_body = (
            f"This Master Intelligence Dataset (Tracking LOT ID: {active_lot_id}) is certified for full institution-wide deployment. "
            "Authorized for unlimited internal sharing among research teams and central database integration within the purchasing organization."
        )

    # 기존 데이터 로드
    xls = pd.ExcelFile(input_path)
    sheet_to_read = "350_Master_Dataset" if "350_Master_Dataset" in xls.sheet_names else xls.sheet_names[0]
    df = pd.read_excel(input_path, sheet_name=sheet_to_read)

    wb = openpyxl.Workbook()

    # ------------------------------------------------------------------
    # Sheet 1: 00_License_Certificate (100% 영문 표기)
    # ------------------------------------------------------------------
    ws_cert = wb.active
    ws_cert.title = "00_License_Certificate"
    ws_cert.views.sheetView[0].showGridLines = True

    navy_fill = PatternFill(start_color='0F172A', end_color='0F172A', fill_type='solid')
    gray_fill = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    ws_cert['A2'] = "HARVESTER MATERIALS PLATFORM"
    ws_cert['A2'].font = Font(name='Calibri', size=11, bold=True, color='2563EB')
    ws_cert['A3'] = cert_title
    ws_cert['A3'].font = Font(name='Calibri', size=15, bold=True, color='0F172A')

    cert_headers = [
        ("Asset Title", "Vol. 01 Solid-State Battery Material AI Screening Master Dataset"),
        ("Tracking LOT ID", active_lot_id),
        ("License Tier", license_tier.upper()),
        ("Permitted Scope", permitted_scope),
        ("Issued Date", datetime.now().strftime("%Y-%m-%d")),
        ("Terms & Conditions", cert_body),
        ("Copyright Notice", "Copyright © 2026 Harvester Materials. All Rights Reserved.")
    ]

    ws_cert.cell(row=5, column=1, value="Property").font = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
    ws_cert.cell(row=5, column=1).fill = navy_fill
    ws_cert.cell(row=5, column=2, value="Certification Details").font = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
    ws_cert.cell(row=5, column=2).fill = navy_fill

    for r_idx, (k, v) in enumerate(cert_headers, start=6):
        c1 = ws_cert.cell(row=r_idx, column=1, value=k)
        c2 = ws_cert.cell(row=r_idx, column=2, value=v)
        c1.font = Font(name='Calibri', size=10, bold=True, color='0F172A')
        c2.font = Font(name='Calibri', size=10, color='334155')
        c1.fill, c2.fill = gray_fill, gray_fill
        c1.border, c2.border = thin_border, thin_border

    ws_cert.column_dimensions['A'].width = 22
    ws_cert.column_dimensions['B'].width = 85

    # ------------------------------------------------------------------
    # Sheet 2: 350_Master_Dataset (세 번째 이미지 스타일 완벽 복원)
    # ------------------------------------------------------------------
    ws_data = wb.create_sheet(title="350_Master_Dataset")
    ws_data.views.sheetView[0].showGridLines = True

    zebra_fill = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
    white_fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')

    # 1) 헤더 행 설정 (높이 28px, 딥 네이비 배경, 흰색 볼드 텍스트, 중앙 정렬)
    ws_data.row_dimensions[1].height = 28
    for col_idx, header in enumerate(df.columns, start=1):
        cell = ws_data.cell(row=1, column=col_idx, value=header)
        cell.font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # 2) 데이터 행 설정 (높이 20px, 교차 줄무늬, 정밀 수치 서식)
    for row_idx, row_data in enumerate(df.values, start=2):
        ws_data.row_dimensions[row_idx].height = 20
        current_fill = zebra_fill if row_idx % 2 == 0 else white_fill

        for col_idx, val in enumerate(row_data, start=1):
            cell = ws_data.cell(row=row_idx, column=col_idx)
            col_name = list(df.columns)[col_idx - 1]

            if col_name == 'Est. Ionic Conductivity (S/cm)':
                cell.value = float(val) if pd.notnull(val) else val
                cell.number_format = '0.00E+00'
                cell.alignment = Alignment(horizontal='right', vertical='center')
                cell.font = Font(name='Calibri', size=10, color='334155')
            elif 'Energy Above Hull' in col_name:
                cell.value = float(val) if pd.notnull(val) else val
                cell.number_format = '0.00'
                cell.alignment = Alignment(horizontal='right', vertical='center')
                cell.font = Font(name='Calibri', size=10, color='334155')
            elif col_name == 'Literature DOI' and str(val).startswith('http'):
                cell.value = str(val)
                cell.font = Font(name='Calibri', size=10, color='2563EB', underline='single')
                cell.alignment = Alignment(horizontal='left', vertical='center')
            else:
                cell.value = str(val)
                align_h = 'center' if col_idx in [1, 3, 4] else 'left'
                cell.alignment = Alignment(horizontal=align_h, vertical='center')
                cell.font = Font(name='Calibri', size=10, color='334155')

            cell.fill = current_fill
            cell.border = thin_border

    # 3) 컬럼 너비 자동 설정 (글자 길이에 맞게 넓고 깔끔하게 자동 확장)
    for col in ws_data.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws_data.column_dimensions[col_letter].width = max(max_len + 5, 16)

    # 4) 틀 고정 (상단 헤더 고정)
    ws_data.freeze_panes = 'A2'

    wb.save(output_path)
    print(f"✨ [{license_tier.upper()}] 영문 라이선스 및 프리미엄 스타일 엑셀 생성 완료! (LOT ID: {active_lot_id})")

if __name__ == "__main__":
    generate_master_excel(license_tier="enterprise")
