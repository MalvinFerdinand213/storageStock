import datetime
import time

class Clock:

	waktu_sekarang = datetime.datetime.now()

	print("Jam = %d" % waktu_sekarang.hour)
	print("Menit = %d" % waktu_sekarang.minute)
	print("Detik = %d" % waktu_sekarang.second)
	print("Mikro Detik = %d" % waktu_sekarang.microsecond)
	print("Tanggal = %d" % waktu_sekarang.day)
	print("Bulan = %d" % waktu_sekarang.month)
	print("Tahun = %d" % waktu_sekarang.year)

	unixtime = time.time()
	print(str(unixtime))