import streamlit as st
import sqlite3
import pandas as pd
import json
from datetime import datetime
import time
import streamlit.components.v1 as components
# =========================================================
# KONFIGURASI APLIKASI
# =========================================================
st.set_page_config(
    page_title="Misconception Physics",
    page_icon="🌊",
    layout="wide"
)
NAMA_DB = "misconception_physics.db"
PASSWORD_GURU = "Guru12345"  # Ganti sebelum aplikasi digunakan secara nyata.
# =========================================================
# BANK SOAL FOUR-TIER DIAGNOSTIC TEST
# Catatan: soal berikut adalah contoh awal dan perlu divalidasi.
# =========================================================
soal = [
    {
        "pertanyaan": "Gelombang elektromagnetik dapat merambat tanpa medium karena ....",
        "opsi": [
            "A. Gelombang elektromagnetik hanya merambat dalam zat padat",
            "B. Gelombang elektromagnetik memerlukan udara",
            "C. Gelombang elektromagnetik dapat merambat di ruang hampa",
            "D. Gelombang elektromagnetik tidak dapat membawa energi",
            "E. Gelombang elektromagnetik memerlukan zat cair"
        ],
        "kunci": "C",
        "alasan": [
            "A. Karena partikel medium harus bergetar untuk merambatkan gelombang.",
            "B. Karena gelombang elektromagnetik tersusun dari medan listrik dan medan magnet yang berosilasi.",
            "C. Karena gelombang elektromagnetik memerlukan partikel udara.",
            "D. Karena gelombang elektromagnetik tidak membawa energi.",
            "E. Karena semua gelombang membutuhkan zat cair."
        ],
        "kunci_alasan": "B",
        "pembahasan": "Gelombang elektromagnetik terdiri atas medan listrik dan medan magnet yang berosilasi sehingga tidak memerlukan medium untuk merambat."
    },
    {
        "pertanyaan": "Cahaya Matahari dapat sampai ke Bumi melalui ruang hampa karena ....",
        "opsi": [
            "A. Cahaya Matahari harus melewati udara",
            "B. Cahaya Matahari tidak memerlukan medium",
            "C. Cahaya Matahari hanya merambat melalui zat cair",
            "D. Cahaya Matahari tidak dapat merambat di ruang hampa",
            "E. Cahaya Matahari dibawa oleh angin"
        ],
        "kunci": "B",
        "alasan": [
            "A. Karena cahaya merupakan gelombang mekanik.",
            "B. Karena gelombang elektromagnetik dapat merambat tanpa medium.",
            "C. Karena ruang hampa sebenarnya berisi udara.",
            "D. Karena cahaya Matahari dibawa oleh partikel angin.",
            "E. Karena semua gelombang membutuhkan partikel perantara."
        ],
        "kunci_alasan": "B",
        "pembahasan": "Cahaya Matahari merupakan gelombang elektromagnetik yang dapat merambat melalui ruang hampa antara Matahari dan Bumi."
    },
    {
        "pertanyaan": "Dua gelombang elektromagnetik merambat di ruang hampa. Jika frekuensi gelombang A lebih tinggi daripada gelombang B, maka panjang gelombang A ....",
        "opsi": [
            "A. Lebih panjang",
            "B. Lebih pendek",
            "C. Sama panjang",
            "D. Tidak memiliki panjang gelombang",
            "E. Tidak dapat dibandingkan"
        ],
        "kunci": "B",
        "alasan": [
            "A. Karena frekuensi dan panjang gelombang berbanding terbalik jika cepat rambat tetap.",
            "B. Karena frekuensi dan panjang gelombang selalu berbanding lurus.",
            "C. Karena frekuensi tidak berhubungan dengan panjang gelombang.",
            "D. Karena panjang gelombang hanya dipengaruhi amplitudo.",
            "E. Karena panjang gelombang tidak berlaku untuk gelombang elektromagnetik."
        ],
        "kunci_alasan": "A",
        "pembahasan": "Berdasarkan persamaan c = fλ, cepat rambat cahaya di ruang hampa tetap. Semakin tinggi frekuensi, semakin pendek panjang gelombangnya."
    },
    {
        "pertanyaan": "Urutan spektrum elektromagnetik dari frekuensi paling rendah ke paling tinggi adalah ....",
        "opsi": [
            "A. Gamma – sinar-X – ultraviolet – tampak – inframerah – mikro – radio",
            "B. Radio – mikro – inframerah – tampak – ultraviolet – sinar-X – gamma",
            "C. Radio – inframerah – mikro – tampak – gamma – ultraviolet – sinar-X",
            "D. Tampak – radio – mikro – inframerah – ultraviolet – gamma – sinar-X",
            "E. Mikro – radio – tampak – inframerah – sinar-X – ultraviolet – gamma"
        ],
        "kunci": "B",
        "alasan": [
            "A. Karena sinar gamma memiliki frekuensi paling rendah.",
            "B. Karena frekuensi meningkat dari gelombang radio menuju sinar gamma.",
            "C. Karena inframerah memiliki frekuensi lebih rendah daripada gelombang mikro.",
            "D. Karena cahaya tampak berada di awal spektrum.",
            "E. Karena gelombang mikro memiliki frekuensi lebih rendah daripada radio."
        ],
        "kunci_alasan": "B",
        "pembahasan": "Urutan spektrum elektromagnetik dari frekuensi rendah ke tinggi adalah radio, mikro, inframerah, cahaya tampak, ultraviolet, sinar-X, dan gamma."
    },
    {
        "pertanyaan": "Gelombang elektromagnetik termasuk gelombang ....",
        "opsi": [
            "A. Longitudinal",
            "B. Transversal",
            "C. Mekanik longitudinal",
            "D. Mekanik transversal",
            "E. Stasioner"
        ],
        "kunci": "B",
        "alasan": [
            "A. Karena arah getarnya sejajar dengan arah rambat.",
            "B. Karena medan listrik dan medan magnet berosilasi tegak lurus terhadap arah rambat.",
            "C. Karena gelombang elektromagnetik selalu membutuhkan medium mekanik.",
            "D. Karena gelombang elektromagnetik hanya merambat pada tali.",
            "E. Karena gelombang elektromagnetik tidak membawa energi."
        ],
        "kunci_alasan": "B",
        "pembahasan": "Gelombang elektromagnetik merupakan gelombang transversal. Medan listrik dan medan magnet saling tegak lurus serta tegak lurus terhadap arah rambat."
    },
    {
        "pertanyaan": "Gelombang elektromagnetik dapat membawa ....",
        "opsi": [
            "A. Materi dari sumber ke penerima",
            "B. Energi",
            "C. Medium perambatan",
            "D. Partikel udara",
            "E. Massa medium"
        ],
        "kunci": "B",
        "alasan": [
            "A. Karena gelombang memindahkan seluruh materi medium.",
            "B. Karena gelombang elektromagnetik dapat memindahkan energi tanpa memindahkan materi secara keseluruhan.",
            "C. Karena gelombang elektromagnetik membawa medium bersamanya.",
            "D. Karena semua gelombang harus membawa partikel udara.",
            "E. Karena energi gelombang sama dengan massa medium."
        ],
        "kunci_alasan": "B",
        "pembahasan": "Gelombang elektromagnetik memindahkan energi dari satu tempat ke tempat lain tanpa memerlukan perpindahan materi secara keseluruhan."
    },
    {
        "pertanyaan": "Sinar ultraviolet memiliki frekuensi .... dibandingkan cahaya tampak.",
        "opsi": [
            "A. Lebih rendah",
            "B. Sama",
            "C. Lebih tinggi",
            "D. Selalu nol",
            "E. Tidak memiliki frekuensi"
        ],
        "kunci": "C",
        "alasan": [
            "A. Karena ultraviolet berada di bawah inframerah dalam spektrum.",
            "B. Karena semua gelombang elektromagnetik memiliki frekuensi yang sama.",
            "C. Karena ultraviolet berada setelah cahaya tampak ke arah frekuensi lebih tinggi.",
            "D. Karena ultraviolet tidak membawa energi.",
            "E. Karena ultraviolet bukan gelombang elektromagnetik."
        ],
        "kunci_alasan": "C",
        "pembahasan": "Ultraviolet memiliki frekuensi lebih tinggi dan panjang gelombang lebih pendek daripada cahaya tampak."
    },
    {
        "pertanyaan": "Paparan sinar ultraviolet yang berlebihan dapat menyebabkan kulit terbakar. Hal ini berkaitan dengan ....",
        "opsi": [
            "A. Frekuensi ultraviolet lebih rendah daripada cahaya tampak",
            "B. Frekuensi ultraviolet lebih tinggi daripada cahaya tampak",
            "C. Ultraviolet tidak memiliki energi",
            "D. Panjang gelombang ultraviolet selalu lebih panjang",
            "E. Ultraviolet termasuk gelombang bunyi"
        ],
        "kunci": "B",
        "alasan": [
            "A. Karena energi foton meningkat seiring meningkatnya frekuensi.",
            "B. Karena energi foton tidak berhubungan dengan frekuensi.",
            "C. Karena semua gelombang elektromagnetik memiliki energi yang sama.",
            "D. Karena ultraviolet tidak dapat berinteraksi dengan kulit.",
            "E. Karena energi hanya dimiliki gelombang mekanik."
        ],
        "kunci_alasan": "A",
        "pembahasan": "Energi foton mengikuti persamaan E = hf. Semakin tinggi frekuensi, semakin besar energi fotonnya."
    },
    {
        "pertanyaan": "Sinar-X digunakan untuk menghasilkan gambar tulang dalam pemeriksaan medis karena ....",
        "opsi": [
            "A. Sinar-X dapat menembus jaringan lunak dan lebih banyak diserap oleh tulang",
            "B. Sinar-X tidak dapat menembus tubuh manusia",
            "C. Sinar-X hanya dipantulkan oleh kulit",
            "D. Sinar-X memiliki frekuensi sama dengan gelombang radio",
            "E. Sinar-X tidak berinteraksi dengan jaringan tubuh"
        ],
        "kunci": "A",
        "alasan": [
            "A. Karena perbedaan penyerapan sinar-X menghasilkan kontras gambar.",
            "B. Karena semua bagian tubuh menyerap sinar-X dalam jumlah sama.",
            "C. Karena tulang tidak menyerap sinar-X.",
            "D. Karena sinar-X merupakan gelombang mekanik.",
            "E. Karena gambar terbentuk tanpa adanya interaksi radiasi."
        ],
        "kunci_alasan": "A",
        "pembahasan": "Sinar-X dapat menembus jaringan lunak, sedangkan tulang menyerap lebih banyak sinar-X sehingga menghasilkan perbedaan intensitas pada gambar."
    },
    {
        "pertanyaan": "Gelombang elektromagnetik yang umum digunakan dalam komunikasi satelit adalah ....",
        "opsi": [
            "A. Gelombang mikro",
            "B. Gelombang bunyi",
            "C. Gelombang air",
            "D. Gelombang pada tali",
            "E. Gelombang pegas"
        ],
        "kunci": "A",
        "alasan": [
            "A. Karena gelombang mikro dapat digunakan untuk mengirimkan informasi dalam komunikasi satelit.",
            "B. Karena gelombang bunyi dapat merambat di ruang hampa.",
            "C. Karena gelombang air memiliki frekuensi sangat tinggi.",
            "D. Karena gelombang pada tali dapat mencapai satelit.",
            "E. Karena gelombang pegas tidak memerlukan medium."
        ],
        "kunci_alasan": "A",
        "pembahasan": "Gelombang mikro merupakan bagian spektrum elektromagnetik yang banyak digunakan dalam komunikasi satelit."
    }
]
# =========================================================
# DATABASE
# =========================================================
def koneksi():
    return sqlite3.connect(NAMA_DB, check_same_thread=False)
