import datetime
import math

CYCLE_PERIODS={"physical":23,
			"emotional":28,
			"intellectual":33,
			"spiritual":53,
			"awareness":48,
			"aesthetic":43,
			"intuition":38}

total_days=lambda x: x.total_seconds()/(3600*24)

def biorhythm_val(birthday,current_date,cycleval):
	delta=current_date-birthday
	delta_days=total_days(delta)
	return math.sin(2*math.pi*delta_days/CYCLE_PERIODS[cycleval])

def biorhythm_intervals(birthday,startdate,enddate,cycleval,interval=100):
	delta=enddate-startdate
	if interval <= 0:
		gap = datetime.timedelta(1)
	else:
		gap=delta/interval
	results=[]
	days_passed = datetime.timedelta(0)
	if delta == days_passed:
			return results
	while days_passed <= delta:
			results.append((total_days(days_passed),biorhythm_val(birthday,days_passed+startdate,cycleval)))
			days_passed+=gap/interval
	return results

if __name__ == "__main__":
	import sys
	now=datetime.datetime.now()
	for d in sys.argv[1:]:
		print("Biorhythm values for a person born on {}".format(d))
		try:
			date=datetime.datetime.strptime(d,'%Y-%m-%d_%H:%M:%S')
		except ValueError:
			date=datetime.datetime.strptime(d,'%Y-%m-%d')
		for k in CYCLE_PERIODS.keys():
			print(k.title(),": ",sep="",end=" ")
			print("{:.2f}".format(biorhythm_val(date,now,k)*100))
	
