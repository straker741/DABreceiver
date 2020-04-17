#!/usr/bin/expect
spawn mysql -u stu -p
expect "Enter password:"
send "korona2020\n"

expect "MariaDB \\\[(none)]>"
send "USE bakalarka;\n"
expect "MariaDB \\\[bakalarka]>"
send "CREATE TABLE IF NOT EXISTS dabtable1 ( id int not null auto_increment primary key, BER REAL(11,10), FIBER REAL(13,10), datetime timestamp DEFAULT current_timestamp );\n"
expect "MariaDB \\\[bakalarka]>"
send "CREATE TABLE IF NOT EXISTS dabtable2 ( id int not null auto_increment primary key, SNR REAL(13,10), bandwidth int, datetime timestamp DEFAULT current_timestamp );\n"
expect "MariaDB \\\[bakalarka]>"
send "CREATE TABLE IF NOT EXISTS temperature ( id int not null auto_increment primary key, temp REAL(6,3), datetime timestamp DEFAULT current_timestamp );\n"
expect "MariaDB \\\[bakalarka]>"
send "quit\n"