def siapkan_database():
    conn = koneksi()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hasil_tes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            kategori TEXT NOT NULL,
            skor INTEGER NOT NULL,
            jawaban TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
siapkan_database()

# Tabel monitoring menyimpan perpindahan fokus tab/jendela browser.
# Browser tidak mengungkap aplikasi lain yang dibuka siswa.
with koneksi() as _conn:
    _conn.execute("""CREATE TABLE IF NOT EXISTS log_monitoring (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        kelas TEXT NOT NULL,
        waktu TEXT NOT NULL,
        kejadian TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Belum ditinjau'
    )""")
    _conn.commit()

_monitor_component = components.declare_component(
    "pemantau_tab_siswa",
    path=str(__import__('pathlib').Path(__file__).parent / "monitor_component")
)

def catat_monitoring_siswa():
    """Catat saat tab/jendela browser kehilangan fokus; bukan bukti kecurangan."""
    if "nama_siswa" not in st.session_state or "kelas_siswa" not in st.session_state:
        return
    kejadian = _monitor_component(default=None, key="monitor_fokus_browser")
    if isinstance(kejadian, dict) and kejadian.get("event_id"):
        event_id = str(kejadian["event_id"])
        if st.session_state.get("monitor_event_terakhir") != event_id:
            st.session_state.monitor_event_terakhir = event_id
            conn = koneksi()
            conn.execute(
                "INSERT INTO log_monitoring (nama, kelas, waktu, kejadian) VALUES (?, ?, ?, ?)",
                (st.session_state.nama_siswa, st.session_state.kelas_siswa,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 kejadian.get("event", "Tab/jendela kehilangan fokus"))
            )
            conn.commit()
            conn.close()
# =========================================================
# FUNGSI PENILAIAN
# =========================================================
def hitung_hasil(respons):
    jumlah_benar_keduanya = 0
    jumlah_salah_yakin_keduanya = 0
    for i, item in enumerate(soal):
        r = respons.get(str(i))
        if not r:
            continue
        jawaban_benar = r["jawaban"] == item["kunci"]
        alasan_benar = r["alasan"] == item["kunci_alasan"]
        yakin_keduanya = (
            r["yakin_jawaban"] == "Yakin"
            and r["yakin_alasan"] == "Yakin"
        )
        if jawaban_benar and alasan_benar:
            jumlah_benar_keduanya += 1
        elif not jawaban_benar and not alasan_benar and yakin_keduanya:
            jumlah_salah_yakin_keduanya += 1
    skor = jumlah_benar_keduanya * 10
    if jumlah_salah_yakin_keduanya >= 3:
        kategori = "Miskonsepsi"
    elif jumlah_benar_keduanya >= 7:
        kategori = "Paham Konsep"
    else:
        kategori = "Tidak Paham Konsep"
    return skor, kategori
