set xlabel "Concurrency"
set ylabel "response_time"
set y2label "Sucess_rate"
set xrange[10:250]
set yrange[0:1000]
set xtics 10,10,250
set ytics nomirror
set y2tics
set term pdfcairo lw 2 font "Times New Roman,8"
set output 'tmp.pdf'
plot "data" u 1:2 w lp pt 5 lc rgbcolor "#2B60DE" axis x1y1 t "response_time","data" u 1:3 w lp pt 7 lc rgbcolor "#F62817" axis x1y2 t "success_rate"
set output
