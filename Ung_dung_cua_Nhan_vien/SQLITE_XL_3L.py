"""
Họ và tên SV: VÕ ĐẠI NGHĨA
MSSV: 1888049
Đề đồ án: QUẢN LÝ NHÂN VIÊN
"""
import json
from pathlib import Path
import random
import sqlite3

Thu_muc_Du_lieu = Path("..\\Dich_vu_Du_lieu")
Thu_muc_HTML = Thu_muc_Du_lieu/"HTML"
Ten_CSDL = "QLNV.sqlite"
Duong_dan_CSDL = f"{Thu_muc_Du_lieu}\\{Ten_CSDL}"

#--Xử lý lưu trữ
def Doc_Khung_HTML():
    Duong_dan = Thu_muc_HTML/"Khung.html"
    Tap_tin = open(Duong_dan, encoding = "utf-8")
    Chuoi_HTML = Tap_tin.read()
    return Chuoi_HTML

def Doc_Cong_ty():
    Cong_ty = {}
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Lenh = "SELECT * FROM CONGTY"
    for Dong in Ket_noi.execute(Lenh):
        Chuoi_JSON = Dong[1]
        Cong_ty = json.loads(Chuoi_JSON)
    Ket_noi.close()
    return Cong_ty

def Doc_Danh_sach_Nhan_vien():
    Danh_sach = []
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Lenh = "SELECT * FROM NHANVIEN"
    for Dong in Ket_noi.execute(Lenh):
        Chuoi_JSON = Dong[1]
        Nhan_vien = json.loads(Chuoi_JSON)
        Danh_sach.append(Nhan_vien)
    Ket_noi.close()
    return Danh_sach

def Ghi_Nhan_vien(Nhan_vien):
    Ma_so = Nhan_vien["Ma_so"]
    Chuoi_JSON = json.dumps(Nhan_vien, indent = 4)
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Lenh = f"UPDATE NHANVIEN SET Chuoi_JSON = '{Chuoi_JSON}' WHERE Ma_so = '{Ma_so}'"
    Ket_noi.execute(Lenh)
    Ket_noi.commit()
    Ket_noi.close()

def Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh):
    Duong_dan = f"..\\Media\\{Nhan_vien['Ma_so']}.png"
    Hinh.save(Duong_dan)
    
#--Xử lý nghiệp vụ
def Tao_Don_Xin_nghi(Nhan_vien, Ngay_Bat_dau, So_ngay, Ly_do):
    if (int(So_ngay) > 0):
        if "Cac_Don_xin_nghi" not in Nhan_vien:
            Nhan_vien["Cac_Don_xin_nghi"] = []
        Don_Xin_nghi_Moi = {}
        Don_Xin_nghi_Moi["STT"] = len(Nhan_vien["Cac_Don_xin_nghi"]) + 1
        Don_Xin_nghi_Moi["Ngay_Bat_dau"] = Ngay_Bat_dau
        Don_Xin_nghi_Moi["So_ngay"] = So_ngay
        Don_Xin_nghi_Moi["Ly_do"] = Ly_do
        Don_Xin_nghi_Moi["Y_kien_cua_QLDV"] = {}
        Don_Xin_nghi_Moi["Y_kien_cua_QLCN"] = {}
        Nhan_vien["Cac_Don_xin_nghi"].append(Don_Xin_nghi_Moi)
        return Nhan_vien
    else:
        return Nhan_vien

#--Xử lý giao diện
def Tao_Chuoi_Tien_te(n):
    Chuoi = "${:,}".format(n)
    Chuoi = Chuoi.replace(",", ".")
    Chuoi = Chuoi.replace("$", "")
    return Chuoi