# =========================================================
# SESSION STATE
# =========================================================
if "nomor_soal" not in st.session_state:
    st.session_state.nomor_soal = 0
if "respons_siswa" not in st.session_state:
    st.session_state.respons_siswa = {}
if "tes_selesai" not in st.session_state:
    st.session_state.tes_selesai = False
if "guru_login" not in st.session_state:
    st.session_state.guru_login = False
if "hasil_terakhir" not in st.session_state:
    st.session_state.hasil_terakhir = None
# =========================================================
# SIDEBAR NAVIGASI
# =========================================================
st.sidebar.title("🌊 Misconception Physics")
st.sidebar.divider()
st.sidebar.caption("Four-Tier Diagnostic Test")
halaman = st.sidebar.selectbox(
    "Pilih Menu",
    ["Dashboard Siswa", "Virtual Lab 3D", "Dashboard Guru"]
)

# Monitoring aktif pada sesi siswa yang sudah mengisi identitas.
if halaman in ["Dashboard Siswa", "Virtual Lab 3D"]:
    catat_monitoring_siswa()
# =========================================================
# DASHBOARD SISWA
# =========================================================
if halaman == "Dashboard Siswa":
    st.title("🧑‍🎓 Dashboard Siswa")
    st.write("Tes Diagnostik Miskonsepsi: Gelombang Elektromagnetik")
    # Jika hasil sudah selesai, siswa hanya melihat hasil tesnya sendiri.
    if st.session_state.tes_selesai and st.session_state.hasil_terakhir:
        hasil = st.session_state.hasil_terakhir
        st.success("Tes berhasil diselesaikan!")
        st.subheader("Hasil Tes Kamu")
        st.write(f"**Nama:** {hasil['nama']}")
        st.write(f"**Kelas:** {hasil['kelas']}")
        st.write(f"**Skor:** {hasil['skor']} dari 100")
        st.write(f"**Kategori:** {hasil['kategori']}")
        st.subheader("Pembahasan Jawaban")
        for i, item in enumerate(soal):
            r = hasil["respons"].get(str(i), {})
            with st.expander(f"Soal {i+1}"):
                st.write(f"**Pertanyaan:** {item['pertanyaan']}")
                st.write(f"**Jawaban kamu:** {r.get('jawaban', '-')}")
                st.write(f"**Kunci jawaban:** {item['kunci']}")
                st.write(f"**Alasan kamu:** {r.get('alasan', '-')}")
                st.write(f"**Kunci alasan:** {item['kunci_alasan']}")
                st.info(item["pembahasan"])
        if st.button("Mulai Tes Baru"):
            st.session_state.nomor_soal = 0
            st.session_state.respons_siswa = {}
            st.session_state.tes_selesai = False
            st.session_state.hasil_terakhir = None
            st.rerun()
    else:
        with st.form("identitas_siswa"):
            nama = st.text_input("Nama lengkap")
            kelas = st.text_input("Kelas")
            mulai = st.form_submit_button("Mulai / Simpan Identitas")
        if mulai:
            if not nama.strip() or not kelas.strip():
                st.error("Nama dan kelas harus diisi.")
            else:
                st.session_state.nama_siswa = nama.strip()
                st.session_state.kelas_siswa = kelas.strip()
                st.success("Identitas tersimpan. Silakan kerjakan soal.")
        if "nama_siswa" in st.session_state and "kelas_siswa" in st.session_state:
            idx = st.session_state.nomor_soal
            item = soal[idx]
            tersimpan = st.session_state.respons_siswa.get(str(idx), {})
            st.progress((idx + 1) / len(soal))
            st.subheader(f"Soal {idx+1} dari {len(soal)}")
            st.write(item["pertanyaan"])
            pilihan_jawaban = [x[0] for x in item["opsi"]]
            jawaban = st.radio(
                "Tier 1 — Pilih jawaban",
                pilihan_jawaban,
                index=pilihan_jawaban.index(tersimpan["jawaban"])
                if tersimpan.get("jawaban") in pilihan_jawaban else None,
                format_func=lambda x: next(o for o in item["opsi"] if o.startswith(x))
            )
            yakin_jawaban = st.radio(
                "Tier 2 — Seberapa yakin dengan jawabanmu?",
                ["Yakin", "Tidak yakin"],
                index=["Yakin", "Tidak yakin"].index(tersimpan["yakin_jawaban"])
                if tersimpan.get("yakin_jawaban") in ["Yakin", "Tidak yakin"] else None,
                horizontal=True,
                key=f"yj_{idx}"
            )
            pilihan_alasan = [x[0] for x in item["alasan"]]
            alasan = st.radio(
                "Tier 3 — Pilih alasan",
                pilihan_alasan,
                index=pilihan_alasan.index(tersimpan["alasan"])
                if tersimpan.get("alasan") in pilihan_alasan else None,
                format_func=lambda x: next(o for o in item["alasan"] if o.startswith(x))
            )
            yakin_alasan = st.radio(
                "Tier 4 — Seberapa yakin dengan alasanmu?",
                ["Yakin", "Tidak yakin"],
                index=["Yakin", "Tidak yakin"].index(tersimpan["yakin_alasan"])
                if tersimpan.get("yakin_alasan") in ["Yakin", "Tidak yakin"] else None,
                horizontal=True,
                key=f"ya_{idx}"
            )
            col1, col2 = st.columns(2)
            with col1:
                if idx > 0 and st.button("⬅️ Sebelumnya"):
                    st.session_state.respons_siswa[str(idx)] = {
                        "jawaban": jawaban,
                        "yakin_jawaban": yakin_jawaban,
                        "alasan": alasan,
                        "yakin_alasan": yakin_alasan
                    }
                    st.session_state.nomor_soal -= 1
                    st.rerun()
            with col2:
                label_tombol = "Selesai & Kirim" if idx == len(soal) - 1 else "Berikutnya ➡️"
                if st.button(label_tombol):
                    if not all([jawaban, yakin_jawaban, alasan, yakin_alasan]):
                        st.error("Lengkapi semua tier sebelum melanjutkan.")
                    else:
                        st.session_state.respons_siswa[str(idx)] = {
                            "jawaban": jawaban,
                            "yakin_jawaban": yakin_jawaban,
                            "alasan": alasan,
                            "yakin_alasan": yakin_alasan
                        }
                        if idx < len(soal) - 1:
                            st.session_state.nomor_soal += 1
                            st.rerun()
                        else:
                            skor, kategori = hitung_hasil(st.session_state.respons_siswa)
                            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            conn = koneksi()
                            conn.execute(
                                """INSERT INTO hasil_tes
                                (nama, kelas, tanggal, kategori, skor, jawaban)
                                VALUES (?, ?, ?, ?, ?, ?)""",
                                (
                                    st.session_state.nama_siswa,
                                    st.session_state.kelas_siswa,
                                    tanggal,
                                    kategori,
                                    skor,
                                    json.dumps(st.session_state.respons_siswa, ensure_ascii=False)
                                )
                            )
                            conn.commit()
                            conn.close()
                            st.session_state.hasil_terakhir = {
                                "nama": st.session_state.nama_siswa,
                                "kelas": st.session_state.kelas_siswa,
                                "skor": skor,
                                "kategori": kategori,
                                "respons": dict(st.session_state.respons_siswa)
                            }
                            st.session_state.tes_selesai = True
                            st.rerun()
