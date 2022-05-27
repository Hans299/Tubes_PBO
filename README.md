> Containerize Pygame with Docker.

## Nama dan NIM Anggota Kelompok
| Nama | NIM | Github |
| :---: | :---: | :---: |
| Faisal Khairul Fasha       | 120140158 | [faisalkfa](https://github.com/faisalkfa)                 |
| Faustine Elvaretta Tambila | 120140157 | [Faustineelvaretta](https://github.com/Faustineelvaretta) |
| Muhammad Hadi Arsa         | 120140150 | [HadiAr20](https://github.com/HadiAr20)                   |
| Syafira Wulandari          | 120140142 | [syafirawulandari](https://github.com/syafirawulandari)   |
| Hans Bonatua Batubara      | 120140131 | [Hans299](https://github.com/Hans299)                     |
| Indra Jaya Putra           | 120140059 | [indraphy](https://github.com/indraphy)                   |

## Dendam Si Tikus
#### Deskripsi Projek
Aplikasi ini merupakan permainan yang dibuat menggunakan library pygame tentang sebuah rocket yang bertahan dan melewati asteroid sambil menghindar dan menghancurkan asteroid dan rocket lain dan ketika 
rocket tekena dengan serangan dari rocket atau serangan asteroid.

## Cara Menjalankan Kontainer
Clone repositori ini atau [unduh disini]() lalu pindahkan pygame scripts ke folder `~/Downloads` seperti pada gambar berikut:

Selanjutnya buka terminal pada direktori folder tersebut lalu jalankan perintah build seperti berikut:

    make build-HandsOnDocker

lalu pastikan ada repositori "HandsOnDocker" pada docker, dengan cara jalankan command images untuk melihat daftar images pada local storage seperti berikut:

    docker images

Jika proses build telah selesai, jalankan perintah run seperti berikut:

untuk Windows

    make run-windows

untuk Linux

    make run-linux

untuk Mac

    make run-mac

Langkah terakhir yaitu menjalankan pygame melalui container yang telah kita buat dengan perintah seperti berikut:

    python3 -m main.py

## Video Demo Kontainer

[![LIHAT VIDEO DISINI]()]()

KLIK GAMBAR UNTUK MELIHAT VIDEO