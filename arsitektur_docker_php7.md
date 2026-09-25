# Arsitektur Docker PHP 7

Dokumen ini memetakan konfigurasi repository per 25 September 2026. Diagram menggambarkan konfigurasi yang didefinisikan dalam file, bukan jaminan bahwa seluruh service sedang berjalan. Pemeriksaan runtime sebelumnya terhalang izin akses Docker Engine.

Platform menjalankan sepuluh direktori aplikasi dalam satu container Apache + PHP 7.4, satu container khusus e-sertifikat, satu server MySQL 5.7 bersama, dan phpMyAdmin. Apache pada container utama sekaligus menjadi reverse proxy untuk e-sertifikat.

Diagram menggunakan Mermaid. Buka Markdown Preview yang mendukung Mermaid untuk menampilkan flowchart. Panah penuh menunjukkan alur komunikasi atau proses; panah putus-putus menunjukkan pemasangan file, konfigurasi, atau penyimpanan.

## 1. Gambaran arsitektur

```mermaid
flowchart TB
    USER["Pengguna / browser"]
    ADMIN["Administrator pada host Docker"]

    subgraph HOST["Host Docker: lokal atau server production"]
        PUBLIC["Port host 80: HTTP<br/>Port host 443: HTTPS production"]
        LOOP["Akses loopback host saja<br/>127.0.0.1"]

        subgraph NET["Jaringan bersama: docker-php7_default"]
            subgraph MAIN["Compose utama: docker-compose.yml + override lingkungan"]
                WEB["web / ci3_web_server<br/>Apache + PHP 7.4<br/>Aplikasi utama dan reverse proxy"]
                DB[("db / mysql_ci3_db<br/>MySQL 5.7 :3306")]
                PMA["phpmyadmin / phpmyadmin_ci3<br/>HTTP :80"]
            end
            subgraph CERTSTACK["Compose e-sertifikat: docker-compose.esertifikat.yml"]
                CERT["esertifikat_app<br/>Apache + PHP 7.4<br/>HTTP :80"]
            end
        end

        SRC["Folder aplikasi pada host"]
        ENV["File .env pada host"]
        VOL[("Named volume db_data")]
        SSL["Folder ssl2026<br/>Sertifikat production"]
    end

    USER --> PUBLIC --> WEB
    ADMIN --> LOOP
    LOOP -->|"81 ke port 80"| PMA
    LOOP -->|"3306 ke port 3306"| DB
    LOOP -->|"8081 ke port 80"| CERT
    WEB -->|"Path /esertifikat: HTTP internal"| CERT
    WEB -->|"Koneksi aplikasi ke db:3306"| DB
    CERT -->|"mysql_ci3_db:3306"| DB
    PMA -->|"PMA_HOST: db"| DB
    SRC -.->|"Bind mount"| WEB
    SRC -.->|"Folder esertifikat"| CERT
    ENV -.-> WEB
    ENV -.-> CERT
    SSL -.->|"TLS berakhir di Apache utama"| WEB
    DB -.->|"/var/lib/mysql"| VOL
```

Nama jaringan `docker-php7_default` diasumsikan berasal dari nama project Compose `docker-php7`. File Compose e-sertifikat menunjuk nama jaringan ini secara eksplisit sebagai jaringan eksternal. Jika nama project utama diubah, referensi jaringan e-sertifikat harus disesuaikan.

Koneksi antar-container memakai nama service/container dan port internal. Reverse proxy mengakses `esertifikat_app:80`, bukan port host `8081`. Jaringan Docker ini juga bukan loopback `localhost` milik container.

## 2. Komponen dan batas sumber daya

| Service           | Container         | Peran                                             | Batas memori / CPU  | Restart          |
| ----------------- | ----------------- | ------------------------------------------------- | ------------------- | ---------------- |
| `web`             | `ci3_web_server`  | Menjalankan aplikasi utama dan proxy e-sertifikat | `2500M` / `2.0` CPU | `unless-stopped` |
| `db`              | `mysql_ci3_db`    | Server database bersama                           | `1500M` / `1.0` CPU | `unless-stopped` |
| `phpmyadmin`      | `phpmyadmin_ci3`  | Antarmuka administrasi database                   | Tidak ditentukan    | `no`             |
| `esertifikat_app` | `esertifikat_app` | Menjalankan aplikasi e-sertifikat                 | `2G` / `1.5` CPU    | `unless-stopped` |

`web` dan `esertifikat_app` masing-masing mendefinisikan reservasi memori `256M`. Nilai CPU adalah batas pemakaian, bukan alokasi core fisik khusus. Semua service tetap berbagi sumber daya host; kapasitas host juga harus menyediakan ruang untuk OS, Docker, dan phpMyAdmin.

