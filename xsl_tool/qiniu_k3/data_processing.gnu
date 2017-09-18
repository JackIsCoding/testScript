set terminal png size 1500,1000 enhanced font "Helvetica,20"
datafile = "data"
set output"data.png"
set title "download 20k time"
set ylabel "time(s)"
plot datafile using 1:2 w lp pt 7,datafile using 1:3 w lp pt 5
