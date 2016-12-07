set xlabel 'Frame Number'
set ylabel 'Size'

set term png size 2000,720
set output output_name


set style line 1 pt 5 lw 2 ps 0.5
set style line 2 pt 7 lw 2 ps 0.5 
set style line 3 pt 8 lw 2 ps 0.5

plot input_name using 1:2 with linespoint t "xc-enc" ls 1, \
             "" using 1:4 with linespoint t "target" ls 2, \
             "" using 1:3 with linespoint t "reported estimate" ls 3
