# health-report
Automatically report and send a message to wechat.
## change home -> school or ohterwise
### school -> home
- report.yml: LONGITUDE_SCHOOL -> LONGITUDE; LATITUDE_SCHOOL -> LATITUDE
- main.py: line 118 -> meta['el']['in_school_button'] -> meta['el']['not_in_school_button']
### home -> school
Reverse actions above.
## ref
- https://github.com/zhizunjiege/BUAA-Daily-Health-Report
- https://github.com/mottled233/buaa_daily_report

## warning
- After 60 days, you must edit the file, otherwise the github actions will be closed!!!
- The changes are taken at 2022.07.16, so the file should be changed at about 2023.01.20.

## miss
- 2022.10.18

  So I changed the 'cron' in report.yml, now it reports every five miniutes past 5:00 pm and 6:00pm, theoretically.