# =========================================================
# PILIH MENU
# =========================================================
if halaman == "Dashboard Guru":
    if not st.session_state.guru_login:
        st.write("Masukkan password untuk mengakses data dan analisis siswa.")
        with st.form("login_guru"):
            password = st.text_input("Password Guru", type="password")
            masuk = st.form_submit_button("Login")
        if masuk:
            if password == PASSWORD_GURU:
                st.session_state.guru_login = True
                st.rerun()
            else:
                st.error("Password salah.")
    else:
        if st.button("Logout Guru"):
            st.session_state.guru_login = False
            st.rerun()
        st.subheader("🚨 Monitoring Aktivitas Siswa")
        st.caption("Peringatan menunjukkan tab/jendela browser kehilangan fokus. Ini bukan bukti bahwa siswa membuka aplikasi tertentu atau melakukan kecurangan.")
        conn_monitor = koneksi()
        log_df = pd.read_sql_query("SELECT * FROM log_monitoring ORDER BY id DESC LIMIT 200", conn_monitor)
        belum_ditinjau = int((log_df["status"] == "Belum ditinjau").sum()) if not log_df.empty else 0
        if belum_ditinjau:
            st.warning(f"Ada {belum_ditinjau} kejadian perpindahan fokus yang belum ditinjau.")
            # Nada pendek; browser mungkin meminta interaksi pengguna sebelum memutar audio.
            import io, wave, math, struct
            _rate = 22050
            _samples = [int(9000 * math.sin(2 * math.pi * 880 * n / _rate)) for n in range(int(_rate * 0.35))]
            _wav = io.BytesIO()
            with wave.open(_wav, 'wb') as _w:
                _w.setnchannels(1); _w.setsampwidth(2); _w.setframerate(_rate)
                _w.writeframes(b''.join(struct.pack('<h', v) for v in _samples))
            st.audio(_wav.getvalue(), format="audio/wav", autoplay=True)
            if st.button("Tandai semua peringatan sudah ditinjau"):
                conn_monitor.execute("UPDATE log_monitoring SET status='Sudah ditinjau' WHERE status='Belum ditinjau'")
                conn_monitor.commit()
                st.rerun()
        if log_df.empty:
            st.info("Belum ada aktivitas perpindahan fokus yang tercatat.")
        else:
            st.dataframe(log_df.rename(columns={"nama":"Nama", "kelas":"Kelas", "waktu":"Waktu", "kejadian":"Kejadian", "status":"Status"})[["Nama", "Kelas", "Waktu", "Kejadian", "Status"]], use_container_width=True, hide_index=True)
        conn_monitor.close()
        st.divider()
        conn = koneksi()
        df = pd.read_sql_query("SELECT * FROM hasil_tes ORDER BY id DESC", conn)
        conn.close()
        if df.empty:
            st.info("Belum ada hasil tes siswa.")
        else:
            st.subheader("📊 Ringkasan Hasil Siswa")
            total_siswa = len(df)
            paham = int((df["kategori"] == "Paham Konsep").sum())
            miskonsepsi = int((df["kategori"] == "Miskonsepsi").sum())
            belum_paham = int((df["kategori"] == "Tidak Paham Konsep").sum())
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Tes", total_siswa)
            c2.metric("Paham Konsep", paham)
            c3.metric("Miskonsepsi", miskonsepsi)
            c4.metric("Tidak Paham", belum_paham)
            st.subheader("Grafik Kategori Pemahaman Siswa")
            grafik_kategori = (
                df["kategori"].value_counts()
                .reindex(["Paham Konsep", "Miskonsepsi", "Tidak Paham Konsep"], fill_value=0)
            )
            st.bar_chart(grafik_kategori)
            st.subheader("📈 Analisis Miskonsepsi per Soal")
            hasil_analisis = []
            respons_semua = [json.loads(x) for x in df["jawaban"].tolist()]
            for i, item in enumerate(soal):
                total = 0
                benar_dua = 0
                indikasi = 0
                for respons_siswa in respons_semua:
                    r = respons_siswa.get(str(i))
                    if r is None:
                        continue
                    total += 1
                    benar_jawaban = r["jawaban"] == item["kunci"]
                    benar_alasan = r["alasan"] == item["kunci_alasan"]
                    if benar_jawaban and benar_alasan:
                        benar_dua += 1
                    if (
                        not benar_jawaban
                        and not benar_alasan
                        and r["yakin_jawaban"] == "Yakin"
                        and r["yakin_alasan"] == "Yakin"
                    ):
                        indikasi += 1
                salah_atau_tidak_lengkap = total - benar_dua
                hasil_analisis.append({
                    "Soal": f"Soal {i+1}",
                    "Jumlah Siswa": total,
                    "Jawaban dan Alasan Benar": benar_dua,
                    "Respons Tidak Sepenuhnya Benar": salah_atau_tidak_lengkap,
                    "Indikasi Miskonsepsi": indikasi,
                    "Persentase Respons Tidak Sepenuhnya Benar": round(
                        salah_atau_tidak_lengkap / total * 100, 1
                    ) if total else 0
                })
            df_analisis = pd.DataFrame(hasil_analisis)
            st.dataframe(df_analisis, use_container_width=True)
            st.write("**Grafik persentase respons yang tidak sepenuhnya benar per soal**")
            st.bar_chart(
                df_analisis.set_index("Soal")[["Persentase Respons Tidak Sepenuhnya Benar"]]
            )
            # Hitung jumlah soal yang dijawab benar pada jawaban DAN alasan.
            def hitung_jawaban_benar(teks_jawaban):
                try:
                    respons = json.loads(teks_jawaban)
                except (TypeError, json.JSONDecodeError):
                    return 0
                jumlah = 0
                for nomor, item_soal in enumerate(soal):
                    r = respons.get(str(nomor), {})
                    if (r.get("jawaban") == item_soal["kunci"] and
                            r.get("alasan") == item_soal["kunci_alasan"]):
                        jumlah += 1
                return jumlah

            df["Jumlah Jawaban dan Alasan Benar"] = df["jawaban"].apply(hitung_jawaban_benar)

            st.subheader("📋 Data Hasil Siswa")
            kolom_tampil = ["nama", "kelas", "tanggal", "kategori", "skor", "Jumlah Jawaban dan Alasan Benar"]
            st.dataframe(
                df[kolom_tampil].rename(columns={
                    "nama": "Nama",
                    "kelas": "Kelas",
                    "tanggal": "Tanggal",
                    "kategori": "Kategori",
                    "skor": "Skor"
                }),
                use_container_width=True
            )
            st.subheader("👥 Daftar Siswa Berdasarkan Kategori")
            for nama_kategori in ["Miskonsepsi", "Paham Konsep", "Tidak Paham Konsep"]:
                data_kategori = df[df["kategori"] == nama_kategori].copy()
                with st.expander(f"{nama_kategori} ({len(data_kategori)} siswa)", expanded=(nama_kategori == "Miskonsepsi")):
                    if data_kategori.empty:
                        st.info("Belum ada siswa dalam kategori ini.")
                    else:
                        st.dataframe(
                            data_kategori[["nama", "kelas", "tanggal", "skor", "Jumlah Jawaban dan Alasan Benar"]]
                            .rename(columns={"nama": "Nama", "kelas": "Kelas", "tanggal": "Tanggal", "skor": "Skor"}),
                            use_container_width=True,
                            hide_index=True
                        )

            st.subheader("🏆 Siswa dengan Jawaban Benar Terbanyak")
            peringkat = df.sort_values(
                ["Jumlah Jawaban dan Alasan Benar", "skor"], ascending=False
            )[["nama", "kelas", "Jumlah Jawaban dan Alasan Benar", "skor"]].head(10)
            st.dataframe(
                peringkat.rename(columns={"nama": "Nama", "kelas": "Kelas", "skor": "Skor"}),
                use_container_width=True,
                hide_index=True
            )

            daftar_siswa = {
                f"{row['nama']} | {row['kelas']} | ID {row['id']}": int(row["id"])
                for _, row in df.iterrows()
            }
            pilihan = st.selectbox("Pilih siswa untuk melihat jawaban", list(daftar_siswa.keys()))
            id_pilihan = daftar_siswa[pilihan]
            data_terpilih = df[df["id"] == id_pilihan].iloc[0]
            respons_terpilih = json.loads(data_terpilih["jawaban"])
            st.subheader("🔎 Detail Jawaban Siswa")
            st.write(f"**Nama:** {data_terpilih['nama']}")
            st.write(f"**Kelas:** {data_terpilih['kelas']}")
            st.write(f"**Kategori:** {data_terpilih['kategori']}")
            st.write(f"**Skor:** {data_terpilih['skor']} dari 100")
            for i, item in enumerate(soal):
                r = respons_terpilih.get(str(i), {})
                with st.expander(f"Soal {i+1}"):
                    st.write(item["pertanyaan"])
                    st.write(f"Jawaban siswa: {r.get('jawaban', '-')}")
                    st.write(f"Kunci jawaban: {item['kunci']}")
                    st.write(f"Keyakinan jawaban: {r.get('yakin_jawaban', '-')}")
                    st.write(f"Alasan siswa: {r.get('alasan', '-')}")
                    st.write(f"Kunci alasan: {item['kunci_alasan']}")
                    st.write(f"Keyakinan alasan: {r.get('yakin_alasan', '-')}")
                    st.info(item["pembahasan"])
            st.subheader("💡 Rekomendasi Tindak Lanjut")
            if data_terpilih["kategori"] == "Paham Konsep":
                st.success(
                    "Siswa dapat diberikan soal pengayaan, penerapan konsep, "
                    "dan pemecahan masalah."
                )
            elif data_terpilih["kategori"] == "Miskonsepsi":
                st.warning(
                    "Siswa perlu mengikuti pembelajaran remedial yang menekankan "
                    "klarifikasi konsep, diskusi, demonstrasi, dan eksperimen."
                )
            else:
                st.info(
                    "Siswa perlu mendapatkan penguatan konsep dasar, contoh konkret, "
                    "latihan bertahap, dan pendampingan guru."
                )
            st.subheader("📥 Unduh Data Hasil Siswa")
            csv_data = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Unduh Data dalam Format CSV",
                data=csv_data,
                file_name="hasil_diagnostik_siswa.csv",
                mime="text/csv"
            )