Kedua service PHP dibangun dari `Dockerfile` yang sama, berbasis `php:7.4-apache`. Dockerfile memasang ekstensi `gd`, `mysqli`, `pdo`, `pdo_mysql`, `zip`, dan `opcache`, serta modul Apache untuk rewrite, header, SSL, kompresi, cache, dan proxy. Tidak ada service PHP-FPM, Nginx, Redis, atau load balancer terpisah dalam Compose yang diperiksa.

## 3. Alur request pengguna

```mermaid
flowchart TD
    START["Browser mengirim request"] --> MODE{"Lingkungan?"}
    MODE -->|"Lokal"| LOCAL["HTTP localhost:80"]
    MODE -->|"Production"| PROTO{"HTTP atau HTTPS?"}
    PROTO -->|"HTTP :80"| REDIR["Apache mengirim redirect 301<br/>ke https://applib.uin-suka.ac.id"]
    REDIR --> TLS["Browser membuka HTTPS :443<br/>TLS ditangani Apache utama"]
    PROTO -->|"HTTPS :443"| TLS
    LOCAL --> ROUTE{"Path request?"}
    TLS --> ROUTE
    ROUTE -->|"/esertifikat"| PROXY["ProxyPass ke<br/>http://esertifikat_app:80/esertifikat"]
    PROXY --> CERT["Apache dan PHP<br/>container e-sertifikat"]
    ROUTE -->|"Path aplikasi utama"| APP["Apache membaca direktori aplikasi<br/>PHP / routing aplikasi bila diperlukan"]
    APP --> NEED{"Perlu database?"}
    CERT --> NEED
    NEED -->|"Ya"| QUERY["Query ke MySQL sesuai konfigurasi aplikasi"]
    QUERY --> RESULT["Aplikasi membentuk response"]
    NEED -->|"Tidak"| RESULT
    RESULT --> RESPONSE["Response dikembalikan ke browser<br/>E-sertifikat melalui proxy utama"]
```

Pada production, proxy meneruskan `Host` dan mengatur `X-Forwarded-Proto: https`. Hubungan Apache utama ke e-sertifikat menggunakan HTTP internal. File statis dapat dilayani langsung oleh Apache tanpa query database; request PHP mengikuti routing masing-masing aplikasi.

Path `/esertifikat` membutuhkan container e-sertifikat yang aktif dan terhubung ke jaringan bersama. Container tersebut tidak tercantum sebagai dependency service `web`.

## 4. Direktori aplikasi dan URL

Document root kedua container PHP adalah `/var/www/html`.

| URL relatif    | Sumber pada host | Lokasi dalam container      | Container                        |
| -------------- | ---------------- | --------------------------- | -------------------------------- |
| `/absensi`     | `./absensi`      | `/var/www/html/absensi`     | `ci3_web_server`                 |
| `/bmn`         | `./bmn`          | `/var/www/html/bmn`         | `ci3_web_server`                 |
| `/serial`      | `./serial`       | `/var/www/html/serial`      | `ci3_web_server`                 |
| `/report`      | `./report`       | `/var/www/html/report`      | `ci3_web_server`                 |
| `/loker`       | `./loker`        | `/var/www/html/loker`       | `ci3_web_server`                 |
| `/new_loker`   | `./new_loker`    | `/var/www/html/new_loker`   | `ci3_web_server`                 |
| `/pintumasuk`  | `./pintumasuk`   | `/var/www/html/pintumasuk`  | `ci3_web_server`                 |
| `/trans`       | `./trans`        | `/var/www/html/trans`       | `ci3_web_server`                 |
| `/carrel`      | `./carrel`       | `/var/www/html/carrel`      | `ci3_web_server`                 |
| `/antrian`     | `./antrian`      | `/var/www/html/antrian`     | `ci3_web_server`                 |
| `/esertifikat` | `./esertifikat`  | `/var/www/html/esertifikat` | `esertifikat_app`, melalui proxy |

Tabel menunjukkan mount yang didefinisikan, bukan hasil uji ketersediaan setiap URL. Khusus `report` dan `trans`, file `application/config/database.php` tidak ditemukan pada path yang diperiksa sehingga detail koneksi databasenya tidak diasumsikan.

## 5. Konfigurasi, database, dan persistensi