def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dien_thoai(Nhan_vien):
    Chuoi_Click = f"""<div data-toggle='dropdown' class='btn btn-primary'>Cập nhật điện thoại</div>"""
    Chuoi_Dropdown = f"""<div class='dropdown-menu'>
                            <form action='/Cap_nhat_Dien_thoai' method='post'>
                                <input name='Th_Dien_thoai' value='{Nhan_vien["Dien_thoai"]}' autocomplete='off' />
                            </form>
                        </div>"""
    Chuoi_Chuc_nang = f"""<div class='dropdown btn'>{Chuoi_Click} {Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang

def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dia_chi(Nhan_vien):
    Chuoi_Click = f"""<div data-toggle='dropdown' class='btn btn-primary'>Cập nhật địa chỉ</div>"""
    Chuoi_Dropdown = f"""<div class='dropdown-menu'>
                            <form action='/Cap_nhat_Dia_chi' method='post'>
                                <input name='Th_Dia_chi' value='{Nhan_vien["Dia_chi"]}' autocomplete='off' />
                            </form>
                        </div>"""
    Chuoi_Chuc_nang = f"""<div class='dropdown btn'>{Chuoi_Click} {Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang

def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Hinh():
    Chuoi_Click = f"""<div data-toggle='dropdown' class='btn btn-primary'>Cập nhật hình</div>"""
    Chuoi_Dropdown = f"""<div class='dropdown-menu'>
                            <form action='/Cap_nhat_Hinh' method='post' enctype='multipart/form-data'>
                                <input name='Th_Hinh' type='file' />
                                <button type='submit' class='btn btn-danger'>Đồng ý</button>
                            </form>
                        </div>"""
    Chuoi_Chuc_nang = f"""<div class='dropdown btn'>{Chuoi_Click} {Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang

def Tao_Chuoi_Dropdown_Chuc_nang_Nop_Don_xin_nghi():
    Chuoi_Click = f"""<div data-toggle='dropdown' class='btn btn-primary'>Nộp đơn xin nghỉ</div>"""
    Chuoi_Dropdown = f"""<div class='dropdown-menu'>
                            <form action='/Nop_Don_xin_nghi' method='post'>
                                <input name='Th_Ngay_Bat_dau' type="date" required>
                                <input name='Th_So_ngay' placeholder='Số ngày muốn nghỉ' required type='number' pattern="?[0-9]" min="1">
                                <input name='Th_Ly_do' placeholder='Lý do nghỉ' required>
                                <button type='submit' class='btn btn-danger'>Đồng ý</button>
                            </form>
                        </div>"""
    Chuoi_Chuc_nang = f"""<div class='dropdown btn'>{Chuoi_Click} {Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang

def Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach):
    Chuoi_HTML_Danh_sach = f"""<div>"""
    for Nhan_vien in Danh_sach:
        Ma_so = Nhan_vien["Ma_so"]
        Ho_ten = Nhan_vien["Ho_ten"]
        Chung_minh_Thu = Nhan_vien["CMND"]
        Ten_Don_vi = Nhan_vien["Don_vi"]["Ten"]
        Ten_Chi_nhanh = Nhan_vien["Don_vi"]["Chi_nhanh"]["Ten"]
        Dien_thoai = Nhan_vien["Dien_thoai"]
        Dia_chi = Nhan_vien["Dia_chi"]
        Chuoi_Hinh = f"""<img src="Media/{Ma_so}.png?x={random.randint(1,1000)}" style="width:60px; height:60px">"""
        Chuoi_Ngoai_ngu = " ".join([Ngoai_ngu["Ten"] for Ngoai_ngu in Nhan_vien["Danh_sach_Ngoai_ngu"]])
        for Ngoai_ngu in Nhan_vien["Danh_sach_Ngoai_ngu"]:
            Chuoi_Ngoai_ngu += Ngoai_ngu["Ten"] + " "
        Chuoi_Nghi_phep = """<hr><div class="table-responsive">
                            <table class="table table-bordered table-hover table-sm table-secondary text-center"><thead>
                                <tr style="margin:10px">
                                    <th scope="col" rowspan="2" colspan="1">STT</th>
                                    <th scope="col" rowspan="2" colspan="1">Ngày bắt đầu nghỉ</th>
                                    <th scope="col" rowspan="2" colspan="1">Số ngày</th>
                                    <th scope="col" rowspan="2" colspan="1">Lý do</th>
                                    <th scope="col" rowspan="1" colspan="2">Ý kiến của quản lý đơn vị</th>
                                    <th scope="col" rowspan="1" colspan="2">Ý kiến của quản lý chi nhánh</th>
                                </tr>
                                <tr style="margin:10px">
                                    <th scope="col">Ngày cho ý kiến</th>
                                    <th scope="col">Ý kiến</th>
                                    <th scope="col">Ngày cho ý kiến</th>
                                    <th scope="col">Ý kiến</th>
                                </tr></thead>
                                <tbody><tr>"""
        if "Cac_Don_xin_nghi" in Nhan_vien:
            for Nghi_phep in Nhan_vien["Cac_Don_xin_nghi"]:
                Lan_nghi = Nghi_phep["STT"]
                Ngay_Bat_dau = Nghi_phep["Ngay_Bat_dau"]
                So_ngay = Nghi_phep["So_ngay"]
                Ly_do = Nghi_phep["Ly_do"]
                if ("Ngay" or "Noi_dung") in Nghi_phep["Y_kien_cua_QLDV"]:
                    Y_kien_cua_QLDV_Ngay = Nghi_phep["Y_kien_cua_QLDV"]["Ngay"]
                    Y_kien_cua_QLDV_Noi_dung = Nghi_phep["Y_kien_cua_QLDV"]["Noi_dung"]
                else:
                    Y_kien_cua_QLDV_Ngay = ""
                    Y_kien_cua_QLDV_Noi_dung = ""
                if ("Ngay" or "Noi_dung") in Nghi_phep["Y_kien_cua_QLCN"]:
                    Y_kien_cua_QLCN_Ngay = Nghi_phep["Y_kien_cua_QLCN"]["Ngay"]
                    Y_kien_cua_QLCN_Noi_dung = Nghi_phep["Y_kien_cua_QLCN"]["Noi_dung"]
                else:
                    Y_kien_cua_QLCN_Ngay = ""
                    Y_kien_cua_QLCN_Noi_dung = ""
                Chuoi_Nghi_phep += f"""<tr style="margin:10px">
                                        <td scope="row" >{Lan_nghi}</td>
                                        <td scope="row" >{Ngay_Bat_dau}</td>
                                        <td scope="row" >{So_ngay}</td>
                                        <td scope="row" >{Ly_do}</td>
                                        <td scope="row" >{Y_kien_cua_QLDV_Ngay}</td>
                                        <td scope="row" >{Y_kien_cua_QLDV_Noi_dung}</td>
                                        <td scope="row" >{Y_kien_cua_QLCN_Ngay}</td>
                                        <td scope="row" >{Y_kien_cua_QLCN_Noi_dung}</td>
                                    </tr>"""
        Chuoi_Nghi_phep += """</tbody></table></div>"""                                        
        Chuoi_Thong_tin = f"""<div class="btn text-left" style="text-align:text">
                                Họ và tên: {Ho_ten} - CMND: {Chung_minh_Thu}<br>
                                Tên đơn vị: {Ten_Don_vi} - Tên chi nhánh: {Ten_Chi_nhanh}<br>
                                SĐT: {Dien_thoai}<br>
                                Địa chỉ: {Dia_chi}<br>
                                Các ngoại ngữ: {Chuoi_Ngoai_ngu}
                            </div>"""
        Chuoi_HTML = f"""<div class="alert alert-info">{Chuoi_Hinh} {Chuoi_Thong_tin} {Chuoi_Nghi_phep}</div>"""
        Chuoi_Thuc_don = f"""<div class="row">
                                {Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dien_thoai(Nhan_vien)}
                                {Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dia_chi(Nhan_vien)}
                                {Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Hinh()}
                                {Tao_Chuoi_Dropdown_Chuc_nang_Nop_Don_xin_nghi()}
                            </div>"""
        Chuoi_HTML = Chuoi_Thuc_don + Chuoi_HTML
        Chuoi_HTML_Danh_sach += Chuoi_HTML
    Chuoi_HTML_Danh_sach += "</div>"
    return Chuoi_HTML_Danh_sach

def Tao_Chuoi_HTML_Thong_bao(Thong_bao):
    Chuoi_HTML = f"""<div class='alert alert-info alert-dismissible'>
                        <button type='button' class='close' data-dismiss='alert'>&times;</button>
                        {Thong_bao}
                    </div>"""
    return Chuoi_HTML

def Tao_Chuoi_HTML_Dang_nhap(Ten_Dang_nhap = "", Mat_khau = "", Thong_bao = ""):
    Chuoi_HTML = f"""<form action='/Dang_nhap' method='post'>
                        <div class='alert' style='height:10px'>Đăng nhập</div>
                        <div class='alert' style='height:30px'>
                            <input name='Th_Ten_Dang_nhap' required='required' value='{Ten_Dang_nhap}' spellcheck='false' autocomplete='off' />
                        </div>
                        <div class='alert' style='height:30px'>
                            <input name='Th_Mat_khau' type='password' required='required' value='{Mat_khau}' spellcheck='false' autocomplete='off' />
                        </div>
                        <div class='alert' style='height:30px'>
                            <button class='btn btn-danger' type='submit'>Đồng ý</button>
                        </div>
                        <div>{Thong_bao}</div>
                    </form>"""
    return Chuoi_HTML