# =========================================================
# VIRTUAL LAB 3D GELOMBANG ELEKTROMAGNETIK
# =========================================================
elif halaman == "Virtual Lab 3D":
    import numpy as np
    import plotly.graph_objects as go
    st.title("🔬 Virtual Lab Gelombang Elektromagnetik")
    st.write(
        "Laboratorium virtual untuk mempelajari 10 konsep "
        "sesuai tes diagnostik Gelombang Elektromagnetik."
    )
    st.info(
        "Petunjuk: Pilih eksperimen, ubah parameternya, "
        "amati ilustrasi, baca penjelasan, lalu jawab latihan."
    )
    daftar_lab = [
        "1. Gelombang elektromagnetik tanpa medium",
        "2. Cahaya Matahari menuju Bumi",
        "3. Hubungan frekuensi dan panjang gelombang",
        "4. Urutan spektrum elektromagnetik",
        "5. Sifat transversal gelombang elektromagnetik",
        "6. Gelombang elektromagnetik membawa energi",
        "7. Frekuensi ultraviolet dan cahaya tampak",
        "8. Energi foton dan radiasi ultraviolet",
        "9. Sinar-X untuk pemeriksaan tulang",
        "10. Gelombang mikro untuk komunikasi satelit"
    ]
    lab = st.selectbox("Pilih eksperimen:", daftar_lab)

    # Video ilustrasi lokal (MP4): simpan video sesuai nama file di folder video_lab.
    from pathlib import Path
    nomor_lab = daftar_lab.index(lab) + 1
    folder_video = Path(__file__).parent / "video_lab"
    file_video = folder_video / f"lab_{nomor_lab:02d}.mp4"
    with st.expander("🎬 Video ilustrasi pembelajaran", expanded=True):
        if file_video.is_file():
            st.video(str(file_video))
            st.caption("Video diputar langsung di aplikasi dari file lokal.")
        else:
            st.info(
                f"Video untuk eksperimen ini belum tersedia. "
                f"Letakkan file MP4 bernama lab_{nomor_lab:02d}.mp4 "
                "di dalam folder video_lab pada folder proyek aplikasi."
            )

    st.divider()
    fig = go.Figure()
    pertanyaan = ""
    pilihan = []
    kunci = ""
    pembahasan = ""
    # =====================================================
    # LAB 1: GELOMBANG TANPA MEDIUM
    # =====================================================
    if lab == daftar_lab[0]:
        st.subheader("Eksperimen 1 — Gelombang tanpa medium")
        st.write(
            "Amati medan listrik dan medan magnet yang "
            "merambat bersama tanpa membutuhkan medium."
        )
        frekuensi = st.slider(
            "Jumlah gelombang",
            1, 8, 3,
            key="lab1_f"
        )
        amplitudo = st.slider(
            "Amplitudo visual",
            1, 5, 2,
            key="lab1_a"
        )
        x = np.linspace(0, 10, 400)
        fase = 2 * np.pi * frekuensi * x / 10
        E = amplitudo * np.sin(fase)
        B = amplitudo * np.sin(fase)
        fig.add_trace(go.Scatter3d(
            x=x, y=E, z=np.zeros_like(x),
            mode="lines",
            name="Medan listrik (E)",
            line=dict(color="red", width=7)
        ))
        fig.add_trace(go.Scatter3d(
            x=x, y=np.zeros_like(x), z=B,
            mode="lines",
            name="Medan magnet (B)",
            line=dict(color="blue", width=7)
        ))
        fig.add_trace(go.Scatter3d(
            x=[0, 10], y=[0, 0], z=[0, 0],
            mode="lines",
            name="Arah rambat",
            line=dict(color="green", width=6)
        ))
        fig.update_layout(
            title="Visualisasi medan listrik dan magnet",
            scene=dict(
                xaxis_title="Arah rambat",
                yaxis_title="Medan listrik",
                zaxis_title="Medan magnet",
                aspectmode="cube"
            ),
            height=550
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success(
            "Konsep: Gelombang elektromagnetik dapat "
            "merambat di ruang hampa karena tidak membutuhkan "
            "medium material."
        )
        st.latex(r"c = 3 \times 10^8 \text{m/s}")
        pertanyaan = "Apakah gelombang elektromagnetik membutuhkan medium?"
        pilihan = ["Ya, selalu", "Tidak membutuhkan medium"]
        kunci = pilihan[1]
        pembahasan = (
            "Gelombang elektromagnetik dapat merambat tanpa medium karena "
            "perambatannya berupa perubahan medan listrik dan medan magnet "
            "yang saling berkaitan. Karena itu, gelombang ini tetap dapat "
            "bergerak di ruang hampa. Hal ini berbeda dengan gelombang bunyi, "
            "yang memerlukan partikel zat seperti udara, air, atau benda padat "
            "untuk meneruskan getaran. Jadi, cahaya dan gelombang radio dapat "
            "merambat di ruang hampa, sedangkan bunyi tidak."
        )
    # =====================================================
    # LAB 2: CAHAYA MATAHARI MENUJU BUMI
    # =====================================================
    elif lab == daftar_lab[1]:
        st.subheader("Eksperimen 2 — Cahaya Matahari menuju Bumi")
        st.write(
            "Amati perjalanan cahaya dari Matahari menuju Bumi "
            "melewati ruang hampa."
        )
        fig.add_trace(go.Scatter(
            x=[0, 10], y=[0, 0],
            mode="lines",
            name="Lintasan cahaya",
            line=dict(color="orange", width=5, dash="dash")
        ))
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode="markers+text",
            text=["MATAHARI"],
            textposition="top center",
            marker=dict(size=35, color="orange"),
            name="Matahari"
        ))
        fig.add_trace(go.Scatter(
            x=[10], y=[0],
            mode="markers+text",
            text=["BUMI"],
            textposition="top center",
            marker=dict(size=28, color="royalblue"),
            name="Bumi"
        ))
        fig.update_layout(
            title="Perjalanan cahaya Matahari melalui ruang hampa",
            xaxis_title="Jarak ilustratif",
            yaxis=dict(visible=False),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success(
            "Cahaya Matahari dapat mencapai Bumi karena cahaya "
            "merupakan gelombang elektromagnetik yang dapat "
            "merambat tanpa medium."
        )
        pertanyaan = "Mengapa cahaya Matahari dapat sampai ke Bumi?"
        pilihan = [
            "Karena ruang hampa memiliki udara",
            "Karena cahaya tidak membutuhkan medium",
            "Karena cahaya adalah gelombang bunyi"
        ]
        kunci = pilihan[1]
        pembahasan = (
            "Cahaya Matahari sampai ke Bumi dengan merambat melalui ruang "
            "antarplanet yang hampir hampa. Cahaya merupakan gelombang "
            "elektromagnetik, sehingga tidak membutuhkan udara atau zat lain "
            "sebagai perantara. Energi dari Matahari dibawa oleh cahaya dan "
            "dapat diterima oleh Bumi, misalnya sebagai cahaya dan panas. "
            "Inilah sebabnya Matahari tetap dapat menerangi Bumi meskipun "
            "sebagian besar ruang di antaranya merupakan ruang hampa."
        )
    # =====================================================
    # LAB 3: FREKUENSI DAN PANJANG GELOMBANG
    # =====================================================
    elif lab == daftar_lab[2]:
        st.subheader("Eksperimen 3 — Frekuensi dan panjang gelombang")
        f_thz = st.slider(
            "Frekuensi (THz)",
            1, 1000, 500,
            key="lab3_f"
        )
        c = 299792458
        f = f_thz * 10**12
        panjang_nm = c / f * 10**9
        x = np.linspace(0, 2, 400)
        y = np.sin(2 * np.pi * x)
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode="lines",
            name="Gelombang",
            line=dict(color="royalblue", width=4)
        ))
        fig.update_layout(
            title="Bentuk gelombang (dua siklus visual)",
            xaxis_title="Posisi dalam satuan panjang gelombang",
            yaxis_title="Amplitudo relatif",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Panjang gelombang", f"{panjang_nm:,.2f} nm")
        st.latex(r"c = f\lambda")
        st.write(
            "Dalam ruang hampa, jika frekuensi meningkat, "
            "panjang gelombang menjadi lebih pendek."
        )
        pertanyaan = (
            "Jika frekuensi gelombang meningkat di ruang hampa, "
            "apa yang terjadi pada panjang gelombangnya?"
        )
        pilihan = [
            "Semakin panjang",
            "Semakin pendek",
            "Tetap sama"
        ]
        kunci = pilihan[1]
        pembahasan = (
            "Di ruang hampa, gelombang elektromagnetik merambat dengan "
            "kelajuan tetap, sekitar 3 × 10⁸ m/s. Hubungan kelajuan, frekuensi, "
            "dan panjang gelombang dinyatakan dengan c = fλ. Karena nilai c "
            "tetap, frekuensi (f) dan panjang gelombang (λ) berbanding terbalik: "
            "ketika frekuensi meningkat, panjang gelombang mengecil; ketika "
            "frekuensi menurun, panjang gelombang membesar. Pada simulasi, "
            "perubahan frekuensi karena itu diikuti perubahan panjang gelombang."
        )
    # =====================================================
    # LAB 4: SPEKTRUM ELEKTROMAGNETIK
    # =====================================================
    elif lab == daftar_lab[3]:
        st.subheader("Eksperimen 4 — Spektrum elektromagnetik")
        nama_spektrum = [
            "Radio", "Mikro", "Inframerah",
            "Cahaya tampak", "Ultraviolet",
            "Sinar-X", "Gamma"
        ]
        nilai = [1, 2, 3, 4, 5, 6, 7]
        fig.add_trace(go.Bar(
            x=nama_spektrum,
            y=nilai,
            text=nama_spektrum,
            textposition="outside",
            marker=dict(
                color=[
                    "gray", "lightblue", "orange",
                    "gold", "violet", "royalblue", "purple"
                ]
            )
        ))
        fig.update_layout(
            title="Urutan spektrum dari frekuensi rendah ke tinggi",
            xaxis_title="Jenis gelombang",
            yaxis=dict(visible=False),
            height=430
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success(
            "Urutan frekuensi meningkat dari radio, mikro, "
            "inframerah, cahaya tampak, ultraviolet, sinar-X, "
            "hingga gamma."
        )
        pertanyaan = (
            "Gelombang manakah yang memiliki frekuensi paling tinggi?"
        )
        pilihan = [
            "Gelombang radio",
            "Cahaya tampak",
            "Sinar gamma"
        ]
        kunci = pilihan[2]
        pembahasan = (
            "Spektrum elektromagnetik mencakup gelombang radio, gelombang "
            "mikro, inframerah, cahaya tampak, ultraviolet, sinar-X, dan sinar "
            "gamma. Urutan tersebut menunjukkan frekuensi yang semakin besar "
            "dan panjang gelombang yang semakin pendek. Sinar gamma memiliki "
            "frekuensi paling tinggi dan panjang gelombang paling pendek, "
            "sedangkan gelombang radio memiliki frekuensi paling rendah dan "
            "panjang gelombang paling panjang. Semua jenis tersebut adalah "
            "gelombang elektromagnetik; yang membedakannya terutama frekuensi "
            "atau panjang gelombangnya."
        )
    # =====================================================
    # LAB 5: SIFAT TRANSVERSAL
    # =====================================================
    elif lab == daftar_lab[4]:
        st.subheader("Eksperimen 5 — Sifat transversal")
        fig.add_trace(go.Scatter3d(
            x=[0, 5], y=[0, 0], z=[0, 0],
            mode="lines+markers",
            name="Arah rambat",
            line=dict(color="green", width=8)
        ))
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 4], z=[0, 0],
            mode="lines+markers",
            name="Medan listrik",
            line=dict(color="red", width=8)
        ))
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[0, 4],
            mode="lines+markers",
            name="Medan magnet",
            line=dict(color="blue", width=8)
        ))
        fig.update_layout(
            title="Tiga arah yang saling tegak lurus",
            scene=dict(
                xaxis_title="Arah rambat",
                yaxis_title="Medan listrik",
                zaxis_title="Medan magnet",
                aspectmode="cube"
            ),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success(
            "Medan listrik, medan magnet, dan arah rambat "
            "saling tegak lurus pada gelombang elektromagnetik "
            "bidang di ruang hampa."
        )
        pertanyaan = (
            "Bagaimana arah medan listrik dan medan magnet "
            "terhadap arah rambat?"
        )
        pilihan = [
            "Sejajar dengan arah rambat",
            "Tegak lurus terhadap arah rambat",
            "Tidak memiliki arah"
        ]
        kunci = pilihan[1]
        pembahasan = (
            "Gelombang elektromagnetik merupakan gelombang transversal. "
            "Artinya, arah osilasi medan listrik dan medan magnet tegak lurus "
            "terhadap arah perambatan gelombang. Kedua medan itu juga saling "
            "tegak lurus. Pada gelombang yang merambat di ruang hampa, ketiga "
            "arah tersebut membentuk tiga arah yang saling tegak lurus. "
            "Sifat ini dapat dibedakan dari gelombang longitudinal, yang "
            "getarannya sejajar dengan arah rambat."
        )
    # =====================================================
    # LAB 6: GELOMBANG MEMBAWA ENERGI
    # =====================================================
    elif lab == daftar_lab[5]:
        st.subheader("Eksperimen 6 — Gelombang membawa energi")
        jumlah = st.slider(
            "Jumlah foton ilustratif",
            1, 20, 5,
            key="lab6_jumlah"
        )
        x = np.linspace(0, 10, jumlah + 2)
        y = np.zeros_like(x)
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode="markers",
            name="Foton (ilustrasi)",
            marker=dict(size=14, color="orange", symbol="circle")
        ))
        fig.add_annotation(
            x=9, y=0.2,
            text="Penerima energi",
            showarrow=False
        )
        fig.update_layout(
            title="Ilustrasi energi dibawa oleh gelombang",
            xaxis_title="Arah rambat",
            yaxis=dict(visible=False),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        st.write(
            "Gelombang elektromagnetik dapat memindahkan energi "
            "dari satu tempat ke tempat lain tanpa memindahkan "
            "materi secara keseluruhan."
        )
        pertanyaan = (
            "Apa yang dapat dibawa gelombang elektromagnetik "
            "ketika merambat?"
        )
        pilihan = [
            "Energi",
            "Medium material",
            "Benda padat"
        ]
        kunci = pilihan[0]
        pembahasan = (
            "Gelombang elektromagnetik memindahkan energi dari sumber ke "
            "tempat lain tanpa memindahkan materi secara keseluruhan. Contohnya, "
            "cahaya Matahari membawa energi yang menghangatkan permukaan Bumi, "
            "dan gelombang mikro dapat membawa energi dalam oven microwave. "
            "Pada ilustrasi, foton digunakan sebagai gambaran paket energi "
            "cahaya. Semakin besar energi yang diterima suatu benda, semakin "
            "besar pula perubahan yang dapat terjadi padanya, misalnya kenaikan "
            "suhu."
        )
    # =====================================================
    # LAB 7: UV DAN CAHAYA TAMPAK
    # =====================================================
    elif lab == daftar_lab[6]:
        st.subheader("Eksperimen 7 — UV dan cahaya tampak")
        f_uv = st.slider(
            "Frekuensi ultraviolet (THz)",
            750, 3000, 900,
            key="lab7_uv"
        )
        f_cahaya = 550
        fig.add_trace(go.Bar(
            x=["Cahaya tampak", "Ultraviolet"],
            y=[f_cahaya, f_uv],
            text=[f"{f_cahaya} THz", f"{f_uv} THz"],
            textposition="outside",
            marker_color=["gold", "purple"]
        ))
        fig.update_layout(
            title="Perbandingan frekuensi",
            yaxis_title="Frekuensi (THz)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.success(
            "Ultraviolet memiliki frekuensi lebih tinggi "
            "daripada cahaya tampak."
        )
        pertanyaan = (
            "Dibandingkan cahaya tampak, frekuensi ultraviolet adalah..."
        )
        pilihan = [
            "Lebih rendah",
            "Sama",
            "Lebih tinggi"
        ]
        kunci = pilihan[2]
        pembahasan = (
            "Sinar ultraviolet (UV) berada setelah cahaya tampak pada spektrum "
            "elektromagnetik, yaitu pada frekuensi yang lebih tinggi dan panjang "
            "gelombang yang lebih pendek. Karena frekuensinya lebih tinggi, "
            "setiap foton ultraviolet membawa energi lebih besar daripada foton "
            "cahaya tampak. Sebagian radiasi UV dari Matahari dapat memengaruhi "
            "kulit; paparan berlebihan dapat menyebabkan kulit terbakar dan "
            "meningkatkan risiko kerusakan kulit. Dampaknya dipengaruhi jenis "
            "UV, intensitas, dan lama paparan."
        )
    # =====================================================
    # LAB 8: ENERGI FOTON DAN UV
    # =====================================================
    elif lab == daftar_lab[7]:
        st.subheader("Eksperimen 8 — Energi foton ultraviolet")
        panjang_uv = st.slider(
            "Panjang gelombang ultraviolet (nm)",
            100, 400, 250,
            key="lab8_lambda"
        )
        energi_ev = 1239.84 / panjang_uv
        fig.add_trace(go.Bar(
            x=["Energi foton"],
            y=[energi_ev],
            text=[f"{energi_ev:.2f} eV"],
            textposition="outside",
            marker_color="purple"
        ))
        fig.update_layout(
            title="Energi satu foton berdasarkan panjang gelombang",
            yaxis_title="Energi (eV)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Energi foton", f"{energi_ev:.3f} eV")
        st.latex(r"E = hf = \frac{hc}{\lambda}")
        st.warning(
            "Paparan ultraviolet berlebihan dapat merusak kulit. "
            "Dampaknya juga dipengaruhi intensitas dan lama paparan."
        )
        pertanyaan = (
            "Jika panjang gelombang semakin pendek, "
            "bagaimana energi fotonnya?"
        )
        pilihan = [
            "Semakin kecil",
            "Semakin besar",
            "Tidak berubah"
        ]
        kunci = pilihan[1]
        pembahasan = (
            "Energi setiap foton mengikuti persamaan E = hf, dengan E sebagai "
            "energi foton, h sebagai konstanta Planck, dan f sebagai frekuensi. "
            "Karena f = c/λ di ruang hampa, energi juga dapat ditulis E = hc/λ. "
            "Artinya, semakin tinggi frekuensi atau semakin pendek panjang "
            "gelombang, semakin besar energi setiap foton. Pada simulasi, ketika "
            "panjang gelombang UV diperkecil, nilai energi foton meningkat. "
            "Energi foton bukan satu-satunya penentu dampak paparan; intensitas "
            "dan durasi paparan juga berpengaruh."
        )
    # =====================================================
    # LAB 9: SINAR-X DAN TULANG
    # =====================================================
    elif lab == daftar_lab[8]:
        st.subheader("Eksperimen 9 — Sinar-X untuk pemeriksaan tulang")
        st.write(
            "Ilustrasi berikut menunjukkan bahwa jaringan "
            "yang berbeda dapat menyerap sinar-X secara berbeda."
        )
        fig.add_trace(go.Bar(
            x=["Jaringan lunak", "Tulang"],
            y=[70, 20],
            text=["Lebih banyak diteruskan", "Lebih banyak diserap"],
            textposition="outside",
            marker_color=["lightblue", "royalblue"]
        ))
        fig.update_layout(
            title="Ilustrasi perbedaan transmisi sinar-X",
            yaxis_title="Transmisi relatif (ilustratif)",
            yaxis=dict(range=[0, 100]),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "Angka pada ilustrasi ini hanya untuk menjelaskan "
            "perbedaan secara kualitatif, bukan data medis terukur."
        )
        st.success(
            "Tulang umumnya menyerap sinar-X lebih banyak "
            "daripada jaringan lunak sehingga dapat terlihat "
            "kontras pada citra radiografi."
        )
        pertanyaan = (
            "Mengapa tulang dapat terlihat pada pemeriksaan sinar-X?"
        )
        pilihan = [
            "Tulang menyerap sinar-X lebih banyak daripada "
            "jaringan lunak",
            "Tulang menghasilkan cahaya sendiri",
            "Sinar-X tidak dapat melewati jaringan lunak"
        ]
        kunci = pilihan[0]
        pembahasan = (
            "Sinar-X dapat melewati tubuh, tetapi setiap jaringan menyerapnya "
            "dengan tingkat yang berbeda. Jaringan lunak umumnya meneruskan "
            "lebih banyak sinar-X, sedangkan tulang yang lebih rapat menyerap "
            "lebih banyak. Detektor menangkap perbedaan jumlah sinar-X yang "
            "sampai setelah melewati tubuh, lalu membentuk kontras pada citra "
            "radiografi. Karena itu, tulang biasanya tampak lebih terang pada "
            "gambar sinar-X. Pemeriksaan ini menggunakan radiasi pengion, "
            "sehingga dilakukan dengan pengaturan dan perlindungan keselamatan "
            "yang sesuai."
        )
    # =====================================================
    # LAB 10: GELOMBANG MIKRO DAN SATELIT
    # =====================================================
    elif lab == daftar_lab[9]:
        st.subheader("Eksperimen 10 — Komunikasi satelit")
        frek_ghz = st.slider(
            "Frekuensi gelombang mikro (GHz)",
            1, 30, 12,
            key="lab10_f"
        )
        panjang_m = 0.299792458 / frek_ghz
        fig.add_trace(go.Scatter(
            x=[0, 5, 10],
            y=[0, 2, 0],
            mode="lines+markers+text",
            text=["Stasiun Bumi", "Satelit", "Penerima"],
            textposition="top center",
            marker=dict(size=[22, 30, 22],
                        color=["royalblue", "orange", "royalblue"]),
            line=dict(color="green", width=4),
            name="Jalur komunikasi"
        ))
        fig.update_layout(
            title="Ilustrasi komunikasi melalui satelit",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.metric(
            "Panjang gelombang",
            f"{panjang_m:.4f} meter"
        )
        st.success(
            "Gelombang mikro digunakan dalam berbagai sistem "
            "komunikasi satelit untuk mengirimkan informasi."
        )
        pertanyaan = (
            "Gelombang elektromagnetik yang umum digunakan "
            "dalam komunikasi satelit adalah..."
        )
        pilihan = [
            "Gelombang mikro",
            "Gelombang bunyi",
            "Gelombang air"
        ]
        kunci = pilihan[0]
        pembahasan = (
            "Gelombang mikro merupakan bagian dari spektrum elektromagnetik "
            "yang digunakan dalam berbagai sistem komunikasi satelit. Antena "
            "di stasiun Bumi mengirimkan sinyal gelombang mikro menuju satelit, "
            "kemudian satelit meneruskan atau memancarkan kembali sinyal ke "
            "wilayah penerima. Informasi dapat dibawa melalui perubahan atau "
            "modulasi sinyal, lalu diolah kembali oleh perangkat penerima. "
            "Hubungan frekuensi dan panjang gelombangnya tetap mengikuti "
            "c = fλ; pada frekuensi yang lebih tinggi, panjang gelombangnya "
            "lebih pendek untuk kelajuan rambat yang sama."
        )
    # =====================================================
    # LATIHAN DAN UMPAN BALIK
    # =====================================================
    st.divider()
    st.subheader("🧠 Uji Pemahaman Eksperimen")
    st.write(pertanyaan)
    jawaban_latihan = st.radio(
        "Pilih jawaban:",
        pilihan,
        index=None,
        key=f"jawaban_latihan_{daftar_lab.index(lab)}"
    )
    if st.button(
        "Periksa Jawaban",
        key=f"periksa_lab_{daftar_lab.index(lab)}"
    ):
        if jawaban_latihan is None:
            st.warning("Pilih jawaban terlebih dahulu.")
        elif jawaban_latihan == kunci:
            st.success("Benar! Pemahaman konsep kamu sudah tepat.")
            st.info(pembahasan)
        else:
            st.error("Belum tepat. Yuk, ikuti remediasi singkat berikut.")
            st.info("Pembahasan konsep: " + pembahasan)
            st.markdown("**Langkah remediasi:**")
            st.markdown("1. Tonton kembali video ilustrasi pada eksperimen ini.\n2. Ubah parameter simulasi dan amati apa yang berubah.\n3. Baca rangkuman konsep, lalu jelaskan kembali dengan kata-katamu sendiri.\n4. Coba lagi latihan pemahaman setelah mempelajari konsep.")
    with st.expander("📘 Baca rangkuman konsep dan remediasi mandiri"):
        st.write(pembahasan)
        st.write("**Coba lakukan:**")
        st.write("1. Putar video ilustrasi di bagian atas.")
        st.write("2. Amati simulasi dan ubah parameter yang tersedia.")
        st.write("3. Catat hubungan sebab-akibat yang kamu amati.")
        st.write("4. Jawab kembali latihan pemahaman untuk mengecek pemahaman.")