```mermaid
flowchart LR
    ENV[".env pada host"] -.-> COMPOSE["Compose membaca variabel<br/>untuk interpolasi konfigurasi"]
    COMPOSE -.-> DBENV["Environment MySQL<br/>root password dan database awal"]
    COMPOSE -.-> CERTENV["Environment e-sertifikat<br/>host, port, user, password"]
    ENV -.-> FILE["Bind mount /var/www/html/.env<br/>pada kedua container PHP"]
    FILE -.-> APPS["Aplikasi utama<br/>membaca sesuai loader masing-masing"]
    CERTENV -.-> CERT["E-sertifikat membaca getenv<br/>database: esertifikat"]
    APPS --> DB[("MySQL bersama")]
    CERT --> DB
    DBENV -.-> DB
    INIT["antrian/database/schema.sql"] -.->|"Init saat data directory baru"| DB
    DB -.-> DATA[("db_data<br/>/var/lib/mysql")]
    CODE["Direktori aplikasi host"] -.->|"Bind mount baca-tulis"| APPS
    CODE -.->|"Kode dan hasil file e-sertifikat"| CERT
```

- **Konfigurasi aplikasi:** mount `.env` menyediakan file. Mount tersebut tidak otomatis membuat semua isinya menjadi environment proses PHP. Sebagian aplikasi mem-parsing file; e-sertifikat membaca variabel koneksi melalui `getenv()` dan menerima environment eksplisit dari Compose.
- **Database utama:** Compose menginisialisasi nama database dari `DB_DATABASE`, dengan fallback `ci3_db`. Database yang digunakan aplikasi dapat berbeda, misalnya melalui `DB_DATABASE_ABSENSI`, `DB_DATABASE_BMN`, `DB_DATABASE_SERIAL`, `DB_DATABASE_LOKER`, dan `DB_DATABASE_CARREL`.
- **Antrian:** memakai `DB_DATABASE_ANTRIAN`, dengan fallback `antrian`. SQL inisialisasi secara eksplisit membuat dan memilih database `antrian`; perubahan nama melalui `.env` perlu diselaraskan dengan SQL tersebut.
- **E-sertifikat:** konfigurasi PHP menetapkan nama database `esertifikat`. Compose menunjuk host `mysql_ci3_db`; database ini tidak otomatis dibuat hanya karena environment service PHP berisi `DB_DATABASE=esertifikat`.
- **Koneksi tambahan:** beberapa aplikasi memiliki grup koneksi lain, misalnya SIPRUS dengan `DB_HOST_IP4` atau host dari konfigurasi bersama. Tujuan aktual mengikuti konfigurasi aplikasi dan `.env`; diagram utama merangkum koneksi MySQL lokal dan tidak menyatakan semua integrasi berada dalam Docker ini.
- **Persistensi MySQL:** data berada pada named volume `db_data` (umumnya bernama `docker-php7_db_data`). Pembuatan ulang container tidak sama dengan penghapusan volume.
- **Persistensi file aplikasi:** kode, upload, dan hasil generasi yang ditulis ke direktori bind mount tersimpan pada filesystem host. File yang ditulis di luar mount mengikuti filesystem container.
- **Bootstrap SQL:** `20-antrian.sql` dipasang read-only. Script init dijalankan saat inisialisasi MySQL baru; bukan mekanisme migrasi otomatis untuk volume yang sudah berisi database.

## 6. Lokal dan production

| Aspek                | Development lokal                       | Production                                   |
| -------------------- | --------------------------------------- | -------------------------------------------- |
| File utama           | `docker-compose.yml`                    | `docker-compose.yml`                         |
| Tambahan konfigurasi | `docker-compose.override.yml`           | `docker-compose.prod.yml`                    |
| Vhost utama          | `vhost.conf`                            | `vhost-ssl.conf`                             |
| Port web host        | `80:80`                                 | `80:80` dan `443:443`                        |
| HTTPS                | Tidak dikonfigurasi pada override lokal | TLS pada Apache utama                        |
| Sertifikat           | Tidak dipasang                          | `./ssl2026` ke `/home/siprusmbr/docker-php7` |
| E-sertifikat         | File Compose tersendiri                 | File Compose tersendiri                      |

Base Compose sendiri tidak mempublikasikan port `web` dan tidak memasang vhost khusus. Override lingkungan melengkapi keduanya. Port `80` dan `443` tidak dibatasi ke loopback oleh mapping Compose; akses dari luar tetap bergantung pada jaringan dan firewall host.

File sertifikat production yang dirujuk vhost adalah `applib.uin-suka.ac.id.crt`, `server.key`, dan `CAIntermediate.crt`. File vhost terpilih dipasang ke `/etc/apache2/sites-enabled/000-default.conf`.

| Akses administrasi pada host Docker | Tujuan                                        |
| ----------------------------------- | --------------------------------------------- |
| `http://127.0.0.1:81`               | phpMyAdmin                                    |
| `127.0.0.1:3306`                    | MySQL dari client pada host                   |
| `http://127.0.0.1:8081/esertifikat` | E-sertifikat langsung untuk pemeriksaan lokal |

Alamat `127.0.0.1` mengacu ke mesin tempat perintah atau browser dijalankan. Pada production, akses loopback ini berada di server, bukan otomatis di laptop administrator.

## 7. Alur build dan startup

```mermaid
flowchart TD
    START["Siapkan folder aplikasi, .env<br/>dan sertifikat untuk production"] --> SELECT["Pilih konfigurasi lokal atau production"]
    SELECT --> BUILD["Build service PHP dari Dockerfile yang sama"]
    BUILD --> IMAGE["PHP 7.4 + Apache + ekstensi<br/>Composer + entrypoint.sh"]
    IMAGE --> NETWORK["Compose utama membuat jaringan default<br/>dan menyiapkan volume db_data"]
    NETWORK --> DB["Mulai container MySQL"]
    DB --> FRESH{"Data directory baru?"}
    FRESH -->|"Ya"| INIT["Inisialisasi database awal<br/>lalu jalankan 20-antrian.sql"]
    FRESH -->|"Tidak"| EXIST["Gunakan data lama<br/>script init tidak dijalankan ulang"]
    INIT --> READY["MySQL siap menerima koneksi" ]
    EXIST --> READY
    DB --> DEP["depends_on saat ini hanya urutan startup<br/>tidak menunggu MySQL sehat"]
    DEP --> WEB["Mulai web dan phpMyAdmin"]
    WEB --> EP["Entrypoint PHP menjalankan<br/>Apache di foreground"]
    NETWORK --> CERT["Jalankan Compose e-sertifikat<br/>bergabung ke jaringan eksternal"]
    CERT --> CEP["Entrypoint mengatur permission<br/>sertifikat dan thumbnails bila ada<br/>lalu menjalankan Apache"]
```

Perintah untuk menjalankan lingkungan lokal:

```bash
docker compose up -d --build
docker compose -f docker-compose.esertifikat.yml up -d --build
```

Perintah untuk menjalankan production:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.esertifikat.yml up -d --build
```

Perintah di atas merupakan petunjuk operasi, bukan perintah yang dijalankan saat pembuatan dokumen ini. Jalankan stack utama terlebih dahulu agar jaringan yang dibutuhkan e-sertifikat tersedia. Tidak ada healthcheck database yang didefinisikan pada konfigurasi saat ini.

## 8. Catatan operasional konfigurasi saat ini

1. `.env` yang diperiksa memilih user database `admin`, sedangkan service MySQL hanya mendefinisikan `MYSQL_ROOT_PASSWORD` dan `MYSQL_DATABASE`. Provisioning user aplikasi beserta grant tiap database harus dipastikan tersedia, terutama untuk instalasi baru.
2. Konfigurasi MySQL mencantumkan `--tls-version=TLSv1.2,TLSv1.3`. Hasil review sebelumnya merekomendasikan `TLSv1.2` untuk MySQL 5.7; diagram tidak menyatakan konfigurasi TLS ini sudah berhasil saat runtime.
3. Slow-query log diarahkan ke `/var/log/mysql/slow.log`, tetapi Compose tidak menyediakan mount log khusus. Keberadaan direktori, izin tulis, persistensi, dan rotasi perlu dipastikan.
4. Volume persisten bukan backup. Repository menyediakan `backup.sh` yang menjalankan dump database melalui container. Jadwal, cakupan database termasuk aplikasi baru, dan hasil restore perlu diperiksa tersendiri; scheduler tidak didefinisikan sebagai service Compose.
5. `phpmyadmin` memakai restart policy `no` dan image tanpa tag versi eksplisit. Service tersebut tidak memiliki batas resource dalam file saat ini.
6. Properti `version: 3.8` masih tertulis dalam file Compose. Validasi Compose sebelumnya berhasil dengan peringatan bahwa properti ini sudah obsolete.
7. Aplikasi utama berbagi proses Apache/PHP dan batas resource container `web`. E-sertifikat memiliki container serta batas resource sendiri, tetapi tetap berbagi MySQL dan host fisik.

## 9. Sumber pemetaan

- [Compose utama](docker-compose.yml), [override lokal](docker-compose.override.yml), [override production](docker-compose.prod.yml), dan [Compose e-sertifikat](docker-compose.esertifikat.yml).
- [Dockerfile](Dockerfile) dan [entrypoint PHP](entrypoint.sh).
- [Vhost lokal](vhost.conf), [vhost production](vhost-ssl.conf), dan [vhost e-sertifikat](vhost_esertifikat.conf).
- [Schema antrian](antrian/database/schema.sql), [konfigurasi database antrian](antrian/application/config/database.php), dan [konfigurasi database e-sertifikat](esertifikat/application/config/database.php).
- Konfigurasi database aplikasi utama yang tersedia, [script backup](backup.sh), dan [README](README.md).

Nilai password dan isi private key tidak dicantumkan dalam dokumen ini.
